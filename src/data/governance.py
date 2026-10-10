"""Fail-closed validation for local, versioned provider decision records.

This module validates record structure and a caller-supplied authoritative
registry snapshot. It is not an identity/authorization service and does not
load remote records, approve investment policy, or activate strategies.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
import hashlib
import json
from typing import Any

VALID_STATUSES = {"Open", "Partially defined", "Approved", "Rejected", "Deferred"}
REQUIRED_FIELDS = {
    "decision_id", "record_version", "status", "scope", "authority",
    "decided_at", "evidence", "rationale", "dependencies",
    "contract_changes", "test_refs", "content_digest",
}


class DecisionRecordError(ValueError):
    """Raised when a decision record is malformed or cannot authorize use."""


def _nonempty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise DecisionRecordError(f"{field} must be a non-empty string")


def canonical_digest(record: Mapping[str, Any]) -> str:
    """Return SHA-256 of canonical record content, excluding content_digest."""
    payload = {key: value for key, value in record.items() if key != "content_digest"}
    try:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise DecisionRecordError("record must be JSON-compatible finite data") from exc
    return hashlib.sha256(encoded).hexdigest()


def validate_decision_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate schema, timestamp, evidence, dependencies, and content digest."""
    if not isinstance(record, Mapping):
        raise DecisionRecordError("record must be a mapping")
    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        raise DecisionRecordError(f"missing required fields: {', '.join(missing)}")
    _nonempty_text(record["decision_id"], "decision_id")
    _nonempty_text(record["record_version"], "record_version")
    if record["status"] not in VALID_STATUSES:
        raise DecisionRecordError("status is not recognized")
    if not isinstance(record["scope"], Mapping) or not record["scope"]:
        raise DecisionRecordError("scope must be a non-empty mapping")
    if not isinstance(record["authority"], Mapping):
        raise DecisionRecordError("authority must be a mapping")
    _nonempty_text(record["authority"].get("owner"), "authority.owner")
    _nonempty_text(record["authority"].get("basis"), "authority.basis")
    _nonempty_text(record["decided_at"], "decided_at")
    try:
        timestamp = datetime.fromisoformat(record["decided_at"].replace("Z", "+00:00"))
    except (ValueError, AttributeError) as exc:
        raise DecisionRecordError("decided_at must be an ISO-8601 timestamp") from exc
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise DecisionRecordError("decided_at must include a timezone offset")
    evidence = record["evidence"]
    if not isinstance(evidence, list):
        raise DecisionRecordError("evidence must be a list")
    for index, item in enumerate(evidence):
        if not isinstance(item, Mapping):
            raise DecisionRecordError(f"evidence[{index}] must be a mapping")
        for field in ("ref", "version", "evidence_date"):
            _nonempty_text(item.get(field), f"evidence[{index}].{field}")
    if record["status"] == "Approved" and not evidence:
        raise DecisionRecordError("Approved record requires evidence")
    _nonempty_text(record["rationale"], "rationale")
    for field in ("dependencies", "contract_changes", "test_refs"):
        value = record[field]
        if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
            raise DecisionRecordError(f"{field} must be a list of non-empty strings")
    if not isinstance(record.get("invalidated", False), bool):
        raise DecisionRecordError("invalidated must be a boolean")
    digest = record["content_digest"]
    _nonempty_text(digest, "content_digest")
    if digest != canonical_digest(record):
        raise DecisionRecordError("content_digest mismatch")
    return dict(record)


