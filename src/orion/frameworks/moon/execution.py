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
        mapped: dict[str, float] = {}
        for allocation in allocations:
            asset = self.mappings[allocation.asset]
            mapped[asset] = mapped.get(asset, 0.0) + allocation.weight
        if abs(sum(a.weight for a in allocations) - sum(mapped.values())) > 1e-12:
            raise ValueError("execution mapping must preserve total allocation weight")
        return tuple(Allocation(AssetId(asset), Decimal(str(weight))) for asset, weight in mapped.items())
