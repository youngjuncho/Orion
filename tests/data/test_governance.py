from copy import deepcopy

import pytest

from data.governance import (
    DecisionRecordError,
    canonical_digest,
    resolve_approved_decisions,
    validate_decision_record,
    validate_registry_lineage,
    invalidate_dependents,
)


def make_record(decision_id="PCD-01", *, dependencies=None, status="Approved", scope=None):
    record = {
        "decision_id": decision_id,
        "record_version": "1",
        "status": status,
        "scope": scope or {"provider": "fixture", "use": "test"},
        "authority": {"owner": "test-owner", "basis": "fixture-only authority"},
        "decided_at": "2026-10-09T12:00:00Z",
        "evidence": [{"ref": "fixture://evidence", "version": "1", "evidence_date": "2026-10-09"}] if status == "Approved" else [],
        "rationale": "Deterministic test fixture only; not an investment approval.",
        "dependencies": list(dependencies or []),
        "contract_changes": ["fixture-contract"],
        "test_refs": ["tests/data/test_governance.py"],
        "content_digest": "pending",
    }
    record["content_digest"] = canonical_digest(record)
    return record


def test_valid_record_passes_schema_and_digest_validation():
    record = make_record()
    assert validate_decision_record(record)["decision_id"] == "PCD-01"


def test_missing_field_fails_closed():
    record = make_record()
    del record["authority"]
    with pytest.raises(DecisionRecordError, match="missing required fields"):
        validate_decision_record(record)


def test_digest_tampering_is_detected():
    record = make_record()
    record["rationale"] = "changed after approval"
    with pytest.raises(DecisionRecordError, match="content_digest mismatch"):
        validate_decision_record(record)


def test_naive_timestamp_is_rejected():
    record = make_record()
    record["decided_at"] = "2026-10-09T12:00:00"
    record["content_digest"] = canonical_digest(record)
    with pytest.raises(DecisionRecordError, match="timezone offset"):
        validate_decision_record(record)


def test_approved_record_requires_evidence():
    record = make_record()
    record["evidence"] = []
    record["content_digest"] = canonical_digest(record)
    with pytest.raises(DecisionRecordError, match="requires evidence"):
        validate_decision_record(record)


def test_unknown_decision_id_is_rejected():
    with pytest.raises(DecisionRecordError, match="unknown decision ID"):
        resolve_approved_decisions({}, ["PCD-01"], {"provider": "fixture"})


def test_scope_mismatch_is_rejected():
    registry = {"PCD-01": make_record()}
    with pytest.raises(DecisionRecordError, match="scope mismatch"):
        resolve_approved_decisions(registry, ["PCD-01"], {"provider": "live-provider"})


def test_unapproved_decision_is_rejected():
    registry = {"PCD-01": make_record(status="Deferred")}
    with pytest.raises(DecisionRecordError, match="not approved"):
        resolve_approved_decisions(registry, ["PCD-01"], {"provider": "fixture"})


def test_invalidated_or_superseded_decision_is_rejected():
    for extra in ({"invalidated": True}, {"superseded_by": "PCD-01-v2"}):
        record = make_record()
        record.update(extra)
        record["content_digest"] = canonical_digest(record)
        with pytest.raises(DecisionRecordError, match="invalidated or superseded"):
            resolve_approved_decisions({"PCD-01": record}, ["PCD-01"], {"provider": "fixture"})


def test_dependency_must_resolve_and_be_approved():
    registry = {"PCD-02": make_record("PCD-02", dependencies=["PCD-01"])}
    with pytest.raises(DecisionRecordError, match="unknown decision ID"):
        resolve_approved_decisions(registry, ["PCD-02"], {"provider": "fixture"})
    registry["PCD-01"] = make_record("PCD-01", status="Deferred")
    with pytest.raises(DecisionRecordError, match="not approved"):
        resolve_approved_decisions(registry, ["PCD-02"], {"provider": "fixture"})


def test_dependency_cycle_is_rejected():
    first = make_record("PCD-01", dependencies=["PCD-02"])
    second = make_record("PCD-02", dependencies=["PCD-01"])
    with pytest.raises(DecisionRecordError, match="cycle"):
        resolve_approved_decisions({"PCD-01": first, "PCD-02": second}, ["PCD-01"], {"provider": "fixture"})


def test_valid_dependency_chain_resolves_deterministically():
    first = make_record("PCD-01")
    second = make_record("PCD-02", dependencies=["PCD-01"])
    result = resolve_approved_decisions(
        {"PCD-01": first, "PCD-02": second}, ["PCD-02"], {"provider": "fixture", "use": "test"}
    )
    assert [item["decision_id"] for item in result] == ["PCD-01", "PCD-02"]
    assert result == resolve_approved_decisions(
        {"PCD-01": first, "PCD-02": second}, ["PCD-02"], {"provider": "fixture", "use": "test"}
    )



def with_digest(record, **extra):
    record.update(extra)
    record["content_digest"] = canonical_digest(record)
    return record


def test_registry_lineage_accepts_reciprocal_supersession_and_preserves_history():
    old = with_digest(make_record("PCD-01"), superseded_by="PCD-02")
    new = with_digest(make_record("PCD-02"), supersedes="PCD-01")
    result = validate_registry_lineage({"PCD-01": old, "PCD-02": new})
    assert [item["decision_id"] for item in result] == ["PCD-01", "PCD-02"]
    assert result[0]["superseded_by"] == "PCD-02"


