"""Typed result contracts exposed by the Orion API layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from .events import Event
from .execution import ExecutionMetadata
from .models import Score, State
from .state import OrionStateSnapshot

T = TypeVar("T")


@dataclass(frozen=True)
class FrameworkResult:
    """Result contract for one framework execution."""

    framework_name: str
    execution_status: str
    state: State | None = None
    score: Score | None = None
    events: tuple[Event, ...] = ()

    def __post_init__(self) -> None:
        _require_non_empty_string("framework_name", self.framework_name)
        _require_non_empty_string("execution_status", self.execution_status)
        if self.state is not None and not isinstance(self.state, State):
            raise ValueError("state must be a State when provided")
        if self.score is not None and not isinstance(self.score, Score):
            raise ValueError("score must be a Score when provided")
        object.__setattr__(self, "events", _typed_tuple(self.events, Event, "events"))


@dataclass(frozen=True)
class HealthReport:
    """Health result contract for runtime and service checks."""

    overall_status: str
    failed_components: tuple[str, ...] = ()
    warning_messages: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_non_empty_string("overall_status", self.overall_status)
        object.__setattr__(
            self,
            "failed_components",
            _non_empty_string_tuple(self.failed_components, "failed_components"),
        )
        object.__setattr__(
            self,
            "warning_messages",
            _non_empty_string_tuple(self.warning_messages, "warning_messages"),
        )


@dataclass(frozen=True)
class OrionResult:
    """Combined result contract for one complete Orion execution."""

    runtime_summary: ExecutionMetadata
    framework_results: tuple[FrameworkResult, ...] = ()
    state_snapshot: OrionStateSnapshot | None = None
    generated_events: tuple[Event, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.runtime_summary, ExecutionMetadata):
            raise ValueError("runtime_summary must be ExecutionMetadata")
        if self.state_snapshot is not None and not isinstance(
            self.state_snapshot, OrionStateSnapshot
        ):
            raise ValueError("state_snapshot must be OrionStateSnapshot when provided")
        object.__setattr__(
            self,
            "framework_results",
            _typed_tuple(
                self.framework_results, FrameworkResult, "framework_results"
            ),
        )
        object.__setattr__(
            self,
            "generated_events",
            _typed_tuple(self.generated_events, Event, "generated_events"),
        )


def _require_non_empty_string(name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")


def _non_empty_string_tuple(values: object, name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name} must be a sequence of strings")
    try:
        items = tuple(values)  # type: ignore[arg-type]
    except TypeError as exc:
        raise ValueError(f"{name} must be a sequence of strings") from exc
    if any(not isinstance(item, str) or not item.strip() for item in items):
        raise ValueError(f"{name} must contain non-empty strings")
    return items


def _typed_tuple(values: object, item_type: type[T], name: str) -> tuple[T, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name} must be a sequence of {item_type.__name__} values")
    try:
        items = tuple(values)  # type: ignore[arg-type]
    except TypeError as exc:
        raise ValueError(
            f"{name} must be a sequence of {item_type.__name__} values"
        ) from exc
    if any(not isinstance(item, item_type) for item in items):
        raise ValueError(f"{name} must contain only {item_type.__name__} values")
    return items
