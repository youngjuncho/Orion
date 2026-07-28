"""Aurora command entry helpers."""

from __future__ import annotations

from orion.frameworks.aurora.engine import AuroraEngine


def run_report() -> int:
    """Run the Aurora report command."""

    report = AuroraEngine().build_report()
    print(f"Aurora Score: {report.score.value}")
    print(f"Current Regime: {report.current_regime}")
    print(f"Regime Direction: {report.regime_direction}")
    print(f"Risk State: {report.risk_state}")
    print(f"Transition Risk: {report.transition_risk}")
    return 0
