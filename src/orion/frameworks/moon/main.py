"""Moon command entry helpers."""

from __future__ import annotations

from orion.frameworks.moon.engine import MoonEngine


def run_report() -> int:
    """Run the Moon report command."""

    report = MoonEngine().build_report()
    print(f"Current Asset: {report.current_asset}")
    print(f"Momentum State: {report.momentum_state}")
    print(f"Risk State: {report.risk_state}")
    print(f"Next Rebalance Date: {report.next_rebalance_date}")
    return 0
