"""Custody/accounting boundary for Orion portfolios."""
from dataclasses import dataclass
import math
from decimal import Decimal
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

    def __post_init__(self) -> None:
        if not isinstance(self.currency, str) or not self.currency.strip():
            raise ValueError("currency must be a non-empty string")
        if isinstance(self.amount, bool) or not isinstance(self.amount, (int, float, Decimal)):
            raise ValueError("cash amount must be a finite non-negative number")
        if not math.isfinite(self.amount) or self.amount < 0:
            raise ValueError("cash amount must be a finite non-negative number")
        object.__setattr__(self, "currency", self.currency.strip().upper())
