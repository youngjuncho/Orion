"""In-memory append-only event collection for one Orion execution."""

from __future__ import annotations

from dataclasses import dataclass, field

from .events import Event


@dataclass
class EventStore:
    """Collect immutable events without providing persistence or publishing."""

    _events: list[Event] = field(default_factory=list, init=False, repr=False)

    @property
    def events(self) -> tuple[Event, ...]:
        """Return events in append order as an immutable view."""

        return tuple(self._events)

    def append(self, event: Event) -> None:
        """Append one event, rejecting duplicate event identifiers."""

        if any(existing.event_id == event.event_id for existing in self._events):
            raise ValueError(f"event_id already exists: {event.event_id}")
        self._events.append(event)

    def extend(self, events: tuple[Event, ...]) -> None:
        """Append a batch atomically with respect to duplicate identifiers."""

        incoming_ids = [event.event_id for event in events]
        if len(incoming_ids) != len(set(incoming_ids)):
            raise ValueError("events must not contain duplicate event_ids")

        existing_ids = {event.event_id for event in self._events}
        duplicates = sorted(existing_ids.intersection(incoming_ids))
        if duplicates:
            raise ValueError(f"event_id already exists: {', '.join(duplicates)}")

        self._events.extend(events)
