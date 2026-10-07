import pytest

from orion.core import ExecutionMetadata, OrionResult, Score
from orion.dashboard import AuroraSummary, MoonSummary, OrionDashboard, OrionDashboardView, PortfolioSummary


def _result() -> OrionResult:
    return OrionResult(
        runtime_summary=ExecutionMetadata("exec-1", "2026-10-07T09:00:00+09:00", "1.0"),
        dashboard_data={
            "aurora": {"score": Score(82), "market_regime": "Risk On", "risk_state": "Stable", "regime_direction": "Improving"},
            "moon": {"active_strategies": ("ADM",), "consensus_allocation": "100% SPYM", "current_holdings": ("SPYM",), "next_rebalance_date": "2026-11-02"},
            "supernova": {"approved_companies": ("NVDA",), "theme_health": "Healthy", "leadership_status": "Leader", "replacement_risk": "Low"},
            "phoenix": {"categories": ("Smart Contract",), "current_leaders": ("SOL",), "challenger_status": "Stable", "replacement_risk": "Low"},
        },
    )


def test_orion_dashboard_build_view_from_runtime_result() -> None:
    view = OrionDashboard().build_view(_result())
    assert isinstance(view, OrionDashboardView)
    assert view.aurora.market_regime == "Risk On"
    assert view.supernova.approved_companies[0] == "NVDA"
    assert view.phoenix.current_leaders[0] == "SOL"


def test_orion_dashboard_does_not_require_framework_engine_calls() -> None:
    view = OrionDashboard().build_view()
    assert view.aurora.market_regime == "Unknown"
    assert view.supernova.approved_companies == ()


def test_moon_dashboard_summary_snapshots_collections() -> None:
    strategies = ["ADM"]
    holdings = ["VTI"]
    summary = MoonSummary(strategies, "100% VTI", holdings, "Monthly")
    strategies.clear(); holdings.clear()
    assert summary.active_strategies == ("ADM",)
    assert summary.current_holdings == ("VTI",)


def test_dashboard_models_reject_invalid_values_and_component_types() -> None:
    with pytest.raises(ValueError, match="total_portfolio_value"):
        PortfolioSummary(float("nan"), "Unknown", "Unknown", "Unknown")
    with pytest.raises(ValueError, match="score"):
        AuroraSummary(80, "Neutral", "Unknown", "Stable")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="portfolio"):
        OrionDashboardView(None, None, None, None, None)  # type: ignore[arg-type]
