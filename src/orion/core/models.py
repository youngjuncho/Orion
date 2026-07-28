"""Core Orion data models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final


class ScoreBand(str, Enum):
    """Normalized score bands used across Orion."""

    EXCEPTIONAL = "exceptional"
    STRONG = "strong"
    HEALTHY = "healthy"
    STABLE = "stable"
    NEUTRAL = "neutral"
    WEAK = "weak"
    DANGER = "danger"
    CRITICAL = "critical"


SCORE_MIN: Final[int] = 0
SCORE_MAX: Final[int] = 100


@dataclass(frozen=True)
class Score:
    """Normalized Orion score in the documented 0-100 range."""

    value: int

    def __post_init__(self) -> None:
        if not SCORE_MIN <= self.value <= SCORE_MAX:
            raise ValueError("score value must be between 0 and 100 inclusive")

    @property
    def band(self) -> ScoreBand:
        if self.value >= 90:
            return ScoreBand.EXCEPTIONAL
        if self.value >= 80:
            return ScoreBand.STRONG
        if self.value >= 70:
            return ScoreBand.HEALTHY
        if self.value >= 60:
            return ScoreBand.STABLE
        if self.value >= 50:
            return ScoreBand.NEUTRAL
        if self.value >= 40:
            return ScoreBand.WEAK
        if self.value >= 30:
            return ScoreBand.DANGER
        return ScoreBand.CRITICAL


@dataclass(frozen=True)
class State:
    """Framework-specific state label."""

    name: str


@dataclass(frozen=True)
class Regime:
    """Market regime with directional context."""

    name: str
    direction: str
    confidence: Score


@dataclass(frozen=True)
class ReviewRecord:
    """Framework review record."""

    date: str
    framework: str
    entity: str
    review_type: str
    outcome: str
    notes: str = ""


@dataclass(frozen=True)
class DecisionRecord:
    """Decision log record."""

    decision_id: str
    date: str
    status: str
    category: str
    title: str
    description: str


@dataclass(frozen=True)
class DashboardCard:
    """Normalized dashboard presentation model."""

    entity_name: str
    score: Score
    state: State
    trend: str
    last_updated: str
