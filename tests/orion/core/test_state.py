import pytest

from orion.core import OrionStateSnapshot


def test_state_snapshot_preserves_documented_fields() -> None:
    snapshot = OrionStateSnapshot(
        timestamp="2026-08-01T09:00:00+09:00",
        execution_id="execution-001",
        orion_version="1.0",
        framework_states={"Aurora": "Neutral", "Moon": "Risk On"},
        portfolio_state={"ETF Allocation": "100%"},
        system_status="Completed",
    )

    assert snapshot.framework_states["Moon"] == "Risk On"
    assert snapshot.system_status == "Completed"


def test_state_snapshot_rejects_unsupported_system_status() -> None:
    with pytest.raises(ValueError, match="system status"):
        OrionStateSnapshot("2026-08-01", "execution-001", "1.0", system_status="Paused")


def test_state_snapshot_rejects_empty_identity_fields() -> None:
    with pytest.raises(ValueError, match="execution_id"):
        OrionStateSnapshot("2026-08-01", "", "1.0")


def test_state_snapshot_rejects_invalid_map_values_and_snapshots_inputs() -> None:
    with pytest.raises(ValueError, match="framework_states"):
        OrionStateSnapshot(
            "2026-08-01",
            "execution-001",
            "1.0",
            framework_states={"Moon": 1},  # type: ignore[dict-item]
        )

    framework_states = {"Moon": "Risk On"}
    snapshot = OrionStateSnapshot(
        "2026-08-01", "execution-002", "1.0", framework_states=framework_states
    )
    framework_states["Moon"] = "Risk Off"

    assert snapshot.framework_states["Moon"] == "Risk On"
