"""Fixture-only contract tests for the Alpha Vantage market-data provider."""

from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse

import pytest

from data.alphavantage import (
    AlphaVantageMonthlyAdjustedProvider,
    AlphaVantageMonthlyAdjustedSource,
    AlphaVantageProviderError,
)


def provider_response(symbol: str) -> bytes:
    dates = [
        "2025-09-30", "2025-10-31", "2025-11-28", "2025-12-31",
        "2026-01-30", "2026-02-27", "2026-03-31", "2026-04-30",
        "2026-05-29", "2026-06-30", "2026-07-31", "2026-08-31",
        "2026-09-30",
    ]
    return json.dumps(
        {
            "Meta Data": {"2. Symbol": symbol},
            "Monthly Adjusted Time Series": {
                observed_at: {
                    "5. adjusted close": str(100 + i),
                    "7. dividend amount": "0.50",
                }
                for i, observed_at in enumerate(dates)
            },
        }
    ).encode("utf-8")


def test_monthly_adjusted_provider_returns_canonical_all_symbol_batch() -> None:
    requested: list[str] = []

    def transport(url: str, timeout: float) -> bytes:
        assert timeout == 3.0
        query = parse_qs(urlparse(url).query)
        assert query["function"] == ["TIME_SERIES_MONTHLY_ADJUSTED"]
        assert query["apikey"] == ["test-secret"]
        symbol = query["symbol"][0]
        requested.append(symbol)
        return provider_response(symbol)

    provider = AlphaVantageMonthlyAdjustedProvider(
        AlphaVantageMonthlyAdjustedSource(
            "test-secret", timeout_seconds=3, transport=transport
        )
    )

    dataset = provider.load()

    assert requested == ["VTI", "VEU", "SGOV"]
    assert len(dataset.observations) == 39
    assert {point.symbol for point in dataset.observations} == {"VTI", "VEU", "SGOV"}
    assert {point.field for point in dataset.observations} == {"adjusted_close"}
    assert {point.source for point in dataset.observations} == {"alpha_vantage"}
    assert dataset.observations[0].value == 100.0
    assert all(point.currency == "USD" for point in dataset.observations)
    assert all(
        point.metadata["provider_function"] == "TIME_SERIES_MONTHLY_ADJUSTED"
        for point in dataset.observations
    )
    assert all("retrieved_at" in point.metadata for point in dataset.observations)


def test_provider_fails_closed_when_one_symbol_is_missing_history() -> None:
    def transport(url: str, timeout: float) -> bytes:
        symbol = parse_qs(urlparse(url).query)["symbol"][0]
        response = json.loads(provider_response(symbol))
        if symbol == "SGOV":
            response["Monthly Adjusted Time Series"] = {
                "2026-08-31": {"5. adjusted close": "100.0"}
            }
        return json.dumps(response).encode("utf-8")

    provider = AlphaVantageMonthlyAdjustedProvider(
        AlphaVantageMonthlyAdjustedSource("test-secret", transport=transport)
    )
    with pytest.raises(AlphaVantageProviderError, match="insufficient"):
        provider.load()


def test_provider_rejects_duplicate_month_keys_in_one_response() -> None:
    def transport(url: str, timeout: float) -> bytes:
        symbol = parse_qs(urlparse(url).query)["symbol"][0]
        return (
            '{"Meta Data":{"2. Symbol":"' + symbol + '"},'
            '"Monthly Adjusted Time Series":{'
            '"2026-09-30":{"5. adjusted close":"110"},'
            '"2026-09-30":{"5. adjusted close":"111"}}}'
        ).encode("utf-8")

    provider = AlphaVantageMonthlyAdjustedProvider(
        AlphaVantageMonthlyAdjustedSource("test-secret", transport=transport)
    )
    with pytest.raises(AlphaVantageProviderError, match="duplicate JSON key"):
        provider.load()


def test_provider_does_not_expose_api_key_in_transport_error() -> None:
    def transport(url: str, timeout: float) -> bytes:
        raise RuntimeError(url)

    source = AlphaVantageMonthlyAdjustedSource(
        "never-print-this-key", transport=transport
    )
    with pytest.raises(AlphaVantageProviderError) as error:
        source.fetch()
    assert "never-print-this-key" not in str(error.value)


def test_provider_requires_configured_api_key() -> None:
    with pytest.raises(ValueError, match="ORION_ALPHA_VANTAGE_API_KEY"):
        AlphaVantageMonthlyAdjustedSource(api_key="")


