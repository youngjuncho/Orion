"""Moon framework entry helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .consensus import ConsensusAllocator
from .execution import ExecutionMapper
from .models import Allocation, MoonReport, PortfolioTarget, StrategyResult
from .portfolio import PortfolioValidator


@dataclass(frozen=True)
class MoonEngine:
    """Minimal Moon engine scaffold."""

    consensus_allocator: ConsensusAllocator = field(default_factory=ConsensusAllocator)
    execution_mapper: ExecutionMapper = field(default_factory=ExecutionMapper)
    portfolio_validator: PortfolioValidator = field(default_factory=PortfolioValidator)

    def build_allocation(self, results: Sequence[StrategyResult]) -> tuple[Allocation, ...]:
        """Build executable allocation from completed strategy results."""

        consensus = self.consensus_allocator.allocate(results)
        executable = self.execution_mapper.map_allocations(consensus)
        return self.portfolio_validator.validate(executable)

    def build_portfolio_target(
        self,
        results: Sequence[StrategyResult],
        *,
        rebalance_date: str,
        status: str,
    ) -> PortfolioTarget:
        """Build a validated target portfolio from completed strategy results."""

        allocations = self.build_allocation(results)
        target = PortfolioTarget(
            allocations=allocations,
            rebalance_date=rebalance_date,
            status=status,
        )
        self.portfolio_validator.validate(target.allocations)
        return target

    def build_report(self) -> MoonReport:
        # TODO: Implement Moon strategy execution and report construction once
        # the market-data and portfolio output contracts are approved.
        return MoonReport(
            portfolio_allocation=(),
            current_holdings=(),
            next_rebalance_date="Unknown",
            strategy_summary=(),
            current_asset="Unknown",
            momentum_state="Unknown",
            risk_state="Unknown",
        )
