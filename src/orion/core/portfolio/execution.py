"""Canonical portfolio execution-order contract."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from ..ids import AssetId, OrderId, PortfolioId, TargetId


class OrderAction(str, Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass(frozen=True)
class ExecutionOrder:
    """Concrete trade instruction derived from a RebalancePlan."""

    order_id: OrderId
    portfolio_id: PortfolioId
    target_id: TargetId
    asset_id: AssetId
    action: OrderAction
    quantity: Decimal
    created_at: datetime
    status: str = "planned"

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("execution order quantity must be positive")
        if not self.status.strip():
            raise ValueError("execution order status must not be empty")
