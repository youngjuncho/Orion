import pytest
from pathlib import Path
from types import SimpleNamespace

from orion.core import (
    Event,
    FrameworkResult,
    FrameworkResult,
    ExecutionMetadata,
    FrameworkRegistry,
    OrionRuntime,
    OrionStateSnapshot,
    RuntimeSession,
    Score,
    load_config,
    make_report_adapter,
)
from orion.core.decision import AcceptedDecision, DecisionCandidate, StateTransition


CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"


def test_public_runtime_executes_all_report_adapters_through_one_boundary():
    registry = FrameworkRegistry()
    for name in ("Aurora", "Moon", "Supernova", "Phoenix"):
        registry.register(name, object())

    reports = {
        "Aurora": SimpleNamespace(score=Score(10)),
        "Moon": SimpleNamespace(),
        "Supernova": SimpleNamespace(),
        "Phoenix": SimpleNamespace(phoenix_score=Score(20)),
    }
    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("e2e-runtime-001", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )

    result = runtime.run(
        {
            name: make_report_adapter(name, lambda name=name: reports[name])
            for name in reports
        },
        dashboard_data={"source": "runtime"},
    )

    assert [item.framework_name for item in result.framework_results] == [
        "Aurora",
        "Moon",
        "Supernova",
        "Phoenix",
    ]
    assert result.framework_results[0].score == Score(10)
    assert result.framework_results[-1].score == Score(20)
    assert result.dashboard_data["source"] == "runtime"
    assert result.generated_events == ()


def test_runtime_decision_state_event_slice_preserves_canonical_order():
    config = load_config(CONFIG_DIR)
    session = RuntimeSession(
        config,
        ExecutionMetadata("e2e-runtime-002", "2026-10-08T00:00:00Z", "v1"),
    )
    session.registry.register("Moon", object())
    session.start()

    candidate = DecisionCandidate(
        "candidate-001", "Moon", "allocation", "Portfolio", "portfolio-001"
    )

    def accept(item: DecisionCandidate) -> AcceptedDecision:
        return AcceptedDecision("decision-001", item, "integration-test")

    def transition(decision: AcceptedDecision) -> StateTransition:
        return StateTransition(
            "transition-001",
            decision.decision_id,
            "Portfolio",
            "portfolio-001",
            "old",
            "new",
        )

    def snapshot(transitions: tuple[StateTransition, ...]) -> OrionStateSnapshot:
        assert transitions[0].transition_id == "transition-001"
        return OrionStateSnapshot(
            "2026-10-08T00:00:01Z",
            session.execution.execution_id,
            "v1",
            {"Moon": "new"},
            {},
            "Running",
        )

    def event_factory(item: StateTransition) -> Event:
        return Event(
            "event-001",
            "State Transition Committed",
            "Domain Event",
            session.execution.start_time,
            session.execution.execution_id,
            "Portfolio",
            item.entity_id,
            previous_state=item.previous_state,
            current_state=item.new_state,
            related_decision=item.decision_id,
        )

    accepted = session.resolve_and_commit(
        (candidate,), accept, transition, snapshot, event_factory
    )

    assert accepted[0].decision_id == "decision-001"
    assert session.states.current.framework_states["Moon"] == "new"
    assert session.events.events[0].related_decision == "decision-001"
    assert session.events.events[0].execution_id == "e2e-runtime-002"


def test_public_runtime_defaults_to_auto_approval_for_lifecycle() -> None:
    config = load_config(CONFIG_DIR)
    runtime = OrionRuntime(
        config,
        ExecutionMetadata("e2e-runtime-auto-001", "2026-10-08T00:00:00Z", "v1"),
    )
    runtime.registry.register("Moon", object())

    candidate = DecisionCandidate(
        "candidate-auto-001", "Moon", "allocation", "Portfolio", "portfolio-001"
    )

    def transition(decision: AcceptedDecision) -> StateTransition:
        assert decision.accepted_by == "orion-runtime:auto-approval"
        return StateTransition(
            "transition-auto-001",
            decision.decision_id,
            "Portfolio",
            "portfolio-001",
            "old",
            "new",
        )

    def snapshot(transitions: tuple[StateTransition, ...]) -> OrionStateSnapshot:
        return OrionStateSnapshot(
            "2026-10-08T00:00:01Z",
            runtime.execution.execution_id,
            "v1",
            {"Moon": "new"},
            {},
            "Running",
        )

    def executor(_):
        return FrameworkResult(
            framework_name="Moon",
            execution_status="Completed",
            decision_candidates=(candidate,),
        )

    result = runtime.run(
        {"Moon": executor},
        transition=transition,
        snapshot=snapshot,
    )

    assert result.state_snapshot is not None
    assert result.generated_events == ()


