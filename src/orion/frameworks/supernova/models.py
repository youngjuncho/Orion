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


@dataclass(frozen=True)
class CandidateCompany:
    """Supernova candidate company."""

    ticker: str
    company_name: str
    theme: str
    status: str
    score: Score


@dataclass(frozen=True)
class ApprovedCompany:
    """Supernova approved company."""

    ticker: str
    theme: str
    leadership_score: Score
    replacement_risk: str
    trend: str


@dataclass(frozen=True)
class SupernovaReport:
    """Normalized Supernova report payload."""

    approved_companies: tuple[ApprovedCompany, ...]
    theme_health: str
    leadership_status: str
    replacement_risk: str
    watchlist: tuple[CandidateCompany, ...] = ()
