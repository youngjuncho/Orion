import pytest

from orion.frameworks.moon import (
    ADMSignalInput,
    ADMStrategy,
    Allocation,
    ConsensusAllocator,
    ExecutionMapper,
    MoonEngine,
    MoonReport,
    Portfolio,
    PortfolioTarget,
    PortfolioValidator,
    Strategy,
    StrategyResult,
    calculate_adjusted_price_return,
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


def test_moon_models_reject_invalid_required_values() -> None:
    with pytest.raises(ValueError, match="asset"):
        Allocation("", 1.0)

    with pytest.raises(ValueError, match="weight"):
        Allocation("SPY", -0.1)

    with pytest.raises(ValueError, match="finite"):
        Allocation("SPY", True)

    with pytest.raises(ValueError, match="unique"):
        StrategyResult("ADM", ("SPY", "SPY"), (0.5, 0.5), "2026-07-26")

    with pytest.raises(ValueError, match="weights"):
        StrategyResult("ADM", ["SPY"], ["invalid"], "2026-07-26")  # type: ignore[arg-type]


def test_moon_models_snapshot_mutable_collection_inputs() -> None:
    assets = ["SPY"]
    weights = [1.0]
    metadata = {"source": "fixture"}
    result = StrategyResult("ADM", assets, weights, "2026-07-26", metadata=metadata)
    allocation = Allocation("SPY", 1.0)
    holdings = [allocation]
    portfolio = Portfolio(holdings, "2026-08-31")
    portfolio_allocations = [allocation]
    strategy_results = [result]
    report = MoonReport(
        portfolio_allocations,
        holdings,
        "2026-08-31",
        strategy_results,
        "SPY",
        "Stable",
        "Neutral",
    )
    assets.clear()
    weights.clear()
    metadata["source"] = "changed"
    holdings.clear()
    portfolio_allocations.clear()
    strategy_results.clear()

    assert result.selected_assets == ("SPY",)
    assert result.weights == (1.0,)
    assert result.metadata["source"] == "fixture"
    assert portfolio.current_holdings == (allocation,)
    assert report.current_holdings == (allocation,)
    assert report.portfolio_allocation == (allocation,)
    assert report.strategy_summary == (result,)


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


def test_adm_signal_input_rejects_invalid_field_types() -> None:
    with pytest.raises(ValueError, match="boolean"):
        ADMSignalInput(
            "2026-07-31",
            {"VTI": 0.12, "VEU": 0.08},
            1,  # type: ignore[arg-type]
            "SGOV",
        )
    with pytest.raises(ValueError, match="finite numbers"):
        ADMSignalInput(
            "2026-07-31",
            {"VTI": True, "VEU": 0.08},  # type: ignore[dict-item]
            True,
            "SGOV",
        )
    with pytest.raises(ValueError, match="mapping"):
        ADMSignalInput("2026-07-31", [], True, "SGOV")  # type: ignore[arg-type]


def test_adm_signal_input_snapshots_relative_momentum() -> None:
    momentum = {"VTI": 0.12, "VEU": 0.08}
    inputs = ADMSignalInput("2026-07-31", momentum, True, "SGOV")
    momentum["VTI"] = -0.5

    assert inputs.relative_momentum["VTI"] == 0.12


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


def test_consensus_allocator_rejects_duplicate_strategies() -> None:
    results = (
        StrategyResult("ADM", ("VTI",), (1.0,), "2026-07-31"),
        StrategyResult("ADM", ("VEU",), (1.0,), "2026-07-31"),
    )

    with pytest.raises(ValueError, match="unique strategies"):
        ConsensusAllocator().allocate(results)


def test_consensus_allocator_rejects_zero_weight_strategy_result() -> None:
    result = StrategyResult("ADM", ("VTI",), (0.0,), "2026-07-31")

    with pytest.raises(ValueError, match="positive"):
        ConsensusAllocator().allocate((result,))


def test_execution_mapper_applies_documented_mapping() -> None:
    allocation = ExecutionMapper().map_allocations((Allocation("SPY", 1.0),))

    assert allocation == (Allocation("SPYM", 1.0),)


def test_execution_mapper_rejects_unmapped_signal_assets() -> None:
    with pytest.raises(ValueError, match="VTI"):
        ExecutionMapper().map_allocations((Allocation("VTI", 1.0),))


def test_moon_engine_builds_executable_allocation_from_strategy_results() -> None:
    results = (StrategyResult("Test", ("SPY",), (1.0,), "2026-07-31"),)

    allocation = MoonEngine().build_allocation(results)

    assert allocation == (Allocation("SPYM", 1.0),)


def test_moon_engine_surfaces_unmapped_strategy_assets() -> None:
    results = (StrategyResult("ADM", ("VTI",), (1.0,), "2026-07-31"),)

    with pytest.raises(ValueError, match="VTI"):
        MoonEngine().build_allocation(results)


def test_moon_engine_builds_validated_portfolio_target() -> None:
    results = (
        StrategyResult("ADM", ("SPY",), (1.0,), "2026-07-31"),
    )

    target = MoonEngine().build_portfolio_target(
        results, rebalance_date="2026-08-31", status="Draft"
    )

    assert target == PortfolioTarget(
        (Allocation("SPYM", 1.0),), "2026-08-31", "Draft"
    )


def test_portfolio_target_snapshots_allocations_and_validates_contract() -> None:
    allocations = [Allocation("SPYM", 0.75), Allocation("QQQM", 0.25)]
    target = PortfolioTarget(allocations, "2026-08-31", "Proposed")
    allocations.clear()

    assert len(target.allocations) == 2
    assert isinstance(target.allocations, tuple)

    with pytest.raises(ValueError, match="total 1.0"):
        PortfolioTarget((Allocation("SPYM", 0.5),), "2026-08-31", "Proposed")
    with pytest.raises(ValueError, match="unique"):
        PortfolioTarget(
            (Allocation("SPYM", 0.5), Allocation("SPYM", 0.5)),
            "2026-08-31",
            "Proposed",
        )


def test_adjusted_price_return_uses_current_over_trailing_minus_one() -> None:
    assert calculate_adjusted_price_return(110.0, 100.0) == pytest.approx(0.1)
    assert calculate_adjusted_price_return(90.0, 100.0) == pytest.approx(-0.1)


@pytest.mark.parametrize(
    "current,trailing",
    [
        (0.0, 100.0),
        (100.0, 0.0),
        (float("nan"), 100.0),
        (100.0, float("inf")),
        (True, 100.0),
    ],
)
def test_adjusted_price_return_rejects_invalid_prices(
    current: object, trailing: object
) -> None:
    with pytest.raises(ValueError, match="finite positive"):
        calculate_adjusted_price_return(current, trailing)  # type: ignore[arg-type]


def test_portfolio_validator_accepts_complete_unique_allocation() -> None:
    allocations = (Allocation("SPYM", 0.75), Allocation("QQQM", 0.25))

    assert PortfolioValidator().validate(allocations) == allocations


def test_portfolio_validator_rejects_duplicate_assets() -> None:
    allocations = (Allocation("SPYM", 0.5), Allocation("SPYM", 0.5))

    with pytest.raises(ValueError, match="unique"):
        PortfolioValidator().validate(allocations)


def test_portfolio_validator_rejects_incomplete_total() -> None:
    with pytest.raises(ValueError, match="total 1.0"):
        PortfolioValidator().validate((Allocation("SPYM", 0.5),))


def test_portfolio_validator_rejects_negative_weight() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        PortfolioValidator().validate((Allocation("SPYM", -0.1), Allocation("QQQM", 1.1)))
