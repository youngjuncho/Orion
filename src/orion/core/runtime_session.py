"""Minimal in-memory Runtime lifecycle coordination."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from .config_loader import OrionConfig
from .event_store import EventStore
from .execution import ExecutionMetadata
from .framework_registry import FrameworkRegistry
from .runtime import RuntimeContext
from .state import SYSTEM_STATUSES
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
