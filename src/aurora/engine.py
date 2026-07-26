"""Aurora framework entry helpers."""

from __future__ import annotations

from dataclasses import dataclass

from src.core import Score

from .models import AuroraReport


@dataclass(frozen=True)
class AuroraEngine:
    """Minimal Aurora engine scaffold."""

    def build_report(self) -> AuroraReport:
        # TODO: Implement Aurora scoring and regime evaluation once the research
        # questions in the Aurora documents are closed.
        return AuroraReport(
            score=Score(0),
            current_regime="Unknown",
            regime_direction="Stable",
            risk_state="Unknown",
            transition_risk="Unknown",
        )
