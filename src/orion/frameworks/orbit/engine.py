"""Orbit static asset-allocation framework."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from ...core.ids import AssetId, PortfolioId, TargetId
from ...core.portfolio import Allocation, PortfolioTarget

@dataclass(frozen=True)
class OrbitEngine:
    """Build a Common PortfolioTarget from Orbit's fixed strategic allocation."""
    allocations: tuple[tuple[str, str], ...] = (
        ("SPYM", "0.30"), ("QQQM", "0.15"), ("VGIT", "0.20"),
        ("VGLT", "0.10"), ("GLDM", "0.10"), ("SIVR", "0.05"), ("SGOV", "0.10"),
    )

    def build_portfolio_target(self, portfolio_id: PortfolioId, *, target_id: TargetId, effective_from: date, version: int = 1) -> PortfolioTarget:
        return PortfolioTarget(
            target_id=target_id,
            portfolio_id=portfolio_id,
            version=version,
            effective_from=effective_from,
            allocations=tuple(Allocation(AssetId(asset), Decimal(weight)) for asset, weight in self.allocations),
        )
