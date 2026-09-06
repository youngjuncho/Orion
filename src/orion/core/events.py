"""Immutable domain event contract for Orion framework outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

EVENT_CATEGORIES = frozenset(
    {"System", "Aurora", "Moon", "Supernova", "Phoenix", "Portfolio", "Governance"}
)
EVENT_SEVERITIES = frozenset({"Information", "Notice", "Warning", "Critical"})


@dataclass(frozen=True)
class Event:
    """A validated, immutable event record."""

    event_id: str
    timestamp: str
    category: str
    event_type: str
    source_framework: str
    entity: str
    previous_state: str
    current_state: str
    severity: str
    description: str = ""
    metadata: Mapping[str, str] = field(default_factory=dict)
    related_decision: str | None = None
    related_review: str | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("event_id", self.event_id),
            ("timestamp", self.timestamp),
            ("category", self.category),
            ("event_type", self.event_type),
            ("source_framework", self.source_framework),
            ("entity", self.entity),
            ("previous_state", self.previous_state),
            ("current_state", self.current_state),
            ("severity", self.severity),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        if self.category not in EVENT_CATEGORIES:
            raise ValueError(f"unsupported event category: {self.category}")
        if self.severity not in EVENT_SEVERITIES:
            raise ValueError(f"unsupported event severity: {self.severity}")

        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
