"""Moon consensus allocation."""
from __future__ import annotations
from dataclasses import dataclass
from math import isclose
from typing import Sequence
from .models import ConsensusAllocation, StrategyResult

@dataclass(frozen=True)
class ConsensusAllocator:
    """Aggregate active strategy results with equal strategy weighting."""
    def allocate(self, results: Sequence[StrategyResult]) -> tuple[ConsensusAllocation, ...]:
        if not results:
            raise ValueError("at least one strategy result is required")
        names = [result.strategy_name for result in results]
        if len(names) != len(set(names)):
            raise ValueError("strategy results must contain unique strategies")
        strategy_weight = 1.0 / len(results)
        aggregated: dict[str, float] = {}
        for result in results:
            result_total = sum(result.weights)
            if result_total <= 0:
                raise ValueError("each strategy result must have positive total weight")
            for asset, weight in zip(result.selected_assets, result.weights):
                normalized = weight / result_total
                aggregated[asset] = aggregated.get(asset, 0.0) + strategy_weight * normalized
        if not isclose(sum(aggregated.values()), 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("consensus allocation must total 1.0")
        return tuple(ConsensusAllocation(asset=asset, weight=weight) for asset, weight in aggregated.items())
