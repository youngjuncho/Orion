"""Dashboard presentation models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from orion.core import Score


@dataclass(frozen=True)
class PortfolioSummary:
    """Top-level dashboard portfolio summary."""

    total_portfolio_value: float
    portfolio_allocation: str
    portfolio_change: str
    last_update: str

    def __post_init__(self) -> None:
        if (
            isinstance(self.total_portfolio_value, bool)
            or not isinstance(self.total_portfolio_value, (int, float))
            or not isfinite(self.total_portfolio_value)
        ):
            raise ValueError("total_portfolio_value must be a finite number")
        _validate_text_fields(
            portfolio_allocation=self.portfolio_allocation,
            portfolio_change=self.portfolio_change,
            last_update=self.last_update,
        )


@dataclass(frozen=True)
class AuroraSummary:
    """Aurora dashboard summary."""

    score: Score
    market_regime: str
    risk_state: str
    regime_direction: str

    def __post_init__(self) -> None:
        if not isinstance(self.score, Score):
            raise ValueError("score must be a Score")
        _validate_text_fields(
            market_regime=self.market_regime,
            risk_state=self.risk_state,
            regime_direction=self.regime_direction,
        )


@dataclass(frozen=True)
class MoonSummary:
    """Moon dashboard summary."""

    active_strategies: tuple[str, ...]
    consensus_allocation: str
    current_holdings: tuple[str, ...]
    next_rebalance_date: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "active_strategies",
            _snapshot_string_tuple(self.active_strategies, "active_strategies"),
        )
        object.__setattr__(
            self,
            "current_holdings",
            _snapshot_string_tuple(self.current_holdings, "current_holdings"),
        )
        _validate_text_fields(
            consensus_allocation=self.consensus_allocation,
            next_rebalance_date=self.next_rebalance_date,
        )


@dataclass(frozen=True)
class SupernovaSummary:
    """Supernova dashboard summary."""

    approved_companies: tuple[str, ...]
    theme_health: str
    leadership_status: str
    replacement_risk: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "approved_companies",
            _snapshot_string_tuple(self.approved_companies, "approved_companies"),
        )
        _validate_text_fields(
            theme_health=self.theme_health,
            leadership_status=self.leadership_status,
            replacement_risk=self.replacement_risk,
        )


@dataclass(frozen=True)
class PhoenixSummary:
    """Phoenix dashboard summary."""

    categories: tuple[str, ...]
    current_leaders: tuple[str, ...]
    challenger_status: str
    replacement_risk: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "categories", _snapshot_string_tuple(self.categories, "categories")
        )
        object.__setattr__(
            self,
            "current_leaders",
            _snapshot_string_tuple(self.current_leaders, "current_leaders"),
        )
        _validate_text_fields(
            challenger_status=self.challenger_status,
            replacement_risk=self.replacement_risk,
        )


@dataclass(frozen=True)
class OrionDashboardView:
    """Composite Orion dashboard view."""

    portfolio: PortfolioSummary
    aurora: AuroraSummary
    moon: MoonSummary
    supernova: SupernovaSummary
    phoenix: PhoenixSummary

    def __post_init__(self) -> None:
        for name, expected_type in (
            ("portfolio", PortfolioSummary),
            ("aurora", AuroraSummary),
            ("moon", MoonSummary),
            ("supernova", SupernovaSummary),
            ("phoenix", PhoenixSummary),
        ):
            if not isinstance(getattr(self, name), expected_type):
                raise ValueError(f"{name} must be a {expected_type.__name__}")


def _validate_text_fields(**values: str) -> None:
    for name, value in values.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")


def _snapshot_string_tuple(values: object, name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name} must be a sequence of strings")
    try:
        items = tuple(values)  # type: ignore[arg-type]
    except TypeError as exc:
        raise ValueError(f"{name} must be a sequence of strings") from exc
    if any(not isinstance(item, str) or not item.strip() for item in items):
        raise ValueError(f"{name} must contain non-empty strings")
    return items
