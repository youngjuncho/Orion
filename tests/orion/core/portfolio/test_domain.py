from datetime import date, datetime, timezone
from decimal import Decimal
import pytest

from orion.core.account import Account, CashBalance, Position
from orion.core.ids import AccountId, AssetId, FrameworkId, PortfolioId, PositionId, TargetId, TransferId
from orion.core.portfolio import Allocation, Portfolio, PortfolioSnapshot, PortfolioState, PortfolioTarget, Transfer


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
