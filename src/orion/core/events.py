"""Immutable domain/lifecycle event contract for Orion."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

EVENT_CATEGORIES = frozenset({"Domain Event", "Lifecycle Event"})
EVENT_SEVERITIES = frozenset({"Information", "Notice", "Warning", "Critical"})


@dataclass(frozen=True)
class Event:
    """A validated, immutable event record using the canonical Core contract."""

    event_id: str
    event_type: str
    event_category: str
    occurred_at: str
    execution_id: str
    entity_type: str
    entity_id: str
    payload: Mapping[str, object] = field(default_factory=dict)
    source_framework: str | None = None
    previous_state: str | None = None
    current_state: str | None = None
    severity: str = "Information"
    description: str = ""
    metadata: Mapping[str, str] = field(default_factory=dict)
    related_decision: str | None = None
    related_review: str | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("event_id", self.event_id),
            ("event_type", self.event_type),
            ("event_category", self.event_category),
            ("occurred_at", self.occurred_at),
            ("execution_id", self.execution_id),
            ("entity_type", self.entity_type),
            ("entity_id", self.entity_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        if self.event_category not in EVENT_CATEGORIES:
            raise ValueError(f"unsupported event category: {self.event_category}")
        if self.severity not in EVENT_SEVERITIES:
            raise ValueError(f"unsupported event severity: {self.severity}")

        if self.source_framework is not None and (
            not isinstance(self.source_framework, str) or not self.source_framework.strip()
        ):
            raise ValueError("source_framework must be a non-empty string when provided")
        for name, value in (
            ("previous_state", self.previous_state),
            ("current_state", self.current_state),
            ("related_decision", self.related_decision),
            ("related_review", self.related_review),
        ):
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{name} must be a non-empty string when provided")
        if not isinstance(self.description, str):
            raise ValueError("description must be a string")
        if not isinstance(self.payload, Mapping):
            raise ValueError("payload must be a mapping")
        payload = dict(self.payload)
        if any(not isinstance(key, str) for key in payload):
            raise ValueError("payload keys must be strings")
        object.__setattr__(self, "payload", MappingProxyType(payload))

        if not isinstance(self.metadata, Mapping):
            raise ValueError("metadata must be a mapping")
        metadata = dict(self.metadata)
        if any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in metadata.items()
        ):
            raise ValueError("metadata keys and values must be strings")
        object.__setattr__(self, "metadata", MappingProxyType(metadata))
