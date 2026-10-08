"""Minimal in-memory Runtime lifecycle coordination."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping, Sequence

from .config_loader import OrionConfig
from .decision import AcceptedDecision, DecisionCandidate, StateTransition
from .events import Event
from .event_store import EventStore
from .execution import ExecutionMetadata
from .api_models import FrameworkResult, OrionResult
from .framework_registry import FrameworkRegistry
from .runtime import RuntimeContext
from .state import SYSTEM_STATUSES, OrionStateSnapshot
from .state_store import StateStore
from orion.services import ServiceRegistry
from data.contracts import MarketDataSet


@dataclass
class RuntimeSession:
    """Coordinate the lifecycle state for one Orion execution."""

    configuration: OrionConfig
    execution: ExecutionMetadata
    registry: FrameworkRegistry = field(default_factory=FrameworkRegistry)
    services: ServiceRegistry = field(default_factory=ServiceRegistry)
    events: EventStore = field(default_factory=EventStore)
    states: StateStore = field(default_factory=StateStore)
    status: str = "Initializing"

    def __post_init__(self) -> None:
        if self.status not in SYSTEM_STATUSES:
            raise ValueError(f"unsupported runtime status: {self.status}")

    def start(self) -> None:
        """Move an initialized runtime into execution."""

        self._transition("Initializing", "Running")

    def complete(self) -> None:
        """Mark a running runtime as completed."""

        self._transition("Running", "Completed")

    def fail(self) -> None:
        """Mark an initializing or running runtime as failed."""

        if self.status not in {"Initializing", "Running"}:
            raise RuntimeError(f"cannot fail runtime from status: {self.status}")
        self.status = "Error"

    def execute_frameworks(
        self,
        executors: Mapping[str, Callable[[RuntimeContext], FrameworkResult]],
        *,
        market_data: MarketDataSet | None = None,
        dashboard_data: Mapping[str, object] | None = None,
    ) -> OrionResult:
        """Execute frameworks and finalize the framework-only Runtime path.

        This preserves the historical public framework-execution boundary. The
        full canonical lifecycle is exposed separately by ``execute_lifecycle``.
        """
        results = self._execute_frameworks(
            executors,
            market_data=market_data,
            dashboard_data=dashboard_data,
        )
        self.complete()
        return self._build_result(results, dashboard_data=dashboard_data)

    def execute_lifecycle(
        self,
        executors: Mapping[str, Callable[[RuntimeContext], FrameworkResult]],
        *,
        accept: Callable[[DecisionCandidate], AcceptedDecision | None],
        transition: Callable[[AcceptedDecision], StateTransition],
        snapshot: Callable[[tuple[StateTransition, ...]], OrionStateSnapshot],
        event_factory: Callable[[StateTransition], Event] | None = None,
        market_data: MarketDataSet | None = None,
        dashboard_data: Mapping[str, object] | None = None,
    ) -> OrionResult:
        """Execute one public canonical Runtime lifecycle.

        Frameworks propose ``DecisionCandidate`` values. The Runtime applies
        the configured acceptance policy (the public Runtime defaults to
        Auto-Approval), then requires explicit transition and snapshot handlers.
        State commit remains authoritative before transition
        events are created.
        """
        results = self._execute_frameworks(
            executors,
            market_data=market_data,
            dashboard_data=dashboard_data,
        )
        candidates = tuple(
            candidate
            for result in results
            for candidate in result.decision_candidates
        )

        try:
            self.resolve_and_commit(
                candidates,
                accept,
                transition,
                snapshot,
                event_factory,
            )
            self.complete()
        except Exception:
            self.fail()
            raise

        return self._build_result(results, dashboard_data=dashboard_data)

    def _execute_frameworks(
        self,
        executors: Mapping[str, Callable[[RuntimeContext], FrameworkResult]],
        *,
        market_data: MarketDataSet | None = None,
        dashboard_data: Mapping[str, object] | None = None,
    ) -> tuple[FrameworkResult, ...]:
        """Execute and validate framework adapters without finalizing the session."""
        if self.status != "Initializing":
            raise RuntimeError(f"cannot execute frameworks from status: {self.status}")

        if set(executors) != set(self.registry.names):
            missing = sorted(set(self.registry.names) - set(executors))
            unknown = sorted(set(executors) - set(self.registry.names))
            details = []
            if missing:
                details.append(f"missing={missing}")
            if unknown:
                details.append(f"unknown={unknown}")
            raise ValueError("framework executor set does not match registry: " + ", ".join(details))

        self.start()
        results: list[FrameworkResult] = []
        try:
            for name in self.registry.names:
                context = self.build_context(
                    market_data=market_data,
                    framework_results={result.framework_name: result for result in results},
                    dashboard_data=dashboard_data,
                )
                result = executors[name](context)
                if not isinstance(result, FrameworkResult):
                    raise TypeError(
                        f"framework '{name}' must return FrameworkResult, "
                        f"got {type(result).__name__}"
                    )
                if result.framework_name != name:
                    raise ValueError(
                        f"framework '{name}' returned result for '{result.framework_name}'"
                    )
                results.append(result)
        except Exception:
            self.fail()
            raise

        generated_events = tuple(
            event
            for result in results
            for event in result.events
        )
        self.record_events(generated_events)
        return tuple(results)

    def _build_result(
        self,
        results: Sequence[FrameworkResult],
        *,
        dashboard_data: Mapping[str, object] | None = None,
    ) -> OrionResult:
        return OrionResult(
            runtime_summary=self.execution,
            framework_results=tuple(results),
            state_snapshot=self.states.current,
            generated_events=self.events.events,
            dashboard_data=dashboard_data or {},
        )

    def resolve_and_commit(
        self,
        candidates: Sequence[DecisionCandidate],
        accept: Callable[[DecisionCandidate], AcceptedDecision | None],
        transition: Callable[[AcceptedDecision], StateTransition],
        snapshot: Callable[[tuple[StateTransition, ...]], OrionStateSnapshot],
        event_factory: Callable[[StateTransition], Event] | None = None,
    ) -> tuple[AcceptedDecision, ...]:
        """Resolve candidates explicitly and commit one resulting state snapshot.

        Runtime owns the orchestration boundary. Frameworks only propose candidates;
        acceptance and state transition are supplied explicitly by the caller. No
        decision is accepted implicitly, and StateStore is the commit boundary.
        Domain Event creation is performed only after successful StateStore commit.
        """
        if self.status != "Running":
            raise RuntimeError(f"cannot resolve decisions from status: {self.status}")

        candidates = tuple(candidates)
        candidate_ids = {candidate.candidate_id for candidate in candidates}
        if len(candidate_ids) != len(candidates):
            raise ValueError("decision candidate IDs must be unique")

        accepted: list[AcceptedDecision] = []
        for candidate in candidates:
            decision = accept(candidate)
            if decision is None:
                continue
            if not isinstance(decision, AcceptedDecision):
                raise TypeError("accept must return AcceptedDecision or None")
            if decision.candidate.candidate_id != candidate.candidate_id:
                raise ValueError("accepted decision must reference the current candidate")
            accepted.append(decision)

        transitions: list[StateTransition] = []
        for decision in accepted:
            state_transition = transition(decision)
            if not isinstance(state_transition, StateTransition):
                raise TypeError("transition must return StateTransition")
            if state_transition.decision_id != decision.decision_id:
                raise ValueError("state transition must reference the accepted decision")
            transitions.append(state_transition)

        if transitions:
            state_snapshot = snapshot(tuple(transitions))
            if not isinstance(state_snapshot, OrionStateSnapshot):
                raise TypeError("snapshot must return OrionStateSnapshot")
            self.states.publish(state_snapshot)

            if event_factory is not None:
                events = tuple(event_factory(item) for item in transitions)
                self.record_events(events)

        return tuple(accepted)

    def record_events(self, events: Sequence[Event]) -> tuple[Event, ...]:
        """Append execution-correlated events after the authoritative commit boundary."""
        events = tuple(events)
        self._validate_events(events)
        self.events.extend(events)
        return events

    def _validate_events(self, events: tuple[Event, ...]) -> None:
        if any(not isinstance(event, Event) for event in events):
            raise TypeError("events must contain only Event values")
        mismatched = [
            event.event_id
            for event in events
            if event.execution_id != self.execution.execution_id
        ]
        if mismatched:
            raise ValueError(
                "all events must use the current execution_id: "
                + ", ".join(mismatched)
            )
        incoming_ids = [event.event_id for event in events]
        if len(incoming_ids) != len(set(incoming_ids)):
            raise ValueError("events must not contain duplicate event_ids")
        existing_ids = {event.event_id for event in self.events.events}
        duplicates = sorted(existing_ids.intersection(incoming_ids))
        if duplicates:
            raise ValueError("event_id already exists: " + ", ".join(duplicates))

    def build_context(
        self,
        *,
        market_data: MarketDataSet | None = None,
        framework_results: Mapping[str, object] | None = None,
        dashboard_data: Mapping[str, object] | None = None,
    ) -> RuntimeContext:
        """Build a read-only context from the current in-memory session state.

        Framework registration must happen before a context is built. This
        helper does not execute frameworks or persist any runtime state.
        """

        return RuntimeContext(
            configuration=self.configuration,
            execution=self.execution,
            market_data=market_data,
            registered_frameworks=self.registry.names,
            services=self.services.snapshot,
            framework_results=framework_results or {},
            system_state=self.states.current,
            dashboard_data=dashboard_data or {},
        )

    def _transition(self, expected: str, target: str) -> None:
        if self.status != expected:
            raise RuntimeError(f"cannot move runtime from {self.status} to {target}")
        self.status = target
