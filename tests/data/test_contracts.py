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


def test_provider_neutral_adapter_normalizes_complete_fake_provider_batch() -> None:
    from data import ProviderNeutralMarketDataAdapter

    class FakeSource:
        def fetch(self) -> dict[str, object]:
            return {
                "as_of": " 2026-10-09 ",
                "observations": [
                    {
                        "symbol": " VTI ",
                        "field": " adjusted_close ",
                        "observed_at": " 2026-10-08 ",
                        "value": 300.5,
                        "source": " fake-provider ",
                        "currency": " USD ",
                        "metadata": {"provider_field": "adjclose", "fixture": "true"},
                    },
                    {
                        "symbol": " VEU ",
                        "field": " adjusted_close ",
                        "observed_at": " 2026-10-08 ",
                        "value": 70.25,
                        "source": " fake-provider ",
                    },
                ],
            }

    dataset = ProviderNeutralMarketDataAdapter(FakeSource()).load()
    assert dataset.as_of == "2026-10-09"
    assert [item.symbol for item in dataset.observations] == ["VTI", "VEU"]
    assert dataset.observations[0].field == "adjusted_close"
    assert dataset.observations[0].metadata["provider_field"] == "adjclose"
    assert dataset.observations[1].currency is None


def test_provider_neutral_adapter_propagates_source_failure_without_partial_dataset() -> None:
    from data import ProviderNeutralMarketDataAdapter

    class FailingSource:
        def fetch(self) -> dict[str, object]:
            raise RuntimeError("fixture source unavailable")

    with pytest.raises(RuntimeError, match="fixture source unavailable"):
        ProviderNeutralMarketDataAdapter(FailingSource()).load()


@pytest.mark.parametrize(
    "batch, message",
    [
        (None, "provider batch must be a mapping"),
        ({"observations": []}, "must include as_of"),
        ({"as_of": "2026-10-09"}, "must include observations"),
        ({"as_of": "2026-10-09", "observations": "not-a-list"}, "iterable of mappings"),
        ({"as_of": "2026-10-09", "observations": [{"symbol": "VTI"}]}, "field"),
    ],
)
def test_provider_neutral_adapter_rejects_malformed_batch(batch: object, message: str) -> None:
    from data import ProviderNeutralMarketDataAdapter

    class FakeSource:
        def fetch(self) -> object:
            return batch

    with pytest.raises(ValueError, match=message):
        ProviderNeutralMarketDataAdapter(FakeSource()).load()  # type: ignore[arg-type]


def test_provider_neutral_adapter_rejects_duplicate_observations_fail_closed() -> None:
    from data import ProviderNeutralMarketDataAdapter

    point = {
        "symbol": "VTI",
        "field": "adjusted_close",
        "observed_at": "2026-10-08",
        "value": 300.5,
        "source": "fake-provider",
    }

    class FakeSource:
        def fetch(self) -> dict[str, object]:
            return {"as_of": "2026-10-09", "observations": [point, point.copy()]}

    with pytest.raises(ValueError, match="duplicate"):
        ProviderNeutralMarketDataAdapter(FakeSource()).load()
