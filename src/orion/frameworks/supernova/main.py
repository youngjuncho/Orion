"""Supernova command entry helpers."""

from __future__ import annotations

from orion.frameworks.supernova.engine import SupernovaEngine


def run_report() -> int:
    """Run the Supernova report command."""

    report = SupernovaEngine().build_report()
    print(f"Approved Companies: {len(report.approved_companies)}")
    print(f"Theme Health: {report.theme_health}")
    print(f"Leadership Status: {report.leadership_status}")
    print(f"Replacement Risk: {report.replacement_risk}")
    return 0