def test_public_runtime_accepts_canonical_market_data_provider() -> None:
    from data import MarketDataPoint, MarketDataSet

    registry = FrameworkRegistry()
    registry.register("Aurora", object())
    market_data = MarketDataSet(
        (MarketDataPoint("SPY", "close", "2026-10-08", 632.1, "test"),),
        "2026-10-08",
    )

    class Provider:
        def load(self) -> MarketDataSet:
            return market_data

    seen = []
    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("e2e-data-001", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )

    def execute(context):
        seen.append(context.market_data)
        return make_report_adapter("Aurora", lambda: SimpleNamespace(score=Score(10)))(context)

    result = runtime.run({"Aurora": execute}, market_data_provider=Provider())

    assert seen == [market_data]
    assert result.framework_results[0].framework_name == "Aurora"


def test_public_runtime_rejects_two_market_data_inputs() -> None:
    from data import MarketDataPoint, MarketDataSet

    registry = FrameworkRegistry()
    registry.register("Aurora", object())
    market_data = MarketDataSet(
        (MarketDataPoint("SPY", "close", "2026-10-08", 1.0, "test"),),
        "2026-10-08",
    )
    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("e2e-data-002", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )

    with pytest.raises(ValueError, match="either market_data or market_data_provider"):
        runtime.run(
            {"Aurora": make_report_adapter("Aurora", lambda: SimpleNamespace(score=Score(10)))},
            market_data=market_data,
            market_data_provider=type("Provider", (), {"load": lambda self: market_data})(),
        )



def test_public_runtime_executes_all_five_frameworks_in_registry_order():
    registry = FrameworkRegistry()
    for name in ("Aurora", "Moon", "Orbit", "Supernova", "Phoenix"):
        registry.register(name, object())

    reports = {
        "Aurora": SimpleNamespace(score=Score(10)),
        "Moon": SimpleNamespace(),
        "Orbit": SimpleNamespace(),
        "Supernova": SimpleNamespace(),
        "Phoenix": SimpleNamespace(phoenix_score=Score(20)),
    }
    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("matrix-runtime-001", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )

    result = runtime.run({
        name: make_report_adapter(name, lambda name=name: reports[name])
        for name in reports
    })

    assert [item.framework_name for item in result.framework_results] == [
        "Aurora", "Moon", "Orbit", "Supernova", "Phoenix"
    ]
    assert result.generated_events == ()


def test_public_runtime_failure_isolated_at_failing_framework_boundary():
    registry = FrameworkRegistry()
    for name in ("Aurora", "Moon", "Orbit", "Supernova", "Phoenix"):
        registry.register(name, object())

    executed = []

    def adapter(name):
        def execute(context):
            executed.append(name)
            if name == "Orbit":
                raise RuntimeError("orbit failure")
            return FrameworkResult(name, "Completed")
        return execute

    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("matrix-runtime-002", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )

    with pytest.raises(RuntimeError, match="orbit failure"):
        runtime.run({name: adapter(name) for name in registry.names})

    assert executed == ["Aurora", "Moon", "Orbit"]


def test_public_runtime_requires_executor_for_every_registered_framework():
    registry = FrameworkRegistry()
    for name in ("Aurora", "Moon", "Orbit", "Supernova", "Phoenix"):
        registry.register(name, object())

    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("matrix-runtime-003", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )

    executors = {
        name: make_report_adapter(name, lambda name=name: SimpleNamespace())
        for name in registry.names
        if name != "Phoenix"
    }
    with pytest.raises(ValueError, match="executor set does not match registry"):
        runtime.run(executors)


def test_public_runtime_does_not_return_partial_orion_result_after_framework_failure():
    registry = FrameworkRegistry()
    for name in ("Aurora", "Moon", "Orbit", "Supernova", "Phoenix"):
        registry.register(name, object())

    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("matrix-runtime-004", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )

    def failing_orbit(_):
        raise ValueError("invalid Orbit result")

    executors = {
        "Aurora": make_report_adapter("Aurora", lambda: SimpleNamespace()),
        "Moon": make_report_adapter("Moon", lambda: SimpleNamespace()),
        "Orbit": failing_orbit,
        "Supernova": make_report_adapter("Supernova", lambda: SimpleNamespace()),
        "Phoenix": make_report_adapter("Phoenix", lambda: SimpleNamespace()),
    }

    with pytest.raises(ValueError, match="invalid Orbit result"):
        runtime.run(executors)


