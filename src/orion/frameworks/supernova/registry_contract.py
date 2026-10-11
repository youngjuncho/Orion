"""Strict local schema contract for Supernova approved-company snapshots.

This module validates shape and domain semantics only. It does not authenticate
issuers, verify signatures, persist anti-rollback state, or authorize execution.
"""
from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
import re
from typing import Any

REGISTRY_TYPE = "supernova.approved_company_state"
SCHEMA_VERSION = 1
REQUIRED_SCOPE_KEYS = frozenset({"framework", "domain", "review_cycle"})
RECORD_FIELDS = frozenset({
    "record_id", "company_id", "decision_ref", "review_cycle",
    "governance_status", "effective_at", "supersedes_record_id",
    "decision_payload_digest",
})
ENVELOPE_FIELDS = frozenset({
    "registry_type", "schema_version", "scope", "records", "source_decision_refs",
    "snapshot_id", "snapshot_version", "generated_at", "authority_ref",
    "signature", "key_id", "signature_algorithm", "content_digest",
})
_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
_TICKER_RE = re.compile(r"^[A-Z][A-Z0-9.-]{0,14}$")


class SupernovaRegistryContractError(ValueError):
    """Raised when an approved-company registry violates its local contract."""


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SupernovaRegistryContractError(f"{field} must be a non-empty string")
    return value


def _timestamp(value: Any, field: str) -> datetime:
    _text(value, field)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SupernovaRegistryContractError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise SupernovaRegistryContractError(f"{field} must include a timezone offset")
    return parsed


def validate_approved_company_record(
    record_id: str, record: Mapping[str, Any], *, expected_review_cycle: str
) -> dict[str, Any]:
    """Validate one explicit governance assertion without inferring approval."""
    _text(record_id, "record key")
    _text(expected_review_cycle, "expected_review_cycle")
    if not isinstance(record, Mapping):
        raise SupernovaRegistryContractError("record must be a mapping")
    missing = sorted(RECORD_FIELDS - set(record))
    unknown = sorted(set(record) - RECORD_FIELDS)
    if missing:
        raise SupernovaRegistryContractError(f"missing record fields: {', '.join(missing)}")
    if unknown:
        raise SupernovaRegistryContractError(f"unknown record fields: {', '.join(unknown)}")
    if _text(record["record_id"], "record_id") != record_id:
        raise SupernovaRegistryContractError("registry key/record_id mismatch")
    company_id = _text(record["company_id"], "company_id")
    if not _TICKER_RE.fullmatch(company_id):
        raise SupernovaRegistryContractError("company_id must be a canonical uppercase ticker")
    _text(record["decision_ref"], "decision_ref")
    cycle = _text(record["review_cycle"], "review_cycle")
    if cycle != expected_review_cycle:
        raise SupernovaRegistryContractError("record review_cycle mismatch")
    if record["governance_status"] != "approved":
        raise SupernovaRegistryContractError("unsupported governance_status; only explicit approved records are accepted")
    _timestamp(record["effective_at"], "effective_at")
    predecessor = record["supersedes_record_id"]
    if predecessor is not None:
        _text(predecessor, "supersedes_record_id")
        if predecessor == record_id:
            raise SupernovaRegistryContractError("record cannot supersede itself")
    digest = _text(record["decision_payload_digest"], "decision_payload_digest")
    if not _DIGEST_RE.fullmatch(digest):
        raise SupernovaRegistryContractError("decision_payload_digest must be a lowercase SHA-256 hex digest")
    return dict(record)


