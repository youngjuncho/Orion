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
        if not isinstance(self.value, int) or isinstance(self.value, bool):
            raise ValueError("score value must be an integer")
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

    def __post_init__(self) -> None:
        _validate_non_empty_strings(name=self.name)


@dataclass(frozen=True)
class Regime:
    """Market regime with directional context."""

    name: str
    direction: str
    confidence: Score

    def __post_init__(self) -> None:
        _validate_non_empty_strings(name=self.name, direction=self.direction)
        if not isinstance(self.confidence, Score):
            raise ValueError("confidence must be a Score")


@dataclass(frozen=True)
class ReviewRecord:
    """Framework review record."""

    date: str
    framework: str
    entity: str
    review_type: str
    outcome: str
    notes: str = ""

    def __post_init__(self) -> None:
        _validate_non_empty_strings(
            date=self.date,
            framework=self.framework,
            entity=self.entity,
            review_type=self.review_type,
            outcome=self.outcome,
        )
        if not isinstance(self.notes, str):
            raise ValueError("notes must be a string")


@dataclass(frozen=True)
class DecisionRecord:
    """Decision log record."""

    decision_id: str
    date: str
    status: str
    category: str
    title: str
    description: str

    def __post_init__(self) -> None:
        _validate_non_empty_strings(
            decision_id=self.decision_id,
            date=self.date,
            status=self.status,
            category=self.category,
            title=self.title,
            description=self.description,
        )


@dataclass(frozen=True)
class DashboardCard:
    """Normalized dashboard presentation model."""

    entity_name: str
    score: Score
    state: State
    trend: str
    last_updated: str

    def __post_init__(self) -> None:
        _validate_non_empty_strings(
            entity_name=self.entity_name,
            trend=self.trend,
            last_updated=self.last_updated,
        )
        if not isinstance(self.score, Score):
            raise ValueError("score must be a Score")
        if not isinstance(self.state, State):
            raise ValueError("state must be a State")


def _validate_non_empty_strings(**values: str) -> None:
    for name, value in values.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")
