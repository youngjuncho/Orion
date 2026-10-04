"""ADM signal generation from documented, precomputed momentum inputs."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from types import MappingProxyType
from typing import Mapping

from .models import StrategyResult

ADM_RISK_ASSETS = ("VTI", "VEU")


def calculate_adjusted_price_return(
    current_adjusted_price: float,
    trailing_adjusted_price: float,
) -> float:
    """Calculate return from two already selected adjusted-price observations.

    The data layer is responsible for supplying the current observation and
    the observation corresponding to the documented trailing period.
    """

    for name, value in (
        ("current_adjusted_price", current_adjusted_price),
        ("trailing_adjusted_price", trailing_adjusted_price),
    ):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a finite positive number")
        if not isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be a finite positive number")

    return current_adjusted_price / trailing_adjusted_price - 1.0


@dataclass(frozen=True)
class ADMSignalInput:
    """Inputs required by the Orion ADM selection rules.

    Momentum values are supplied by an upstream data/calculation layer. This
    object does not select market observations or define their freshness rules.
    """

    signal_date: str
    relative_momentum: Mapping[str, float]
    absolute_momentum_positive: bool
    defensive_asset: str

    def __post_init__(self) -> None:
        if not isinstance(self.signal_date, str) or not self.signal_date.strip():
            raise ValueError("signal_date must be a non-empty string")
        if (
            not isinstance(self.defensive_asset, str)
            or not self.defensive_asset.strip()
        ):
            raise ValueError("defensive_asset must be a non-empty string")
        if self.defensive_asset in ADM_RISK_ASSETS:
            raise ValueError("defensive_asset must be separate from ADM risk assets")
        if not isinstance(self.absolute_momentum_positive, bool):
            raise ValueError("absolute_momentum_positive must be a boolean")
        if not isinstance(self.relative_momentum, Mapping):
            raise ValueError("relative_momentum must be a mapping")
        if any(not isinstance(asset, str) for asset in self.relative_momentum):
            raise ValueError("relative_momentum keys must be strings")

        missing = [
            asset for asset in ADM_RISK_ASSETS if asset not in self.relative_momentum
        ]
        if missing:
            raise ValueError(f"relative_momentum is missing: {', '.join(missing)}")
        for asset, momentum in self.relative_momentum.items():
            if (
                isinstance(momentum, bool)
                or not isinstance(momentum, (int, float))
                or not isfinite(momentum)
            ):
                raise ValueError("relative momentum values must be finite numbers")

        object.__setattr__(
            self,
            "relative_momentum",
            MappingProxyType(dict(self.relative_momentum)),
        )


@dataclass(frozen=True)
class ADMStrategy:
    """The documented ADM selection rules within Moon."""

    defensive_asset: str
    name: str = "ADM"
    version: str = "1.0"
    status: str = "Active"

    def __post_init__(self) -> None:
        if (
            not isinstance(self.defensive_asset, str)
            or not self.defensive_asset.strip()
        ):
            raise ValueError("defensive_asset must be a non-empty string")
        if self.defensive_asset in ADM_RISK_ASSETS:
            raise ValueError("defensive_asset must be separate from ADM risk assets")

    def calculate_signal(self, inputs: ADMSignalInput) -> StrategyResult:
        """Select one target asset from already-calculated ADM inputs."""

        if not isinstance(inputs, ADMSignalInput):
            raise ValueError("inputs must be an ADMSignalInput")
        if inputs.defensive_asset != self.defensive_asset:
            raise ValueError("input defensive_asset must match the strategy configuration")

        us_momentum = inputs.relative_momentum["VTI"]
        international_momentum = inputs.relative_momentum["VEU"]
        if us_momentum == international_momentum:
            raise ValueError("relative momentum tie is not defined by the ADM specification")

        winner = "VTI" if us_momentum > international_momentum else "VEU"
        selected_asset = winner if inputs.absolute_momentum_positive else self.defensive_asset
        state = "Risk On" if inputs.absolute_momentum_positive else "Risk Off"

        metadata = {
            "relative_momentum_vti": str(us_momentum),
            "relative_momentum_veu": str(international_momentum),
            "absolute_momentum_positive": str(inputs.absolute_momentum_positive).lower(),
        }
        return StrategyResult(
            strategy_name=self.name,
            selected_assets=(selected_asset,),
            weights=(1.0,),
            signal_date=inputs.signal_date,
            state=state,
            metadata=metadata,
        )

    def generate_result(self, inputs: ADMSignalInput) -> StrategyResult:
        """Generate the standard Moon strategy result."""

        return self.calculate_signal(inputs)
