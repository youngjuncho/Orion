"""Supernova framework models."""

from __future__ import annotations

from dataclasses import dataclass

from orion.core import Score


@dataclass(frozen=True)
class Theme:
    """Supernova theme model."""

    theme_name: str
    state: str
    score: Score
    trend: str

    def __post_init__(self) -> None:
        for name, value in (("theme_name", self.theme_name), ("state", self.state), ("trend", self.trend)):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True)
class CandidateCompany:
    """Supernova candidate company."""

    ticker: str
    company_name: str
    theme: str
    status: str
    score: Score

    def __post_init__(self) -> None:
        for name, value in (
            ("ticker", self.ticker),
            ("company_name", self.company_name),
            ("theme", self.theme),
            ("status", self.status),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True)
class ApprovedCompany:
    """Supernova approved company."""

    ticker: str
    theme: str
    leadership_score: Score
    replacement_risk: str
    trend: str

    def __post_init__(self) -> None:
        for name, value in (("ticker", self.ticker), ("theme", self.theme), ("replacement_risk", self.replacement_risk), ("trend", self.trend)):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True)
class SupernovaReport:
    """Normalized Supernova report payload."""

    approved_companies: tuple[ApprovedCompany, ...]
    theme_health: str
    leadership_status: str
    replacement_risk: str
    watchlist: tuple[CandidateCompany, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (
            ("theme_health", self.theme_health),
            ("leadership_status", self.leadership_status),
            ("replacement_risk", self.replacement_risk),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
