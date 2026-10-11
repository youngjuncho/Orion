from datetime import datetime, timezone

import pytest

from data.governance import canonical_digest, canonical_snapshot_digest, validate_authoritative_registry_snapshot
from data.registry_acceptance_service import (
    RegistryAcceptanceService,
    RegistryAcceptanceServiceError,
)
from data.registry_high_water_store import HighWaterMarkConflict, SQLiteHighWaterMarkStore

SCOPE = {"provider": "fixture", "use": "test"}
AUTHORITY = "fixture-authority://registry"
REGISTRY = "fixture.decision_registry"
NOW = datetime(2026, 10, 9, 12, 1, tzinfo=timezone.utc)


def record():
    result = {
        "decision_id": "PCD-01", "record_version": "1", "status": "Approved",
        "scope": dict(SCOPE),
        "authority": {"owner": "fixture-owner", "basis": "test-only"},
        "decided_at": "2026-10-09T12:00:00Z",
        "evidence": [{"ref": "fixture://evidence", "version": "1", "evidence_date": "2026-10-09"}],
        "rationale": "Fixture only; not an investment approval.", "dependencies": [],
        "contract_changes": ["fixture-contract"],
        "test_refs": ["tests/data/test_registry_acceptance_service.py"],
        "content_digest": "pending",
    }
    result["content_digest"] = canonical_digest(result)
    return result


def snapshot(version=1, **updates):
    result = {
        "snapshot_id": f"fixture-snapshot-{version}", "snapshot_version": version,
        "generated_at": "2026-10-09T12:00:00Z", "scope": dict(SCOPE),
        "authority_ref": AUTHORITY, "registry_type": REGISTRY,
        "signature": "fixture-signature", "key_id": "fixture-key",
        "signature_algorithm": "fixture-test", "records": {"PCD-01": record()},
        "content_digest": "pending",
    }
    result.update(updates)
    result["content_digest"] = canonical_snapshot_digest(result)
    return result


def make_service(store, validator=validate_authoritative_registry_snapshot, **extra):
    options = {
        "expected_scope": SCOPE,
        "now": NOW,
        "max_age_seconds": 300,
        "trusted_authorities": {AUTHORITY},
        "signature_verifier": lambda *_args: True,
    }
    options.update(extra)
    return RegistryAcceptanceService(store, validator=validator, validation_options=options)


def test_service_validates_before_atomic_acceptance(tmp_path):
    store = SQLiteHighWaterMarkStore(tmp_path / "state.sqlite3")
    service = make_service(store)
    event = service.accept(snapshot(), authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE)
    assert event.snapshot_version == 1
    assert store.get_version(authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE) == 1
    assert store.list_pending_acceptances() == [event]


def test_validation_failure_does_not_advance_hwm_or_enqueue_event(tmp_path):
    store = SQLiteHighWaterMarkStore(tmp_path / "state.sqlite3")
    service = make_service(store, signature_verifier=lambda *_args: False)
    with pytest.raises(ValueError, match="signature verification failed"):
        service.accept(snapshot(), authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE)
    assert store.get_version(authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE) is None
    assert store.list_pending_acceptances() == []


@pytest.mark.parametrize("field,value,match", [
    ("authority_ref", "other-authority", "authority does not match"),
    ("registry_type", "other.registry", "registry_type does not match"),
    ("scope", {"provider": "fixture", "use": "different"}, "scope must exactly match"),
])
def test_identity_mismatch_fails_before_validator(tmp_path, field, value, match):
    store = SQLiteHighWaterMarkStore(tmp_path / "state.sqlite3")
    calls = []
    def validator(candidate, *, last_accepted_version, **_kwargs):
        calls.append(last_accepted_version)
        return candidate
    service = make_service(store, validator=validator)
    candidate = snapshot(**{field: value})
    with pytest.raises(RegistryAcceptanceServiceError, match=match):
        service.accept(candidate, authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE)
    assert calls == []
    assert store.list_pending_acceptances() == []


