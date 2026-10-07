"""Common portfolio domain models."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from ..ids import FrameworkId, PortfolioId, TargetId
from .allocation import Allocation

@dataclass(frozen=True)
class Portfolio:
    portfolio_id: PortfolioId
    framework_id: FrameworkId
    name: str
    status: str = "active"

@dataclass(frozen=True)
class PortfolioTarget:
    target_id: TargetId
    portfolio_id: PortfolioId
    version: int
    effective_from: date
    allocations: tuple[Allocation, ...]
    effective_to: date | None = None

    def __post_init__(self) -> None:
        if self.version < 1:
            raise ValueError("target version must be >= 1")
        allocations = tuple(self.allocations)
        if not allocations:
            raise ValueError("portfolio target must contain at least one allocation")
        if len({a.asset_id for a in allocations}) != len(allocations):
            raise ValueError("portfolio target assets must be unique")
        if sum((a.weight for a in allocations), Decimal("0")) != Decimal("1"):
            raise ValueError("portfolio target weights must total 1.0")
        object.__setattr__(self, "allocations", allocations)
