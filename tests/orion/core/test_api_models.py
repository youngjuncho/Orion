import pytest

from orion.core import ExecutionMetadata, FrameworkResult, HealthReport, OrionResult, Score, State


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
