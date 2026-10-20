"""Research-only BAA-G12 signal calculations.

This module deliberately does not load market data, resolve execution tickers,
register a strategy with the Moon runtime, or submit orders. Callers must supply
validated, date-aligned monthly total-return price observations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import isfinite
from types import MappingProxyType
from typing import Mapping, Sequence

from data.contracts import MarketDataSet

from .models import StrategyResult

BAA_CANARY_ASSETS = ("SPY", "VWO", "VEA", "BND")
BAA_OFFENSIVE_ASSETS = (
    "SPY", "QQQ", "IWM", "VGK", "EWJ", "VWO",
    "VNQ", "DBC", "GLD", "TLT", "HYG", "LQD",
)
BAA_DEFENSIVE_ASSETS = ("TIP", "DBC", "BIL", "IEF", "TLT", "LQD", "BND")
BAA_REQUIRED_ASSETS = tuple(dict.fromkeys(
    BAA_CANARY_ASSETS + BAA_OFFENSIVE_ASSETS + BAA_DEFENSIVE_ASSETS
))
BAA_LOOKBACK_MONTHS = 12
BAA_MOMENTUM_WEIGHTS = ((1, 12), (3, 4), (6, 2), (12, 1))


def _validated_prices(monthly_prices: Sequence[float], *, field_name: str) -> tuple[float, ...]:
    if isinstance(monthly_prices, (str, bytes)):
        raise ValueError(f"{field_name} must be a sequence of prices")
    try:
        prices = tuple(monthly_prices)
    except TypeError as exc:
        raise ValueError(f"{field_name} must be a sequence of prices") from exc
    if len(prices) < BAA_LOOKBACK_MONTHS + 1:
        raise ValueError(f"{field_name} requires at least 13 monthly prices")
    prices = prices[-(BAA_LOOKBACK_MONTHS + 1):]
    for price in prices:
        if isinstance(price, bool) or not isinstance(price, (int, float)) or not isfinite(price) or price <= 0:
            raise ValueError(f"{field_name} must contain only finite positive prices")
    return prices


def calculate_13612w_momentum(monthly_prices: Sequence[float]) -> float:
    """Return the unnormalized 13612W momentum from 13 month-end prices.

    Prices must be ordered oldest to newest. The caller owns date alignment,
    observation freshness, and the chosen total-return price-series convention.
    """
    prices = _validated_prices(monthly_prices, field_name="monthly_prices")
    current = prices[-1]
    return sum(
        weight * (current / prices[-months_ago - 1] - 1.0)
        for months_ago, weight in BAA_MOMENTUM_WEIGHTS
    )


def calculate_sma12_momentum(monthly_prices: Sequence[float]) -> float:
    """Return current price divided by the mean of 13 monthly prices, minus one."""
    prices = _validated_prices(monthly_prices, field_name="monthly_prices")
    return prices[-1] / (sum(prices) / len(prices)) - 1.0


@dataclass(frozen=True)
class BAASignalInput:
    """Validated, date-aligned monthly total-return price series for BAA-G12."""

    signal_date: str
    monthly_prices: Mapping[str, Sequence[float]]

    def __post_init__(self) -> None:
        if not isinstance(self.signal_date, str) or not self.signal_date.strip():
            raise ValueError("signal_date must be a non-empty string")
        if not isinstance(self.monthly_prices, Mapping):
            raise ValueError("monthly_prices must be a mapping")
        missing = [asset for asset in BAA_REQUIRED_ASSETS if asset not in self.monthly_prices]
        if missing:
            raise ValueError(f"monthly_prices is missing required assets: {', '.join(missing)}")
        normalized: dict[str, tuple[float, ...]] = {}
        for asset in BAA_REQUIRED_ASSETS:
            normalized[asset] = _validated_prices(
                self.monthly_prices[asset], field_name=f"monthly_prices[{asset}]"
            )
        object.__setattr__(self, "monthly_prices", MappingProxyType(normalized))


def build_baa_signal_input(
    dataset: MarketDataSet,
    *,
    signal_month: str,
) -> BAASignalInput:
    """Build BAA input from 13 complete monthly bars in a canonical dataset.

    ``signal_month`` must be ``YYYY-MM`` and names the last month to include.
    Each required asset must have exactly one ``adjusted_close`` observation
    in each of the 13 calendar months ending at that month. Each observation
    must carry ``month_end_session_verified=true`` metadata, supplied only by
    an adapter or validation step that verified the date against the final
    valid US market session. All required assets must use the same observed
    session date in each month. The signal date is the verified observation
    date for ``signal_month``, not the calendar month's final calendar date.
    This attestation does not independently validate the provider or certify
    adjusted close as a total-return series. Missing months, multiple bars per
    month, malformed dates, unverified/misaligned session dates, non-USD
    observations, and non-positive/non-numeric values fail closed. No provider
    calls, interpolation, forward-fill, or source fallback occurs.
    """
    if not isinstance(dataset, MarketDataSet):
        raise ValueError("dataset must be a MarketDataSet")
    if not isinstance(signal_month, str) or len(signal_month) != 7:
        raise ValueError("signal_month must use YYYY-MM format")
    try:
        target_month = date.fromisoformat(f"{signal_month}-01")
    except ValueError as exc:
        raise ValueError("signal_month must use YYYY-MM format") from exc
    if target_month.strftime("%Y-%m") != signal_month:
        raise ValueError("signal_month must use YYYY-MM format")
    # ``as_of`` may be a date or ISO timestamp. Requiring a parseable date
    # prevents the builder from treating the current, potentially incomplete
    # month as a completed monthly signal period.
    if not isinstance(dataset.as_of, str) or len(dataset.as_of) < 10:
        raise ValueError("dataset.as_of must begin with an ISO YYYY-MM-DD date")
    try:
        as_of_date = date.fromisoformat(dataset.as_of[:10])
    except ValueError as exc:
        raise ValueError("dataset.as_of must begin with an ISO YYYY-MM-DD date") from exc
    if as_of_date.isoformat() != dataset.as_of[:10]:
        raise ValueError("dataset.as_of must begin with an ISO YYYY-MM-DD date")
    if (target_month.year, target_month.month) >= (as_of_date.year, as_of_date.month):
        raise ValueError("signal_month must be earlier than the dataset.as_of month")

    target_months: list[str] = []
    year, month = target_month.year, target_month.month
    for _ in range(BAA_LOOKBACK_MONTHS + 1):
        target_months.append(f"{year:04d}-{month:02d}")
        month -= 1
        if month == 0:
            year -= 1
            month = 12
    target_months.reverse()
    target_set = set(target_months)
    selected: dict[str, dict[str, float]] = {asset: {} for asset in BAA_REQUIRED_ASSETS}
    selected_dates: dict[str, dict[str, str]] = {asset: {} for asset in BAA_REQUIRED_ASSETS}

    for point in dataset.observations:
        if point.symbol not in selected or point.field != "adjusted_close":
            continue
        if not isinstance(point.observed_at, str) or len(point.observed_at) != 10:
            raise ValueError(f"{point.symbol} observed_at must use YYYY-MM-DD format")
        try:
            observed = date.fromisoformat(point.observed_at)
        except ValueError as exc:
            raise ValueError(f"{point.symbol} observed_at must use YYYY-MM-DD format") from exc
        if observed.isoformat() != point.observed_at:
            raise ValueError(f"{point.symbol} observed_at must use YYYY-MM-DD format")
        month_key = point.observed_at[:7]
        if month_key not in target_set:
            continue
        if month_key in selected[point.symbol]:
            raise ValueError(
                f"multiple adjusted_close observations for {point.symbol} in {month_key}"
            )
        if point.metadata.get("month_end_session_verified") != "true":
            raise ValueError(
                f"{point.symbol} observation in {month_key} lacks verified final US trading-session metadata"
            )
        if point.currency != "USD":
            raise ValueError(f"{point.symbol} observation in {month_key} must use USD currency")
        value = point.value
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{point.symbol} observation in {month_key} must be numeric")
        if not isfinite(value) or value <= 0:
            raise ValueError(
                f"{point.symbol} observation in {month_key} must be finite and positive"
            )
        selected[point.symbol][month_key] = float(value)
        selected_dates[point.symbol][month_key] = point.observed_at

    for month_key in target_months:
        session_dates = {
            selected_dates[asset][month_key]
            for asset in BAA_REQUIRED_ASSETS
            if month_key in selected_dates[asset]
        }
        if len(session_dates) > 1:
            details = ", ".join(sorted(session_dates))
            raise ValueError(
                f"BAA observations in {month_key} must share one verified final US trading-session date; found {details}"
            )

    for asset in BAA_REQUIRED_ASSETS:
        missing_months = [month_key for month_key in target_months if month_key not in selected[asset]]
        if missing_months:
            raise ValueError(
                f"{asset} is missing adjusted_close months: {', '.join(missing_months)}"
            )

    signal_date = selected_dates[BAA_REQUIRED_ASSETS[0]][signal_month]
    return BAASignalInput(
        signal_date=signal_date,
        monthly_prices={
            asset: tuple(selected[asset][month_key] for month_key in target_months)
            for asset in BAA_REQUIRED_ASSETS
        },
    )


@dataclass(frozen=True)
class BAAStrategy:
    """Research-only BAA-G12 selector; not registered with the Moon runtime."""

    name: str = "BAA-G12"
    version: str = "0.1.0-research"
    status: str = "Research"

    def calculate_signal(self, inputs: BAASignalInput) -> StrategyResult:
        if not isinstance(inputs, BAASignalInput):
            raise ValueError("inputs must be a BAASignalInput")

        canary = {
            asset: calculate_13612w_momentum(inputs.monthly_prices[asset])
            for asset in BAA_CANARY_ASSETS
        }
        state = "Risk Off" if any(score < 0.0 for score in canary.values()) else "Risk On"

        offensive_scores = {
            asset: calculate_sma12_momentum(inputs.monthly_prices[asset])
            for asset in BAA_OFFENSIVE_ASSETS
        }
        defensive_scores = {
            asset: calculate_sma12_momentum(inputs.monthly_prices[asset])
            for asset in BAA_DEFENSIVE_ASSETS
        }
        defensive_absolute_scores = {
            asset: calculate_13612w_momentum(inputs.monthly_prices[asset])
            for asset in BAA_DEFENSIVE_ASSETS
        }
        offensive_ranked = sorted(
            BAA_OFFENSIVE_ASSETS,
            key=lambda asset: (-offensive_scores[asset], BAA_OFFENSIVE_ASSETS.index(asset)),
        )
        defensive_ranked = sorted(
            BAA_DEFENSIVE_ASSETS,
            key=lambda asset: (-defensive_scores[asset], BAA_DEFENSIVE_ASSETS.index(asset)),
        )

        replacements: list[str] = []
        if state == "Risk On":
            selected = offensive_ranked[:6]
            weights = {asset: 1.0 / 6.0 for asset in selected}
        else:
            # Preserve three equal-weight slots. Repeated BIL replacements are
            # aggregated to satisfy StrategyResult's unique-asset contract.
            slots = defensive_ranked[:3]
            selected_slots = [
                "BIL" if defensive_absolute_scores[asset] < defensive_absolute_scores["BIL"] else asset
                for asset in slots
            ]
            replacements = [
                original for original, replacement in zip(slots, selected_slots)
                if original != replacement
            ]
            weights: dict[str, float] = {}
            for asset in selected_slots:
                weights[asset] = weights.get(asset, 0.0) + 1.0 / 3.0
            selected = list(weights)

        # Avoid floating point drift in the final slot's weight.
        if selected:
            last = selected[-1]
            weights[last] = 1.0 - sum(weight for asset, weight in weights.items() if asset != last)

        return StrategyResult(
            strategy_name=self.name,
            selected_assets=tuple(selected),
            weights=tuple(weights[asset] for asset in selected),
            signal_date=inputs.signal_date,
            state=state,
            metadata={
                "method": "BAA_G12",
                "canary_13612w": ";".join(f"{asset}:{canary[asset]:.12g}" for asset in BAA_CANARY_ASSETS),
                "offensive_sma12_ranked": ",".join(offensive_ranked),
                "defensive_sma12_ranked": ",".join(defensive_ranked),
                "defensive_13612w": ";".join(
                    f"{asset}:{defensive_absolute_scores[asset]:.12g}" for asset in BAA_DEFENSIVE_ASSETS
                ),
                "selected_slots": ",".join(selected_slots) if state == "Risk Off" else ",".join(selected),
                "bil_replacements": ",".join(replacements),
                "price_series": "caller-supplied-monthly-total-return-series",
                "execution_status": "research-only-not-executable",
            },
        )

    def generate_result(self, inputs: BAASignalInput) -> StrategyResult:
        return self.calculate_signal(inputs)