def test_public_runtime_runs_canonical_decision_state_event_lifecycle() -> None:
    registry = FrameworkRegistry()
    registry.register("Moon", object())
    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("step18-runtime-001", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )
    candidate = DecisionCandidate(
        "candidate-step18-001", "Moon", "allocation", "Portfolio", "portfolio-001"
    )
    observed = []

    def execute(_context):
        return FrameworkResult("Moon", "Completed", decision_candidates=(candidate,))

    def accept(item):
        observed.append(("accept", runtime.states.current))
        return AcceptedDecision("decision-step18-001", item, "step18-test")

    def transition(decision):
        observed.append(("transition", runtime.states.current))
        return StateTransition(
            "transition-step18-001",
            decision.decision_id,
            "Portfolio",
            "portfolio-001",
            "old",
            "new",
        )

    def snapshot(transitions):
        observed.append(("snapshot", runtime.states.current))
        assert transitions[0].decision_id == "decision-step18-001"
        return OrionStateSnapshot(
            "2026-10-08T00:00:01Z",
            runtime.execution.execution_id,
            "v1",
            {"Moon": "new"},
            {},
            "Running",
        )

    def event_factory(item):
        observed.append(("event", runtime.states.current))
        assert runtime.states.current is None
        return Event(
            "event-step18-001",
            "State Transition Committed",
            "Domain Event",
            "2026-10-08T00:00:01Z",
            runtime.execution.execution_id,
            item.entity_type,
            item.entity_id,
            previous_state=item.previous_state,
            current_state=item.new_state,
            related_decision=item.decision_id,
        )

    result = runtime.run(
        {"Moon": execute},
        accept=accept,
        transition=transition,
        snapshot=snapshot,
        event_factory=event_factory,
    )

    assert [item[0] for item in observed] == ["accept", "transition", "snapshot", "event"]
    assert [item[1] for item in observed] == [None, None, None, None]
    assert result.state_snapshot is not None
    assert result.state_snapshot.framework_states["Moon"] == "new"
    assert result.generated_events[0].related_decision == "decision-step18-001"
    assert runtime.states.current == result.state_snapshot
    assert runtime.events.events == result.generated_events


def test_public_runtime_rejected_candidate_completes_without_state_commit() -> None:
    registry = FrameworkRegistry()
    registry.register("Moon", object())
    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("step18-runtime-002", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )
    candidate = DecisionCandidate(
        "candidate-step18-002", "Moon", "allocation", "Portfolio", "portfolio-002"
    )

    result = runtime.run(
        {"Moon": lambda _: FrameworkResult("Moon", "Completed", decision_candidates=(candidate,))},
        accept=lambda _: None,
        transition=lambda _: (_ for _ in ()).throw(AssertionError("must not transition")),
        snapshot=lambda _: (_ for _ in ()).throw(AssertionError("must not snapshot")),
    )

    assert result.state_snapshot is None
    assert result.generated_events == ()
    assert runtime.states.current is None


def test_public_runtime_preserves_framework_only_path_without_lifecycle_handlers() -> None:
    registry = FrameworkRegistry()
    registry.register("Moon", object())
    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("step18-runtime-003", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )

    candidate = DecisionCandidate(
        "candidate-step18-003", "Moon", "allocation", "Portfolio", "portfolio-003"
    )
    result = runtime.run(
        {"Moon": lambda _: FrameworkResult("Moon", "Completed", decision_candidates=(candidate,))}
    )

    assert result.framework_results[0].decision_candidates == (candidate,)
    assert result.state_snapshot is None
    assert result.generated_events == ()


def test_lifecycle_failure_discards_framework_events_and_state_snapshot() -> None:
    session = RuntimeSession(
        load_config(CONFIG_DIR),
        ExecutionMetadata("atomic-runtime-001", "2026-10-08T00:00:00Z", "v1"),
    )
    session.registry.register("Moon", object())
    candidate = DecisionCandidate("atomic-candidate-001", "Moon", "allocation", "Portfolio", "p1")
    framework_event = Event(
        "framework-event-001", "Framework Completed", "Lifecycle Event",
        session.execution.start_time, session.execution.execution_id, "Framework", "Moon",
    )

    def executor(_):
        return FrameworkResult(
            "Moon", "Completed", events=(framework_event,), decision_candidates=(candidate,)
        )

    def transition(decision):
        return StateTransition("atomic-transition-001", decision.decision_id, "Portfolio", "p1", None, "ready")

    def snapshot(_):
        return OrionStateSnapshot(
            session.execution.start_time, session.execution.execution_id, "v1", {}, {}, "Running"
        )

    with pytest.raises(RuntimeError, match="event factory failed"):
        session.execute_lifecycle(
            {"Moon": executor},
            accept=lambda item: AcceptedDecision("atomic-decision-001", item, "test"),
            transition=transition,
            snapshot=snapshot,
            event_factory=lambda _: (_ for _ in ()).throw(RuntimeError("event factory failed")),
        )

    assert session.status == "Error"
    assert session.states.snapshots == ()
    assert session.events.events == ()


