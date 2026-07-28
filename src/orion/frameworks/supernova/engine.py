"""Supernova framework entry helpers."""

from __future__ import annotations

from dataclasses import dataclass

from orion.core import Score

from .models import ApprovedCompany, SupernovaReport


@dataclass(frozen=True)
class SupernovaEngine:
    """Minimal Supernova engine scaffold."""

    def build_report(self) -> SupernovaReport:
        # TODO: Implement Supernova theme, candidate, and leadership evaluation
        # once the scoring and review rules are closed in the research docs.
        return SupernovaReport(
            approved_companies=(
                ApprovedCompany("NVDA", "Digital Transformation", Score(0), "Unknown", "Unknown"),
                ApprovedCompany("GOOGL", "Digital Transformation", Score(0), "Unknown", "Unknown"),
                ApprovedCompany("ISRG", "Demographics", Score(0), "Unknown", "Unknown"),
                ApprovedCompany("PLTR", "Digital Transformation", Score(0), "Unknown", "Unknown"),
                ApprovedCompany("CEG", "Decarbonization", Score(0), "Unknown", "Unknown"),
            ),
            theme_health="Unknown",
            leadership_status="Unknown",
            replacement_risk="Unknown",
            watchlist=(),
        )
