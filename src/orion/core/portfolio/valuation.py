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
        if any(not value.is_finite() or value < 0 for value in values.values()):
            raise ValueError("asset values must be finite and non-negative")
        cash = Decimal(str(self.cash_value))
        if not cash.is_finite() or cash < 0:
            raise ValueError("cash value must be finite and non-negative")
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
    valuation_currency: str,
    cash_fx_rates: Mapping[str, Decimal | int | float] | None = None,
) -> PortfolioValuation:
    """Value positions using caller-supplied canonical prices.

    Prices and converted cash are expressed in ``valuation_currency``. Rates
    are valuation-currency units per one unit of source currency. No FX lookup
    or price discovery is performed here.
    """
    if state.portfolio_id is None:
        raise ValueError("portfolio state must have a portfolio_id")
    if not isinstance(valuation_currency, str) or not valuation_currency.strip():
        raise ValueError("valuation_currency must be a non-empty string")
    valuation_currency = valuation_currency.strip().upper()
    rates: dict[str, Decimal] = {}
    for currency, rate in (cash_fx_rates or {}).items():
        if not isinstance(currency, str) or not currency.strip():
            raise ValueError("FX currency keys must be non-empty strings")
        normalized_currency = currency.strip().upper()
        if normalized_currency in rates:
            raise ValueError(f"duplicate FX rate currency: {normalized_currency}")
        decimal_rate = Decimal(str(rate))
        if not decimal_rate.is_finite() or decimal_rate <= 0:
            raise ValueError("FX rates must be finite and positive")
        rates[normalized_currency] = decimal_rate
    cash_keys: set[tuple[object, str]] = set()
    cash_total = Decimal("0")
    for balance in state.cash:
        key = (balance.account_id, balance.currency.strip().upper())
        if key in cash_keys:
            raise ValueError(f"duplicate cash balance for account/currency: {key}")
        cash_keys.add(key)
        amount = Decimal(str(balance.amount))
        if not amount.is_finite() or amount < 0:
            raise ValueError("cash amounts must be finite and non-negative")
        if key[1] == valuation_currency:
            rate = Decimal("1")
        else:
            try:
                rate = rates[key[1]]
            except KeyError as exc:
                raise ValueError(f"missing FX rate for cash currency: {key[1]}") from exc
        cash_total += amount * rate

    price_map = {asset_id: Decimal(str(price)) for asset_id, price in prices.items()}
    values: dict[AssetId, Decimal] = {}
    for position in state.positions:
        if position.asset_id not in price_map:
            raise ValueError(f"missing valuation price for asset: {position.asset_id}")
        price = price_map[position.asset_id]
        if not price.is_finite() or price < 0:
            raise ValueError("valuation prices must be finite and non-negative")
        quantity = Decimal(str(position.quantity))
        if not quantity.is_finite() or quantity < 0:
            raise ValueError("position quantities must be finite and non-negative")
        values[position.asset_id] = values.get(position.asset_id, Decimal("0")) + quantity * price
    return PortfolioValuation(state.portfolio_id, as_of, values, cash_total)


def current_allocations_from_valuation(valuation: PortfolioValuation) -> tuple[Allocation, ...]:
    """Project non-cash asset weights from an authoritative valuation."""
    total = valuation.total_value
    return tuple(
        Allocation(asset_id=asset_id, weight=value / total)
        for asset_id, value in sorted(valuation.asset_values.items(), key=lambda item: str(item[0]))
        if value > 0
    )
