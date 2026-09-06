"""Translation from documented Moon signal assets to execution assets."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isclose
from types import MappingProxyType
from typing import Mapping, Sequence

from .models import Allocation

DOCUMENTED_EXECUTION_MAPPING = MappingProxyType(
    {
        "SPY": "SPYM",
        "QQQ": "QQQM",
        "IWM": "VTWO",
        "EFA": "VEA",
        "EEM": "VWO",
        "AGG": "BND",
        "BIL": "SGOV",
        "SHY": "SCHO",
        "IEF": "VGIT",
        "TLT": "VGLT",
        "TIP": "SCHP",
        "LQD": "VCIT",
        "HYG": "SPHY",
        "BWX": "BNDX",
        "EMB": "VWOB",
        "GLD": "GLDM",
        "DBC": "BCI",
        "VNQ": "USRT",
        "SLV": "SIVR",
    }
)


@dataclass(frozen=True)
class ExecutionMapper:
    """Apply only signal-to-execution mappings approved in documentation."""

    mappings: Mapping[str, str] = field(
        default_factory=lambda: DOCUMENTED_EXECUTION_MAPPING
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "mappings", MappingProxyType(dict(self.mappings)))

    def map_allocations(self, allocations: Sequence[Allocation]) -> tuple[Allocation, ...]:
        """Translate and aggregate allocations using the configured mapping."""

        missing = sorted({allocation.asset for allocation in allocations if allocation.asset not in self.mappings})
        if missing:
            raise ValueError(f"no approved execution mapping for: {', '.join(missing)}")

        mapped: dict[str, float] = {}
        for allocation in allocations:
            execution_asset = self.mappings[allocation.asset]
            mapped[execution_asset] = mapped.get(execution_asset, 0.0) + allocation.weight

        source_total = sum(allocation.weight for allocation in allocations)
        mapped_total = sum(mapped.values())
        if not isclose(source_total, mapped_total, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("execution mapping must preserve total allocation weight")

        return tuple(Allocation(asset=asset, weight=weight) for asset, weight in mapped.items())
