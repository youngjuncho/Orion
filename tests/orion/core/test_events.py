import pytest

from orion.core import Event


def test_event_preserves_documented_fields() -> None:
    event = Event(
        event_id="event-001",
        timestamp="2026-08-01T09:00:00+09:00",
        category="Moon",
        event_type="Consensus Allocation Updated",
        source_framework="Moon",
        entity="Portfolio",
        previous_state="SPYM 100%",
        current_state="QQQM 50%, SPYM 50%",
        severity="Notice",
        metadata={"signal_date": "2026-07-31"},
    )

    assert event.category == "Moon"
    assert event.metadata["signal_date"] == "2026-07-31"


def test_event_rejects_unsupported_category() -> None:
    with pytest.raises(ValueError, match="category"):
        Event("event-001", "2026-08-01", "Unknown", "State Updated", "Moon", "Portfolio", "A", "B", "Notice")


def test_event_rejects_unsupported_severity() -> None:
    with pytest.raises(ValueError, match="severity"):
        Event("event-001", "2026-08-01", "Moon", "State Updated", "Moon", "Portfolio", "A", "B", "Urgent")


def test_event_rejects_empty_required_fields() -> None:
    with pytest.raises(ValueError, match="event_id"):
        Event("", "2026-08-01", "Moon", "State Updated", "Moon", "Portfolio", "A", "B", "Notice")


def test_event_rejects_non_string_metadata_values() -> None:
    with pytest.raises(ValueError, match="metadata keys and values"):
        Event(
            "event-001",
            "2026-08-01",
            "Moon",
            "State Updated",
            "Moon",
            "Portfolio",
            "A",
            "B",
            "Notice",
            metadata={"attempt": 1},  # type: ignore[dict-item]
        )
