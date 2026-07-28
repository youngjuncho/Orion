"""Dashboard presentation models."""

from __future__ import annotations

from dataclasses import dataclass

from orion.core import Score


@dataclass(frozen=True)
class PortfolioSummary:
    """Top-level dashboard portfolio summary."""

    total_portfolio_value: float
    portfolio_allocation: str
    portfolio_change: str
    last_update: str


@dataclass(frozen=True)
class AuroraSummary:
    """Aurora dashboard summary."""

    score: Score
    market_regime: str
    risk_state: str
    regime_direction: str


@dataclass(frozen=True)
class MoonSummary:
    """Moon dashboard summary."""

    active_strategies: tuple[str, ...]
    consensus_allocation: str
    current_holdings: tuple[str, ...]
    next_rebalance_date: str


@dataclass(frozen=True)
class SupernovaSummary:
    """Supernova dashboard summary."""

    approved_companies: tuple[str, ...]
    theme_health: str
    leadership_status: str
    replacement_risk: str


@dataclass(frozen=True)
class PhoenixSummary:
    """Phoenix dashboard summary."""

    categories: tuple[str, ...]
    current_leaders: tuple[str, ...]
    challenger_status: str
    replacement_risk: str


@dataclass(frozen=True)
class OrionDashboardView:
    """Composite Orion dashboard view."""

    portfolio: PortfolioSummary
    aurora: AuroraSummary
    moon: MoonSummary
    supernova: SupernovaSummary
    phoenix: PhoenixSummary
