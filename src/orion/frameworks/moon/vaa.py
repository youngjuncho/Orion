"""VAA G12 + Easy Trading signal selection from monthly adjusted closes."""

from __future__ import annotations

from calendar import monthrange
from dataclasses import dataclass
from datetime import date
from math import floor, isfinite
from types import MappingProxyType
from typing import Mapping, Sequence

from data.contracts import MarketDataSet

from .models import StrategyResult

VAA_OFFENSIVE_ASSETS = (
    "SPY", "IWM", "QQQ", "VGK", "EWJ", "VWO",
    "VNQ", "GSG", "GLD", "TLT", "HYG", "LQD",
)
VAA_DEFENSIVE_ASSETS = ("SHY", "IEF", "LQD")
VAA_MOMENTUM_WEIGHTS = ((1, 12), (3, 4), (6, 2), (12, 1))
VAA_LOOKBACK_MONTHS = 12


def calculate_13612w_momentum(monthly_adjusted_closes: Sequence[float]) -> float:
    """Calculate 13612W momentum from at least 13 ordered monthly adjusted closes.

    The final value is the latest completed month-end observation. Values must
    be oldest-to-newest and strictly positive; observation selection and date
    freshness are the responsibility of the upstream data layer.
    """
    if isinstance(monthly_adjusted_closes, (str, bytes)):
        raise ValueError("monthly_adjusted_closes must be a sequence of prices")
    try:
        prices = tuple(monthly_adjusted_closes)
    except TypeError as exc:
        raise ValueError("monthly_adjusted_closes must be a sequence of prices") from exc
    if len(prices) < VAA_LOOKBACK_MONTHS + 1:
        raise ValueError("13612W momentum requires at least 13 monthly prices")
    prices = prices[-(VAA_LOOKBACK_MONTHS + 1):]
    for price in prices:
        if isinstance(price, bool) or not isinstance(price, (int, float)) or not isfinite(price) or price <= 0:
            raise ValueError("monthly adjusted closes must be finite positive numbers")
    current = prices[-1]
    return sum(weight * (current / prices[-months_ago - 1] - 1.0)
               for months_ago, weight in VAA_MOMENTUM_WEIGHTS)


@dataclass(frozen=True)
class VAASignalInput:
    """Complete, date-aligned 13612W scores for the G12 and defensive universes."""

    signal_date: str
    offensive_momentum: Mapping[str, float]
    defensive_momentum: Mapping[str, float]

    def __post_init__(self) -> None:
        if not isinstance(self.signal_date, str) or not self.signal_date.strip():
            raise ValueError("signal_date must be a non-empty string")
        for field_name, values, universe in (
            ("offensive_momentum", self.offensive_momentum, VAA_OFFENSIVE_ASSETS),
            ("defensive_momentum", self.defensive_momentum, VAA_DEFENSIVE_ASSETS),
        ):
            if not isinstance(values, Mapping):
                raise ValueError(f"{field_name} must be a mapping")
            missing = [asset for asset in universe if asset not in values]
            if missing:
                raise ValueError(f"{field_name} is missing: {', '.join(missing)}")
            for asset in universe:
                score = values[asset]
                if isinstance(score, bool) or not isinstance(score, (int, float)) or not isfinite(score):
                    raise ValueError(f"{field_name}[{asset}] must be a finite number")
            object.__setattr__(self, field_name, MappingProxyType(dict(values)))


def _vaa_iso_date(value: str, name: str) -> date:
    if not isinstance(value, str) or len(value) != 10:
        raise ValueError(f"{name} must use YYYY-MM-DD format")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{name} must use YYYY-MM-DD format") from exc
    if parsed.isoformat() != value:
        raise ValueError(f"{name} must use YYYY-MM-DD format")
    return parsed


def build_vaa_signal_input(
    monthly_observations: Mapping[str, Sequence[tuple[str, float]]],
    *,
    as_of_date: str,
) -> VAASignalInput:
    """Build a complete VAA input from dated monthly adjusted-close series.

    Each series is oldest-to-newest. All required assets must share the same
    13-or-more observation dates, with no missing calendar month, and the last
    observation must belong to the last completed calendar month at as_of_date.
    This function does not fetch data or certify exchange calendars/provider SLA.
    """
    as_of = _vaa_iso_date(as_of_date, "as_of_date")
    if not isinstance(monthly_observations, Mapping):
        raise ValueError("monthly_observations must be a mapping")
    universe = tuple(dict.fromkeys(VAA_OFFENSIVE_ASSETS + VAA_DEFENSIVE_ASSETS))
    missing = [asset for asset in universe if asset not in monthly_observations]
    if missing:
        raise ValueError(f"monthly_observations is missing: {', '.join(missing)}")

    parsed_series: dict[str, tuple[tuple[date, float], ...]] = {}
    reference_dates: tuple[date, ...] | None = None
    for asset in universe:
        raw_series = monthly_observations[asset]
        if isinstance(raw_series, (str, bytes)):
            raise ValueError(f"{asset} observations must be a sequence")
        try:
            rows = tuple(raw_series)
        except TypeError as exc:
            raise ValueError(f"{asset} observations must be a sequence") from exc
        if len(rows) < VAA_LOOKBACK_MONTHS + 1:
            raise ValueError(f"{asset} requires at least 13 monthly observations")
        parsed: list[tuple[date, float]] = []
        for row in rows:
            if not isinstance(row, (tuple, list)) or len(row) != 2:
                raise ValueError(f"{asset} observations must be (date, adjusted_close) pairs")
            observed = _vaa_iso_date(row[0], f"{asset} observation date")
            price = row[1]
            if isinstance(price, bool) or not isinstance(price, (int, float)) or not isfinite(price) or price <= 0:
                raise ValueError(f"{asset} adjusted closes must be finite positive numbers")
            parsed.append((observed, float(price)))
        dates = tuple(item[0] for item in parsed)
        if any(later <= earlier for earlier, later in zip(dates, dates[1:])):
            raise ValueError(f"{asset} observation dates must be strictly increasing")
        for earlier, later in zip(dates, dates[1:]):
            expected_year = earlier.year + (1 if earlier.month == 12 else 0)
            expected_month = 1 if earlier.month == 12 else earlier.month + 1
            if (later.year, later.month) != (expected_year, expected_month):
                raise ValueError(f"{asset} observations must not skip calendar months")
        if reference_dates is None:
            reference_dates = dates
        elif dates != reference_dates:
            raise ValueError("all VAA assets must have the same observation dates")
        parsed_series[asset] = tuple(parsed)

    assert reference_dates is not None
    latest = reference_dates[-1]
    previous_month_year = as_of.year if as_of.month > 1 else as_of.year - 1
    previous_month = as_of.month - 1 if as_of.month > 1 else 12
    if (latest.year, latest.month) != (previous_month_year, previous_month):
        raise ValueError("latest observation must be in the last completed calendar month")

    scores: dict[str, float] = {}
    for asset, series in parsed_series.items():
        scores[asset] = calculate_13612w_momentum([price for _, price in series])
    signal_date = latest.isoformat()
    return VAASignalInput(
        signal_date=signal_date,
        offensive_momentum={asset: scores[asset] for asset in VAA_OFFENSIVE_ASSETS},
        defensive_momentum={asset: scores[asset] for asset in VAA_DEFENSIVE_ASSETS},
    )


