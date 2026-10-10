from datetime import date, datetime
from decimal import Decimal

import pytest

from orion.core import (
    FrameworkRegistry,
    ExecutionMetadata,
    OrionRuntime,
    make_moon_portfolio_adapter,
)
from orion.core.ids import AccountId, AssetId, PortfolioId, PositionId, TargetId
from orion.core.account.models import CashBalance
from orion.core.account.position import Position
from orion.core.portfolio import Allocation, PortfolioState
from data.contracts import MarketDataPoint, MarketDataSet
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


def test_moon_adapter_context_factory_receives_runtime_market_data_and_configuration() -> None:
    dataset = MarketDataSet(
        (MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 100.0, "fixture"),),
        "2026-10-08",
    )
    received = []

    def results_from_context(context):
        received.append(context)
        assert context.market_data is dataset
        assert context.configuration.system.currency == "KRW"
        return _strategies()

    result = _runtime().run(
        {
            "Moon": make_moon_portfolio_adapter(
                None,
                PortfolioId("moon-main"),
                target_id=TargetId("moon-context-target"),
                effective_from=date(2026, 10, 8),
                context_strategy_results_factory=results_from_context,
            )
        },
        market_data=dataset,
    )

    assert len(received) == 1
    assert result.framework_results[0].decision_candidates[0].entity_id == "moon-context-target"


def test_moon_adapter_adds_rebalance_plan_when_current_state_and_prices_are_supplied() -> None:
    state = PortfolioState(
        PortfolioId("moon-main"),
        datetime.fromisoformat("2026-10-08T00:00:00+00:00"),
        (Position(PositionId("pos-1"), AccountId("acct-1"), AssetId("SPYM"), 2),),
        (CashBalance(AccountId("acct-1"), "KRW", 100),),
    )
    result = _runtime().run(
        {
            "Moon": make_moon_portfolio_adapter(
                _strategies,
                PortfolioId("moon-main"),
                target_id=TargetId("moon-rebalance-target"),
                effective_from=date(2026, 10, 8),
                portfolio_state_factory=lambda _: state,
                valuation_prices_factory=lambda _: {AssetId("SPYM"): Decimal("50")},
            )
        }
    )

    candidate = result.framework_results[0].decision_candidates[0]
    plan = candidate.payload["rebalance_plan"]
    assert plan.as_of == "2026-10-08"
    assert [(change.asset_id, change.delta_weight) for change in plan.changes] == [
        (AssetId("SPYM"), Decimal("0.2")),
        (AssetId("VGLT"), Decimal("0.3")),
    ]


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
