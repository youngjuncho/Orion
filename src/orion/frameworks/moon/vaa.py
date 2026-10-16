"""VAA G12 + Easy Trading signal selection from monthly adjusted closes."""

from __future__ import annotations

from dataclasses import dataclass
from math import floor, isfinite
from types import MappingProxyType
from typing import Mapping, Sequence

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
