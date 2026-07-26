from src.dashboard import OrionDashboard, OrionDashboardView


def test_orion_dashboard_build_view() -> None:
    view = OrionDashboard().build_view()

    assert isinstance(view, OrionDashboardView)
    assert view.aurora.market_regime == "Unknown"
    assert view.supernova.approved_companies[0] == "NVDA"
    assert view.phoenix.current_leaders[0] == "SOL"