def resolve_approved_decisions(
    registry: Mapping[str, Mapping[str, Any]],
    required_ids: Sequence[str],
    requested_scope: Mapping[str, Any],
) -> tuple[dict[str, Any], ...]:
    """Resolve required IDs against an explicitly authoritative registry snapshot.

    Scope is intentionally exact for every requested key: an approval with a
    missing or different value cannot authorize a broader or different use.
    Every dependency must itself be present, valid, approved, and in scope.
    """
    if not isinstance(registry, Mapping):
        raise DecisionRecordError("authoritative registry must be a mapping")
    if not isinstance(requested_scope, Mapping) or not requested_scope:
        raise DecisionRecordError("requested_scope must be a non-empty mapping")
    resolved: dict[str, dict[str, Any]] = {}
    visiting: set[str] = set()

    def visit(decision_id: str) -> dict[str, Any]:
        if decision_id in resolved:
            return resolved[decision_id]
        if decision_id in visiting:
            raise DecisionRecordError(f"dependency cycle detected at {decision_id}")
        raw = registry.get(decision_id)
        if raw is None:
            raise DecisionRecordError(f"unknown decision ID: {decision_id}")
        record = validate_decision_record(raw)
        if record["decision_id"] != decision_id:
            raise DecisionRecordError(f"registry key/decision ID mismatch: {decision_id}")
        if record["status"] != "Approved":
            raise DecisionRecordError(f"decision is not approved: {decision_id}")
        if record.get("invalidated", False) or record.get("superseded_by"):
            raise DecisionRecordError(f"decision is invalidated or superseded: {decision_id}")
        for key, value in requested_scope.items():
            if record["scope"].get(key) != value:
                raise DecisionRecordError(f"scope mismatch for {decision_id}: {key}")
        visiting.add(decision_id)
        for dependency in record["dependencies"]:
            visit(dependency)
        visiting.remove(decision_id)
        resolved[decision_id] = record
        return record

    for required_id in required_ids:
        _nonempty_text(required_id, "required decision ID")
        visit(required_id)
    return tuple(resolved[key] for key in sorted(resolved))


def resolve_registry_approved_decisions(
    registry: Mapping[str, Mapping[str, Any]],
    required_ids: Sequence[str],
    requested_scope: Mapping[str, Any],
) -> tuple[dict[str, Any], ...]:
    """Validate registry-wide supersession lineage before resolving approvals.

    This is the safer entry point when the caller claims to supply a complete
    authoritative snapshot. It still cannot prove that the snapshot is truly
    authoritative, current, or signed; that requires a separate trust service.
    """
    validate_registry_lineage(registry)
    return resolve_approved_decisions(registry, required_ids, requested_scope)



def validate_registry_lineage(
    registry: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], ...]:
    """Validate a local registry snapshot's supersession links and cycles.

    The registry is a caller-supplied snapshot, not a trusted remote authority.
    Historical records remain in the snapshot; supersession marks them unusable
    for new authorization without deleting the audit trail.
    """
    if not isinstance(registry, Mapping):
        raise DecisionRecordError("registry snapshot must be a mapping")

    validated: dict[str, dict[str, Any]] = {}
    for key, raw in registry.items():
        _nonempty_text(key, "registry key")
        record = validate_decision_record(raw)
        if record["decision_id"] != key:
            raise DecisionRecordError(f"registry key/decision ID mismatch: {key}")
        validated[key] = record

    edges: dict[str, str] = {}
    for decision_id, record in validated.items():
        successor = record.get("superseded_by")
        if successor is None:
            continue
        _nonempty_text(successor, f"{decision_id}.superseded_by")
        if successor == decision_id:
            raise DecisionRecordError(f"self-supersession detected: {decision_id}")
        if successor not in validated:
            raise DecisionRecordError(
                f"supersession target missing from registry snapshot: {decision_id} -> {successor}"
            )
        if validated[successor].get("supersedes") != decision_id:
            raise DecisionRecordError(
                f"supersession link is not reciprocal: {decision_id} -> {successor}"
            )
        edges[decision_id] = successor

    # Check the reverse direction too: a successor must not claim a predecessor
    # unless that predecessor reciprocally points to the successor.
    for decision_id, record in validated.items():
        predecessor = record.get("supersedes")
        if predecessor is None:
            continue
        _nonempty_text(predecessor, f"{decision_id}.supersedes")
        if predecessor == decision_id:
            raise DecisionRecordError(f"self-supersession detected: {decision_id}")
        if predecessor not in validated:
            raise DecisionRecordError(
                f"supersession predecessor missing from registry snapshot: {decision_id} <- {predecessor}"
            )
        if validated[predecessor].get("superseded_by") != decision_id:
            raise DecisionRecordError(
                f"supersession link is not reciprocal: {decision_id} supersedes {predecessor}"
            )

    for start in edges:
        seen: set[str] = set()
        current = start
        while current in edges:
            if current in seen:
                raise DecisionRecordError(f"supersession cycle detected at {current}")
            seen.add(current)
            current = edges[current]

    return tuple(validated[key] for key in sorted(validated))


