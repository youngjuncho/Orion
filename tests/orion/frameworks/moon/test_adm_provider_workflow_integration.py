"""Fixture-only integration of the concrete provider and isolated ADM workflow."""

from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse

import pytest

from data.alphavantage import (
    AlphaVantageMonthlyAdjustedProvider,
    AlphaVantageMonthlyAdjustedSource,
    AlphaVantageProviderError,
)
from orion.frameworks.moon.adm_workflow import run_adm_data_workflow


MONTH_ENDS = (
    "2025-09-30",
    "2025-10-31",
    "2025-11-28",
    "2025-12-31",
    "2026-01-30",
    "2026-02-27",
    "2026-03-31",
    "2026-04-30",
    "2026-05-29",
    "2026-06-30",
    "2026-07-31",
    "2026-08-31",
    "2026-09-30",
)


def response_for(symbol: str) -> bytes:
    # Synthetic provider-shaped fixture; values are not market observations.
    base = {"VTI": 100.0, "VEU": 100.0, "SGOV": 100.0}[symbol]
    increment = {"VTI": 2.0, "VEU": 1.0, "SGOV": 0.25}[symbol]
    return json.dumps(
        {
            "Meta Data": {"2. Symbol": symbol},
            "Monthly Adjusted Time Series": {
                observed_at: {
                    "5. adjusted close": str(base + index * increment),
                    "7. dividend amount": "0.25",
                }
                for index, observed_at in enumerate(MONTH_ENDS)
            },
        }
    ).encode("utf-8")


def test_concrete_provider_output_runs_through_adm_workflow_in_memory() -> None:
    requested_symbols: list[str] = []

    def transport(url: str, timeout: float) -> bytes:
        query = parse_qs(urlparse(url).query)
        assert timeout == 2.0
        assert query["function"] == ["TIME_SERIES_MONTHLY_ADJUSTED"]
        assert query["apikey"] == ["fixture-key"]
        symbol = query["symbol"][0]
        requested_symbols.append(symbol)
        return response_for(symbol)

    provider = AlphaVantageMonthlyAdjustedProvider(
        AlphaVantageMonthlyAdjustedSource(
            "fixture-key", timeout_seconds=2.0, transport=transport
        )
    )

    result = run_adm_data_workflow(provider)

    assert requested_symbols == ["VTI", "VEU", "SGOV"]
    assert len(result.dataset.observations) == 39
    assert {point.source for point in result.dataset.observations} == {"alpha_vantage"}
    assert result.assessment.targets.current_target_date == "2026-09-30"
    assert result.assessment.selected_risk_asset == "VTI"
    assert result.assessment.signal_assembly_ready is False
    assert not hasattr(result, "signal")


def test_provider_failure_prevents_workflow_result() -> None:
    requested_symbols: list[str] = []

    def transport(url: str, timeout: float) -> bytes:
        symbol = parse_qs(urlparse(url).query)["symbol"][0]
        requested_symbols.append(symbol)
        if symbol == "SGOV":
            response = json.loads(response_for(symbol))
            response["Monthly Adjusted Time Series"] = {
                "2026-09-30": {"5. adjusted close": "100.0"}
            }
            return json.dumps(response).encode("utf-8")
        return response_for(symbol)

    provider = AlphaVantageMonthlyAdjustedProvider(
        AlphaVantageMonthlyAdjustedSource("fixture-key", transport=transport)
    )

    with pytest.raises(AlphaVantageProviderError, match="insufficient"):
        run_adm_data_workflow(provider)

    assert requested_symbols == ["VTI", "VEU", "SGOV"]
