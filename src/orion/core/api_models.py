"""Typed result contracts exposed by the Orion API layer."""

from __future__ import annotations

from dataclasses import dataclass

from .events import Event
from .execution import ExecutionMetadata
from .models import Score, State
from .state import OrionStateSnapshot


@dataclass(frozen=True)
class FrameworkResult:
    """Result contract for one framework execution."""

    framework_name: str
    execution_status: str
    state: State | None = None
    score: Score | None = None
    events: tuple[Event, ...] = ()

    def __post_init__(self) -> None:
        if not self.framework_name.strip():
            raise ValueError("framework_name must not be empty")
        if not self.execution_status.strip():
            raise ValueError("execution_status must not be empty")


@dataclass(frozen=True)
class HealthReport:
    """Health result contract for runtime and service checks."""

    overall_status: str
    failed_components: tuple[str, ...] = ()
    warning_messages: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.overall_status.strip():
            raise ValueError("overall_status must not be empty")


@dataclass(frozen=True)
class OrionResult:
    """Combined result contract for one complete Orion execution."""

    runtime_summary: ExecutionMetadata
    framework_results: tuple[FrameworkResult, ...] = ()
    state_snapshot: OrionStateSnapshot | None = None
    generated_events: tuple[Event, ...] = ()
