"""Acceptance tests for the provider-neutral adapter boundary.

These tests verify explicit mapping and fail-closed behavior. They do not
approve a live provider or claim provider-specific semantic validation.
"""

import pytest

from data import ProviderNeutralMarketDataAdapter


def _point(
    *,
    symbol: str = "VTI",
    field: str = "adjusted_close",
    observed_at: str = "2026-10-08",
    value: float = 100.0,
    source: str = "fixture-provider",
    metadata: dict[str, str] | None = None,
) -> dict[str, object]:
    return {
        "symbol": symbol,
        "field": field,
        "observed_at": observed_at,
        "value": value,
        "source": source,
        "metadata": metadata or {},
    }


class FixtureSource:
    def __init__(self, batch: object) -> None:
        self.batch = batch

    def fetch(self) -> object:
        return self.batch


def _adapter(batch: object) -> ProviderNeutralMarketDataAdapter:
    return ProviderNeutralMarketDataAdapter(FixtureSource(batch))  # type: ignore[arg-type]


def test_acceptance_explicit_field_mapping_never_substitutes_close_for_adjusted_close() -> None:
    dataset = _adapter(
        {"as_of": "2026-10-09", "observations": [_point(field="close")]}
    ).load()

    assert dataset.observations[0].field == "close"
    from orion.frameworks.moon.adm_data import calculate_adm_asset_return

    with pytest.raises(ValueError, match="missing observation"):
        calculate_adm_asset_return(
            dataset,
            symbol="VTI",
            field="adjusted_close",
            current_observed_at="2026-10-08",
            trailing_observed_at="2025-10-08",
        )


def test_acceptance_timestamp_is_preserved_as_opaque_source_value() -> None:
    timestamp = "2026-10-08T16:00:00-04:00"
    dataset = _adapter(
        {"as_of": "retrieved-at-source", "observations": [_point(observed_at=timestamp)]}
    ).load()

    assert dataset.observations[0].observed_at == timestamp
    assert dataset.as_of == "retrieved-at-source"


def test_acceptance_missing_required_moon_asset_blocks_relative_momentum_calculation() -> None:
    dataset = _adapter(
        {
            "as_of": "2026-10-09",
            "observations": [
                _point(symbol="VTI", observed_at="2025-10-08", value=80.0),
                _point(symbol="VTI", observed_at="2026-10-08", value=100.0),
            ],
        }
    ).load()

    from orion.frameworks.moon.adm_data import calculate_adm_relative_momentum

    with pytest.raises(ValueError, match="VEU"):
        calculate_adm_relative_momentum(
            dataset,
            field="adjusted_close",
            current_target_date="2026-10-08",
            trailing_target_date="2025-10-08",
        )


def test_acceptance_duplicate_revision_for_same_canonical_identity_fails_closed() -> None:
    original = _point(metadata={"revision_id": "r1"})
    revised = _point(value=101.0, metadata={"revision_id": "r2"})

    with pytest.raises(ValueError, match="duplicate"):
        _adapter(
            {"as_of": "2026-10-09", "observations": [original, revised]}
        ).load()


def test_acceptance_provenance_is_preserved_without_fabricating_missing_fields() -> None:
    point = _point(
        metadata={
            "provider_field": "adjclose",
            "retrieved_at": "2026-10-09T00:00:00Z",
            "adapter_version": "fixture-1",
            "revision_id": "snapshot-7",
        }
    )
    dataset = _adapter({"as_of": "2026-10-09", "observations": [point]}).load()

    normalized = dataset.observations[0]
    assert normalized.source == "fixture-provider"
    assert dict(normalized.metadata) == point["metadata"]
    assert "timezone" not in normalized.metadata


def test_acceptance_source_failure_cannot_reach_downstream_signal_consumer() -> None:
    class FailingSource:
        def fetch(self) -> object:
            raise RuntimeError("source unavailable")

    downstream_calls: list[str] = []

    def consume_for_signal_generation(dataset: object) -> None:
        downstream_calls.append("called")

    with pytest.raises(RuntimeError, match="source unavailable"):
        dataset = ProviderNeutralMarketDataAdapter(FailingSource()).load()
        consume_for_signal_generation(dataset)

    assert downstream_calls == []
