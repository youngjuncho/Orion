from datetime import date
from decimal import Decimal

import pytest

from orion.core.ids import PortfolioId, TargetId
from orion.core.portfolio import Allocation, PortfolioTarget
from orion.frameworks.moon import (
    ADMSignalInput,
    ADMStrategy,
    ConsensusAllocation,
    ConsensusAllocator,
    ExecutionMapper,
    MoonEngine,
    MoonReport,
    Strategy,
    StrategyResult,
    calculate_adjusted_price_return,
)


def test_moon_model_shapes() -> None:
    strategy = Strategy("ADM", "1.0", "Active")
    result = StrategyResult("ADM", ("SPY",), (1.0,), "2026-07-26")
    allocation = Allocation("SPYM", Decimal("1.0"))
    report = MoonReport((allocation,), (allocation,), "2026-08-31", (result,), "SPY", "Stable", "Neutral")
    assert strategy.name == "ADM"
    assert result.selected_assets == ("SPY",)
    assert allocation.asset_id == "SPYM"
    assert report.strategy_summary[0].signal_date == "2026-07-26"


def test_moon_engine_build_report() -> None:
    report = MoonEngine().build_report()
    assert report.current_asset == "Unknown"
    assert report.momentum_state == "Unknown"


def test_moon_models_reject_invalid_required_values() -> None:
    with pytest.raises(ValueError, match="asset"):
        ConsensusAllocation("", 1.0)
    with pytest.raises(ValueError, match="weight"):
        ConsensusAllocation("SPY", -0.1)
    with pytest.raises(ValueError, match="finite"):
        ConsensusAllocation("SPY", True)
    with pytest.raises(ValueError, match="unique"):
        StrategyResult("ADM", ("SPY", "SPY"), (0.5, 0.5), "2026-07-26")
    with pytest.raises(ValueError, match="weights"):
        StrategyResult("ADM", ["SPY"], ["invalid"], "2026-07-26")  # type: ignore[arg-type]


def test_moon_models_snapshot_mutable_collection_inputs() -> None:
    assets = ["SPY"]
    weights = [1.0]
    metadata = {"source": "fixture"}
    result = StrategyResult("ADM", assets, weights, "2026-07-26", metadata=metadata)
    allocation = Allocation("SPYM", Decimal("1.0"))
    holdings = [allocation]
    report = MoonReport([allocation], holdings, "2026-08-31", [result], "SPY", "Stable", "Neutral")
    assets.clear(); weights.clear(); metadata["source"] = "changed"; holdings.clear()
    assert result.selected_assets == ("SPY",)
    assert result.metadata["source"] == "fixture"
    assert report.current_holdings == (allocation,)
    assert report.portfolio_allocation == (allocation,)


def test_adm_selects_relative_momentum_winner_when_absolute_momentum_is_positive() -> None:
    result = ADMStrategy("SGOV").generate_result(
        ADMSignalInput("2026-07-31", {"VTI": 0.12, "VEU": 0.08}, True, "SGOV")
    )
    assert result.selected_assets == ("VTI",)
    assert result.weights == (1.0,)
    assert result.state == "Risk On"


def test_adm_selects_defensive_asset_when_absolute_momentum_is_negative() -> None:
    result = ADMStrategy("SGOV").calculate_signal(
        ADMSignalInput("2026-07-31", {"VTI": 0.12, "VEU": 0.08}, False, "SGOV")
    )
    assert result.selected_assets == ("SGOV",)
    assert result.state == "Risk Off"


def test_adm_rejects_undefined_relative_momentum_tie() -> None:
    inputs = ADMSignalInput("2026-07-31", {"VTI": 0.08, "VEU": 0.08}, True, "SGOV")
    with pytest.raises(ValueError, match="tie"):
        ADMStrategy("SGOV").calculate_signal(inputs)


def test_adm_signal_input_rejects_invalid_field_types() -> None:
    with pytest.raises(ValueError, match="boolean"):
        ADMSignalInput("2026-07-31", {"VTI": 0.12}, 1, "SGOV")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="finite numbers"):
        ADMSignalInput("2026-07-31", {"VTI": True, "VEU": 0.08}, True, "SGOV")  # type: ignore[dict-item]
    with pytest.raises(ValueError, match="mapping"):
        ADMSignalInput("2026-07-31", [], True, "SGOV")  # type: ignore[arg-type]


def test_adm_signal_input_snapshots_relative_momentum() -> None:
    momentum = {"VTI": 0.12, "VEU": 0.08}
    inputs = ADMSignalInput("2026-07-31", momentum, True, "SGOV")
    momentum["VTI"] = -0.5
    assert inputs.relative_momentum["VTI"] == 0.12


def test_consensus_allocator_returns_moon_specific_consensus_allocation() -> None:
    results = (
        StrategyResult("ADM", ("VTI",), (1.0,), "2026-07-31"),
        StrategyResult("BAA", ("VTI", "QQQ"), (0.5, 0.5), "2026-07-31"),
    )
    allocation = ConsensusAllocator().allocate(results)
    assert allocation == (ConsensusAllocation("VTI", 0.75), ConsensusAllocation("QQQ", 0.25))


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


def test_execution_mapper_returns_common_allocations() -> None:
    allocation = ExecutionMapper().map_allocations((ConsensusAllocation("SPY", 1.0),))
    assert allocation == (Allocation("SPYM", Decimal("1.0")),)


@pytest.mark.parametrize("asset", ("VTI", "VEU", "SGOV"))
def test_execution_mapper_preserves_adm_signal_assets(asset: str) -> None:
    allocation = ExecutionMapper().map_allocations((ConsensusAllocation(asset, 1.0),))
    assert allocation == (Allocation(asset, Decimal("1.0")),)


def test_execution_mapper_maps_bil_to_sgov() -> None:
    allocation = ExecutionMapper().map_allocations((ConsensusAllocation("BIL", 1.0),))
    assert allocation == (Allocation("SGOV", Decimal("1.0")),)


def test_moon_engine_builds_common_executable_allocation() -> None:
    results = (StrategyResult("Test", ("SPY",), (1.0,), "2026-07-31"),)
    allocation = MoonEngine().build_allocation(results)
    assert allocation == (Allocation("SPYM", Decimal("1.0")),)


def test_moon_engine_builds_common_portfolio_target() -> None:
    results = (StrategyResult("ADM", ("SPY",), (1.0,), "2026-07-31"),)
    target = MoonEngine().build_portfolio_target(
        results,
        PortfolioId("MOON"),
        target_id=TargetId("MOON-1"),
        effective_from=date(2026, 8, 31),
    )
    assert target.portfolio_id == PortfolioId("MOON")
    assert target.allocations == (Allocation("SPYM", Decimal("1.0")),)


def test_adjusted_price_return_uses_current_over_trailing_minus_one() -> None:
    assert calculate_adjusted_price_return(110.0, 100.0) == pytest.approx(0.1)
    assert calculate_adjusted_price_return(90.0, 100.0) == pytest.approx(-0.1)
