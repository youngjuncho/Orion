"""Canonical portfolio execution-order contract."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Mapping
from ..ids import AssetId, OrderId, PortfolioId, TargetId
from .operations import RebalanceAction, RebalancePlan


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


@dataclass(frozen=True)
class ExecutionSizingInput:
    """Explicit executable quantities and order identities for a rebalance plan.

    Quantity calculation and order-id assignment remain outside the common
    portfolio domain. This contract only carries those already-resolved inputs
    into concrete ExecutionOrder construction.
    """

    quantities: Mapping[AssetId, Decimal]
    order_ids: Mapping[AssetId, OrderId]

    def __post_init__(self) -> None:
        quantities = {asset_id: Decimal(str(quantity)) for asset_id, quantity in self.quantities.items()}
        if any(quantity <= 0 for quantity in quantities.values()):
            raise ValueError("execution sizing quantities must be positive")
        if set(quantities) != set(self.order_ids):
            raise ValueError("execution sizing must provide quantity and order_id for the same assets")
        object.__setattr__(self, "quantities", quantities)


def build_execution_orders(
    plan: RebalancePlan,
    sizing: ExecutionSizingInput,
    *,
    created_at: datetime,
) -> tuple[ExecutionOrder, ...]:
    """Materialize a RebalancePlan using explicitly supplied executable inputs.

    This operation does not calculate quantities, prices, fees, lot sizes,
    fractional-share rules, or broker constraints. Those policies must be
    resolved before calling this boundary.
    """
    plan_assets = {change.asset_id for change in plan.changes}
    if plan_assets != set(sizing.quantities):
        raise ValueError("execution sizing assets must exactly match rebalance-plan changes")
    orders = []
    for change in plan.changes:
        action = OrderAction.BUY if change.action is RebalanceAction.BUY else OrderAction.SELL
        orders.append(
            ExecutionOrder(
                order_id=sizing.order_ids[change.asset_id],
                portfolio_id=plan.portfolio_id,
                target_id=plan.target_id,
                asset_id=change.asset_id,
                action=action,
                quantity=sizing.quantities[change.asset_id],
                created_at=created_at,
            )
        )
    return tuple(orders)
