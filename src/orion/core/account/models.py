"""Custody/accounting boundary for Orion portfolios."""
from dataclasses import dataclass
from ..ids import AccountId, PortfolioId

@dataclass(frozen=True)
class Account:
    account_id: AccountId
    portfolio_id: PortfolioId
    name: str
    provider: str
    currency: str
    status: str = "active"

@dataclass(frozen=True)
class CashBalance:
    account_id: AccountId
    currency: str
    amount: float
