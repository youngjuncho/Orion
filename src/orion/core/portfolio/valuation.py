"""Portfolio valuation inputs and current-allocation projection."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping

from ..ids import AssetId, PortfolioId
from .allocation import Allocation
from .state import PortfolioState


@dataclass(frozen=True)
class PortfolioValuation:
    """Authoritative valuation supplied to portfolio operations for one state."""

    portfolio_id: PortfolioId
    as_of: str
    asset_values: Mapping[AssetId, Decimal]
    cash_value: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if not str(self.portfolio_id).strip():
            raise ValueError("portfolio_id must not be empty")
        if not isinstance(self.as_of, str) or not self.as_of.strip():
            raise ValueError("as_of must be a non-empty string")
        values = {asset_id: Decimal(str(value)) for asset_id, value in self.asset_values.items()}
        if any(value < 0 for value in values.values()):
            raise ValueError("asset values must be non-negative")
        cash = Decimal(str(self.cash_value))
        if cash < 0:
            raise ValueError("cash value must be non-negative")
        total = sum(values.values(), Decimal("0")) + cash
        if total <= 0:
            raise ValueError("total portfolio valuation must be positive")
        object.__setattr__(self, "asset_values", values)
        object.__setattr__(self, "cash_value", cash)

    @property
    def total_value(self) -> Decimal:
        return sum(self.asset_values.values(), Decimal("0")) + self.cash_value


def value_portfolio_state(
    state: PortfolioState,
    prices: Mapping[AssetId, Decimal | int | float],
    *,
    as_of: str,
    cash_value: Decimal | int | float = Decimal("0"),
) -> PortfolioValuation:
    """Value positions using caller-supplied canonical prices.

    This function performs no FX conversion and no price discovery. The caller
    is responsible for supplying prices already normalized to the portfolio's
    valuation currency.
    """
    if state.portfolio_id is None:
        raise ValueError("portfolio state must have a portfolio_id")
    price_map = {asset_id: Decimal(str(price)) for asset_id, price in prices.items()}
    values: dict[AssetId, Decimal] = {}
    for position in state.positions:
        if position.asset_id not in price_map:
            raise ValueError(f"missing valuation price for asset: {position.asset_id}")
        price = price_map[position.asset_id]
        if price < 0:
            raise ValueError("valuation prices must be non-negative")
        values[position.asset_id] = values.get(position.asset_id, Decimal("0")) + Decimal(str(position.quantity)) * price
    return PortfolioValuation(state.portfolio_id, as_of, values, Decimal(str(cash_value)))


def current_allocations_from_valuation(valuation: PortfolioValuation) -> tuple[Allocation, ...]:
    """Project non-cash asset weights from an authoritative valuation."""
    total = valuation.total_value
    return tuple(
        Allocation(asset_id=asset_id, weight=value / total)
        for asset_id, value in sorted(valuation.asset_values.items(), key=lambda item: str(item[0]))
        if value > 0
    )
