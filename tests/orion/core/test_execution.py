import pytest

from orion.core import ExecutionMetadata


def test_execution_metadata_preserves_runtime_fields() -> None:
    metadata = ExecutionMetadata(
        execution_id="execution-001",
        start_time="2026-08-01T09:00:00+09:00",
        orion_version="1.0",
        end_time="2026-08-01T09:00:02+09:00",
        duration_seconds=2.0,
    )

    assert metadata.execution_id == "execution-001"
    assert metadata.duration_seconds == 2.0


def test_execution_metadata_rejects_negative_duration() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        ExecutionMetadata("execution-001", "2026-08-01", "1.0", duration_seconds=-1.0)


def test_execution_metadata_rejects_empty_required_field() -> None:
    with pytest.raises(ValueError, match="start_time"):
        ExecutionMetadata("execution-001", "", "1.0")
