"""Moon framework models."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isclose, isfinite
from types import MappingProxyType
from typing import Mapping, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Strategy:
    """Moon strategy metadata."""

    name: str
    version: str
    status: str

    def __post_init__(self) -> None:
        _require_non_empty_strings(
            name=self.name, version=self.version, status=self.status
        )


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
        _require_non_empty_strings(
            strategy_name=self.strategy_name,
            signal_date=self.signal_date,
            state=self.state,
        )
        selected_assets = _tuple_of_type(
            self.selected_assets, str, "selected_assets"
        )
        weights = _as_tuple(self.weights, "weights")
        if not selected_assets:
            raise ValueError("selected_assets must not be empty")
        if any(not asset.strip() for asset in selected_assets):
            raise ValueError("selected asset names must not be empty strings")
        if len(selected_assets) != len(weights):
            raise ValueError("selected_assets and weights must have the same length")
        if any(
            isinstance(weight, bool)
            or not isinstance(weight, (int, float))
            or not isfinite(weight)
            or weight < 0
            for weight in weights
        ):
            raise ValueError("weights must be finite and non-negative")
        if len(selected_assets) != len(set(selected_assets)):
            raise ValueError("selected assets must be unique")
        if not isinstance(self.metadata, Mapping):
            raise ValueError("metadata must be a mapping")
        metadata = dict(self.metadata)
        if any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in metadata.items()
        ):
            raise ValueError("metadata keys and values must be strings")
        object.__setattr__(self, "selected_assets", selected_assets)
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "metadata", MappingProxyType(metadata))


@dataclass(frozen=True)
class Allocation:
    """Moon portfolio allocation output."""

    asset: str
    weight: float

    def __post_init__(self) -> None:
        _require_non_empty_strings(asset=self.asset)
        if (
            isinstance(self.weight, bool)
            or not isinstance(self.weight, (int, float))
            or not isfinite(self.weight)
            or self.weight < 0
        ):
            raise ValueError("weight must be finite and non-negative")


@dataclass(frozen=True)
class PortfolioTarget:
    """Desired Moon portfolio allocation expressed in execution assets."""

    allocations: tuple[Allocation, ...]
    rebalance_date: str
    status: str

    def __post_init__(self) -> None:
        allocations = _tuple_of_type(self.allocations, Allocation, "allocations")
        if not allocations:
            raise ValueError("portfolio target must contain at least one allocation")
        if len({item.asset for item in allocations}) != len(allocations):
            raise ValueError("portfolio target assets must be unique")
        if not isclose(
            sum(item.weight for item in allocations),
            1.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise ValueError("portfolio target weights must total 1.0")
        _require_non_empty_strings(
            rebalance_date=self.rebalance_date, status=self.status
        )
        object.__setattr__(self, "allocations", allocations)


@dataclass(frozen=True)
class Portfolio:
    """Moon portfolio state."""

    current_holdings: tuple[Allocation, ...]
    next_rebalance_date: str

    def __post_init__(self) -> None:
        _require_non_empty_strings(next_rebalance_date=self.next_rebalance_date)
        holdings = _tuple_of_type(
            self.current_holdings, Allocation, "current_holdings"
        )
        object.__setattr__(self, "current_holdings", holdings)


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

    def __post_init__(self) -> None:
        _require_non_empty_strings(
            next_rebalance_date=self.next_rebalance_date,
            current_asset=self.current_asset,
            momentum_state=self.momentum_state,
            risk_state=self.risk_state,
        )
        object.__setattr__(
            self,
            "portfolio_allocation",
            _tuple_of_type(
                self.portfolio_allocation, Allocation, "portfolio_allocation"
            ),
        )
        object.__setattr__(
            self,
            "current_holdings",
            _tuple_of_type(self.current_holdings, Allocation, "current_holdings"),
        )
        object.__setattr__(
            self,
            "strategy_summary",
            _tuple_of_type(
                self.strategy_summary, StrategyResult, "strategy_summary"
            ),
        )


def _require_non_empty_strings(**values: object) -> None:
    for name, value in values.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")


def _tuple_of_type(values: object, item_type: type[T], name: str) -> tuple[T, ...]:
    items = _as_tuple(values, name)
    if any(not isinstance(item, item_type) for item in items):
        raise ValueError(f"{name} must contain only {item_type.__name__} values")
    return items


def _as_tuple(values: object, name: str) -> tuple:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name} must be a collection, not text")
    try:
        items = tuple(values)  # type: ignore[arg-type]
    except TypeError as exc:
        raise ValueError(f"{name} must be a collection") from exc
    return items
