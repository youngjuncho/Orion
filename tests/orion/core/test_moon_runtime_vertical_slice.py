from datetime import date
from decimal import Decimal

import pytest

from orion.core import (
    FrameworkRegistry,
    ExecutionMetadata,
    OrionRuntime,
    make_moon_portfolio_adapter,
)
from orion.core.ids import PortfolioId, TargetId
from orion.core.portfolio import Allocation
from orion.frameworks.moon import ADMSignalInput, ADMStrategy
from orion.frameworks.moon.models import StrategyResult


def _runtime() -> OrionRuntime:
    registry = FrameworkRegistry()
    registry.register("Moon", object())
    return OrionRuntime(
        configuration=__import__("orion.core", fromlist=["load_config"]).load_config(),
        execution=ExecutionMetadata(
            execution_id="moon-vertical-001",
            start_time="2026-10-08T00:00:00+00:00",
            orion_version="v1",
        ),
        registry=registry,
    )


def _strategies() -> tuple[StrategyResult, ...]:
    return (
        StrategyResult("S1", ("SPY", "TLT"), (0.6, 0.4), "2026-10-08"),
        StrategyResult("S2", ("SPY", "TLT"), (0.8, 0.2), "2026-10-08"),
    )


def test_moon_adapter_exposes_canonical_portfolio_target_candidate() -> None:
    runtime = _runtime()
    result = runtime.run(
        {
            "Moon": make_moon_portfolio_adapter(
                _strategies,
                PortfolioId("moon-main"),
                target_id=TargetId("moon-target-001"),
                effective_from=date(2026, 10, 8),
            )
        }
    )

    framework_result = result.framework_results[0]
    candidate = framework_result.decision_candidates[0]
    target = candidate.payload["portfolio_target"]

    assert candidate.framework_name == "Moon"
    assert candidate.entity_type == "PortfolioTarget"
    assert candidate.entity_id == "moon-target-001"
    assert target.portfolio_id == "moon-main"
    assert target.target_id == "moon-target-001"
    assert sum((allocation.weight for allocation in target.allocations)) == 1
    assert {allocation.asset_id for allocation in target.allocations} == {"SPYM", "VGLT"}


def test_moon_adapter_rejects_non_strategy_results() -> None:
    runtime = _runtime()
    with pytest.raises(TypeError, match="StrategyResult"):
        runtime.run(
            {
                "Moon": make_moon_portfolio_adapter(
                    lambda: (object(),),
                    PortfolioId("moon-main"),
                    target_id=TargetId("moon-target-002"),
                    effective_from=date(2026, 10, 8),
                )
            }
        )


@pytest.mark.parametrize(
    ("relative_momentum", "absolute_momentum_positive", "expected_asset"),
    (
        ({"VTI": 0.20, "VEU": 0.10}, True, "VTI"),
        ({"VTI": 0.10, "VEU": 0.20}, True, "VEU"),
        ({"VTI": 0.20, "VEU": 0.10}, False, "SGOV"),
    ),
)
def test_adm_selection_reaches_portfolio_target(
    relative_momentum: dict[str, float],
    absolute_momentum_positive: bool,
    expected_asset: str,
) -> None:
    strategy_result = ADMStrategy("SGOV").calculate_signal(
        ADMSignalInput(
            signal_date="2026-10-08",
            relative_momentum=relative_momentum,
            absolute_momentum_positive=absolute_momentum_positive,
            defensive_asset="SGOV",
        )
    )
    runtime = _runtime()

    result = runtime.run(
        {
            "Moon": make_moon_portfolio_adapter(
                lambda: (strategy_result,),
                PortfolioId("moon-main"),
                target_id=TargetId(f"adm-{expected_asset}"),
                effective_from=date(2026, 10, 8),
            )
        }
    )

    target = result.framework_results[0].decision_candidates[0].payload["portfolio_target"]
    assert target.allocations == (Allocation(expected_asset, Decimal("1.0")),)