@pytest.mark.parametrize(
    "timeout_seconds",
    [0, -1, float("nan"), float("inf"), float("-inf"), True, 10**1000],
)
def test_provider_rejects_non_finite_or_non_positive_timeout(
    timeout_seconds: object,
) -> None:
    with pytest.raises(ValueError, match="finite positive"):
        AlphaVantageMonthlyAdjustedSource("test-secret", timeout_seconds=timeout_seconds)


@pytest.mark.parametrize(
    ("provider_notice", "expected_code"),
    [
        (
            {"Error Message": "Invalid API call."},
            "API_KEY_OR_REQUEST_NOTICE",
        ),
        (
            {"Note": "API call frequency exceeded."},
            "API_RATE_LIMIT",
        ),
        (
            {
                "Information":
                    "This endpoint requires a premium subscription."
            },
            "API_PREMIUM_OR_PLAN_NOTICE",
        ),
        (
            {"Information": "Invalid API key"},
            "API_KEY_OR_REQUEST_NOTICE",
        ),
        (
            {"Information": "Thank you for using Alpha Vantage."},
            "API_INFORMATION_NOTICE",
        ),
    ],
)
def test_provider_rejects_documented_notice_payloads_without_partial_batch(
    provider_notice: dict[str, str],
    expected_code: str,
) -> None:
    def transport(url: str, timeout: float) -> bytes:
        return json.dumps(provider_notice).encode("utf-8")

    provider = AlphaVantageMonthlyAdjustedProvider(
        AlphaVantageMonthlyAdjustedSource(
            "test-secret",
            transport=transport,
        )
    )

    with pytest.raises(AlphaVantageProviderError, match="notice") as error:
        provider.load()

    error_message = str(error.value)
    assert expected_code in error_message
    assert "test-secret" not in error_message
    assert "no partial batch was accepted" in error_message

    raw_notice = next(iter(provider_notice.values()))
    assert raw_notice not in error_message

def test_provider_rejects_response_for_different_symbol() -> None:
    def transport(url: str, timeout: float) -> bytes:
        requested = parse_qs(urlparse(url).query)["symbol"][0]
        wrong = "VEU" if requested == "VTI" else requested
        return provider_response(wrong)

    provider = AlphaVantageMonthlyAdjustedProvider(
        AlphaVantageMonthlyAdjustedSource("test-secret", transport=transport)
    )
    with pytest.raises(AlphaVantageProviderError, match="unexpected instrument identity"):
        provider.load()


def test_provider_rejects_non_finite_adjusted_close() -> None:
    def transport(url: str, timeout: float) -> bytes:
        symbol = parse_qs(urlparse(url).query)["symbol"][0]
        response = json.loads(provider_response(symbol))
        first_date = next(iter(response["Monthly Adjusted Time Series"]))
        response["Monthly Adjusted Time Series"][first_date]["5. adjusted close"] = "NaN"
        return json.dumps(response).encode("utf-8")

    provider = AlphaVantageMonthlyAdjustedProvider(
        AlphaVantageMonthlyAdjustedSource("test-secret", transport=transport)
    )
    with pytest.raises(AlphaVantageProviderError, match="non-positive"):
        provider.load()


@pytest.mark.parametrize("malformed_price", [True, False, None, [], {}])
def test_provider_rejects_non_numeric_json_adjusted_close(malformed_price: object) -> None:
    def transport(url: str, timeout: float) -> bytes:
        symbol = parse_qs(urlparse(url).query)["symbol"][0]
        response = json.loads(provider_response(symbol))
        first_date = next(iter(response["Monthly Adjusted Time Series"]))
        response["Monthly Adjusted Time Series"][first_date]["5. adjusted close"] = malformed_price
        return json.dumps(response).encode("utf-8")

    provider = AlphaVantageMonthlyAdjustedProvider(
        AlphaVantageMonthlyAdjustedSource("test-secret", transport=transport)
    )
    with pytest.raises(AlphaVantageProviderError, match="invalid adjusted close"):
        provider.load()


def test_provider_rejects_multiple_bars_in_the_same_calendar_month() -> None:
    def transport(url: str, timeout: float) -> bytes:
        symbol = parse_qs(urlparse(url).query)["symbol"][0]
        response = json.loads(provider_response(symbol))
        series = response["Monthly Adjusted Time Series"]
        # Keep the existing September bar and add a second distinct date in September.
        series["2026-09-29"] = {"5. adjusted close": "111.0"}
        return json.dumps(response).encode("utf-8")

    provider = AlphaVantageMonthlyAdjustedProvider(
        AlphaVantageMonthlyAdjustedSource("test-secret", transport=transport)
    )
    with pytest.raises(AlphaVantageProviderError, match="multiple monthly bars"):
        provider.load()
