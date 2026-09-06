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

    def __post_init__(self) -> None:
        for name, value in (("category_name", self.category_name), ("state", self.state), ("trend", self.trend)):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True)
class CandidateAsset:
    """Phoenix candidate asset."""

    ticker: str
    name: str
    category: str
    score: Score
    status: str

    def __post_init__(self) -> None:
        for name, value in (("ticker", self.ticker), ("name", self.name), ("category", self.category), ("status", self.status)):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True)
class Leader:
    """Phoenix category leader."""

    asset: str
    category: str
    replacement_risk: str
    trend: str
    score: Score

    def __post_init__(self) -> None:
        for name, value in (("asset", self.asset), ("category", self.category), ("replacement_risk", self.replacement_risk), ("trend", self.trend)):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True)
class Challenger:
    """Phoenix category challenger."""

    asset: str
    category: str
    score: Score
    distance_to_leader: int

    def __post_init__(self) -> None:
        for name, value in (("asset", self.asset), ("category", self.category)):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True)
class PhoenixReport:
    """Normalized Phoenix report payload."""

    categories: tuple[Category, ...]
    current_leaders: tuple[Leader, ...]
    challengers: tuple[Challenger, ...]
    phoenix_score: Score
    replacement_risk: str

    def __post_init__(self) -> None:
        if not self.replacement_risk.strip():
            raise ValueError("replacement_risk must not be empty")