def test_registry_lineage_rejects_missing_or_nonreciprocal_successor():
    old = with_digest(make_record("PCD-01"), superseded_by="PCD-02")
    with pytest.raises(DecisionRecordError, match="target missing"):
        validate_registry_lineage({"PCD-01": old})
    new = with_digest(make_record("PCD-02"))
    with pytest.raises(DecisionRecordError, match="not reciprocal"):
        validate_registry_lineage({"PCD-01": old, "PCD-02": new})


def test_registry_lineage_rejects_supersession_cycle():
    first = with_digest(make_record("PCD-01"), superseded_by="PCD-02", supersedes="PCD-02")
    second = with_digest(make_record("PCD-02"), superseded_by="PCD-01", supersedes="PCD-01")
    with pytest.raises(DecisionRecordError, match="cycle"):
        validate_registry_lineage({"PCD-01": first, "PCD-02": second})


def test_invalidation_returns_transitive_dependents_without_mutating_records():
    first = make_record("PCD-01")
    second = make_record("PCD-02", dependencies=["PCD-01"])
    third = make_record("PCD-03", dependencies=["PCD-02"])
    registry = {"PCD-01": first, "PCD-02": second, "PCD-03": third}
    assert invalidate_dependents(registry, ["PCD-01"]) == ("PCD-02", "PCD-03")
    assert registry["PCD-02"]["status"] == "Approved"


def make_snapshot(records=None, **extra):
    from data.governance import canonical_snapshot_digest
    snapshot = {
        "snapshot_id": "fixture-snapshot-001",
        "snapshot_version": "1",
        "generated_at": "2026-10-09T12:00:00Z",
        "scope": {"provider": "fixture", "use": "test"},
        "authority_ref": "fixture-authority://registry",
        "records": records or {"PCD-01": make_record("PCD-01")},
        "content_digest": "pending",
    }
    snapshot.update(extra)
    snapshot["content_digest"] = canonical_snapshot_digest(snapshot)
    return snapshot


def test_authoritative_snapshot_contract_accepts_fresh_scoped_snapshot():
    from datetime import datetime, timezone
    from data.governance import validate_authoritative_registry_snapshot
    snapshot = make_snapshot()
    validated = validate_authoritative_registry_snapshot(
        snapshot,
        expected_scope={"provider": "fixture", "use": "test"},
        now=datetime(2026, 10, 9, 12, 1, tzinfo=timezone.utc),
        max_age_seconds=300,
    )
    assert validated["snapshot_id"] == "fixture-snapshot-001"


def test_authoritative_snapshot_rejects_missing_metadata_and_bad_digest():
    from datetime import datetime, timezone
    from data.governance import validate_authoritative_registry_snapshot
    snapshot = make_snapshot()
    del snapshot["authority_ref"]
    with pytest.raises(DecisionRecordError, match="missing required fields"):
        validate_authoritative_registry_snapshot(
            snapshot, expected_scope={"provider": "fixture"},
            now=datetime(2026, 10, 9, 12, 1, tzinfo=timezone.utc), max_age_seconds=300,
        )
    snapshot = make_snapshot()
    snapshot["snapshot_version"] = "tampered"
    with pytest.raises(DecisionRecordError, match="digest mismatch"):
        validate_authoritative_registry_snapshot(
            snapshot, expected_scope={"provider": "fixture"},
            now=datetime(2026, 10, 9, 12, 1, tzinfo=timezone.utc), max_age_seconds=300,
        )


def test_authoritative_snapshot_rejects_scope_mismatch_and_stale_snapshot():
    from datetime import datetime, timezone
    from data.governance import validate_authoritative_registry_snapshot
    snapshot = make_snapshot()
    with pytest.raises(DecisionRecordError, match="scope mismatch"):
        validate_authoritative_registry_snapshot(
            snapshot, expected_scope={"provider": "live"},
            now=datetime(2026, 10, 9, 12, 1, tzinfo=timezone.utc), max_age_seconds=300,
        )
    with pytest.raises(DecisionRecordError, match="stale"):
        validate_authoritative_registry_snapshot(
            snapshot, expected_scope={"provider": "fixture"},
            now=datetime(2026, 10, 9, 13, 0, tzinfo=timezone.utc), max_age_seconds=300,
        )


def test_authoritative_snapshot_rejects_naive_and_excessively_future_timestamps():
    from datetime import datetime, timezone
    from data.governance import canonical_snapshot_digest, validate_authoritative_registry_snapshot
    snapshot = make_snapshot(generated_at="2026-10-09T12:00:00")
    snapshot["content_digest"] = canonical_snapshot_digest(snapshot)
    with pytest.raises(DecisionRecordError, match="timezone offset"):
        validate_authoritative_registry_snapshot(
            snapshot, expected_scope={"provider": "fixture"},
            now=datetime(2026, 10, 9, 12, 1, tzinfo=timezone.utc), max_age_seconds=300,
        )
    snapshot = make_snapshot(generated_at="2026-10-09T13:00:00Z")
    with pytest.raises(DecisionRecordError, match="future"):
        validate_authoritative_registry_snapshot(
            snapshot, expected_scope={"provider": "fixture"},
            now=datetime(2026, 10, 9, 12, 1, tzinfo=timezone.utc), max_age_seconds=300,
        )
