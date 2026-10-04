import pytest

from orion.core import DashboardCard, DecisionRecord, Regime, ReviewRecord, Score, ScoreBand, State


def test_score_band_mapping() -> None:
    assert Score(95).band == ScoreBand.EXCEPTIONAL
    assert Score(82).band == ScoreBand.STRONG
    assert Score(71).band == ScoreBand.HEALTHY
    assert Score(62).band == ScoreBand.STABLE
    assert Score(55).band == ScoreBand.NEUTRAL
    assert Score(42).band == ScoreBand.WEAK
    assert Score(31).band == ScoreBand.DANGER
    assert Score(0).band == ScoreBand.CRITICAL


def test_score_rejects_out_of_range_value() -> None:
    with pytest.raises(ValueError):
        Score(-1)


@pytest.mark.parametrize("value", [True, 1.5])
def test_score_rejects_non_integer_values(value: object) -> None:
    with pytest.raises(ValueError, match="integer"):
        Score(value)  # type: ignore[arg-type]


def test_core_models_are_immutable() -> None:
    card = DashboardCard(
        entity_name="Aurora",
        score=Score(76),
        state=State("Risk On"),
        trend="Stable",
        last_updated="2026-07-26",
    )

    with pytest.raises(Exception):
        card.trend = "Improving"  # type: ignore[misc]


def test_review_and_decision_records_shape() -> None:
    review = ReviewRecord("2026-07-26", "Moon", "ADM", "Monthly", "Approved")
    decision = DecisionRecord("D-999", "2026-07-26", "Approved", "Core", "Title", "Desc")

    assert review.framework == "Moon"
    assert decision.decision_id == "D-999"


def test_regime_uses_score_confidence() -> None:
    regime = Regime("Risk On", "Improving", Score(88))

    assert regime.confidence.band == ScoreBand.STRONG


def test_core_models_reject_missing_required_text_and_wrong_nested_types() -> None:
    with pytest.raises(ValueError, match="name"):
        State("  ")
    with pytest.raises(ValueError, match="confidence"):
        Regime("Risk On", "Improving", "high")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="score"):
        DashboardCard("Aurora", 70, State("Risk On"), "Stable", "today")  # type: ignore[arg-type]