def build_vaa_signal_input_from_dataset(
    dataset: MarketDataSet,
    *,
    field: str = "adjusted_close",
    as_of_date: str | None = None,
) -> VAASignalInput:
    """Adapt a normalized MarketDataSet to the VAA dated-series contract.

    Duplicate identities are rejected by MarketDataSet itself. For required VAA
    observations this adapter also rejects mixed provider sources and nonnumeric
    or missing monthly values, and delegates date alignment to the pure builder.
    """
    if not isinstance(dataset, MarketDataSet):
        raise ValueError("dataset must be a MarketDataSet")
    if not isinstance(field, str) or not field.strip():
        raise ValueError("field must be a non-empty string")
    effective_as_of = dataset.as_of if as_of_date is None else as_of_date
    universe = tuple(dict.fromkeys(VAA_OFFENSIVE_ASSETS + VAA_DEFENSIVE_ASSETS))
    relevant = [point for point in dataset.observations if point.symbol in universe and point.field == field]
    sources = {point.source for point in relevant}
    if len(sources) > 1:
        raise ValueError("VAA observations must use a single data source")
    series: dict[str, list[tuple[str, float]]] = {asset: [] for asset in universe}
    for point in relevant:
        value = point.value
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or value <= 0:
            raise ValueError(f"{point.symbol} adjusted closes must be finite positive numbers")
        series[point.symbol].append((point.observed_at, float(value)))
    missing = [asset for asset in universe if not series[asset]]
    if missing:
        raise ValueError(f"MarketDataSet is missing adjusted_close observations for: {', '.join(missing)}")
    for asset in universe:
        series[asset].sort(key=lambda row: row[0])
    return build_vaa_signal_input(series, as_of_date=effective_as_of)


@dataclass(frozen=True)
class VAAStrategy:
    """G12 offensive universe, T=2/B=4 Easy Trading allocation rule."""

    name: str = "VAA"
    version: str = "1.0"
    status: str = "Research"

    def calculate_signal(self, inputs: VAASignalInput) -> StrategyResult:
        if not isinstance(inputs, VAASignalInput):
            raise ValueError("inputs must be a VAASignalInput")

        # Stable tie-breaking follows the declared universe order.
        offensive_ranked = sorted(VAA_OFFENSIVE_ASSETS,
                                  key=lambda asset: (-inputs.offensive_momentum[asset], VAA_OFFENSIVE_ASSETS.index(asset)))
        defensive_ranked = sorted(VAA_DEFENSIVE_ASSETS,
                                  key=lambda asset: (-inputs.defensive_momentum[asset], VAA_DEFENSIVE_ASSETS.index(asset)))
        breadth = sum(inputs.offensive_momentum[asset] <= 0 for asset in VAA_OFFENSIVE_ASSETS)
        defensive_fraction = min(1.0, floor(breadth * 2 / 4) / 2)

        if defensive_fraction == 0.0:
            selected = (offensive_ranked[0], offensive_ranked[1])
            weights = (0.5, 0.5)
            state = "Offensive"
        elif defensive_fraction == 0.5:
            offensive = offensive_ranked[0]
            defensive = next(asset for asset in defensive_ranked if asset != offensive)
            selected = (offensive, defensive)
            weights = (0.5, 0.5)
            state = "Mixed"
        else:
            selected = (defensive_ranked[0],)
            weights = (1.0,)
            state = "Defensive"

        return StrategyResult(
            strategy_name=self.name,
            selected_assets=selected,
            weights=weights,
            signal_date=inputs.signal_date,
            state=state,
            metadata={
                "method": "G12_Easy_Trading_T2_B4",
                "offensive_nonpositive_count": str(breadth),
                "defensive_fraction": str(defensive_fraction),
                "offensive_ranked": ",".join(offensive_ranked),
                "defensive_ranked": ",".join(defensive_ranked),
            },
        )

    def generate_result(self, inputs: VAASignalInput) -> StrategyResult:
        return self.calculate_signal(inputs)