def validate_approved_company_snapshot(
    snapshot: Mapping[str, Any], *, expected_review_cycle: str
) -> dict[str, Any]:
    """Validate the proposed Supernova envelope and its domain-specific records.

    This is deliberately not a signature, freshness, digest, lineage, or
    anti-rollback verifier. Call the generic authoritative snapshot validator
    separately, with its trust inputs, before any future consumer relies on it.
    """
    if not isinstance(snapshot, Mapping):
        raise SupernovaRegistryContractError("snapshot must be a mapping")
    missing = sorted(ENVELOPE_FIELDS - set(snapshot))
    unknown = sorted(set(snapshot) - ENVELOPE_FIELDS)
    if missing:
        raise SupernovaRegistryContractError(f"missing envelope fields: {', '.join(missing)}")
    if unknown:
        raise SupernovaRegistryContractError(f"unknown envelope fields: {', '.join(unknown)}")
    if snapshot["registry_type"] != REGISTRY_TYPE:
        raise SupernovaRegistryContractError("registry_type mismatch")
    version = snapshot["schema_version"]
    if isinstance(version, bool) or not isinstance(version, int) or version != SCHEMA_VERSION:
        raise SupernovaRegistryContractError("unsupported schema_version")
    _text(snapshot["snapshot_id"], "snapshot_id")
    version = snapshot["snapshot_version"]
    if isinstance(version, bool) or not isinstance(version, int) or version <= 0:
        raise SupernovaRegistryContractError("snapshot_version must be a positive integer")
    _timestamp(snapshot["generated_at"], "generated_at")
    for field in ("authority_ref", "signature", "key_id", "signature_algorithm", "content_digest"):
        _text(snapshot[field], field)
    if not _DIGEST_RE.fullmatch(snapshot["content_digest"]):
        raise SupernovaRegistryContractError("content_digest must be a lowercase SHA-256 hex digest")
    scope = snapshot["scope"]
    if not isinstance(scope, Mapping) or set(scope) != REQUIRED_SCOPE_KEYS:
        raise SupernovaRegistryContractError("scope must contain exactly framework, domain, and review_cycle")
    if scope.get("framework") != "Supernova" or scope.get("domain") != "approved_company_state":
        raise SupernovaRegistryContractError("scope does not identify the Supernova approved-company domain")
    cycle = _text(scope.get("review_cycle"), "scope.review_cycle")
    if cycle != expected_review_cycle:
        raise SupernovaRegistryContractError("snapshot review_cycle mismatch")
    refs = snapshot["source_decision_refs"]
    if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or not ref.strip() for ref in refs):
        raise SupernovaRegistryContractError("source_decision_refs must be a non-empty list of strings")
    if len(refs) != len(set(refs)):
        raise SupernovaRegistryContractError("source_decision_refs must not contain duplicates")
    records = snapshot["records"]
    if not isinstance(records, Mapping) or not records:
        raise SupernovaRegistryContractError("records must be a non-empty mapping")
    validated: dict[str, dict[str, Any]] = {}
    seen_companies: set[str] = set()
    for key, raw in records.items():
        record = validate_approved_company_record(key, raw, expected_review_cycle=cycle)
        if record["decision_ref"] not in refs:
            raise SupernovaRegistryContractError(f"decision_ref missing from source_decision_refs: {key}")
        if record["company_id"] in seen_companies:
            raise SupernovaRegistryContractError(f"duplicate company_id: {record['company_id']}")
        seen_companies.add(record["company_id"])
        validated[key] = record
    return {**dict(snapshot), "records": validated}


def validate_trusted_approved_company_snapshot(
    snapshot: Mapping[str, Any],
    *,
    expected_review_cycle: str,
    now: datetime,
    max_age_seconds: int,
    trusted_authorities: set[str] | frozenset[str] | list[str] | tuple[str, ...],
    signature_verifier: Any,
    last_accepted_version: int | None,
    max_future_skew_seconds: int = 0,
) -> dict[str, Any]:
    """Compose generic authenticity checks with Supernova domain validation.

    The caller must persist ``snapshot_version`` as the high-water mark only
    after the enclosing state update succeeds. This function does not persist
    state, implement cryptography, or activate/authorize investment actions.
    """
    from data.governance import validate_authoritative_registry_snapshot

    if not isinstance(snapshot, Mapping):
        raise SupernovaRegistryContractError("snapshot must be a mapping")
    expected_scope = {
        "framework": "Supernova",
        "domain": "approved_company_state",
        "review_cycle": expected_review_cycle,
    }
    try:
        trusted = validate_authoritative_registry_snapshot(
            snapshot,
            expected_scope=expected_scope,
            now=now,
            max_age_seconds=max_age_seconds,
            max_future_skew_seconds=max_future_skew_seconds,
            trusted_authorities=trusted_authorities,
            signature_verifier=signature_verifier,
            last_accepted_version=last_accepted_version,
            # Supernova has a different record schema; validate its lineage below.
            validate_record_lineage=False,
        )
        validated = validate_approved_company_snapshot(
            trusted, expected_review_cycle=expected_review_cycle
        )
        _validate_company_lineage(validated["records"])
    except Exception as exc:
        if isinstance(exc, SupernovaRegistryContractError):
            raise
        raise SupernovaRegistryContractError(
            f"trusted Supernova snapshot validation failed: {exc}"
        ) from exc
    return validated


def _validate_company_lineage(records: Mapping[str, Mapping[str, Any]]) -> None:
    """Validate predecessor links for the Supernova-specific record schema."""
    for record_id, record in records.items():
        predecessor_id = record["supersedes_record_id"]
        if predecessor_id is None:
            continue
        predecessor = records.get(predecessor_id)
        if predecessor is None:
            raise SupernovaRegistryContractError(
                f"supersession predecessor missing from snapshot: {record_id} -> {predecessor_id}"
            )
        if predecessor["company_id"] != record["company_id"]:
            raise SupernovaRegistryContractError(
                f"supersession company mismatch: {record_id} -> {predecessor_id}"
            )
    for start in records:
        seen: set[str] = set()
        current: str | None = start
        while current is not None:
            if current in seen:
                raise SupernovaRegistryContractError(
                    f"supersession cycle detected at {current}"
                )
            seen.add(current)
            current_record = records[current]
            current = current_record["supersedes_record_id"]
