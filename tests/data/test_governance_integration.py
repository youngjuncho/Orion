"""Integration checks for decision revocation and authorization resolution."""
from copy import deepcopy

import pytest

from data.governance import (
    DecisionRecordError,
    canonical_digest,
    invalidate_dependents,
    resolve_registry_approved_decisions,
)


def record(decision_id, *, dependencies=None, **extra):
    value = {
        "decision_id": decision_id,
        "record_version": "1",
        "status": "Approved",
        "scope": {"provider": "fixture", "use": "test"},
        "authority": {"owner": "fixture-owner", "basis": "test-only"},
        "decided_at": "2026-10-09T12:00:00Z",
        "evidence": [{"ref": "fixture://evidence", "version": "1", "evidence_date": "2026-10-09"}],
        "rationale": "Test fixture only; not a real approval.",
        "dependencies": list(dependencies or []),
        "contract_changes": ["fixture-contract"],
        "test_refs": ["tests/data/test_governance_integration.py"],
        "content_digest": "pending",
    }
    value.update(extra)
    value["content_digest"] = canonical_digest(value)
    return value


def resign(value):
    value["content_digest"] = canonical_digest(value)
    return value


def test_revoked_root_blocks_transitive_dependent_at_resolution_time():
    root = record("PCD-ROOT", invalidated=True)
    middle = record("PCD-MID", dependencies=["PCD-ROOT"])
    leaf = record("PCD-LEAF", dependencies=["PCD-MID"])
    registry = {r["decision_id"]: r for r in (root, middle, leaf)}

    assert invalidate_dependents(registry, ["PCD-ROOT"]) == ("PCD-LEAF", "PCD-MID")
    with pytest.raises(DecisionRecordError, match="invalidated or superseded"):
        resolve_registry_approved_decisions(registry, ["PCD-LEAF"], {"provider": "fixture", "use": "test"})


def test_superseded_dependency_blocks_descendant_even_if_descendant_still_says_approved():
    old = record("PCD-V1", superseded_by="PCD-V2")
    dependent = record("PCD-CHILD", dependencies=["PCD-V1"])
    new = record("PCD-V2", supersedes="PCD-V1")
    registry = {r["decision_id"]: r for r in (old, new, dependent)}

    with pytest.raises(DecisionRecordError, match="invalidated or superseded"):
        resolve_registry_approved_decisions(registry, ["PCD-CHILD"], {"provider": "fixture", "use": "test"})


def test_valid_replacement_chain_resolves_only_through_new_decision():
    old = record("PCD-V1", superseded_by="PCD-V2")
    new = record("PCD-V2", supersedes="PCD-V1")
    dependent = record("PCD-CHILD", dependencies=["PCD-V2"])
    registry = {r["decision_id"]: r for r in (old, new, dependent)}

    result = resolve_registry_approved_decisions(
        registry, ["PCD-CHILD"], {"provider": "fixture", "use": "test"}
    )
    assert [item["decision_id"] for item in result] == ["PCD-CHILD", "PCD-V2"]
    assert all(item["decision_id"] != "PCD-V1" for item in result)


def test_registry_entrypoint_rejects_nonreciprocal_predecessor_claim():
    old = record("PCD-V1")
    new = record("PCD-V2", supersedes="PCD-V1")
    registry = {"PCD-V1": old, "PCD-V2": new}

    with pytest.raises(DecisionRecordError, match="not reciprocal"):
        resolve_registry_approved_decisions(
            registry, ["PCD-V2"], {"provider": "fixture", "use": "test"}
        )


def test_invalidation_impact_analysis_does_not_mutate_but_resolution_fails_closed():
    root = record("PCD-ROOT")
    child = record("PCD-CHILD", dependencies=["PCD-ROOT"])
    registry = {"PCD-ROOT": root, "PCD-CHILD": child}
    before = deepcopy(registry)
    impact = invalidate_dependents(registry, ["PCD-ROOT"])
    assert impact == ("PCD-CHILD",)
    assert registry == before

    registry["PCD-ROOT"]["invalidated"] = True
    resign(registry["PCD-ROOT"])
    with pytest.raises(DecisionRecordError, match="invalidated or superseded"):
        resolve_registry_approved_decisions(
            registry, ["PCD-CHILD"], {"provider": "fixture", "use": "test"}
        )


def test_unrelated_approval_remains_resolvable_after_another_branch_is_invalidated():
    revoked = record("PCD-REVOKED", invalidated=True)
    affected = record("PCD-AFFECTED", dependencies=["PCD-REVOKED"])
    independent = record("PCD-INDEPENDENT")
    registry = {r["decision_id"]: r for r in (revoked, affected, independent)}

    result = resolve_registry_approved_decisions(
        registry, ["PCD-INDEPENDENT"], {"provider": "fixture", "use": "test"}
    )
    assert [item["decision_id"] for item in result] == ["PCD-INDEPENDENT"]
