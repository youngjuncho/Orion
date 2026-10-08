"""CLI helpers for invoking framework commands through the public Runtime."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from orion.core import FrameworkRegistry, ExecutionMetadata, OrionRuntime, make_report_adapter, load_config
from orion.frameworks.aurora import AuroraEngine
from orion.frameworks.moon import MoonEngine
from orion.frameworks.phoenix import PhoenixEngine
from orion.frameworks.supernova import SupernovaEngine


def run_framework_report(framework: str) -> int:
    """Run one report-capable framework through OrionRuntime."""

    factories = {
        "aurora": ("Aurora", AuroraEngine().build_report),
        "moon": ("Moon", MoonEngine().build_report),
        "supernova": ("Supernova", SupernovaEngine().build_report),
        "phoenix": ("Phoenix", PhoenixEngine().build_report),
    }
    try:
        name, factory = factories[framework]
    except KeyError as exc:
        raise ValueError(f"framework report is not runtime-adapted: {framework}") from exc

    captured: list[object] = []

    def runtime_factory() -> object:
        report = factory()
        captured.append(report)
        return report

    registry = FrameworkRegistry()
    registry.register(name, object())
    now = datetime.now(timezone.utc).isoformat()
    execution = ExecutionMetadata(
        execution_id=f"cli-{uuid4().hex}",
        start_time=now,
        orion_version="v1",
    )
    runtime = OrionRuntime(load_config(), execution, registry=registry)
    runtime.run({name: make_report_adapter(name, runtime_factory)})
    report = captured[0]
    _print_report(name, report)
    return 0


def _print_report(name: str, report: object) -> None:
    if name == "Aurora":
        print(f"Aurora Score: {report.score.value}")
        print(f"Current Regime: {report.current_regime}")
        print(f"Regime Direction: {report.regime_direction}")
        print(f"Risk State: {report.risk_state}")
        print(f"Transition Risk: {report.transition_risk}")
    elif name == "Moon":
        print(f"Current Asset: {report.current_asset}")
        print(f"Momentum State: {report.momentum_state}")
        print(f"Risk State: {report.risk_state}")
        print(f"Next Rebalance Date: {report.next_rebalance_date}")
    elif name == "Supernova":
        print(f"Approved Companies: {len(report.approved_companies)}")
        print(f"Theme Health: {report.theme_health}")
        print(f"Leadership Status: {report.leadership_status}")
        print(f"Replacement Risk: {report.replacement_risk}")
    elif name == "Phoenix":
        print(f"Phoenix Score: {report.phoenix_score.value}")
        print(f"Categories: {len(report.categories)}")
        print(f"Current Leaders: {len(report.current_leaders)}")
        print(f"Replacement Risk: {report.replacement_risk}")
