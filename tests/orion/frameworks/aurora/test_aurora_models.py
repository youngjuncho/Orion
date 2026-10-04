import pytest

from orion.frameworks.aurora import AuroraEngine, AuroraIndicator, AuroraReport, AuroraRegime
from orion.core import Score


def test_aurora_model_shapes() -> None:
    indicator = AuroraIndicator("SPY Trend", "Trend", 1.0, Score(75), "Approved")
    regime = AuroraRegime("Risk On", Score(82), "Improving", Score(70))
    report = AuroraReport(
        score=Score(61),
        current_regime="Neutral",
        regime_direction="Stable",
        risk_state="Unknown",
        transition_risk="Low",
        indicators=(indicator,),
    )

    assert indicator.score.band.value == "healthy"
    assert regime.confidence.band.value == "healthy"
    assert report.indicators[0].name == "SPY Trend"


def test_aurora_engine_build_report() -> None:
    report = AuroraEngine().build_report()

    assert report.score.value == 0
    assert report.current_regime == "Unknown"


def test_aurora_models_reject_empty_required_fields() -> None:
    with pytest.raises(ValueError, match="name"):
        AuroraIndicator("", "Trend", 1.0, Score(0), "Neutral")


def test_aurora_report_snapshots_indicator_collection() -> None:
    indicators = [AuroraIndicator("Trend", "Trend", 1.0, Score(70), "Neutral")]
    report = AuroraReport(Score(70), "Neutral", "Stable", "Unknown", "Low", indicators)
    indicators.clear()

    assert len(report.indicators) == 1
    assert isinstance(report.indicators, tuple)
    with pytest.raises(ValueError, match="AuroraIndicator"):
        AuroraReport(Score(0), "Unknown", "Stable", "Unknown", "Low", ("bad",))
