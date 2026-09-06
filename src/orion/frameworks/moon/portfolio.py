"""Validation for executable Moon portfolio allocations."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, isfinite
from typing import Sequence

from .models import Allocation


@dataclass(frozen=True)
class PortfolioValidator:
    """Validate the structural rules for a final allocation."""

    tolerance: float = 1e-12

    def validate(self, allocations: Sequence[Allocation]) -> tuple[Allocation, ...]:
        if not allocations:
            raise ValueError("at least one allocation is required")

        assets = [allocation.asset for allocation in allocations]
        if any(not asset.strip() for asset in assets):
            raise ValueError("allocation assets must not be empty")
        if len(assets) != len(set(assets)):
            raise ValueError("allocation assets must be unique")

        for allocation in allocations:
            if isinstance(allocation.weight, bool) or not isfinite(allocation.weight):
                raise ValueError("allocation weights must be finite numbers")
            if allocation.weight < 0:
                raise ValueError("allocation weights must be non-negative")

        total = sum(allocation.weight for allocation in allocations)
        if not isclose(total, 1.0, rel_tol=0.0, abs_tol=self.tolerance):
            raise ValueError("allocation weights must total 1.0")

        return tuple(allocations)