def test_store_append_failure_rolls_back_snapshot_and_event_batch(monkeypatch) -> None:
    session = RuntimeSession(
        load_config(CONFIG_DIR),
        ExecutionMetadata("atomic-runtime-store-failure", "2026-10-08T00:00:00Z", "v1"),
    )
    session.registry.register("Moon", object())
    candidate = DecisionCandidate("atomic-candidate-store-failure", "Moon", "allocation", "Portfolio", "p1")
    transition_event = Event(
        "transition-event-store-failure", "State Transition Committed", "Domain Event",
        session.execution.start_time, session.execution.execution_id, "Portfolio", "p1",
    )
    original_extend = session.events.extend

    def failing_extend(events):
        original_extend(events)
        raise RuntimeError("event store failed")

    monkeypatch.setattr(session.events, "extend", failing_extend)

    with pytest.raises(RuntimeError, match="event store failed"):
        session.execute_lifecycle(
            {"Moon": lambda _: FrameworkResult("Moon", "Completed", decision_candidates=(candidate,))},
            accept=lambda item: AcceptedDecision("atomic-decision-store-failure", item, "test"),
            transition=lambda decision: StateTransition(
                "atomic-transition-store-failure", decision.decision_id, "Portfolio", "p1", None, "ready"
            ),
            snapshot=lambda _: OrionStateSnapshot(
                session.execution.start_time, session.execution.execution_id, "v1", {}, {}, "Running"
            ),
            event_factory=lambda _: transition_event,
        )

    assert session.status == "Error"
    assert session.states.snapshots == ()
    assert session.events.events == ()


@pytest.mark.parametrize(
    ("snapshot_execution_id", "snapshot_status", "transition_entity", "error"),
    (
        ("other-execution", "Running", ("Portfolio", "p1"), "snapshot execution_id"),
        ("atomic-runtime-002", "Completed", ("Portfolio", "p1"), "system_status"),
        ("atomic-runtime-002", "Running", ("Portfolio", "other"), "entity must match"),
    ),
)
def test_commit_validation_failure_leaves_both_stores_unchanged(
    snapshot_execution_id: str,
    snapshot_status: str,
    transition_entity: tuple[str, str],
    error: str,
) -> None:
    session = RuntimeSession(
        load_config(CONFIG_DIR),
        ExecutionMetadata("atomic-runtime-002", "2026-10-08T00:00:00Z", "v1"),
    )
    session.registry.register("Moon", object())
    candidate = DecisionCandidate("atomic-candidate-002", "Moon", "allocation", "Portfolio", "p1")
    candidate_event = Event(
        "framework-event-002", "Framework Completed", "Lifecycle Event",
        session.execution.start_time, session.execution.execution_id, "Framework", "Moon",
    )

    def executor(_):
        return FrameworkResult(
            "Moon", "Completed", events=(candidate_event,), decision_candidates=(candidate,)
        )

    def transition(decision):
        return StateTransition(
            "atomic-transition-002", decision.decision_id,
            transition_entity[0], transition_entity[1], None, "ready",
        )

    def snapshot(_):
        return OrionStateSnapshot(
            session.execution.start_time, snapshot_execution_id, "v1", {}, {}, snapshot_status
        )

    with pytest.raises(ValueError, match=error):
        session.execute_lifecycle(
            {"Moon": executor},
            accept=lambda item: AcceptedDecision("atomic-decision-002", item, "test"),
            transition=transition,
            snapshot=snapshot,
        )

    assert session.status == "Error"
    assert session.states.snapshots == ()
    assert session.events.events == ()


def test_public_runtime_rejects_second_run() -> None:
    registry = FrameworkRegistry()
    registry.register("Moon", object())
    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("single-run-001", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )
    executor = {"Moon": lambda _: FrameworkResult("Moon", "Completed")}

    runtime.run(executor)
    with pytest.raises(RuntimeError, match="only be run once"):
        runtime.run(executor)


def test_public_runtime_validates_dashboard_input_before_execution() -> None:
    registry = FrameworkRegistry()
    registry.register("Moon", object())
    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("dashboard-validation-001", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )
    executor = {"Moon": lambda _: FrameworkResult("Moon", "Completed")}

    with pytest.raises(ValueError, match="dashboard_data must be a mapping"):
        runtime.run(executor, dashboard_data=[("invalid", "shape")])

    assert runtime.run(executor).generated_events == ()


def test_public_runtime_rejects_partial_decision_lifecycle_handlers() -> None:
    registry = FrameworkRegistry()
    registry.register("Moon", object())
    runtime = OrionRuntime(
        load_config(CONFIG_DIR),
        ExecutionMetadata("step18-runtime-004", "2026-10-08T00:00:00Z", "v1"),
        registry=registry,
    )

    with pytest.raises(ValueError, match="accept, transition, and snapshot"):
        runtime.run(
            {"Moon": lambda _: FrameworkResult("Moon", "Completed")},
            accept=lambda _: None,
        )
