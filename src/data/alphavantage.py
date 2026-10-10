"""Alpha Vantage monthly adjusted-price provider for personal ADM research.

The provider maps the documented monthly adjusted-close field into Orion's
canonical market-data contract. It does not calculate or authorize an ADM
signal, and it intentionally performs no retries, caching, or persistence.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from math import isfinite
from typing import Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .adapters import ProviderNeutralMarketDataAdapter
from .contracts import MarketDataSet


class AlphaVantageProviderError(RuntimeError):
    """A sanitized provider or response-contract failure."""


def _http_get(url: str, timeout_seconds: float) -> bytes:
    request = Request(url, headers={"User-Agent": "Orion-ADM/1.0"})
    with urlopen(request, timeout=timeout_seconds) as response:
        return response.read()


class AlphaVantageMonthlyAdjustedSource:
    """Fetch monthly adjusted closes for VTI, VEU, and SGOV.

    The API key is read from ``ORION_ALPHA_VANTAGE_API_KEY`` unless supplied
    explicitly. The monthly endpoint returns the last trading day of each
    month and avoids the premium daily-adjusted endpoint for this monthly
    strategy. A network request is made only when ``fetch`` is called.
    """

    endpoint = "https://www.alphavantage.co/query"
    source_id = "alpha_vantage"
    symbols = ("VTI", "VEU", "SGOV")
    provider_field = "5. adjusted close"

    def __init__(
        self,
        api_key: str | None = None,
        *,
        timeout_seconds: float = 15.0,
        transport: Callable[[str, float], bytes] | None = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("ORION_ALPHA_VANTAGE_API_KEY")
        if not isinstance(resolved_key, str) or not resolved_key.strip():
            raise ValueError("ORION_ALPHA_VANTAGE_API_KEY is required")
        if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)) or timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if transport is not None and not callable(transport):
            raise ValueError("transport must be callable")
        self._api_key = resolved_key.strip()
        self._timeout_seconds = float(timeout_seconds)
        self._transport = transport or _http_get

    def fetch(self) -> Mapping[str, object]:
        """Return one complete canonical-shaped raw batch or fail closed."""

        retrieved_at = datetime.now(timezone.utc).isoformat()
        observations: list[dict[str, object]] = []
        for symbol in self.symbols:
            query = urlencode(
                {
                    "function": "TIME_SERIES_MONTHLY_ADJUSTED",
                    "symbol": symbol,
                    "apikey": self._api_key,
                }
            )
            url = f"{self.endpoint}?{query}"
            try:
                payload = self._transport(url, self._timeout_seconds)
            except HTTPError as exc:
                raise AlphaVantageProviderError(
                    f"Alpha Vantage HTTP request failed (status {exc.code})"
                ) from None
            except (URLError, TimeoutError, OSError):
                raise AlphaVantageProviderError("Alpha Vantage request failed") from None
            except Exception:
                # Avoid leaking the credential-bearing URL from transport errors.
                raise AlphaVantageProviderError("Alpha Vantage request failed") from None

            try:
                response = json.loads(payload)
            except (TypeError, UnicodeDecodeError, json.JSONDecodeError):
                raise AlphaVantageProviderError("Alpha Vantage returned invalid JSON") from None
            if not isinstance(response, Mapping):
                raise AlphaVantageProviderError("Alpha Vantage response must be an object")
            if any(key in response for key in ("Error Message", "Note", "Information")):
                raise AlphaVantageProviderError(
                    "Alpha Vantage rejected the request or returned a notice; no partial batch was accepted"
                )

            metadata = response.get("Meta Data")
            if not isinstance(metadata, Mapping) or metadata.get("2. Symbol") != symbol:
                raise AlphaVantageProviderError(
                    f"Alpha Vantage returned unexpected instrument identity for {symbol}"
                )
            series_keys = [
                key for key in response
                if isinstance(key, str) and key.startswith("Monthly Adjusted Time Series")
            ]
            if len(series_keys) != 1 or not isinstance(response[series_keys[0]], Mapping):
                raise AlphaVantageProviderError(
                    f"Alpha Vantage monthly adjusted series is missing for {symbol}"
                )

            series = response[series_keys[0]]
            symbol_observations = 0
            for observed_at, row in series.items():
                if not isinstance(observed_at, str) or not isinstance(row, Mapping):
                    raise AlphaVantageProviderError(
                        f"Alpha Vantage returned a malformed monthly row for {symbol}"
                    )
                try:
                    if datetime.strptime(observed_at, "%Y-%m-%d").date().isoformat() != observed_at:
                        raise ValueError
                    price = float(row[self.provider_field])
                except (KeyError, TypeError, ValueError, OverflowError):
                    raise AlphaVantageProviderError(
                        f"Alpha Vantage returned an invalid adjusted close for {symbol}"
                    ) from None
                if not isfinite(price) or price <= 0:
                    raise AlphaVantageProviderError(
                        f"Alpha Vantage returned a non-positive adjusted close for {symbol}"
                    )
                observations.append(
                    {
                        "symbol": symbol,
                        "field": "adjusted_close",
                        "observed_at": observed_at,
                        "value": price,
                        "source": self.source_id,
                        "currency": "USD",
                        "metadata": {
                            "provider_symbol": symbol,
                            "provider_function": "TIME_SERIES_MONTHLY_ADJUSTED",
                            "provider_field": self.provider_field,
                            "adjustment_basis": "provider-adjusted; splits and cash dividends",
                            "retrieved_at": retrieved_at,
                        },
                    }
                )
                symbol_observations += 1
            if symbol_observations < 13:
                raise AlphaVantageProviderError(
                    f"Alpha Vantage history is insufficient for a trailing-12-month return ({symbol})"
                )

        return {
            "as_of": retrieved_at[:10],
            "observations": observations,
        }


class AlphaVantageMonthlyAdjustedProvider:
    """Canonical ``MarketDataProvider`` backed by monthly adjusted prices."""

    def __init__(self, source: AlphaVantageMonthlyAdjustedSource) -> None:
        if not isinstance(source, AlphaVantageMonthlyAdjustedSource):
            raise ValueError("source must be AlphaVantageMonthlyAdjustedSource")
        self._adapter = ProviderNeutralMarketDataAdapter(source)

    def load(self) -> MarketDataSet:
        """Fetch and normalize all three complete histories."""

        return self._adapter.load()
