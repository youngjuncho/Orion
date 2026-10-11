"""Durable, atomic anti-rollback high-water marks for authoritative registries.

This is a local SQLite implementation of the storage contract. It does not
validate snapshots, authenticate authorities, or provide distributed consensus.
Use a trusted local database path and a storage/backup policy appropriate to
production. A successful advance is committed before it returns.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sqlite3
import time
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from contextlib import closing
from typing import Any


class HighWaterMarkError(RuntimeError):
    """Base error for high-water mark storage failures."""


class HighWaterMarkConflict(HighWaterMarkError):
    """Raised when the expected current version does not match stored state."""


class HighWaterMarkStorageError(HighWaterMarkError):
    """Raised when state cannot be read or durably committed."""


@dataclass(frozen=True)
class RegistryAcceptanceEvent:
    """Durable acceptance record for idempotent downstream materialization."""

    event_id: str
    authority_ref: str
    registry_type: str
    scope: dict[str, Any]
    snapshot_version: int
    snapshot_id: str
    content_digest: str
    status: str


@dataclass(frozen=True)
class RegistryAcceptanceLease:
    """Temporary exclusive claim to attempt processing one acceptance event."""

    event: RegistryAcceptanceEvent
    worker_id: str
    lease_token: str
    lease_expires_at: float


def _canonical_scope(scope: Mapping[str, Any]) -> tuple[str, str]:
    if not isinstance(scope, Mapping) or not scope:
        raise ValueError("scope must be a non-empty mapping")
    try:
        encoded = json.dumps(
            dict(scope), sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("scope must contain canonical JSON-compatible values") from exc
    return encoded, hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _version(value: int | None, field: str, *, allow_none: bool = False) -> None:
    if value is None and allow_none:
        return
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer" + (" or None" if allow_none else ""))


class SQLiteHighWaterMarkStore:
    """Atomically store monotonically increasing versions per trust scope.

    The key is the exact tuple of authority reference, registry type, and
    canonical scope. ``advance`` is compare-and-swap: callers must provide the
    version they previously read (or ``None`` for first acceptance). A stale
    concurrent writer is rejected instead of silently overwriting newer state.
    """

    def __init__(self, database_path: str | Path, *, timeout_seconds: float = 5.0) -> None:
        if str(database_path) == ":memory:":
            raise ValueError("a file-backed database is required for durable high-water state")
        if not isinstance(timeout_seconds, (int, float)) or isinstance(timeout_seconds, bool) or timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.timeout_seconds = float(timeout_seconds)
        try:
            with closing(self._connect()) as connection:
                connection.execute("PRAGMA journal_mode=WAL")
                connection.execute(
                    """CREATE TABLE IF NOT EXISTS registry_high_water_mark (
                        authority_ref TEXT NOT NULL,
                        registry_type TEXT NOT NULL,
                        scope_digest TEXT NOT NULL,
                        scope_json TEXT NOT NULL,
                        accepted_version INTEGER NOT NULL CHECK (accepted_version > 0),
                        PRIMARY KEY (authority_ref, registry_type, scope_digest)
                    )"""
                )
                connection.execute(
                    """CREATE TABLE IF NOT EXISTS registry_acceptance_event (
                        event_id TEXT PRIMARY KEY,
                        authority_ref TEXT NOT NULL,
                        registry_type TEXT NOT NULL,
                        scope_digest TEXT NOT NULL,
                        scope_json TEXT NOT NULL,
                        snapshot_version INTEGER NOT NULL CHECK (snapshot_version > 0),
                        snapshot_id TEXT NOT NULL,
                        content_digest TEXT NOT NULL,
                        status TEXT NOT NULL CHECK (status IN ('pending', 'applied')),
                        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
                        applied_at TEXT,
                        UNIQUE (authority_ref, registry_type, scope_digest, snapshot_version)
                    )"""
                )
                connection.execute(
                    "CREATE INDEX IF NOT EXISTS registry_acceptance_pending_idx "
                    "ON registry_acceptance_event(status, created_at, event_id)"
                )
                # Backward-compatible migration for databases created before leases.
                columns = {
                    row[1] for row in connection.execute(
                        "PRAGMA table_info(registry_acceptance_event)"
                    ).fetchall()
                }
                if "lease_owner" not in columns:
                    connection.execute("ALTER TABLE registry_acceptance_event ADD COLUMN lease_owner TEXT")
                if "lease_token" not in columns:
                    connection.execute("ALTER TABLE registry_acceptance_event ADD COLUMN lease_token TEXT")
                if "lease_expires_at" not in columns:
                    connection.execute("ALTER TABLE registry_acceptance_event ADD COLUMN lease_expires_at REAL")
        except (sqlite3.Error, OSError) as exc:
            raise HighWaterMarkStorageError("could not initialize high-water mark store") from exc

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=self.timeout_seconds, isolation_level=None)
        connection.execute("PRAGMA busy_timeout = %d" % int(self.timeout_seconds * 1000))
        return connection

    @staticmethod
    def _identity(authority_ref: str, registry_type: str, scope: Mapping[str, Any]) -> tuple[str, str, str, str, str]:
        if not isinstance(authority_ref, str) or not authority_ref.strip():
            raise ValueError("authority_ref must be a non-empty string")
        if not isinstance(registry_type, str) or not registry_type.strip():
            raise ValueError("registry_type must be a non-empty string")
        scope_json, digest = _canonical_scope(scope)
        return authority_ref, registry_type, digest, scope_json, digest

    def get_version(
        self, *, authority_ref: str, registry_type: str, scope: Mapping[str, Any]
    ) -> int | None:
        authority, registry, scope_digest, _scope_json, _ = self._identity(authority_ref, registry_type, scope)
        try:
            with closing(self._connect()) as connection:
                row = connection.execute(
                    "SELECT accepted_version FROM registry_high_water_mark "
                    "WHERE authority_ref = ? AND registry_type = ? AND scope_digest = ?",
                    (authority, registry, scope_digest),
                ).fetchone()
            return None if row is None else int(row[0])
        except (sqlite3.Error, OSError) as exc:
            raise HighWaterMarkStorageError("could not read high-water mark") from exc

    def advance(
        self, *, authority_ref: str, registry_type: str, scope: Mapping[str, Any],
        expected_current_version: int | None, new_version: int,
    ) -> int:
        """Atomically advance state, requiring a matching read and a higher version."""
        _version(expected_current_version, "expected_current_version", allow_none=True)
        _version(new_version, "new_version")
        if new_version == 0:
            raise ValueError("new_version must be a positive integer")
        if expected_current_version is not None and new_version <= expected_current_version:
            raise ValueError("new_version must be strictly greater than expected_current_version")
        authority, registry, scope_digest, scope_json, _ = self._identity(authority_ref, registry_type, scope)
        try:
            with closing(self._connect()) as connection:
                connection.execute("BEGIN IMMEDIATE")
                row = connection.execute(
                    "SELECT accepted_version, scope_json FROM registry_high_water_mark "
                    "WHERE authority_ref = ? AND registry_type = ? AND scope_digest = ?",
                    (authority, registry, scope_digest),
                ).fetchone()
                current = None if row is None else int(row[0])
                if row is not None and row[1] != scope_json:
                    raise HighWaterMarkStorageError("scope digest collision detected")
                if current != expected_current_version:
                    raise HighWaterMarkConflict(
                        f"high-water mark changed: expected {expected_current_version!r}, found {current!r}"
                    )
                if current is not None and new_version <= current:
                    raise HighWaterMarkConflict("new version is not greater than stored high-water mark")
                if current is None:
                    connection.execute(
                        "INSERT INTO registry_high_water_mark "
                        "(authority_ref, registry_type, scope_digest, scope_json, accepted_version) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (authority, registry, scope_digest, scope_json, new_version),
                    )
                else:
                    cursor = connection.execute(
                        "UPDATE registry_high_water_mark SET accepted_version = ? "
                        "WHERE authority_ref = ? AND registry_type = ? AND scope_digest = ? "
                        "AND accepted_version = ?",
                        (new_version, authority, registry, scope_digest, current),
                    )
                    if cursor.rowcount != 1:
                        raise HighWaterMarkConflict("compare-and-swap update lost a race")
                connection.execute("COMMIT")
            return new_version
        except (HighWaterMarkConflict, HighWaterMarkStorageError):
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise
        except (sqlite3.Error, OSError) as exc:
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise HighWaterMarkStorageError("could not commit high-water mark") from exc


    def accept_snapshot(
        self, *, authority_ref: str, registry_type: str, scope: Mapping[str, Any],
        expected_current_version: int | None, snapshot_version: int,
        snapshot_id: str, content_digest: str,
    ) -> RegistryAcceptanceEvent:
        """Atomically advance the HWM and enqueue a durable acceptance event.

        Call only after the snapshot's authority, signature, digest, scope, and
        freshness have been validated. This method does not perform those checks.
        A downstream consumer should apply pending events idempotently, then call
        ``mark_applied``. If application fails or the process crashes, the event
        remains pending and can be replayed without accepting the snapshot again.
        """
        _version(expected_current_version, "expected_current_version", allow_none=True)
        _version(snapshot_version, "snapshot_version")
        if snapshot_version == 0:
            raise ValueError("snapshot_version must be a positive integer")
        if expected_current_version is not None and snapshot_version <= expected_current_version:
            raise ValueError("snapshot_version must be strictly greater than expected_current_version")
        if not isinstance(snapshot_id, str) or not snapshot_id.strip():
            raise ValueError("snapshot_id must be a non-empty string")
        if not isinstance(content_digest, str) or len(content_digest) != 64:
            raise ValueError("content_digest must be a 64-character SHA-256 hex digest")
        try:
            int(content_digest, 16)
        except ValueError as exc:
            raise ValueError("content_digest must be a 64-character SHA-256 hex digest") from exc

        authority, registry, scope_digest, scope_json, _ = self._identity(authority_ref, registry_type, scope)
        event_id = str(uuid.uuid4())
        try:
            with closing(self._connect()) as connection:
                connection.execute("BEGIN IMMEDIATE")
                row = connection.execute(
                    "SELECT accepted_version, scope_json FROM registry_high_water_mark "
                    "WHERE authority_ref = ? AND registry_type = ? AND scope_digest = ?",
                    (authority, registry, scope_digest),
                ).fetchone()
                current = None if row is None else int(row[0])
                if row is not None and row[1] != scope_json:
                    raise HighWaterMarkStorageError("scope digest collision detected")
                if current != expected_current_version:
                    raise HighWaterMarkConflict(
                        f"high-water mark changed: expected {expected_current_version!r}, found {current!r}"
                    )
                if current is not None and snapshot_version <= current:
                    raise HighWaterMarkConflict("snapshot version is not greater than stored high-water mark")
                if current is None:
                    connection.execute(
                        "INSERT INTO registry_high_water_mark "
                        "(authority_ref, registry_type, scope_digest, scope_json, accepted_version) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (authority, registry, scope_digest, scope_json, snapshot_version),
                    )
                else:
                    cursor = connection.execute(
                        "UPDATE registry_high_water_mark SET accepted_version = ? "
                        "WHERE authority_ref = ? AND registry_type = ? AND scope_digest = ? "
                        "AND accepted_version = ?",
                        (snapshot_version, authority, registry, scope_digest, current),
                    )
                    if cursor.rowcount != 1:
                        raise HighWaterMarkConflict("compare-and-swap update lost a race")
                connection.execute(
                    "INSERT INTO registry_acceptance_event "
                    "(event_id, authority_ref, registry_type, scope_digest, scope_json, "
                    "snapshot_version, snapshot_id, content_digest, status) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')",
                    (event_id, authority, registry, scope_digest, scope_json,
                     snapshot_version, snapshot_id, content_digest.lower()),
                )
                connection.execute("COMMIT")
            return RegistryAcceptanceEvent(
                event_id=event_id, authority_ref=authority, registry_type=registry,
                scope=json.loads(scope_json), snapshot_version=snapshot_version,
                snapshot_id=snapshot_id, content_digest=content_digest.lower(), status="pending",
            )
        except (HighWaterMarkConflict, HighWaterMarkStorageError):
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise
        except (sqlite3.Error, OSError) as exc:
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise HighWaterMarkStorageError("could not atomically record registry acceptance") from exc

    @staticmethod
    def _event_from_row(row: tuple[Any, ...]) -> RegistryAcceptanceEvent:
        return RegistryAcceptanceEvent(
            event_id=row[0], authority_ref=row[1], registry_type=row[2],
            scope=json.loads(row[3]), snapshot_version=int(row[4]),
            snapshot_id=row[5], content_digest=row[6], status=row[7],
        )

    def list_pending_acceptances(self, *, limit: int = 100) -> list[RegistryAcceptanceEvent]:
        """Return durable events awaiting idempotent downstream application."""
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1 or limit > 10000:
            raise ValueError("limit must be an integer between 1 and 10000")
        try:
            with closing(self._connect()) as connection:
                rows = connection.execute(
                    "SELECT event_id, authority_ref, registry_type, scope_json, snapshot_version, "
                    "snapshot_id, content_digest, status FROM registry_acceptance_event "
                    "WHERE status = 'pending' ORDER BY authority_ref, registry_type, scope_digest, snapshot_version LIMIT ?", (limit,),
                ).fetchall()
            return [self._event_from_row(row) for row in rows]
        except (sqlite3.Error, OSError, ValueError, TypeError) as exc:
            raise HighWaterMarkStorageError("could not read pending registry acceptances") from exc

    def count_pending_acceptances(self) -> int:
        """Return the exact number of journal events awaiting application."""
        try:
            with closing(self._connect()) as connection:
                row = connection.execute(
                    "SELECT COUNT(*) FROM registry_acceptance_event WHERE status = 'pending'"
                ).fetchone()
            return int(row[0])
        except (sqlite3.Error, OSError) as exc:
            raise HighWaterMarkStorageError("could not count pending registry acceptances") from exc

    def mark_applied(self, event_id: str) -> None:
        """Acknowledge downstream application; repeated acknowledgements are safe."""
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError("event_id must be a non-empty string")
        try:
            with closing(self._connect()) as connection:
                connection.execute("BEGIN IMMEDIATE")
                cursor = connection.execute(
                    "UPDATE registry_acceptance_event SET status = 'applied', "
                    "applied_at = COALESCE(applied_at, strftime('%Y-%m-%dT%H:%M:%fZ', 'now')) "
                    "WHERE event_id = ? AND status = 'pending' AND lease_token IS NULL", (event_id,),
                )
                if cursor.rowcount == 0:
                    row = connection.execute(
                        "SELECT status, lease_token FROM registry_acceptance_event WHERE event_id = ?", (event_id,),
                    ).fetchone()
                    if row is None:
                        raise ValueError("unknown acceptance event_id")
                    if row[0] == "pending" and row[1] is not None:
                        raise HighWaterMarkConflict("event is leased; only the current lease holder may acknowledge it")
                    if row[0] != "applied":
                        raise HighWaterMarkStorageError("unexpected acceptance event state")
                connection.execute("COMMIT")
        except (HighWaterMarkStorageError, HighWaterMarkConflict):
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise
        except ValueError:
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise
        except (sqlite3.Error, OSError) as exc:
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise HighWaterMarkStorageError("could not acknowledge registry acceptance") from exc


    def claim_pending_acceptances(
        self, *, worker_id: str, limit: int = 1, lease_seconds: float = 30.0,
        now: float | None = None,
    ) -> list[RegistryAcceptanceLease]:
        """Atomically lease eligible events, preserving version order per scope.

        A pending event blocks later pending versions in its scope even while it
        is leased. Expired leases may be reclaimed. ``now`` exists for deterministic
        tests; production callers should omit it and use wall-clock time.
        """
        if not isinstance(worker_id, str) or not worker_id.strip():
            raise ValueError("worker_id must be a non-empty string")
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 10000:
            raise ValueError("limit must be an integer between 1 and 10000")
        if (not isinstance(lease_seconds, (int, float)) or isinstance(lease_seconds, bool)
                or not math.isfinite(lease_seconds) or lease_seconds <= 0):
            raise ValueError("lease_seconds must be a finite positive number")
        timestamp = time.time() if now is None else now
        if not isinstance(timestamp, (int, float)) or isinstance(timestamp, bool) or not math.isfinite(timestamp):
            raise ValueError("now must be a finite numeric timestamp")
        expires = float(timestamp) + float(lease_seconds)
        try:
            with closing(self._connect()) as connection:
                connection.execute("BEGIN IMMEDIATE")
                rows = connection.execute(
                    "SELECT e.event_id, e.authority_ref, e.registry_type, e.scope_json, "
                    "e.snapshot_version, e.snapshot_id, e.content_digest, e.status "
                    "FROM registry_acceptance_event AS e "
                    "WHERE e.status = 'pending' "
                    "AND (e.lease_expires_at IS NULL OR e.lease_expires_at <= ?) "
                    "AND NOT EXISTS (SELECT 1 FROM registry_acceptance_event AS earlier "
                    "WHERE earlier.authority_ref = e.authority_ref "
                    "AND earlier.registry_type = e.registry_type "
                    "AND earlier.scope_digest = e.scope_digest "
                    "AND earlier.status = 'pending' "
                    "AND earlier.snapshot_version < e.snapshot_version) "
                    "ORDER BY e.created_at, e.event_id LIMIT ?",
                    (float(timestamp), limit),
                ).fetchall()
                leases = []
                for row in rows:
                    token = str(uuid.uuid4())
                    cursor = connection.execute(
                        "UPDATE registry_acceptance_event SET lease_owner = ?, lease_token = ?, "
                        "lease_expires_at = ? WHERE event_id = ? AND status = 'pending' "
                        "AND (lease_expires_at IS NULL OR lease_expires_at <= ?)",
                        (worker_id, token, expires, row[0], float(timestamp)),
                    )
                    if cursor.rowcount != 1:
                        raise HighWaterMarkConflict("acceptance lease changed during claim")
                    leases.append(RegistryAcceptanceLease(
                        event=self._event_from_row(row), worker_id=worker_id,
                        lease_token=token, lease_expires_at=expires,
                    ))
                connection.execute("COMMIT")
            return leases
        except HighWaterMarkConflict:
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise
        except (sqlite3.Error, OSError) as exc:
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise HighWaterMarkStorageError("could not claim pending registry acceptances") from exc

    def acknowledge_claim(self, lease: RegistryAcceptanceLease, *, now: float | None = None) -> None:
        """Mark an event applied only if the caller still owns an unexpired lease."""
        if not isinstance(lease, RegistryAcceptanceLease):
            raise TypeError("lease must be a RegistryAcceptanceLease")
        timestamp = time.time() if now is None else now
        if not isinstance(timestamp, (int, float)) or isinstance(timestamp, bool):
            raise ValueError("now must be a finite numeric timestamp")
        import math
        if not math.isfinite(timestamp):
            raise ValueError("now must be a finite numeric timestamp")
        try:
            with closing(self._connect()) as connection:
                connection.execute("BEGIN IMMEDIATE")
                cursor = connection.execute(
                    "UPDATE registry_acceptance_event SET status = 'applied', "
                    "applied_at = COALESCE(applied_at, strftime('%Y-%m-%dT%H:%M:%fZ', 'now')), "
                    "lease_owner = NULL, lease_token = NULL, lease_expires_at = NULL "
                    "WHERE event_id = ? AND status = 'pending' AND lease_owner = ? "
                    "AND lease_token = ? AND lease_expires_at > ?",
                    (lease.event.event_id, lease.worker_id, lease.lease_token, float(timestamp)),
                )
                if cursor.rowcount != 1:
                    raise HighWaterMarkConflict("lease is stale, expired, or no longer owned by this worker")
                connection.execute("COMMIT")
        except HighWaterMarkConflict:
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise
        except (sqlite3.Error, OSError) as exc:
            try:
                if "connection" in locals() and connection.in_transaction:
                    connection.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise HighWaterMarkStorageError("could not acknowledge leased registry acceptance") from exc
