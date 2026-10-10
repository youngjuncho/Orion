"""Portfolio operations distinct from portfolio state."""
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from ..ids import AssetId, PortfolioId, TargetId, TransferId
from .allocation import Allocation
from .models import PortfolioTarget
from .state import PortfolioState
from .valuation import value_portfolio_state, current_allocations_from_valuation

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


def build_rebalance_plan(
    target: PortfolioTarget,
    current_allocations: tuple[Allocation, ...] | list[Allocation],
    *,
    as_of: str,
) -> RebalancePlan:
    """Build a deterministic weight-delta plan from current and target allocations.

    This operation deliberately stops at weight deltas. Concrete execution
    quantities require portfolio valuation and/or price data and therefore
    remain outside this contract.
    """
    current: dict[AssetId, Decimal] = {}
    for allocation in current_allocations:
        if allocation.asset_id in current:
            raise ValueError(f"duplicate current allocation for asset: {allocation.asset_id}")
        current[allocation.asset_id] = allocation.weight
    target_weights = {allocation.asset_id: allocation.weight for allocation in target.allocations}
    asset_ids = sorted(set(current) | set(target_weights), key=str)
    changes: list[RebalanceChange] = []
    for asset_id in asset_ids:
        current_weight = current.get(asset_id, Decimal("0"))
        target_weight = target_weights.get(asset_id, Decimal("0"))
        delta = target_weight - current_weight
        if delta == Decimal("0"):
            continue
        changes.append(
            RebalanceChange(
                asset_id=asset_id,
                action=RebalanceAction.BUY if delta > Decimal("0") else RebalanceAction.SELL,
                target_weight=target_weight,
                current_weight=current_weight,
                delta_weight=delta,
            )
        )
    return RebalancePlan(
        portfolio_id=target.portfolio_id,
        target_id=target.target_id,
        as_of=as_of,
        changes=tuple(changes),
    )


def build_rebalance_plan_from_state(
    target: PortfolioTarget,
    state: PortfolioState,
    prices: dict[AssetId, Decimal | int | float],
    *,
    as_of: str,
    cash_value: Decimal | int | float = Decimal("0"),
) -> RebalancePlan:
    """Build a weight-based rebalance plan from portfolio state and supplied prices."""
    if state.portfolio_id != target.portfolio_id:
        raise ValueError("portfolio state and target must reference the same portfolio")
    valuation = value_portfolio_state(state, prices, as_of=as_of, cash_value=cash_value)
    current = current_allocations_from_valuation(valuation)
    return build_rebalance_plan(target, current, as_of=as_of)
