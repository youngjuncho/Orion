"""ADM signal generation from documented, precomputed momentum inputs."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from types import MappingProxyType
from typing import Mapping

from .models import StrategyResult

ADM_RISK_ASSETS = ("VTI", "VEU")


@dataclass(frozen=True)
class ADMSignalInput:
    """Inputs required by the Orion ADM selection rules.

    Momentum values are supplied by an upstream data/calculation layer. This
    object does not define the unresolved total-return or dividend methods.
    """

    signal_date: str
    relative_momentum: Mapping[str, float]
    absolute_momentum_positive: bool
    defensive_asset: str

    def __post_init__(self) -> None:
        if not self.signal_date.strip():
            raise ValueError("signal_date must not be empty")
        if not self.defensive_asset.strip():
            raise ValueError("defensive_asset must not be empty")
        if self.defensive_asset in ADM_RISK_ASSETS:
            raise ValueError("defensive_asset must be separate from ADM risk assets")

        missing = [asset for asset in ADM_RISK_ASSETS if asset not in self.relative_momentum]
        if missing:
            raise ValueError(f"relative_momentum is missing: {', '.join(missing)}")
        if any(not isfinite(self.relative_momentum[asset]) for asset in ADM_RISK_ASSETS):
            raise ValueError("relative momentum values must be finite")

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
        if not self.defensive_asset.strip():
            raise ValueError("defensive_asset must not be empty")
        if self.defensive_asset in ADM_RISK_ASSETS:
            raise ValueError("defensive_asset must be separate from ADM risk assets")

    def calculate_signal(self, inputs: ADMSignalInput) -> StrategyResult:
        """Select one target asset from already-calculated ADM inputs."""

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
