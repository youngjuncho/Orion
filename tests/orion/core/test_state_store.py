import pytest

from orion.core import OrionStateSnapshot, StateStore


def make_snapshot(execution_id: str) -> OrionStateSnapshot:
    return OrionStateSnapshot("2026-08-01", execution_id, "1.0", system_status="Completed")


def test_state_store_preserves_snapshots_and_tracks_current() -> None:
    store = StateStore()
    first = make_snapshot("execution-001")
    second = make_snapshot("execution-002")

    store.publish(first)
    store.publish(second)

    assert store.snapshots == (first, second)
    assert store.current == second


def test_state_store_starts_without_current_snapshot() -> None:
    assert StateStore().current is None


def test_state_store_rejects_duplicate_execution_id() -> None:
    store = StateStore()
    store.publish(make_snapshot("execution-001"))

    with pytest.raises(ValueError, match="already exists"):
        store.publish(make_snapshot("execution-001"))
