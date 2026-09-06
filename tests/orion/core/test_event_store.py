import pytest

from orion.core import Event, EventStore


def make_event(event_id: str) -> Event:
    return Event(event_id, "2026-08-01", "System", "Engine Started", "System", "Orion", "Idle", "Running", "Information")


def test_event_store_preserves_append_order() -> None:
    store = EventStore()
    first = make_event("event-001")
    second = make_event("event-002")

    store.extend((first, second))

    assert store.events == (first, second)


def test_event_store_rejects_duplicate_event_id() -> None:
    store = EventStore()
    store.append(make_event("event-001"))

    with pytest.raises(ValueError, match="already exists"):
        store.append(make_event("event-001"))


def test_event_store_rejects_duplicate_batch_without_partial_append() -> None:
    store = EventStore()
    first = make_event("event-001")
    second = make_event("event-001")

    with pytest.raises(ValueError, match="duplicate"):
        store.extend((first, second))

    assert store.events == ()
