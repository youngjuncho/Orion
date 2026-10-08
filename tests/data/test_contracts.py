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


def test_market_data_provider_contract_returns_canonical_dataset() -> None:
    class Provider:
        def load(self) -> MarketDataSet:
            return MarketDataSet(
                (MarketDataPoint("SPY", "close", "2026-10-08", 1.0, "test"),),
                "2026-10-08",
            )

    from data import MarketDataProvider

    provider: MarketDataProvider = Provider()
    assert provider.load().as_of == "2026-10-08"


def test_normalize_observation_trims_source_text() -> None:
    from data import normalize_observation

    point = normalize_observation(
        {
            "symbol": " SPY ",
            "field": " close ",
            "observed_at": " 2026-10-08 ",
            "value": 1.0,
            "source": " example-source ",
            "currency": " USD ",
        }
    )

    assert point.symbol == "SPY"
    assert point.field == "close"
    assert point.observed_at == "2026-10-08"
    assert point.source == "example-source"
    assert point.currency == "USD"


def test_normalize_observation_rejects_non_mapping() -> None:
    from data import normalize_observation

    with pytest.raises(ValueError, match="mapping"):
        normalize_observation([])  # type: ignore[arg-type]


def test_normalize_observation_normalizes_missing_currency() -> None:
    from data import normalize_observation

    point = normalize_observation(
        {
            "symbol": "BTC",
            "field": "close",
            "observed_at": "2026-10-08",
            "value": 100.0,
            "source": "test",
        }
    )

    assert point.currency is None


def test_normalize_dataset_builds_canonical_batch() -> None:
    from data import normalize_dataset

    dataset = normalize_dataset(
        [
            {
                "symbol": "SPY",
                "field": "close",
                "observed_at": "2026-10-08",
                "value": 1.0,
                "source": "test",
            },
            {
                "symbol": "QQQM",
                "field": "close",
                "observed_at": "2026-10-08",
                "value": 2.0,
                "source": "test",
            },
        ],
        as_of=" 2026-10-08 ",
    )

    assert dataset.as_of == "2026-10-08"
    assert len(dataset.observations) == 2


def test_normalize_dataset_reuses_duplicate_validation() -> None:
    from data import normalize_dataset

    observations = [
        {
            "symbol": "SPY",
            "field": "close",
            "observed_at": "2026-10-08",
            "value": 1.0,
            "source": "test",
        },
        {
            "symbol": "SPY",
            "field": "close",
            "observed_at": "2026-10-08",
            "value": 2.0,
            "source": "test",
        },
    ]

    with pytest.raises(ValueError, match="duplicate"):
        normalize_dataset(observations, as_of="2026-10-08")


def test_validate_dataset_preserves_canonical_identity() -> None:
    from data import validate_dataset

    dataset = MarketDataSet(
        (MarketDataPoint("SPY", "close", "2026-10-08", 1.0, "test"),),
        "2026-10-08",
    )

    assert validate_dataset(dataset) is dataset
