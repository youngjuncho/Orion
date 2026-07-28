"""Moon framework entry helpers."""

from __future__ import annotations

from dataclasses import dataclass

from .models import MoonReport


@dataclass(frozen=True)
class MoonEngine:
    """Minimal Moon engine scaffold."""

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
