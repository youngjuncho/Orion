"""Deterministic projection from selected accounts into portfolio state."""

from __future__ import annotations

from datetime import datetime
from typing import Sequence

from ..account.models import Account, CashBalance
from ..account.position import Position
from ..ids import PortfolioId
from .state import PortfolioState


def build_portfolio_state(
    portfolio_id: PortfolioId,
    as_of: datetime,
    accounts: Sequence[Account],
    positions: Sequence[Position],
    cash: Sequence[CashBalance],
) -> PortfolioState:
    """Build a stable PortfolioState from caller-selected portfolio accounts.

    Account selection and status policy remain caller-owned. Every supplied
    account must belong to ``portfolio_id``; every position and cash row must
    refer to one of those accounts. Ambiguous identities and duplicate
    account/currency balances are rejected instead of silently discarded.
    """
    if not isinstance(portfolio_id, str) or not portfolio_id.strip():
        raise ValueError("portfolio_id must be a non-empty PortfolioId")
    if not isinstance(as_of, datetime):
        raise TypeError("as_of must be a datetime")

    account_rows = tuple(accounts)
    if not account_rows:
        raise ValueError("at least one account is required to project a portfolio state")
    if any(not isinstance(account, Account) for account in account_rows):
        raise TypeError("accounts must contain Account values")
    account_ids = [account.account_id for account in account_rows]
    if any(not isinstance(account_id, str) or not account_id.strip() for account_id in account_ids):
        raise ValueError("account IDs must be non-empty strings")
    if len(account_ids) != len(set(account_ids)):
        raise ValueError("account IDs must be unique")
    if any(account.portfolio_id != portfolio_id for account in account_rows):
        raise ValueError("all accounts must belong to the requested portfolio")
    known_accounts = set(account_ids)

    position_rows = tuple(positions)
    if any(not isinstance(position, Position) for position in position_rows):
        raise TypeError("positions must contain Position values")
    position_ids = [position.position_id for position in position_rows]
    if any(not isinstance(position_id, str) or not position_id.strip() for position_id in position_ids):
        raise ValueError("position IDs must be non-empty strings")
    if any(
        not isinstance(position.account_id, str)
        or not position.account_id.strip()
        or not isinstance(position.asset_id, str)
        or not position.asset_id.strip()
        for position in position_rows
    ):
        raise ValueError("position account and asset IDs must be non-empty strings")
    if len(position_ids) != len(set(position_ids)):
        raise ValueError("position IDs must be unique")
    if any(position.account_id not in known_accounts for position in position_rows):
        raise ValueError("every position must reference one of the supplied accounts")

    cash_rows = tuple(cash)
    if any(not isinstance(balance, CashBalance) for balance in cash_rows):
        raise TypeError("cash must contain CashBalance values")
    if any(not isinstance(balance.account_id, str) or not balance.account_id.strip() for balance in cash_rows):
        raise ValueError("cash account IDs must be non-empty strings")
    cash_keys = [(balance.account_id, balance.currency.strip().upper()) for balance in cash_rows]
    if any(account_id not in known_accounts for account_id, _ in cash_keys):
        raise ValueError("every cash balance must reference one of the supplied accounts")
    if len(cash_keys) != len(set(cash_keys)):
        raise ValueError("cash balances must be unique per account and currency")

    ordered_positions = tuple(
        sorted(
            position_rows,
            key=lambda item: (str(item.account_id), str(item.position_id), str(item.asset_id)),
        )
    )
    ordered_cash = tuple(
        sorted(cash_rows, key=lambda item: (str(item.account_id), item.currency))
    )
    return PortfolioState(portfolio_id, as_of, ordered_positions, ordered_cash)
