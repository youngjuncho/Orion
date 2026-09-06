"""Moon framework entry helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .consensus import ConsensusAllocator
from .execution import ExecutionMapper
from .models import Allocation, MoonReport, StrategyResult


@dataclass(frozen=True)
class MoonEngine:
    """Minimal Moon engine scaffold."""

    consensus_allocator: ConsensusAllocator = field(default_factory=ConsensusAllocator)
    execution_mapper: ExecutionMapper = field(default_factory=ExecutionMapper)

    def build_allocation(self, results: Sequence[StrategyResult]) -> tuple[Allocation, ...]:
        """Build executable allocation from completed strategy results."""

        consensus = self.consensus_allocator.allocate(results)
        return self.execution_mapper.map_allocations(consensus)

    def build_report(self) -> MoonReport:
        # TODO: Implement Moon strategy execution and consensus allocation once
        # the engine-specific strategy modules are added.
        return MoonReport(
            portfolio_allocation=(),
            current_holdings=(),
            next_rebalance_date="Unknown",
            strategy_summary=(),
            current_asset="Unknown",
            momentum_state="Unknown",
            risk_state="Unknown",
        )
