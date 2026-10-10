"""Adapters from framework engines to the canonical Runtime result contract."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable, Sequence

from .api_models import FrameworkResult
from .decision import DecisionCandidate
from .ids import PortfolioId, TargetId
from .portfolio import PortfolioTarget
from .runtime import RuntimeContext


FrameworkAdapter = Callable[[RuntimeContext], FrameworkResult]


@dataclass(frozen=True)
class ReportFrameworkAdapter:
    """Adapt an existing framework report engine without changing its domain API."""

    framework_name: str
    report_factory: Callable[[], object]

    def __call__(self, _: RuntimeContext) -> FrameworkResult:
        report = self.report_factory()
        score = getattr(report, "score", None)
        if score is None:
            score = getattr(report, "phoenix_score", None)
        return FrameworkResult(
            framework_name=self.framework_name,
            execution_status="Completed",
            score=score,
        )


def make_report_adapter(framework_name: str, report_factory: Callable[[], object]) -> FrameworkAdapter:
    """Create the canonical Runtime adapter for an existing report engine."""

    return ReportFrameworkAdapter(framework_name, report_factory)


@dataclass(frozen=True)
class MoonPortfolioAdapter:
    """Expose Moon's canonical allocation lifecycle at the Runtime boundary.

    The adapter consumes StrategyResult values from either a precomputed
    factory or an explicit RuntimeContext-aware factory, then delegates
    consensus and execution-asset translation to MoonEngine. The latter can
    use the current MarketDataSet without the Core layer choosing data policy.
    It does not accept, reject, persist, or execute the resulting decision.
    """

    strategy_results_factory: Callable[[], Sequence[object]] | None
    portfolio_id: PortfolioId
    target_id: TargetId
    effective_from: date
    version: int = 1
    context_strategy_results_factory: Callable[[RuntimeContext], Sequence[object]] | None = None

    def __post_init__(self) -> None:
        if (self.strategy_results_factory is None) == (self.context_strategy_results_factory is None):
            raise ValueError("provide exactly one Moon strategy results factory")

    def __call__(self, context: RuntimeContext) -> FrameworkResult:
        from orion.frameworks.moon import MoonEngine
        from orion.frameworks.moon.models import StrategyResult

        if self.context_strategy_results_factory is not None:
            results = tuple(self.context_strategy_results_factory(context))
        else:
            assert self.strategy_results_factory is not None
            results = tuple(self.strategy_results_factory())
        if not all(isinstance(result, StrategyResult) for result in results):
            raise TypeError("Moon strategy_results_factory must return StrategyResult values")

        target = MoonEngine().build_portfolio_target(
            results,
            self.portfolio_id,
            target_id=self.target_id,
            effective_from=self.effective_from,
            version=self.version,
        )
        candidate = DecisionCandidate(
            candidate_id=f"moon-target:{self.target_id}",
            framework_name="Moon",
            decision_type="PortfolioTargetProposal",
            entity_type="PortfolioTarget",
            entity_id=str(self.target_id),
            payload={
                "portfolio_target": target,
                "strategy_results": results,
            },
        )
        return FrameworkResult(
            framework_name="Moon",
            execution_status="Completed",
            decision_candidates=(candidate,),
        )


@dataclass(frozen=True)
class OrbitPortfolioAdapter:
    """Expose Orbit's static PortfolioTarget through the Runtime boundary.

    Orbit remains an independent framework: the adapter only maps its existing
    static target into the Common Portfolio decision contract.
    """

    portfolio_id: PortfolioId
    target_id: TargetId
    effective_from: date
    version: int = 1

    def __call__(self, _: RuntimeContext) -> FrameworkResult:
        from orion.frameworks.orbit import OrbitEngine

        target = OrbitEngine().build_portfolio_target(
            self.portfolio_id,
            target_id=self.target_id,
            effective_from=self.effective_from,
            version=self.version,
        )
        candidate = DecisionCandidate(
            candidate_id=f"orbit-target:{self.target_id}",
            framework_name="Orbit",
            decision_type="PortfolioTargetProposal",
            entity_type="PortfolioTarget",
            entity_id=str(self.target_id),
            payload={"portfolio_target": target},
        )
        return FrameworkResult(
            framework_name="Orbit",
            execution_status="Completed",
            decision_candidates=(candidate,),
        )


def make_orbit_portfolio_adapter(
    portfolio_id: PortfolioId,
    *,
    target_id: TargetId,
    effective_from: date,
    version: int = 1,
) -> FrameworkAdapter:
    """Create the canonical Runtime adapter for Orbit PortfolioTarget proposals."""

    return OrbitPortfolioAdapter(
        portfolio_id=portfolio_id,
        target_id=target_id,
        effective_from=effective_from,
        version=version,
    )


def make_moon_portfolio_adapter(
    strategy_results_factory: Callable[[], Sequence[object]] | None,
    portfolio_id: PortfolioId,
    *,
    target_id: TargetId,
    effective_from: date,
    version: int = 1,
    context_strategy_results_factory: Callable[[RuntimeContext], Sequence[object]] | None = None,
) -> FrameworkAdapter:
    """Create the canonical Runtime adapter for Moon PortfolioTarget proposals."""

    return MoonPortfolioAdapter(
        strategy_results_factory=strategy_results_factory,
        portfolio_id=portfolio_id,
        target_id=target_id,
        effective_from=effective_from,
        version=version,
        context_strategy_results_factory=context_strategy_results_factory,
    )
