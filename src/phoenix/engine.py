"""Phoenix framework entry helpers."""

from __future__ import annotations

from dataclasses import dataclass

from src.core import Score

from .models import Category, Challenger, Leader, PhoenixReport


@dataclass(frozen=True)
class PhoenixEngine:
    """Minimal Phoenix engine scaffold."""

    def build_report(self) -> PhoenixReport:
        # TODO: Implement Phoenix category leadership evaluation once the
        # leadership rules and scoring questions are closed in the research docs.
        return PhoenixReport(
            categories=(
                Category("Smart Contract Platforms", Score(0), "Unknown", "Unknown"),
                Category("Oracle Networks", Score(0), "Unknown", "Unknown"),
                Category("Real World Assets", Score(0), "Unknown", "Unknown"),
                Category("AI Infrastructure", Score(0), "Unknown", "Unknown"),
                Category("Data Availability", Score(0), "Unknown", "Unknown"),
            ),
            current_leaders=(
                Leader("SOL", "Smart Contract Platforms", "Unknown", "Unknown", Score(0)),
                Leader("LINK", "Oracle Networks", "Unknown", "Unknown", Score(0)),
                Leader("ONDO", "Real World Assets", "Unknown", "Unknown", Score(0)),
                Leader("TAO", "AI Infrastructure", "Unknown", "Unknown", Score(0)),
                Leader("TIA", "Data Availability", "Unknown", "Unknown", Score(0)),
            ),
            challengers=(
                Challenger("SUI", "Smart Contract Platforms", Score(0), 0),
                Challenger("API3", "Oracle Networks", Score(0), 0),
                Challenger("PENDLE", "Real World Assets", Score(0), 0),
                Challenger("RENDER", "AI Infrastructure", Score(0), 0),
                Challenger("AVAIL", "Data Availability", Score(0), 0),
            ),
            phoenix_score=Score(0),
            replacement_risk="Unknown",
        )