def test_service_injects_current_hwm_into_validator_and_rejects_replay(tmp_path):
    store = SQLiteHighWaterMarkStore(tmp_path / "state.sqlite3")
    seen = []
    def validator(candidate, *, last_accepted_version, **kwargs):
        seen.append(last_accepted_version)
        return validate_authoritative_registry_snapshot(
            candidate, last_accepted_version=last_accepted_version, **kwargs,
        )
    service = make_service(store, validator=validator)
    service.accept(snapshot(1), authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE)
    with pytest.raises(ValueError, match="rollback or replay"):
        service.accept(snapshot(1), authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE)
    assert seen == [None, 1]
    assert store.get_version(authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE) == 1
    assert len(store.list_pending_acceptances()) == 1


def test_cas_conflict_requires_fresh_validation_instead_of_blind_retry(tmp_path):
    store = SQLiteHighWaterMarkStore(tmp_path / "state.sqlite3")
    def racing_validator(candidate, *, last_accepted_version, **kwargs):
        validated = validate_authoritative_registry_snapshot(
            candidate, last_accepted_version=last_accepted_version, **kwargs,
        )
        # Simulate another writer advancing state after validation but before CAS.
        store.advance(authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE,
                      expected_current_version=None, new_version=2)
        return validated
    service = make_service(store, validator=racing_validator)
    with pytest.raises(HighWaterMarkConflict):
        service.accept(snapshot(1), authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE)
    assert store.get_version(authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE) == 2
    assert store.list_pending_acceptances() == []


def test_validator_cannot_change_signed_identity_fields(tmp_path):
    store = SQLiteHighWaterMarkStore(tmp_path / "state.sqlite3")
    def mutating_validator(candidate, *, last_accepted_version, **_kwargs):
        return {**candidate, "snapshot_id": "rewritten"}
    service = make_service(store, validator=mutating_validator)
    with pytest.raises(RegistryAcceptanceServiceError, match="changed or omitted"):
        service.accept(snapshot(), authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE)
    assert store.get_version(authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE) is None


def test_service_prevents_validation_options_from_overriding_hwm(tmp_path):
    store = SQLiteHighWaterMarkStore(tmp_path / "state.sqlite3")
    with pytest.raises(RegistryAcceptanceServiceError, match="managed by the acceptance service"):
        make_service(store, last_accepted_version=999)


def test_validator_cannot_mutate_candidate_in_place_to_bypass_digest(tmp_path):
    store = SQLiteHighWaterMarkStore(tmp_path / "state.sqlite3")
    def mutating_validator(candidate, *, last_accepted_version, **_kwargs):
        candidate["records"]["PCD-01"]["rationale"] = "mutated after verification"
        return candidate
    service = make_service(store, validator=mutating_validator)
    with pytest.raises(RegistryAcceptanceServiceError, match="content that no longer matches"):
        service.accept(snapshot(), authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE)
    assert store.get_version(authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE) is None
    assert store.list_pending_acceptances() == []


def test_validator_cannot_mutate_the_callers_snapshot(tmp_path):
    store = SQLiteHighWaterMarkStore(tmp_path / "state.sqlite3")
    candidate = snapshot()
    original_rationale = candidate["records"]["PCD-01"]["rationale"]
    def mutating_validator(copy_of_candidate, *, last_accepted_version, **_kwargs):
        copy_of_candidate["records"]["PCD-01"]["rationale"] = "changed"
        return copy_of_candidate
    service = make_service(store, validator=mutating_validator)
    with pytest.raises(RegistryAcceptanceServiceError, match="content that no longer matches"):
        service.accept(candidate, authority_ref=AUTHORITY, registry_type=REGISTRY, scope=SCOPE)
    assert candidate["records"]["PCD-01"]["rationale"] == original_rationale
