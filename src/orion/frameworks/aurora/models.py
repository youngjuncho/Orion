"""Aurora framework models."""

from __future__ import annotations

from dataclasses import dataclass

from orion.core import Score


@dataclass(frozen=True)
class AuroraIndicator:
    """A single Aurora indicator."""

    name: str
    category: str
    value: float | int | str | None
    score: Score
    state: str


@dataclass(frozen=True)
class AuroraRegime:
    """Aurora regime output."""

    regime: str
    score: Score
    direction: str
    confidence: Score


@dataclass(frozen=True)
class AuroraReport:
    """Normalized Aurora report payload."""

    score: Score
    current_regime: str
    regime_direction: str
    risk_state: str
    transition_risk: str
    indicators: tuple[AuroraIndicator, ...] = ()
