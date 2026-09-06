import pytest

from orion.frameworks.moon import (
    ADMSignalInput,
    ADMStrategy,
    Allocation,
    ConsensusAllocator,
    MoonEngine,
    MoonReport,
    Portfolio,
    Strategy,
    StrategyResult,
)


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


def test_adm_selects_relative_momentum_winner_when_absolute_momentum_is_positive() -> None:
    result = ADMStrategy("SGOV").generate_result(
        ADMSignalInput(
            signal_date="2026-07-31",
            relative_momentum={"VTI": 0.12, "VEU": 0.08},
            absolute_momentum_positive=True,
            defensive_asset="SGOV",
        )
    )

    assert result.selected_assets == ("VTI",)
    assert result.weights == (1.0,)
    assert result.state == "Risk On"


def test_adm_selects_defensive_asset_when_absolute_momentum_is_negative() -> None:
    result = ADMStrategy("SGOV").calculate_signal(
        ADMSignalInput(
            signal_date="2026-07-31",
            relative_momentum={"VTI": 0.12, "VEU": 0.08},
            absolute_momentum_positive=False,
            defensive_asset="SGOV",
        )
    )

    assert result.selected_assets == ("SGOV",)
    assert result.state == "Risk Off"


def test_adm_rejects_undefined_relative_momentum_tie() -> None:
    inputs = ADMSignalInput(
        signal_date="2026-07-31",
        relative_momentum={"VTI": 0.08, "VEU": 0.08},
        absolute_momentum_positive=True,
        defensive_asset="SGOV",
    )

    with pytest.raises(ValueError, match="tie"):
        ADMStrategy("SGOV").calculate_signal(inputs)


def test_consensus_allocator_applies_equal_strategy_weight_and_aggregates_assets() -> None:
    results = (
        StrategyResult("ADM", ("VTI",), (1.0,), "2026-07-31"),
        StrategyResult("BAA", ("VTI", "QQQ"), (0.5, 0.5), "2026-07-31"),
    )

    allocation = ConsensusAllocator().allocate(results)

    assert allocation == (
        Allocation("VTI", 0.75),
        Allocation("QQQ", 0.25),
    )


def test_consensus_allocator_requires_strategy_results() -> None:
    with pytest.raises(ValueError, match="at least one"):
        ConsensusAllocator().allocate(())


def test_consensus_allocator_rejects_zero_weight_strategy_result() -> None:
    result = StrategyResult("ADM", ("VTI",), (0.0,), "2026-07-31")

    with pytest.raises(ValueError, match="positive"):
        ConsensusAllocator().allocate((result,))