def invalidate_dependents(
    registry: Mapping[str, Mapping[str, Any]],
    invalidated_ids: Sequence[str],
) -> tuple[str, ...]:
    """Return dependent decisions that must be re-reviewed after invalidation.

    This is a planning helper only: it does not mutate or sign records. A
    decision is included if it transitively depends on any invalidated ID.
    """
    if not isinstance(registry, Mapping):
        raise DecisionRecordError("registry snapshot must be a mapping")
    targets = set(invalidated_ids)
    for decision_id in targets:
        _nonempty_text(decision_id, "invalidated decision ID")
    reverse: dict[str, set[str]] = {}
    for key, raw in registry.items():
        record = validate_decision_record(raw)
        if record["decision_id"] != key:
            raise DecisionRecordError(f"registry key/decision ID mismatch: {key}")
        for dependency in record["dependencies"]:
            reverse.setdefault(dependency, set()).add(key)

    impacted: set[str] = set()
    frontier = list(targets)
    while frontier:
        current = frontier.pop()
        for dependent in reverse.get(current, set()):
            if dependent not in impacted and dependent not in targets:
                impacted.add(dependent)
                frontier.append(dependent)
    return tuple(sorted(impacted))


def canonical_snapshot_digest(snapshot: Mapping[str, Any]) -> str:
    """Return a digest for snapshot metadata and its embedded record registry."""
    payload = {key: value for key, value in snapshot.items() if key != "content_digest"}
    try:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise DecisionRecordError("snapshot must be JSON-compatible finite data") from exc
    return hashlib.sha256(encoded).hexdigest()


def validate_authoritative_registry_snapshot(
    snapshot: Mapping[str, Any],
    *,
    expected_scope: Mapping[str, Any],
    now: datetime,
    max_age_seconds: int,
    max_future_skew_seconds: int = 0,
) -> dict[str, Any]:
    """Validate a caller-supplied registry snapshot contract and resolve its local integrity.

    This verifies declared metadata, digest, scope, age, and record lineage. It does
    not authenticate the issuer, prove that no newer snapshot exists, or fetch a
    trusted remote registry. Callers must supply those guarantees separately.
    """
    from datetime import timezone

    if not isinstance(snapshot, Mapping):
        raise DecisionRecordError("snapshot must be a mapping")
    required = {"snapshot_id", "snapshot_version", "generated_at", "scope", "authority_ref", "records", "content_digest"}
    missing = sorted(required - set(snapshot))
    if missing:
        raise DecisionRecordError(f"snapshot missing required fields: {', '.join(missing)}")
    for field in ("snapshot_id", "snapshot_version", "generated_at", "authority_ref", "content_digest"):
        _nonempty_text(snapshot[field], f"snapshot.{field}")
    if not isinstance(snapshot["scope"], Mapping) or not snapshot["scope"]:
        raise DecisionRecordError("snapshot.scope must be a non-empty mapping")
    if not isinstance(expected_scope, Mapping) or not expected_scope:
        raise DecisionRecordError("expected_scope must be a non-empty mapping")
    for key, value in expected_scope.items():
        if snapshot["scope"].get(key) != value:
            raise DecisionRecordError(f"snapshot scope mismatch: {key}")
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise DecisionRecordError("now must be a timezone-aware datetime")
    if not isinstance(max_age_seconds, int) or isinstance(max_age_seconds, bool) or max_age_seconds < 0:
        raise DecisionRecordError("max_age_seconds must be a non-negative integer")
    if not isinstance(max_future_skew_seconds, int) or isinstance(max_future_skew_seconds, bool) or max_future_skew_seconds < 0:
        raise DecisionRecordError("max_future_skew_seconds must be a non-negative integer")
    try:
        generated_at = datetime.fromisoformat(snapshot["generated_at"].replace("Z", "+00:00"))
    except (ValueError, AttributeError) as exc:
        raise DecisionRecordError("snapshot.generated_at must be an ISO-8601 timestamp") from exc
    if generated_at.tzinfo is None or generated_at.utcoffset() is None:
        raise DecisionRecordError("snapshot.generated_at must include a timezone offset")
    age_seconds = (now.astimezone(timezone.utc) - generated_at.astimezone(timezone.utc)).total_seconds()
    if age_seconds < -max_future_skew_seconds:
        raise DecisionRecordError("snapshot generated_at is too far in the future")
    if age_seconds > max_age_seconds:
        raise DecisionRecordError("snapshot is stale")
    records = snapshot["records"]
    if not isinstance(records, Mapping) or not records:
        raise DecisionRecordError("snapshot.records must be a non-empty mapping")
    if snapshot["content_digest"] != canonical_snapshot_digest(snapshot):
        raise DecisionRecordError("snapshot content_digest mismatch")
    validate_registry_lineage(records)
    return dict(snapshot)
