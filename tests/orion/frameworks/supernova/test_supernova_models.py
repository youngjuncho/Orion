import pytest

from orion.core import Score
from orion.frameworks.supernova import ApprovedCompany, CandidateCompany, SupernovaEngine, SupernovaReport, Theme


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
