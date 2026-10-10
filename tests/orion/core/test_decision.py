from orion.core.decision import AcceptedDecision, DecisionCandidate, StateTransition, auto_approve


def candidate():
    return DecisionCandidate("c-1", "Moon", "allocation", "Portfolio", "p-1", {"weight": 0.5})


def test_decision_contracts_are_immutable_and_typed():
    c = candidate()
    a = AcceptedDecision("d-1", c, "runtime")
    t = StateTransition("t-1", a.decision_id, "Portfolio", "p-1", "old", "new", {"reason": "accepted"})
    assert a.candidate is c
    assert t.decision_id == "d-1"
    assert c.payload["weight"] == 0.5


def test_invalid_decision_candidate_rejected():
    try:
        DecisionCandidate("", "Moon", "allocation", "Portfolio", "p-1")
    except ValueError as exc:
        assert "candidate_id" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_auto_approve_materializes_existing_accepted_decision_contract():
    candidate = DecisionCandidate("c-auto", "Moon", "allocation", "Portfolio", "p-1")

    accepted = auto_approve(candidate)

    assert accepted.candidate is candidate
    assert accepted.decision_id == "accepted:c-auto"
    assert accepted.accepted_by == "orion-runtime:auto-approval"
    assert accepted.conditions is None


def test_default_auto_approval_also_accepts_rebalance_plan_proposals():
    plan_candidate = DecisionCandidate(
        "moon-rebalance:p-1",
        "Moon",
        "RebalancePlanProposal",
        "RebalancePlan",
        "p-1",
    )

    accepted = auto_approve(plan_candidate)

    assert accepted.candidate is plan_candidate
    assert accepted.accepted_by == "orion-runtime:auto-approval"
