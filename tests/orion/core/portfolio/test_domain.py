from datetime import date, datetime, timezone
from decimal import Decimal
import pytest

from orion.core.account import Account, CashBalance, Position
from orion.core.ids import AccountId, AssetId, FrameworkId, PortfolioId, PositionId, TargetId, TransferId
from orion.core.portfolio import Allocation, Portfolio, PortfolioSnapshot, PortfolioState, PortfolioTarget, Transfer, build_rebalance_plan
from orion.core.portfolio.operations import RebalanceAction


def test_portfolio_has_identity_not_holdings() -> None:
    portfolio = Portfolio(PortfolioId("P1"), FrameworkId("ORBIT"), "Orbit")
    assert portfolio.portfolio_id == PortfolioId("P1")
    assert not hasattr(portfolio, "current_holdings")


def test_target_enforces_unique_assets_and_total_weight() -> None:
    target = PortfolioTarget(TargetId("T1"), PortfolioId("P1"), 1, date(2026, 11, 2), (Allocation(AssetId("SPYM"), Decimal("1.0")),))
    assert target.allocations[0].asset_id == AssetId("SPYM")
    with pytest.raises(ValueError, match="unique"):
        PortfolioTarget(TargetId("T2"), PortfolioId("P1"), 1, date(2026, 11, 2), (Allocation(AssetId("SPYM"), Decimal("0.5")), Allocation(AssetId("SPYM"), Decimal("0.5"))))


def test_state_is_current_projection_and_snapshot_is_historical_capture() -> None:
    account = Account(AccountId("A1"), PortfolioId("P1"), "Broker", "BrokerX", "USD")
    position = Position(PositionId("POS1"), account.account_id, AssetId("SPYM"), 10)
    cash = CashBalance(account.account_id, "USD", 1000)
    state = PortfolioState(PortfolioId("P1"), datetime.now(timezone.utc), (position,), (cash,))
    snapshot = PortfolioSnapshot(state, state.as_of)
    assert snapshot.state is state


def test_transfer_is_distinct_from_rebalance_and_requires_different_portfolios() -> None:
    transfer = Transfer(TransferId("X1"), PortfolioId("MOON"), PortfolioId("ORBIT"), AssetId("SGOV"), Decimal("2"))
    assert transfer.source_portfolio_id == PortfolioId("MOON")
    with pytest.raises(ValueError, match="must differ"):
        Transfer(TransferId("X2"), PortfolioId("P1"), PortfolioId("P1"), AssetId("SGOV"), Decimal("1"))


def test_execution_order_is_distinct_from_execution_metadata() -> None:
    from datetime import datetime, timezone
    from decimal import Decimal
    from orion.core.ids import AssetId, OrderId, PortfolioId, TargetId
    from orion.core.portfolio import ExecutionOrder, OrderAction

    order = ExecutionOrder(
        order_id=OrderId("O-1"),
        portfolio_id=PortfolioId("MOON"),
        target_id=TargetId("T-1"),
        asset_id=AssetId("SPYM"),
        action=OrderAction.BUY,
        quantity=Decimal("10"),
        created_at=datetime.now(timezone.utc),
    )
    assert order.asset_id == AssetId("SPYM")
    assert order.action is OrderAction.BUY


def test_rebalance_plan_is_derived_from_target_and_current_weights() -> None:
    target = PortfolioTarget(
        TargetId("T-RB"), PortfolioId("P1"), 1, date(2026, 11, 2),
        (
            Allocation(AssetId("SPYM"), Decimal("0.6")),
            Allocation(AssetId("QQQM"), Decimal("0.4")),
        ),
    )
    plan = build_rebalance_plan(
        target,
        (
            Allocation(AssetId("SPYM"), Decimal("0.5")),
            Allocation(AssetId("SGOV"), Decimal("0.5")),
        ),
        as_of="2026-11-02",
    )
    assert plan.portfolio_id == PortfolioId("P1")
    assert [(c.asset_id, c.action, c.delta_weight) for c in plan.changes] == [
        (AssetId("QQQM"), RebalanceAction.BUY, Decimal("0.4")),
        (AssetId("SGOV"), RebalanceAction.SELL, Decimal("-0.5")),
        (AssetId("SPYM"), RebalanceAction.BUY, Decimal("0.1")),
    ]


def test_rebalance_plan_omits_zero_delta_assets() -> None:
    target = PortfolioTarget(
        TargetId("T-RB2"), PortfolioId("P1"), 1, date(2026, 11, 2),
        (Allocation(AssetId("SPYM"), Decimal("1.0")),),
    )
    plan = build_rebalance_plan(
        target, (Allocation(AssetId("SPYM"), Decimal("1.0")),), as_of="2026-11-02"
    )
    assert plan.changes == ()


def test_execution_orders_require_explicit_sizing_inputs():
    from datetime import datetime, timezone
    from orion.core.ids import OrderId
    from orion.core.portfolio import ExecutionSizingInput, build_execution_orders, OrderAction

    target = PortfolioTarget(
        TargetId("T-EXEC"), PortfolioId("P1"), 1, date(2026, 11, 2),
        (Allocation(AssetId("SPYM"), Decimal("1.0")),),
    )
    plan = build_rebalance_plan(
        target, (Allocation(AssetId("SPYM"), Decimal("0.5")),), as_of="2026-11-02"
    )
    sizing = ExecutionSizingInput(
        quantities={AssetId("SPYM"): Decimal("2")},
        order_ids={AssetId("SPYM"): OrderId("O-SPYM")},
    )
    orders = build_execution_orders(
        plan, sizing, created_at=datetime(2026, 11, 2, tzinfo=timezone.utc)
    )
    assert len(orders) == 1
    assert orders[0].quantity == Decimal("2")
    assert orders[0].action is OrderAction.BUY


def test_execution_sizing_must_match_rebalance_assets():
    from orion.core.ids import OrderId
    from orion.core.portfolio import ExecutionSizingInput
    with pytest.raises(ValueError, match="same assets"):
        ExecutionSizingInput(
            quantities={AssetId("SPYM"): Decimal("1")},
            order_ids={AssetId("QQQM"): OrderId("O-QQQM")},
        )
