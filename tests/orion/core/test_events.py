import pytest
from orion.core import Event


def make_event(**overrides: object) -> Event:
    values = {
        "event_id": "event-001",
        "event_type": "State Updated",
        "event_category": "Domain Event",
        "occurred_at": "2026-08-01T09:00:00+09:00",
        "execution_id": "execution-001",
        "entity_type": "Portfolio",
        "entity_id": "MOON",
        "payload": {"signal_date": "2026-07-31"},
        "severity": "Notice",
    }
    values.update(overrides)
    return Event(**values)


def test_event_uses_canonical_contract() -> None:
    event = make_event(source_framework="Moon")
    assert event.event_category == "Domain Event"
    assert event.execution_id == "execution-001"
    assert event.entity_type == "Portfolio"
    assert event.entity_id == "MOON"
    assert event.payload["signal_date"] == "2026-07-31"


def test_event_rejects_unsupported_category() -> None:
    with pytest.raises(ValueError, match="category"):
        make_event(event_category="Moon")


def test_event_requires_execution_and_entity_identity() -> None:
    with pytest.raises(ValueError, match="execution_id"):
        make_event(execution_id="")
    with pytest.raises(ValueError, match="entity_id"):
        make_event(entity_id="")


def test_event_rejects_unsupported_severity() -> None:
    with pytest.raises(ValueError, match="severity"):
        make_event(severity="Urgent")
