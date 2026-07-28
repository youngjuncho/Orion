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
