from datetime import datetime, timezone

import pytest

from orion.core.account.models import Account, CashBalance
from orion.core.account.position import Position
from orion.core.ids import AccountId, AssetId, PortfolioId, PositionId
from orion.core.portfolio import build_portfolio_state


def test_build_portfolio_state_aggregates_selected_accounts_deterministically():
    portfolio_id = PortfolioId("P1")
    account_a = Account(AccountId("A1"), portfolio_id, "Broker A", "A", "USD")
    account_b = Account(AccountId("A2"), portfolio_id, "Broker B", "B", "KRW")
    positions = (
        Position(PositionId("P2"), AccountId("A2"), AssetId("VTI"), 1),
        Position(PositionId("P1"), AccountId("A1"), AssetId("VTI"), 2),
    )
    cash = (
        CashBalance(AccountId("A2"), "KRW", 1000),
        CashBalance(AccountId("A1"), "USD", 10),
    )
    as_of = datetime(2026, 10, 10, tzinfo=timezone.utc)

    state = build_portfolio_state(
        portfolio_id, as_of, (account_b, account_a), positions, cash
    )

    assert state.portfolio_id == portfolio_id
    assert state.as_of == as_of
    assert state.positions == tuple(sorted(positions, key=lambda row: (str(row.account_id), str(row.position_id), str(row.asset_id))))
    assert state.cash == tuple(sorted(cash, key=lambda row: (str(row.account_id), row.currency)))


def test_build_portfolio_state_rejects_foreign_accounts_and_orphan_rows():
    portfolio_id = PortfolioId("P1")
    foreign_account = Account(
        AccountId("A2"), PortfolioId("P2"), "Other", "Broker", "KRW"
    )
    valid_account = Account(AccountId("A1"), portfolio_id, "Main", "Broker", "KRW")
    as_of = datetime(2026, 10, 10, tzinfo=timezone.utc)

    with pytest.raises(ValueError, match="belong to the requested portfolio"):
        build_portfolio_state(portfolio_id, as_of, (valid_account, foreign_account), (), ())

    with pytest.raises(ValueError, match="one of the supplied accounts"):
        build_portfolio_state(
            portfolio_id,
            as_of,
            (valid_account,),
            (Position(PositionId("P1"), AccountId("A2"), AssetId("VTI"), 1),),
            (),
        )


def test_build_portfolio_state_rejects_duplicate_account_currency_cash():
    portfolio_id = PortfolioId("P1")
    account = Account(AccountId("A1"), portfolio_id, "Main", "Broker", "KRW")
    duplicate_cash = (
        CashBalance(AccountId("A1"), "USD", 1),
        CashBalance(AccountId("A1"), "usd", 2),
    )

    with pytest.raises(ValueError, match="unique per account and currency"):
        build_portfolio_state(
            portfolio_id,
            datetime(2026, 10, 10, tzinfo=timezone.utc),
            (account,),
            (),
            duplicate_cash,
        )
