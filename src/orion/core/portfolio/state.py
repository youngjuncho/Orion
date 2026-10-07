"""Current and historical portfolio state projections."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from ..account.models import CashBalance
from ..account.position import Position
from ..ids import PortfolioId

@dataclass(frozen=True)
class PortfolioState:
    portfolio_id: PortfolioId
    as_of: datetime
    positions: tuple[Position, ...]
    cash: tuple[CashBalance, ...]

@dataclass(frozen=True)
class PortfolioSnapshot:
    state: PortfolioState
    captured_at: datetime
