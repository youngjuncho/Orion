from pathlib import Path

import pytest

from orion.core import ExecutionMetadata, RuntimeSession, load_config


def make_session() -> RuntimeSession:
    config = load_config(Path(__file__).resolve().parents[3] / "config")
    execution = ExecutionMetadata("execution-001", "2026-08-01T09:00:00+09:00", "1.0")
    return RuntimeSession(config, execution)


def test_runtime_session_follows_documented_lifecycle() -> None:
    session = make_session()

    assert session.status == "Initializing"
    service = object()
    session.services.register("Configuration", service)
    assert session.services.get("Configuration") is service
    session.start()
    assert session.status == "Running"
    session.complete()
    assert session.status == "Completed"


def test_runtime_session_can_fail_before_completion() -> None:
    session = make_session()
    session.start()
    session.fail()

    assert session.status == "Error"


def test_runtime_sessions_own_independent_in_memory_stores_and_registries() -> None:
    first = make_session()
    second = make_session()
    marker = object()
    first.registry.register("Moon", marker)
    first.services.register("Marker", marker)

    assert second.registry.names == ()
    assert second.services.names == ()
    assert first.events is not second.events
    assert first.states is not second.states


def test_runtime_session_rejects_invalid_transition() -> None:
    session = make_session()
    session.start()
    session.complete()

    with pytest.raises(RuntimeError, match="cannot move"):
        session.start()


def test_runtime_session_builds_read_only_context_from_registered_components() -> None:
    session = make_session()
    framework = object()
    service = object()
    session.registry.register("Moon", framework)
    session.services.register("Configuration", service)

    context = session.build_context(
        framework_results={"Moon": "result"},
        dashboard_data={"status": "ready"},
    )

    assert context.registered_frameworks == ("Moon",)
    assert context.services["Configuration"] is service
    assert context.framework_results["Moon"] == "result"
    assert context.dashboard_data["status"] == "ready"


def test_runtime_session_requires_registered_framework_for_context() -> None:
    with pytest.raises(ValueError, match="at least one framework"):
        make_session().build_context()


def test_execute_frameworks_assembles_orion_result():
    from orion.core import FrameworkResult, Score

    session = make_session()
    session.registry.register("Aurora", object())
    session.registry.register("Moon", object())

    def aurora(context):
        assert context.registered_frameworks == ("Aurora", "Moon")
        return FrameworkResult("Aurora", "Completed", score=Score(10))

    def moon(context):
        assert "Aurora" in context.framework_results
        return FrameworkResult("Moon", "Completed")

    result = session.execute_frameworks({"Aurora": aurora, "Moon": moon})

    assert session.status == "Completed"
    assert [item.framework_name for item in result.framework_results] == ["Aurora", "Moon"]
    assert result.framework_results[0].score == Score(10)


def test_execute_frameworks_rejects_non_canonical_result():
    session = make_session()
    session.registry.register("Aurora", object())

    with pytest.raises(TypeError, match="FrameworkResult"):
        session.execute_frameworks({"Aurora": lambda context: "bad"})

    assert session.status == "Error"


def test_execute_frameworks_requires_exact_registry_match():
    session = make_session()
    session.registry.register("Aurora", object())

    with pytest.raises(ValueError, match="registry"):
        session.execute_frameworks({})

    assert session.status == "Initializing"


def test_runtime_resolves_and_commits_accepted_decision():
    from orion.core.decision import AcceptedDecision, DecisionCandidate, StateTransition
    from orion.core.state import OrionStateSnapshot

    session = make_session()
    session.start()
    candidate = DecisionCandidate("c-1", "Moon", "allocation", "Portfolio", "p-1")

    accepted = session.resolve_and_commit(
        [candidate],
        lambda item: AcceptedDecision("d-1", item, "test"),
        lambda decision: StateTransition("t-1", decision.decision_id, "Portfolio", "p-1", "old", "new"),
        lambda transitions: OrionStateSnapshot("2026-10-07T00:00:00Z", session.execution.execution_id, "test", {"Moon": "new"}, {}, "Running"),
    )

    assert accepted[0].decision_id == "d-1"
    assert session.states.current is not None
    assert session.states.current.framework_states["Moon"] == "new"


def test_runtime_does_not_commit_rejected_candidate():
    from orion.core.decision import DecisionCandidate

    session = make_session()
    session.start()
    candidate = DecisionCandidate("c-1", "Moon", "allocation", "Portfolio", "p-1")
    accepted = session.resolve_and_commit(
        [candidate], lambda item: None,
        lambda decision: (_ for _ in ()).throw(AssertionError("must not transition")),
        lambda transitions: (_ for _ in ()).throw(AssertionError("must not snapshot")),
    )
    assert accepted == ()
    assert session.states.current is None


def test_runtime_records_execution_correlated_events() -> None:
    from orion.core import Event

    session = make_session()
    session.start()
    event = Event(
        event_id="event-001",
        event_type="Framework Completed",
        event_category="Lifecycle Event",
        occurred_at=session.execution.start_time,
        execution_id=session.execution.execution_id,
        entity_type="Framework",
        entity_id="Moon",
        source_framework="Moon",
    )

    recorded = session.record_events([event])

    assert recorded == (event,)
    assert session.events.events == (event,)


def test_runtime_rejects_event_from_another_execution() -> None:
    from orion.core import Event

    session = make_session()
    session.start()
    event = Event(
        event_id="event-001",
        event_type="Framework Completed",
        event_category="Lifecycle Event",
        occurred_at=session.execution.start_time,
        execution_id="other-execution",
        entity_type="Framework",
        entity_id="Moon",
    )

    with pytest.raises(ValueError, match="execution_id"):
        session.record_events([event])

    assert session.events.events == ()


def test_runtime_emits_transition_events_only_after_state_commit() -> None:
    from orion.core import Event
    from orion.core.decision import AcceptedDecision, DecisionCandidate, StateTransition
    from orion.core.state import OrionStateSnapshot

    session = make_session()
    session.start()
    candidate = DecisionCandidate("c-1", "Moon", "allocation", "Portfolio", "p-1")
    observed = []

    def make_event(transition: StateTransition) -> Event:
        observed.append(session.states.current)
        return Event(
            event_id="event-transition-001",
            event_type="State Transition Committed",
            event_category="Domain Event",
            occurred_at=session.execution.start_time,
            execution_id=session.execution.execution_id,
            entity_type=transition.entity_type,
            entity_id=transition.entity_id,
            previous_state=transition.previous_state,
            current_state=transition.new_state,
            related_decision=transition.decision_id,
        )

    session.resolve_and_commit(
        [candidate],
        lambda item: AcceptedDecision("d-1", item, "test"),
        lambda decision: StateTransition("t-1", decision.decision_id, "Portfolio", "p-1", "old", "new"),
        lambda transitions: OrionStateSnapshot(
            "2026-10-07T00:00:00Z",
            session.execution.execution_id,
            "test",
            {"Moon": "new"},
            {},
            "Running",
        ),
        event_factory=make_event,
    )

    assert observed[0] is not None
    assert observed[0].framework_states["Moon"] == "new"
    assert session.events.events[0].related_decision == "d-1"
    assert session.events.events[0].execution_id == session.execution.execution_id
