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


def _approved_registry_snapshot() -> dict:
    digest = "a" * 64
    record = {
        "record_id": "D049-NVDA-2026-10-05",
        "company_id": "NVDA",
        "decision_ref": "D-049",
        "review_cycle": "2026-10-05",
        "governance_status": "approved",
        "effective_at": "2026-10-05T00:00:00Z",
        "supersedes_record_id": None,
        "decision_payload_digest": digest,
    }
    return {
        "registry_type": "supernova.approved_company_state",
        "schema_version": 1,
        "scope": {"framework": "Supernova", "domain": "approved_company_state", "review_cycle": "2026-10-05"},
        "records": {record["record_id"]: record},
        "source_decision_refs": ["D-049"],
        "snapshot_id": "snap-2026-10-05-001",
        "snapshot_version": 1,
        "generated_at": "2026-10-06T00:00:00Z",
        "authority_ref": "proposal-only-authority",
        "signature": "proposal-only-signature",
        "key_id": "proposal-only-key",
        "signature_algorithm": "proposal-only-algorithm",
        "content_digest": digest,
    }


def test_supernova_approved_company_registry_schema_accepts_explicit_record() -> None:
    from orion.frameworks.supernova.registry_contract import validate_approved_company_snapshot

    result = validate_approved_company_snapshot(_approved_registry_snapshot(), expected_review_cycle="2026-10-05")
    assert result["records"]["D049-NVDA-2026-10-05"]["company_id"] == "NVDA"


@pytest.mark.parametrize("mutate, message", [
    (lambda s: s.update(registry_type="research.candidate_universe"), "registry_type mismatch"),
    (lambda s: s.update(snapshot_version=True), "snapshot_version must be a positive integer"),
    (lambda s: s["scope"].update(review_cycle="other-cycle"), "snapshot review_cycle mismatch"),
    (lambda s: s["records"]["D049-NVDA-2026-10-05"].update(governance_status="candidate"), "only explicit approved records"),
    (lambda s: s["records"]["D049-NVDA-2026-10-05"].update(company_id="nvda"), "canonical uppercase ticker"),
    (lambda s: s["records"]["D049-NVDA-2026-10-05"].update(decision_payload_digest="bad"), "lowercase SHA-256"),
    (lambda s: s["records"]["D049-NVDA-2026-10-05"].update(decision_ref="D-999"), "missing from source_decision_refs"),
    (lambda s: s.update(unrecognized_field="nope"), "unknown envelope fields"),
])
def test_supernova_approved_company_registry_schema_rejects_invalid_snapshot(mutate, message: str) -> None:
    from copy import deepcopy
    from orion.frameworks.supernova.registry_contract import SupernovaRegistryContractError, validate_approved_company_snapshot

    snapshot = deepcopy(_approved_registry_snapshot())
    mutate(snapshot)
    with pytest.raises(SupernovaRegistryContractError, match=message):
        validate_approved_company_snapshot(snapshot, expected_review_cycle="2026-10-05")


def test_supernova_approved_company_registry_rejects_duplicate_company_identity() -> None:
    from copy import deepcopy
    from orion.frameworks.supernova.registry_contract import SupernovaRegistryContractError, validate_approved_company_snapshot

    snapshot = deepcopy(_approved_registry_snapshot())
    record = dict(snapshot["records"]["D049-NVDA-2026-10-05"])
    record.update(record_id="D049-NVDA-duplicate")
    snapshot["records"][record["record_id"]] = record
    with pytest.raises(SupernovaRegistryContractError, match="duplicate company_id"):
        validate_approved_company_snapshot(snapshot, expected_review_cycle="2026-10-05")


def _trusted_supernova_snapshot():
    from data.governance import canonical_snapshot_digest
    snapshot = _approved_registry_snapshot()
    snapshot["content_digest"] = canonical_snapshot_digest(snapshot)
    return snapshot


def test_supernova_trusted_snapshot_composes_authenticity_and_domain_contracts():
    from datetime import datetime, timezone
    from orion.frameworks.supernova.registry_contract import validate_trusted_approved_company_snapshot

    snapshot = _trusted_supernova_snapshot()
    result = validate_trusted_approved_company_snapshot(
        snapshot,
        expected_review_cycle="2026-10-05",
        now=datetime(2026, 10, 6, 0, 1, tzinfo=timezone.utc),
        max_age_seconds=3600,
        trusted_authorities={"proposal-only-authority"},
        signature_verifier=lambda *args: True,
        last_accepted_version=0,
    )
    assert result["records"]["D049-NVDA-2026-10-05"]["company_id"] == "NVDA"


def test_supernova_trusted_snapshot_rejects_rollback_and_untrusted_authority():
    from copy import deepcopy
    from datetime import datetime, timezone
    from data.governance import canonical_snapshot_digest
    from orion.frameworks.supernova.registry_contract import SupernovaRegistryContractError, validate_trusted_approved_company_snapshot

    kwargs = dict(
        expected_review_cycle="2026-10-05",
        now=datetime(2026, 10, 6, 0, 1, tzinfo=timezone.utc),
        max_age_seconds=3600,
        trusted_authorities={"proposal-only-authority"},
        signature_verifier=lambda *args: True,
        last_accepted_version=1,
    )
    with pytest.raises(SupernovaRegistryContractError, match="rollback or replay"):
        validate_trusted_approved_company_snapshot(_trusted_supernova_snapshot(), **kwargs)

    snapshot = deepcopy(_trusted_supernova_snapshot())
    snapshot["authority_ref"] = "untrusted-authority"
    snapshot["content_digest"] = canonical_snapshot_digest(snapshot)
    with pytest.raises(SupernovaRegistryContractError, match="authority is not trusted"):
        validate_trusted_approved_company_snapshot(snapshot, **{**kwargs, "last_accepted_version": 0})


def test_supernova_trusted_snapshot_rejects_invalid_domain_lineage():
    from copy import deepcopy
    from datetime import datetime, timezone
    from data.governance import canonical_snapshot_digest
    from orion.frameworks.supernova.registry_contract import SupernovaRegistryContractError, validate_trusted_approved_company_snapshot

    snapshot = deepcopy(_trusted_supernova_snapshot())
    snapshot["records"]["D049-NVDA-2026-10-05"]["supersedes_record_id"] = "missing-predecessor"
    snapshot["content_digest"] = canonical_snapshot_digest(snapshot)
    with pytest.raises(SupernovaRegistryContractError, match="predecessor missing"):
        validate_trusted_approved_company_snapshot(
            snapshot,
            expected_review_cycle="2026-10-05",
            now=datetime(2026, 10, 6, 0, 1, tzinfo=timezone.utc),
            max_age_seconds=3600,
            trusted_authorities={"proposal-only-authority"},
            signature_verifier=lambda *args: True,
            last_accepted_version=0,
        )
