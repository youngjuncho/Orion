from datetime import datetime, timezone
from decimal import Decimal
import pytest
from orion.core.account.models import CashBalance
from orion.core.account.position import Position
from orion.core.ids import AccountId, AssetId, PortfolioId, PositionId
from orion.core.portfolio import PortfolioState, PortfolioTarget, Allocation, current_allocations_from_valuation, value_portfolio_state, build_rebalance_plan_from_state
from orion.core.ids import TargetId
from datetime import date


def test_value_portfolio_state_and_project_current_allocations():
    state = PortfolioState(
        PortfolioId("P1"), datetime.now(timezone.utc),
        (Position(PositionId("POS1"), AccountId("A1"), AssetId("SPYM"), 2),
         Position(PositionId("POS2"), AccountId("A1"), AssetId("QQQM"), 1)),
        (CashBalance(AccountId("A1"), "USD", 100.0),),
    )
    valuation = value_portfolio_state(
        state, {AssetId("SPYM"): Decimal("50"), AssetId("QQQM"): Decimal("100")},
        as_of="2026-10-08", cash_value=Decimal("100"),
    )
    assert valuation.total_value == Decimal("300")
    allocations = current_allocations_from_valuation(valuation)
    assert [(a.asset_id, a.weight) for a in allocations] == [
        (AssetId("QQQM"), Decimal("0.3333333333333333333333333333")),
        (AssetId("SPYM"), Decimal("0.3333333333333333333333333333")),
    ]


def test_value_portfolio_state_requires_price_for_every_position():
    state = PortfolioState(
        PortfolioId("P1"), datetime.now(timezone.utc),
        (Position(PositionId("POS1"), AccountId("A1"), AssetId("SPYM"), 2),), (),
    )
    with pytest.raises(ValueError, match="missing valuation price"):
        value_portfolio_state(state, {}, as_of="2026-10-08")


def test_build_rebalance_plan_from_state_uses_supplied_valuation():
    state = PortfolioState(
        PortfolioId("P1"), datetime.now(timezone.utc),
        (Position(PositionId("POS1"), AccountId("A1"), AssetId("SPYM"), 2),), (),
    )
    target = PortfolioTarget(
        TargetId("T1"), PortfolioId("P1"), 1, date(2026, 10, 8),
        (Allocation(AssetId("SPYM"), Decimal("0.5")),
         Allocation(AssetId("QQQM"), Decimal("0.5"))),
    )
    plan = build_rebalance_plan_from_state(
        target, state, {AssetId("SPYM"): Decimal("50")}, as_of="2026-10-08", cash_value=Decimal("100")
    )
    assert [(c.asset_id, c.action.value, c.delta_weight) for c in plan.changes] == [
        (AssetId("QQQM"), "buy", Decimal("0.5")),
    ]
