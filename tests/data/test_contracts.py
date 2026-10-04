import pytest

from data import MarketDataPoint, MarketDataSet


def test_market_data_point_preserves_normalized_observation() -> None:
    point = MarketDataPoint(
        symbol="SPY",
        field="close",
        observed_at="2026-07-31",
        value=632.10,
        source="example-source",
        currency="USD",
        metadata={"frequency": "daily"},
    )

    assert point.identity == ("SPY", "close", "2026-07-31")
    assert point.metadata["frequency"] == "daily"


def test_market_data_point_rejects_empty_required_fields() -> None:
    with pytest.raises(ValueError, match="symbol"):
        MarketDataPoint("", "close", "2026-07-31", 1.0, "source")


def test_market_data_point_rejects_non_finite_float() -> None:
    with pytest.raises(ValueError, match="finite"):
        MarketDataPoint("SPY", "close", "2026-07-31", float("nan"), "source")


@pytest.mark.parametrize("value", [True, [], {}])
def test_market_data_point_rejects_unsupported_value_types(value: object) -> None:
    with pytest.raises(ValueError, match="value"):
        MarketDataPoint("SPY", "close", "2026-07-31", value, "source")  # type: ignore[arg-type]


def test_market_data_point_rejects_non_string_metadata() -> None:
    with pytest.raises(ValueError, match="metadata keys and values"):
        MarketDataPoint(
            "SPY",
            "close",
            "2026-07-31",
            1.0,
            "source",
            metadata={"frequency": 1},  # type: ignore[dict-item]
        )


def test_market_data_set_rejects_duplicate_observations() -> None:
    point = MarketDataPoint("SPY", "close", "2026-07-31", 1.0, "source")

    with pytest.raises(ValueError, match="duplicate"):
        MarketDataSet((point, point), "2026-07-31")


def test_market_data_set_snapshots_observations_and_rejects_invalid_members() -> None:
    point = MarketDataPoint("SPY", "close", "2026-07-31", 1.0, "source")
    observations = [point]
    dataset = MarketDataSet(observations, "2026-07-31")
    observations.clear()

    assert dataset.observations == (point,)
    with pytest.raises(ValueError, match="MarketDataPoint"):
        MarketDataSet(["not-an-observation"], "2026-07-31")  # type: ignore[arg-type]
