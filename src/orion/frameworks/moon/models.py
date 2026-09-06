"""Moon framework models."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from typing import Mapping

from orion.core import Score


@dataclass(frozen=True)
class Strategy:
    """Moon strategy metadata."""

    name: str
    version: str
    status: str


@dataclass(frozen=True)
class StrategyResult:
    """A single strategy output."""

    strategy_name: str
    selected_assets: tuple[str, ...]
    weights: tuple[float, ...]
    signal_date: str
    state: str = "Unknown"
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.strategy_name.strip():
            raise ValueError("strategy_name must not be empty")
        if not self.signal_date.strip():
            raise ValueError("signal_date must not be empty")
        if not self.selected_assets:
            raise ValueError("selected_assets must not be empty")
        if len(self.selected_assets) != len(self.weights):
            raise ValueError("selected_assets and weights must have the same length")
        if any(not asset.strip() for asset in self.selected_assets):
            raise ValueError("selected asset names must not be empty")
        if any(not isfinite(weight) or weight < 0 for weight in self.weights):
            raise ValueError("weights must be finite and non-negative")

        metadata = self.metadata if isinstance(self.metadata, Mapping) else dict(self.metadata)
        object.__setattr__(self, "metadata", MappingProxyType(dict(metadata)))


@dataclass(frozen=True)
class Allocation:
    """Moon portfolio allocation output."""

    asset: str
    weight: float


@dataclass(frozen=True)
class Portfolio:
    """Moon portfolio state."""

    current_holdings: tuple[Allocation, ...]
    next_rebalance_date: str


@dataclass(frozen=True)
class MoonReport:
    """Normalized Moon report payload."""

    portfolio_allocation: tuple[Allocation, ...]
    current_holdings: tuple[Allocation, ...]
    next_rebalance_date: str
    strategy_summary: tuple[StrategyResult, ...]
    current_asset: str
    momentum_state: str
    risk_state: str
