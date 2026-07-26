from src.moon import Allocation, MoonEngine, MoonReport, Portfolio, Strategy, StrategyResult


def test_moon_model_shapes() -> None:
    strategy = Strategy("ADM", "1.0", "Active")
    result = StrategyResult("ADM", ("SPY",), (1.0,), "2026-07-26")
    allocation = Allocation("SPY", 1.0)
    portfolio = Portfolio((allocation,), "2026-08-31")
    report = MoonReport(
        portfolio_allocation=(allocation,),
        current_holdings=(allocation,),
        next_rebalance_date="2026-08-31",
        strategy_summary=(result,),
        current_asset="SPY",
        momentum_state="Stable",
        risk_state="Neutral",
    )

    assert strategy.name == "ADM"
    assert result.selected_assets == ("SPY",)
    assert portfolio.current_holdings[0].weight == 1.0
    assert report.strategy_summary[0].signal_date == "2026-07-26"


def test_moon_engine_build_report() -> None:
    report = MoonEngine().build_report()

    assert report.current_asset == "Unknown"
    assert report.momentum_state == "Unknown"
