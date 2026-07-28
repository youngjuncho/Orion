"""Phoenix framework models."""

from __future__ import annotations

from dataclasses import dataclass

from orion.core import Score


@dataclass(frozen=True)
class Category:
    """Phoenix category model."""

    category_name: str
    score: Score
    state: str
    trend: str


@dataclass(frozen=True)
class CandidateAsset:
    """Phoenix candidate asset."""

    ticker: str
    name: str
    category: str
    score: Score
    status: str


@dataclass(frozen=True)
class Leader:
    """Phoenix category leader."""

    asset: str
    category: str
    replacement_risk: str
    trend: str
    score: Score


@dataclass(frozen=True)
class Challenger:
    """Phoenix category challenger."""

    asset: str
    category: str
    score: Score
    distance_to_leader: int


@dataclass(frozen=True)
class PhoenixReport:
    """Normalized Phoenix report payload."""

    categories: tuple[Category, ...]
    current_leaders: tuple[Leader, ...]
    challengers: tuple[Challenger, ...]
    phoenix_score: Score
    replacement_risk: str
