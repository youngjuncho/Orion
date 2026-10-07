import pytest

from orion.core import (
    Event,
    ExecutionMetadata,
    FrameworkResult,
    HealthReport,
    OrionResult,
    Score,
    State,
)


def test_framework_result_connects_state_score_and_events() -> None:
    result = FrameworkResult(
        framework_name="Aurora",
        execution_status="Completed",
        state=State("Risk On"),
        score=Score(80),
    )

    assert result.framework_name == "Aurora"
    assert result.score == Score(80)


def test_health_report_preserves_failures_and_warnings() -> None:
    report = HealthReport("Warning", ("Market Data",), ("Stale data",))

    assert report.failed_components == ("Market Data",)
    assert report.warning_messages == ("Stale data",)


def test_orion_result_requires_runtime_summary() -> None:
    summary = ExecutionMetadata("execution-001", "2026-08-01", "1.0")
    result = OrionResult(summary)

    assert result.runtime_summary == summary


def test_api_contracts_reject_empty_names() -> None:
    with pytest.raises(ValueError, match="framework_name"):
        FrameworkResult("", "Completed")

    with pytest.raises(ValueError, match="overall_status"):
        HealthReport("")


def test_result_contracts_snapshot_collection_inputs() -> None:
    event = Event(
        event_id="event-001",
        event_type="Started",
        event_category="Lifecycle Event",
        occurred_at="2026-08-01",
        execution_id="execution-001",
        entity_type="Runtime",
        entity_id="Orion",
        payload={},
    )
    events = [event]
    framework = FrameworkResult("Moon", "Completed", events=events)
    frameworks = [framework]
    result = OrionResult(
        ExecutionMetadata("execution-001", "today", "1.0"), frameworks
    )
    events.clear()
    frameworks.clear()

    assert framework.events == (event,)
    assert result.framework_results == (framework,)
    assert isinstance(result.framework_results, tuple)


def test_api_contracts_reject_invalid_collection_members() -> None:
    with pytest.raises(ValueError, match="warning_messages"):
        HealthReport("Warning", warning_messages=[""])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="FrameworkResult"):
        OrionResult(
            ExecutionMetadata("execution-001", "today", "1.0"),
            ["bad"],  # type: ignore[arg-type]
        )
