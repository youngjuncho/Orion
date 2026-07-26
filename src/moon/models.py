"""Moon framework models."""

from __future__ import annotations

from dataclasses import dataclass

from src.core import Score


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
