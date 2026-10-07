"""Orion dashboard presentation boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from orion.core import OrionResult, Score

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
    """Read-only presentation layer over an official Orion runtime result."""

    def build_view(self, result: OrionResult | None = None) -> OrionDashboardView:
        """Build a view from Runtime/OrionResult output, never from Framework engines."""
        data: Mapping[str, object] = result.dashboard_data if result is not None else {}
        aurora = _mapping(data.get("aurora"))
        moon = _mapping(data.get("moon"))
        supernova = _mapping(data.get("supernova"))
        phoenix = _mapping(data.get("phoenix"))
        portfolio = _mapping(data.get("portfolio"))

        score_value = aurora.get("score", 0)
        score = score_value if isinstance(score_value, Score) else Score(int(score_value or 0))
        return OrionDashboardView(
            portfolio=PortfolioSummary(
                total_portfolio_value=float(portfolio.get("total_portfolio_value", 0.0)),
                portfolio_allocation=str(portfolio.get("portfolio_allocation", "Unknown")),
                portfolio_change=str(portfolio.get("portfolio_change", "Unknown")),
                last_update=str(portfolio.get("last_update", "Unknown")),
            ),
            aurora=AuroraSummary(
                score=score,
                market_regime=str(aurora.get("market_regime", "Unknown")),
                risk_state=str(aurora.get("risk_state", "Unknown")),
                regime_direction=str(aurora.get("regime_direction", "Unknown")),
            ),
            moon=MoonSummary(
                active_strategies=tuple(str(x) for x in moon.get("active_strategies", ())),
                consensus_allocation=str(moon.get("consensus_allocation", "Unknown")),
                current_holdings=tuple(str(x) for x in moon.get("current_holdings", ())),
                next_rebalance_date=str(moon.get("next_rebalance_date", "Unknown")),
            ),
            supernova=SupernovaSummary(
                approved_companies=tuple(str(x) for x in supernova.get("approved_companies", ())),
                theme_health=str(supernova.get("theme_health", "Unknown")),
                leadership_status=str(supernova.get("leadership_status", "Unknown")),
                replacement_risk=str(supernova.get("replacement_risk", "Unknown")),
            ),
            phoenix=PhoenixSummary(
                categories=tuple(str(x) for x in phoenix.get("categories", ())),
                current_leaders=tuple(str(x) for x in phoenix.get("current_leaders", ())),
                challenger_status=str(phoenix.get("challenger_status", "Unknown")),
                replacement_risk=str(phoenix.get("replacement_risk", "Unknown")),
            ),
        )


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, Mapping) else {}


def render_dashboard(result: OrionResult | None = None) -> int:
    """Render an Orion dashboard from an official runtime result."""
    view = OrionDashboard().build_view(result)
    print("Orion Dashboard")
    print(f"Aurora: {view.aurora.market_regime} ({view.aurora.score.value})")
    print(f"Moon: {len(view.moon.current_holdings)} holdings")
    print(f"Supernova: {len(view.supernova.approved_companies)} approved companies")
    print(f"Phoenix: {len(view.phoenix.current_leaders)} leaders")
    return 0
