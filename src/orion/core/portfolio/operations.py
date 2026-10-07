"""Portfolio operations distinct from portfolio state."""
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from ..ids import AssetId, PortfolioId, TargetId, TransferId

class RebalanceAction(str, Enum):
    BUY = "buy"
    SELL = "sell"

@dataclass(frozen=True)
class RebalanceChange:
    asset_id: AssetId
    action: RebalanceAction
    target_weight: Decimal
    current_weight: Decimal
    delta_weight: Decimal

@dataclass(frozen=True)
class RebalancePlan:
    portfolio_id: PortfolioId
    target_id: TargetId
    as_of: str
    changes: tuple[RebalanceChange, ...]

class TransferStatus(str, Enum):
    PLANNED = "planned"
    SETTLED = "settled"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class Transfer:
    transfer_id: TransferId
    source_portfolio_id: PortfolioId
    destination_portfolio_id: PortfolioId
    asset_id: AssetId
    quantity: Decimal
    status: TransferStatus = TransferStatus.PLANNED

    def __post_init__(self) -> None:
        if self.source_portfolio_id == self.destination_portfolio_id:
            raise ValueError("source and destination portfolios must differ")
        if self.quantity <= 0:
            raise ValueError("transfer quantity must be positive")
