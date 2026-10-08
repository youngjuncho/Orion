"""Public Orion Runtime application boundary."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping

from data.contracts import MarketDataProvider, MarketDataSet

from .api_models import FrameworkResult, OrionResult
from .decision import AcceptedDecision, DecisionCandidate, StateTransition, auto_approve
from .events import Event
from .state import OrionStateSnapshot
from .config_loader import OrionConfig
from .execution import ExecutionMetadata
from .framework_registry import FrameworkRegistry
from .runtime_session import RuntimeSession
from .runtime import RuntimeContext
from .state_store import StateStore
from .framework_adapters import FrameworkAdapter
from .event_store import EventStore
from orion.services import ServiceRegistry


FrameworkExecutor = FrameworkAdapter


@dataclass
class OrionRuntime:
    """Public entry point that creates and runs one RuntimeSession.

    The public boundary delegates lifecycle orchestration to RuntimeSession.
    It does not contain framework investment methodology or duplicate the
    decision/state/event contracts owned by the Core Runtime.
    """

    configuration: OrionConfig
    execution: ExecutionMetadata
    registry: FrameworkRegistry = field(default_factory=FrameworkRegistry)
    services: ServiceRegistry = field(default_factory=ServiceRegistry)
    events: EventStore = field(default_factory=EventStore)
    states: StateStore = field(default_factory=StateStore)

    def create_session(self) -> RuntimeSession:
        """Create the in-memory session used for one public runtime call."""

        return RuntimeSession(
            configuration=self.configuration,
            execution=self.execution,
            registry=self.registry,
            services=self.services,
            events=self.events,
            states=self.states,
        )

    def run(
        self,
        executors: Mapping[str, FrameworkExecutor],
        *,
        accept: Callable[[DecisionCandidate], AcceptedDecision | None] | None = None,
        transition: Callable[[AcceptedDecision], StateTransition] | None = None,
        snapshot: Callable[[tuple[StateTransition, ...]], OrionStateSnapshot] | None = None,
        event_factory: Callable[[StateTransition], Event] | None = None,
        market_data: MarketDataSet | None = None,
        dashboard_data: Mapping[str, object] | None = None,
        market_data_provider: MarketDataProvider | None = None,
    ) -> OrionResult:
        """Execute registered frameworks with an optional canonical data handoff.

        ``market_data`` remains a valid direct-input path for tests and callers
        that already possess a validated ``MarketDataSet``. A provider is used
        only when direct data is omitted; source collection and normalization
        remain outside the Runtime boundary.
        """
        if market_data is not None and market_data_provider is not None:
            raise ValueError("provide either market_data or market_data_provider, not both")

        if market_data_provider is not None:
            market_data = market_data_provider.load()
            if not isinstance(market_data, MarketDataSet):
                raise TypeError("market_data_provider.load() must return MarketDataSet")

        session = self.create_session()
        lifecycle_handlers = (accept, transition, snapshot, event_factory)
        has_handlers = any(handler is not None for handler in lifecycle_handlers)
        if has_handlers and (transition is None or snapshot is None):
            raise ValueError(
                "accept, transition, and snapshot must be provided together for the decision lifecycle; "
                "accept may be omitted to use Auto-Approval"
            )
        if has_handlers and accept is None:
            accept = auto_approve

        if not has_handlers:
            return session.execute_frameworks(
                executors,
                market_data=market_data,
                dashboard_data=dashboard_data,
            )

        return session.execute_lifecycle(
            executors,
            accept=accept,
            transition=transition,
            snapshot=snapshot,
            event_factory=event_factory,
            market_data=market_data,
            dashboard_data=dashboard_data,
        )
