"""Guarded orchestration for authoritative registry snapshot acceptance.

The service binds the caller's exact trust scope to the durable HWM key, reads
that HWM, validates the candidate against the observed version, then performs a
compare-and-swap acceptance transaction. It intentionally does not connect to a
Runtime or framework consumer.
"""
from __future__ import annotations

import json
from copy import deepcopy
from collections.abc import Callable, Mapping
from typing import Any

from data.governance import canonical_snapshot_digest, validate_authoritative_registry_snapshot
from data.registry_high_water_store import (
    RegistryAcceptanceEvent,
    SQLiteHighWaterMarkStore,
)


class RegistryAcceptanceServiceError(ValueError):
    """Raised when the acceptance orchestration contract is not satisfied."""


def _canonical_mapping(value: Mapping[str, Any], field: str) -> str:
    if not isinstance(value, Mapping) or not value:
        raise RegistryAcceptanceServiceError(f"{field} must be a non-empty mapping")
    try:
        return json.dumps(
            dict(value), sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise RegistryAcceptanceServiceError(
            f"{field} must contain canonical JSON-compatible values"
        ) from exc


class RegistryAcceptanceService:
    """Validate before persisting acceptance, with HWM CAS as the commit gate.

    ``validator`` must validate all required trust and domain properties and
    accept ``last_accepted_version`` as a keyword argument. ``validation_options``
    contains the other validator arguments, such as the trusted-authority set,
    signature verifier, freshness policy, and expected scope. The service owns
    the HWM value and does not permit callers to override it.
    """

    def __init__(
        self,
        store: SQLiteHighWaterMarkStore,
        *,
        validator: Callable[..., Mapping[str, Any]] = validate_authoritative_registry_snapshot,
        validation_options: Mapping[str, Any],
    ) -> None:
        if not isinstance(store, SQLiteHighWaterMarkStore):
            raise TypeError("store must be a SQLiteHighWaterMarkStore")
        if not callable(validator):
            raise TypeError("validator must be callable")
        if not isinstance(validation_options, Mapping):
            raise TypeError("validation_options must be a mapping")
        if "last_accepted_version" in validation_options:
            raise RegistryAcceptanceServiceError(
                "last_accepted_version is managed by the acceptance service"
            )
        self._store = store
        self._validator = validator
        self._validation_options = dict(validation_options)

    def accept(
        self,
        snapshot: Mapping[str, Any],
        *,
        authority_ref: str,
        registry_type: str,
        scope: Mapping[str, Any],
    ) -> RegistryAcceptanceEvent:
        """Validate a snapshot against current durable state, then atomically accept.

        A concurrent HWM change raises ``HighWaterMarkConflict``. The caller
        must reload and revalidate; this method never retries stale validation.
        """
        if not isinstance(snapshot, Mapping):
            raise RegistryAcceptanceServiceError("snapshot must be a mapping")
        if not isinstance(authority_ref, str) or not authority_ref.strip():
            raise RegistryAcceptanceServiceError("authority_ref must be non-empty")
        if not isinstance(registry_type, str) or not registry_type.strip():
            raise RegistryAcceptanceServiceError("registry_type must be non-empty")
        scope_json = _canonical_mapping(scope, "scope")
        if snapshot.get("authority_ref") != authority_ref:
            raise RegistryAcceptanceServiceError("snapshot authority does not match acceptance identity")
        if snapshot.get("registry_type") != registry_type:
            raise RegistryAcceptanceServiceError("snapshot registry_type does not match acceptance identity")
        snapshot_scope_json = _canonical_mapping(snapshot.get("scope"), "snapshot.scope")
        if snapshot_scope_json != scope_json:
            raise RegistryAcceptanceServiceError("snapshot scope must exactly match the durable HWM scope")

        expected_scope = self._validation_options.get("expected_scope")
        if expected_scope is not None:
            if _canonical_mapping(expected_scope, "expected_scope") != scope_json:
                raise RegistryAcceptanceServiceError(
                    "validator expected_scope must exactly match the durable HWM scope"
                )

        # Preserve the original signed envelope independently of validator behavior.
        try:
            original = deepcopy(dict(snapshot))
            candidate = deepcopy(original)
        except Exception as exc:
            raise RegistryAcceptanceServiceError("snapshot cannot be defensively copied") from exc

        current = self._store.get_version(
            authority_ref=authority_ref, registry_type=registry_type, scope=scope,
        )
        validated = self._validator(
            candidate, last_accepted_version=current, **self._validation_options,
        )
        if not isinstance(validated, Mapping):
            raise RegistryAcceptanceServiceError("validator must return a validated mapping")

        # A domain validator may normalize record payloads, but it must not alter
        # the identity or signed envelope fields used for durable acceptance.
        for field in (
            "authority_ref", "registry_type", "scope", "snapshot_id",
            "snapshot_version", "content_digest",
        ):
            if validated.get(field) != original.get(field):
                raise RegistryAcceptanceServiceError(
                    f"validator changed or omitted signed identity field: {field}"
                )
        try:
            recomputed_digest = canonical_snapshot_digest(validated)
        except Exception as exc:
            raise RegistryAcceptanceServiceError("validator returned a non-canonical snapshot") from exc
        if recomputed_digest != validated.get("content_digest"):
            raise RegistryAcceptanceServiceError(
                "validator returned content that no longer matches the signed digest"
            )

        return self._store.accept_snapshot(
            authority_ref=authority_ref,
            registry_type=registry_type,
            scope=scope,
            expected_current_version=current,
            snapshot_version=validated["snapshot_version"],
            snapshot_id=validated["snapshot_id"],
            content_digest=validated["content_digest"],
        )
