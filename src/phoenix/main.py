"""Phoenix command entry helpers."""

from __future__ import annotations

from src.phoenix.engine import PhoenixEngine


def run_report() -> int:
    """Run the Phoenix report command."""

    report = PhoenixEngine().build_report()
    print(f"Phoenix Score: {report.phoenix_score.value}")
    print(f"Categories: {len(report.categories)}")
    print(f"Current Leaders: {len(report.current_leaders)}")
    print(f"Replacement Risk: {report.replacement_risk}")
    return 0
