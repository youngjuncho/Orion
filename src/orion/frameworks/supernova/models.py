"""Supernova framework models."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from orion.core import Score


COMPANY_SCORE_WEIGHTS: dict[str, int] = {
    "Theme Exposure": 20,
    "Competitive Moat": 25,
    "Leadership Position": 25,
    "Growth Quality": 15,
    "Execution Quality": 15,
}

PORTFOLIO_STATES = {"Approved", "Watchlist", "Review Required", "Retired"}
LEADERSHIP_ROLES = {"Leader", "Challenger", "Candidate"}
REPLACEMENT_RISKS = {"Very Low", "Low", "Medium", "High", "Critical"}
PLACEHOLDER_REPLACEMENT_RISK = "Unknown"
GOVERNANCE_ACTIONS = {"Continue", "Promote", "Review", "Replace", "Retire"}


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
class EvidenceSource:
    """Provenance record for evidence used in a Supernova assessment."""

    source_type: str
    source_name: str
    reference: str
    publication_date: str = ""
    access_date: str = ""
    relevant_period: str = ""

    def __post_init__(self) -> None:
        for name, value in ((
            ("source_type", self.source_type),
            ("source_name", self.source_name),
            ("reference", self.reference),
        )):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        for name, value in ((
            ("publication_date", self.publication_date),
            ("access_date", self.access_date),
            ("relevant_period", self.relevant_period),
        )):
            if not isinstance(value, str):
                raise ValueError(f"{name} must be a string")


@dataclass(frozen=True)
class CompanyScoreReview:
    """Evidence-backed review of one company scoring dimension."""

    entity: str
    dimension: str
    score: Score
    evidence: str
    assessment: str
    review_date: str
    reviewer: str = ""
    sources: tuple[EvidenceSource, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (
            ("entity", self.entity),
            ("dimension", self.dimension),
            ("evidence", self.evidence),
            ("assessment", self.assessment),
            ("review_date", self.review_date),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        if not isinstance(self.score, Score):
            raise ValueError("score must be a Score")
        if not isinstance(self.reviewer, str):
            raise ValueError("reviewer must be a string")
        sources = tuple(self.sources)
        if any(not isinstance(source, EvidenceSource) for source in sources):
            raise ValueError("sources must contain EvidenceSource values")
        object.__setattr__(self, "sources", sources)


@dataclass(frozen=True)
class CompanyResearchRecord:
    """One dated research cycle for a company."""

    ticker: str
    review_date: str
    dimension_reviews: tuple[CompanyScoreReview, ...]

    def __post_init__(self) -> None:
        if not self.ticker.strip():
            raise ValueError("ticker must not be empty")
        if not self.review_date.strip():
            raise ValueError("review_date must not be empty")
        reviews = tuple(self.dimension_reviews)
        if not reviews:
            raise ValueError("dimension_reviews must not be empty")
        if any(not isinstance(review, CompanyScoreReview) for review in reviews):
            raise ValueError("dimension_reviews must contain CompanyScoreReview values")
        dimensions = [review.dimension.strip().lower() for review in reviews]
        if len(dimensions) != len(set(dimensions)):
            raise ValueError("dimension_reviews must not contain duplicate dimensions")
        if any(review.entity.strip().upper() != self.ticker.strip().upper() for review in reviews):
            raise ValueError("dimension_reviews entities must match ticker")
        if any(review.review_date != self.review_date for review in reviews):
            raise ValueError("dimension_reviews review_date must match record review_date")
        object.__setattr__(self, "dimension_reviews", reviews)

    def company_score(self) -> Score:
        """Return the weighted 0-100 Company Score for this research record."""
        expected = {name.lower() for name in COMPANY_SCORE_WEIGHTS}
        actual = {review.dimension.strip().lower() for review in self.dimension_reviews}
        missing = expected - actual
        extra = actual - expected
        if extra:
            raise ValueError(f"unsupported company score dimensions: {sorted(extra)}")
        if missing:
            raise ValueError(f"missing company score dimensions: {sorted(missing)}")

        scores = {review.dimension.strip().lower(): review.score.value for review in self.dimension_reviews}
        total = Decimal("0")
        for dimension, weight in COMPANY_SCORE_WEIGHTS.items():
            total += Decimal(scores[dimension.lower()]) * Decimal(weight) / Decimal(100)
        value = int(total.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        return Score(value)


@dataclass(frozen=True)
class GovernanceDecision:
    """Documented governance result; does not derive from score thresholds."""

    ticker: str
    review_date: str
    company_score: Score
    portfolio_state: str
    leadership_role: str
    replacement_risk: str
    action: str
    rationale: str
    evidence_summary: str
    approved_by: str

    def __post_init__(self) -> None:
        for name, value in (
            ("ticker", self.ticker),
            ("review_date", self.review_date),
            ("rationale", self.rationale),
            ("evidence_summary", self.evidence_summary),
            ("approved_by", self.approved_by),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        if not isinstance(self.company_score, Score):
            raise ValueError("company_score must be a Score")
        if self.portfolio_state not in PORTFOLIO_STATES:
            raise ValueError(f"unsupported portfolio_state: {self.portfolio_state}")
        if self.leadership_role not in LEADERSHIP_ROLES:
            raise ValueError(f"unsupported leadership_role: {self.leadership_role}")
        if self.replacement_risk not in REPLACEMENT_RISKS:
            raise ValueError(f"unsupported replacement_risk: {self.replacement_risk}")
        if self.action not in GOVERNANCE_ACTIONS:
            raise ValueError(f"unsupported governance action: {self.action}")
        if self.action == "Promote" and self.portfolio_state != "Approved":
            raise ValueError("Promote requires portfolio_state=Approved")
        if self.action == "Replace" and self.portfolio_state != "Approved":
            raise ValueError("Replace requires portfolio_state=Approved")
        if self.action == "Retire" and self.portfolio_state != "Retired":
            raise ValueError("Retire requires portfolio_state=Retired")


@dataclass(frozen=True)
class ApprovedCompany:
    """Supernova approved company with separate portfolio and leadership roles."""

    ticker: str
    theme: str
    company_score: Score
    replacement_risk: str
    trend: str
    leadership_role: str = "Leader"
    portfolio_state: str = "Approved"

    def __post_init__(self) -> None:
        for name, value in (("ticker", self.ticker), ("theme", self.theme), ("replacement_risk", self.replacement_risk), ("trend", self.trend), ("leadership_role", self.leadership_role), ("portfolio_state", self.portfolio_state)):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        if self.replacement_risk not in REPLACEMENT_RISKS | {PLACEHOLDER_REPLACEMENT_RISK}:
            raise ValueError(f"unsupported replacement_risk: {self.replacement_risk}")
        if self.leadership_role not in LEADERSHIP_ROLES:
            raise ValueError(f"unsupported leadership_role: {self.leadership_role}")
        if self.portfolio_state not in PORTFOLIO_STATES:
            raise ValueError(f"unsupported portfolio_state: {self.portfolio_state}")
        if self.portfolio_state == "Approved" and self.leadership_role not in {"Leader", "Challenger"}:
            raise ValueError("Approved companies must have Leader or Challenger leadership_role")


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

        approved = tuple(self.approved_companies)
        watchlist = tuple(self.watchlist)
        if any(not isinstance(item, ApprovedCompany) for item in approved):
            raise ValueError("approved_companies must contain ApprovedCompany values")
        if any(not isinstance(item, CandidateCompany) for item in watchlist):
            raise ValueError("watchlist must contain CandidateCompany values")
        object.__setattr__(self, "approved_companies", approved)
        object.__setattr__(self, "watchlist", watchlist)
