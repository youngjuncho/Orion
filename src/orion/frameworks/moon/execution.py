"""Translation from Moon signal assets to Common Portfolio allocations."""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from types import MappingProxyType
from typing import Mapping, Sequence
from ...core.portfolio import Allocation
from ...core.ids import AssetId
from .models import ConsensusAllocation

DOCUMENTED_EXECUTION_MAPPING = MappingProxyType({
    "VTI": "VTI", "VEU": "VEU", "SGOV": "SGOV",
    "SPY": "SPYM", "QQQ": "QQQM", "IWM": "VTWO", "EFA": "VEA", "EEM": "VWO",
    "AGG": "BND", "BIL": "SGOV", "SHY": "SCHO", "IEF": "VGIT", "TLT": "VGLT",
    "TIP": "SCHP", "LQD": "VCIT", "HYG": "SPHY", "BWX": "BNDX", "EMB": "VWOB",
    "GLD": "GLDM", "DBC": "BCI", "VNQ": "USRT", "SLV": "SIVR",
})

@dataclass(frozen=True)
class ExecutionMapper:
    mappings: Mapping[str, str] = field(default_factory=lambda: DOCUMENTED_EXECUTION_MAPPING)
    def __post_init__(self) -> None:
        object.__setattr__(self, "mappings", MappingProxyType(dict(self.mappings)))
    def map_allocations(self, allocations: Sequence[ConsensusAllocation]) -> tuple[Allocation, ...]:
        missing = sorted({a.asset for a in allocations if a.asset not in self.mappings})
        if missing:
            raise ValueError(f"no approved execution mapping for: {', '.join(missing)}")
        mapped: dict[str, Decimal] = {}
        for allocation in allocations:
            asset = self.mappings[allocation.asset]
            weight = Decimal(str(allocation.weight))
            mapped[asset] = mapped.get(asset, Decimal("0")) + weight

        source_total = sum((Decimal(str(a.weight)) for a in allocations), Decimal("0"))
        if abs(float(source_total) - 1.0) <= 1e-12:
            source_total = Decimal("1")
        mapped_total = sum(mapped.values(), Decimal("0"))
        if abs(float(mapped_total) - float(source_total)) > 1e-12:
            raise ValueError("execution mapping must preserve total allocation weight")

        # Consensus is calculated in floating-point space, while the common
        # PortfolioTarget contract requires an exact Decimal total of 1.0.
        # Preserve the mapped weights and absorb only the representational
        # remainder into the final allocation.
        items = list(mapped.items())
        if items:
            running = sum((weight for _, weight in items[:-1]), Decimal("0"))
            items[-1] = (items[-1][0], source_total - running)
        return tuple(Allocation(AssetId(asset), weight) for asset, weight in items)
