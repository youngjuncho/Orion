import pytest

from orion.core import Score
from orion.frameworks.phoenix import CandidateAsset, Challenger, Category, Leader, PhoenixEngine, PhoenixReport


def test_phoenix_model_shapes() -> None:
    category = Category("Smart Contract Platforms", Score(81), "Competitive", "Stable")
    leader = Leader("SOL", "Smart Contract Platforms", "Low", "Stable", Score(92))
    challenger = Challenger("SUI", "Smart Contract Platforms", Score(78), 14)
    asset = CandidateAsset("SOL", "Solana", "Smart Contract Platforms", Score(92), "Approved")
    report = PhoenixReport(
        categories=(category,),
        current_leaders=(leader,),
        challengers=(challenger,),
        phoenix_score=Score(74),
        replacement_risk="Low",
    )

    assert category.score.band.value == "strong"
    assert asset.name == "Solana"
    assert report.current_leaders[0].asset == "SOL"


def test_phoenix_engine_build_report() -> None:
    report = PhoenixEngine().build_report()

    assert report.phoenix_score.value == 0
    assert len(report.categories) == 5


def test_phoenix_models_reject_empty_required_values() -> None:
    with pytest.raises(ValueError, match="asset"):
        Leader("", "Smart Contracts", "Low", "Stable", Score(70))


def test_phoenix_report_snapshots_framework_collections() -> None:
    categories = [Category("Smart Contracts", Score(80), "Competitive", "Stable")]
    leaders = [Leader("SOL", "Smart Contracts", "Low", "Stable", Score(90))]
    challengers = [Challenger("SUI", "Smart Contracts", Score(75), 15)]
    report = PhoenixReport(categories, leaders, challengers, Score(80), "Low")
    categories.clear()
    leaders.clear()
    challengers.clear()

    assert len(report.categories) == len(report.current_leaders) == 1
    assert len(report.challengers) == 1
    assert isinstance(report.categories, tuple)
    with pytest.raises(ValueError, match="Category"):
        PhoenixReport(("bad",), (), (), Score(0), "Low")
