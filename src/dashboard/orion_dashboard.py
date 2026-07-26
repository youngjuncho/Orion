"""Orion top-level dashboard builder."""

from __future__ import annotations

from dataclasses import dataclass

from src.aurora import AuroraEngine
from src.core import Score
from src.moon import MoonEngine
from src.phoenix import PhoenixEngine
from src.supernova import SupernovaEngine

from .models import (
    AuroraSummary,
    MoonSummary,
    OrionDashboardView,
    PhoenixSummary,
    PortfolioSummary,
    SupernovaSummary,
)


@dataclass(frozen=True)
class OrionDashboard:
    """Read-only dashboard composition layer."""

    def build_view(self) -> OrionDashboardView:
        # TODO: Replace placeholder mappings with live framework outputs once
        # the dashboard rendering layer is connected to the UI implementation.
        aurora_report = AuroraEngine().build_report()
        moon_report = MoonEngine().build_report()
        supernova_report = SupernovaEngine().build_report()
        phoenix_report = PhoenixEngine().build_report()

        return OrionDashboardView(
            portfolio=PortfolioSummary(
                total_portfolio_value=0.0,
                portfolio_allocation="Unknown",
                portfolio_change="Unknown",
                last_update="Unknown",
            ),
            aurora=AuroraSummary(
                score=aurora_report.score,
                market_regime=aurora_report.current_regime,
                risk_state=aurora_report.risk_state,
                regime_direction=aurora_report.regime_direction,
            ),
            moon=MoonSummary(
                active_strategies=(),
                consensus_allocation="Unknown",
                current_holdings=tuple(allocation.asset for allocation in moon_report.current_holdings),
                next_rebalance_date=moon_report.next_rebalance_date,
            ),
            supernova=SupernovaSummary(
                approved_companies=tuple(company.ticker for company in supernova_report.approved_companies),
                theme_health=supernova_report.theme_health,
                leadership_status=supernova_report.leadership_status,
                replacement_risk=supernova_report.replacement_risk,
            ),
            phoenix=PhoenixSummary(
                categories=tuple(category.category_name for category in phoenix_report.categories),
                current_leaders=tuple(leader.asset for leader in phoenix_report.current_leaders),
                challenger_status="Unknown",
                replacement_risk=phoenix_report.replacement_risk,
            ),
        )


def render_dashboard() -> int:
    """Render the Orion dashboard as a textual summary."""

    view = OrionDashboard().build_view()
    print("Orion Dashboard")
    print(f"Aurora: {view.aurora.market_regime} ({view.aurora.score.value})")
    print(f"Moon: {len(view.moon.current_holdings)} holdings")
    print(f"Supernova: {len(view.supernova.approved_companies)} approved companies")
    print(f"Phoenix: {len(view.phoenix.current_leaders)} leaders")
    return 0
