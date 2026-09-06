"""Minimal in-memory Runtime lifecycle coordination."""

from __future__ import annotations

from dataclasses import dataclass, field

from .config_loader import OrionConfig
from .event_store import EventStore
from .execution import ExecutionMetadata
from .framework_registry import FrameworkRegistry
from .state import SYSTEM_STATUSES
from .state_store import StateStore


@dataclass
class RuntimeSession:
    """Coordinate the lifecycle state for one Orion execution."""

    configuration: OrionConfig
    execution: ExecutionMetadata
    registry: FrameworkRegistry = field(default_factory=FrameworkRegistry)
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

    def _transition(self, expected: str, target: str) -> None:
        if self.status != expected:
            raise RuntimeError(f"cannot move runtime from {self.status} to {target}")
        self.status = target
