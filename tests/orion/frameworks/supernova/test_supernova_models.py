import pytest

from orion.core import Score
from orion.frameworks.supernova import (
    ApprovedCompany,
    CandidateCompany,
    CompanyResearchRecord,
    CompanyScoreReview,
    EvidenceSource,
    SupernovaEngine,
    SupernovaReport,
    Theme,
)


def test_supernova_model_shapes() -> None:
    theme = Theme("Digital Transformation", "Active", Score(84), "Established")
    candidate = CandidateCompany("NVDA", "NVIDIA", "Digital Transformation", "Candidate", Score(92))
    approved = ApprovedCompany("NVDA", "Digital Transformation", Score(98), "Low", "Strong")
    report = SupernovaReport(
        approved_companies=(approved,),
        theme_health="Healthy",
        leadership_status="Stable",
        replacement_risk="Low",
        watchlist=(candidate,),
    )

    assert theme.score.band.value == "strong"
    assert candidate.company_name == "NVIDIA"
    assert approved.company_score.value == 98
    assert approved.leadership_role == "Leader"
    assert approved.portfolio_state == "Approved"
    assert report.approved_companies[0].ticker == "NVDA"


def test_supernova_engine_build_report() -> None:
    report = SupernovaEngine().build_report()

    assert len(report.approved_companies) == 5
    assert report.approved_companies[0].ticker == "NVDA"


def test_supernova_models_reject_empty_required_values() -> None:
    with pytest.raises(ValueError, match="ticker"):
        CandidateCompany("", "NVIDIA", "AI", "Approved", Score(80))


def test_supernova_report_snapshots_company_collections() -> None:
    approved = [ApprovedCompany("NVDA", "AI", Score(90), "Low", "Strong")]
    watchlist = [CandidateCompany("AMD", "AMD", "AI", "Candidate", Score(75))]
    report = SupernovaReport(approved, "Healthy", "Stable", "Low", watchlist)
    approved.clear()
    watchlist.clear()

    assert len(report.approved_companies) == 1
    assert len(report.watchlist) == 1
    assert isinstance(report.approved_companies, tuple)
    with pytest.raises(ValueError, match="ApprovedCompany"):
        SupernovaReport(("bad",), "Healthy", "Stable", "Low")


def test_company_score_review_requires_evidence_contract() -> None:
    filing = EvidenceSource(
        source_type="Primary",
        source_name="SEC filing",
        reference="10-Q",
        publication_date="2026-08-01",
        access_date="2026-10-05",
        relevant_period="Q2 2026",
    )
    research = EvidenceSource(
        source_type="Secondary",
        source_name="Industry research",
        reference="Semiconductor industry report",
    )
    review = CompanyScoreReview(
        entity="NVDA",
        dimension="Competitive Moat",
        score=Score(92),
        evidence="Durable ecosystem and switching costs supported by primary disclosures.",
        assessment="Moat remains exceptionally durable.",
        review_date="2026-10-05",
        reviewer="YJ",
        sources=(filing, research),
    )

    assert review.score.band.value == "exceptional"
    assert review.sources == (filing, research)

    record = CompanyResearchRecord("NVDA", "2026-10-05", (review,))
    assert record.ticker == "NVDA"
    assert record.dimension_reviews == (review,)

    with pytest.raises(ValueError, match="evidence"):
        CompanyScoreReview("NVDA", "Competitive Moat", Score(90), "", "Strong", "2026-10-05")
    with pytest.raises(ValueError, match="duplicate dimensions"):
        CompanyResearchRecord("NVDA", "2026-10-05", (review, review))


def test_company_research_record_aggregates_five_dimensions() -> None:
    scores = {
        "Theme Exposure": 90,
        "Competitive Moat": 80,
        "Leadership Position": 95,
        "Growth Quality": 70,
        "Execution Quality": 85,
    }
    reviews = tuple(
        CompanyScoreReview(
            entity="NVDA",
            dimension=dimension,
            score=Score(score),
            evidence="Evidence",
            assessment="Assessment",
            review_date="2026-10-05",
        )
        for dimension, score in scores.items()
    )
    record = CompanyResearchRecord("NVDA", "2026-10-05", reviews)

    assert record.company_score().value == 85


def test_company_research_record_rejects_missing_or_extra_dimensions() -> None:
    base = CompanyScoreReview(
        entity="NVDA",
        dimension="Theme Exposure",
        score=Score(80),
        evidence="Evidence",
        assessment="Assessment",
        review_date="2026-10-05",
    )
    record = CompanyResearchRecord("NVDA", "2026-10-05", (base,))
    with pytest.raises(ValueError, match="missing company score dimensions"):
        record.company_score()

    extra = CompanyScoreReview(
        entity="NVDA",
        dimension="Unsupported",
        score=Score(80),
        evidence="Evidence",
        assessment="Assessment",
        review_date="2026-10-05",
    )
    with pytest.raises(ValueError, match="unsupported company score dimensions"):
        CompanyResearchRecord("NVDA", "2026-10-05", (base, extra)).company_score()


def test_company_research_record_rejects_mismatched_entity_or_date() -> None:
    review = CompanyScoreReview(
        entity="GOOGL",
        dimension="Theme Exposure",
        score=Score(80),
        evidence="Evidence",
        assessment="Assessment",
        review_date="2026-10-05",
    )
    with pytest.raises(ValueError, match="entities must match"):
        CompanyResearchRecord("NVDA", "2026-10-05", (review,))

    review = CompanyScoreReview(
        entity="NVDA",
        dimension="Theme Exposure",
        score=Score(80),
        evidence="Evidence",
        assessment="Assessment",
        review_date="2026-09-30",
    )
    with pytest.raises(ValueError, match="review_date must match"):
        CompanyResearchRecord("NVDA", "2026-10-05", (review,))


def test_governance_decision_keeps_score_and_state_separate() -> None:
    from orion.frameworks.supernova import GovernanceDecision

    decision = GovernanceDecision(
        ticker="NVDA",
        review_date="2026-10-05",
        company_score=Score(85),
        portfolio_state="Approved",
        leadership_role="Leader",
        replacement_risk="Low",
        action="Continue",
        rationale="Evidence supports continued long-term leadership.",
        evidence_summary="Primary filings and industry evidence reviewed.",
        approved_by="YJ",
    )
    assert decision.company_score.value == 85
    assert decision.action == "Continue"


def test_governance_decision_rejects_unsupported_values() -> None:
    from orion.frameworks.supernova import GovernanceDecision

    kwargs = dict(
        ticker="NVDA",
        review_date="2026-10-05",
        company_score=Score(85),
        portfolio_state="Approved",
        leadership_role="Leader",
        replacement_risk="Low",
        action="Continue",
        rationale="Rationale",
        evidence_summary="Evidence",
        approved_by="YJ",
    )
    with pytest.raises(ValueError, match="unsupported leadership_role"):
        GovernanceDecision(**{**kwargs, "leadership_role": "Owner"})
    with pytest.raises(ValueError, match="unsupported replacement_risk"):
        GovernanceDecision(**{**kwargs, "replacement_risk": "Unknown"})


def test_approved_company_validates_governance_dimensions() -> None:
    with pytest.raises(ValueError, match="unsupported replacement_risk"):
        ApprovedCompany("NVDA", "AI", Score(90), "Bogus", "Strong")
    with pytest.raises(ValueError, match="Approved companies must"):
        ApprovedCompany("NVDA", "AI", Score(90), "Low", "Strong", "Candidate", "Approved")
