import pytest

from orion.core import Score
from orion.dashboard import (
    AuroraSummary,
    MoonSummary,
    OrionDashboard,
    OrionDashboardView,
    PortfolioSummary,
)


def test_orion_dashboard_build_view() -> None:
    view = OrionDashboard().build_view()

    assert isinstance(view, OrionDashboardView)
    assert view.aurora.market_regime == "Unknown"
    assert view.supernova.approved_companies[0] == "NVDA"
    assert view.phoenix.current_leaders[0] == "SOL"


def test_moon_dashboard_summary_snapshots_collections() -> None:
    strategies = ["ADM"]
    holdings = ["VTI"]
    summary = MoonSummary(strategies, "100% VTI", holdings, "Monthly")
    strategies.clear()
    holdings.clear()

    assert summary.active_strategies == ("ADM",)
    assert summary.current_holdings == ("VTI",)


def test_dashboard_models_reject_invalid_values_and_component_types() -> None:
    with pytest.raises(ValueError, match="total_portfolio_value"):
        PortfolioSummary(float("nan"), "Unknown", "Unknown", "Unknown")
    with pytest.raises(ValueError, match="score"):
        AuroraSummary(80, "Neutral", "Unknown", "Stable")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="portfolio"):
        OrionDashboardView(None, None, None, None, None)  # type: ignore[arg-type]
