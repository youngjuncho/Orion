"""Moon framework entry helpers."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Sequence
from ...core.ids import PortfolioId, TargetId
from ...core.portfolio import Allocation, PortfolioTarget
from .consensus import ConsensusAllocator
from .execution import ExecutionMapper
from .models import MoonReport, StrategyResult

@dataclass(frozen=True)
class MoonEngine:
    consensus_allocator: ConsensusAllocator = field(default_factory=ConsensusAllocator)
    execution_mapper: ExecutionMapper = field(default_factory=ExecutionMapper)

    def build_allocation(self, results: Sequence[StrategyResult]) -> tuple[Allocation, ...]:
        return self.execution_mapper.map_allocations(self.consensus_allocator.allocate(results))

    def build_portfolio_target(
        self,
        results: Sequence[StrategyResult],
        portfolio_id: PortfolioId,
        *,
        target_id: TargetId,
        effective_from: date,
        version: int = 1,
    ) -> PortfolioTarget:
        return PortfolioTarget(
            target_id=target_id,
            portfolio_id=portfolio_id,
            version=version,
            effective_from=effective_from,
            allocations=self.build_allocation(results),
        )

    def build_report(self) -> MoonReport:
        return MoonReport(
            portfolio_allocation=(), current_holdings=(), next_rebalance_date="Unknown",
            strategy_summary=(), current_asset="Unknown", momentum_state="Unknown", risk_state="Unknown",
        )
