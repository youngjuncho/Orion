#!/usr/bin/env python3
"""Fetch a reproducible VAA-G12 monthly adjusted-close CSV from Alpha Vantage.

Requires ORION_ALPHA_VANTAGE_API_KEY. Makes one request per unique VAA asset
(14 total), uses the documented monthly adjusted-close field, discards the
current incomplete month, and fails closed on missing or inconsistent data.
The API key, credential-bearing URLs, and raw provider payloads are never logged.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import time
from calendar import monthrange
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OFFENSIVE = ("SPY", "IWM", "QQQ", "VGK", "EWJ", "VWO", "VNQ", "GSG", "GLD", "TLT", "HYG", "LQD")
DEFENSIVE = ("SHY", "IEF", "LQD")
SYMBOLS = tuple(dict.fromkeys(OFFENSIVE + DEFENSIVE))
ENDPOINT = "https://www.alphavantage.co/query"


class FetchError(RuntimeError):
    """Sanitized data acquisition or validation failure."""


def _http_get(url: str, timeout_seconds: float) -> bytes:
    request = Request(url, headers={"User-Agent": "Orion-VAA-Research/1.0"})
    with urlopen(request, timeout=timeout_seconds) as response:
        return response.read()


def _previous_month(as_of: date) -> tuple[int, int]:
    return (as_of.year - 1, 12) if as_of.month == 1 else (as_of.year, as_of.month - 1)


def _month_end(year: int, month: int) -> str:
    return date(year, month, monthrange(year, month)[1]).isoformat()


def _month_key(value: str) -> tuple[int, int]:
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError):
        raise FetchError("provider returned an invalid monthly observation date") from None
    if parsed.isoformat() != value:
        raise FetchError("provider returned a non-canonical observation date")
    return parsed.year, parsed.month


def fetch_monthly_prices(
    api_key: str,
    as_of: date,
    *,
    transport: Callable[[str, float], bytes] = _http_get,
    sleep: Callable[[float], None] = time.sleep,
    min_interval_seconds: float = 13.0,
    timeout_seconds: float = 20.0,
) -> tuple[list[str], dict[str, dict[tuple[int, int], float]], dict[str, str]]:
    """Return month-end labels, per-symbol prices, and source observation dates."""
    if not api_key.strip():
        raise FetchError("ORION_ALPHA_VANTAGE_API_KEY is required")
    if min_interval_seconds < 0 or timeout_seconds <= 0:
        raise FetchError("invalid request timing configuration")

    cutoff = _previous_month(as_of)
    prices: dict[str, dict[tuple[int, int], float]] = {}
    observed_dates: dict[str, str] = {}
    retrieved_at = datetime.now(timezone.utc).isoformat()

    for index, symbol in enumerate(SYMBOLS):
        if index:
            sleep(min_interval_seconds)
        query = urlencode({
            "function": "TIME_SERIES_MONTHLY_ADJUSTED",
            "symbol": symbol,
            "apikey": api_key.strip(),
        })
        try:
            payload = transport(f"{ENDPOINT}?{query}", timeout_seconds)
        except HTTPError as exc:
            raise FetchError(f"provider HTTP request failed (status {exc.code}) for {symbol}") from None
        except (URLError, TimeoutError, OSError):
            raise FetchError(f"provider request failed for {symbol}") from None
        except Exception:
            raise FetchError(f"provider request failed for {symbol}") from None

        try:
            response = json.loads(payload)
        except (TypeError, UnicodeDecodeError, json.JSONDecodeError):
            raise FetchError(f"provider returned invalid JSON for {symbol}") from None
        if not isinstance(response, Mapping):
            raise FetchError(f"provider response shape invalid for {symbol}")
        if any(key in response for key in ("Error Message", "Note", "Information")):
            # Do not echo provider text: it may contain request details or other sensitive content.
            raise FetchError(f"provider rejected or rate-limited the request for {symbol}; no CSV written")
        metadata = response.get("Meta Data")
        series = response.get("Monthly Adjusted Time Series")
        if not isinstance(metadata, Mapping) or metadata.get("2. Symbol") != symbol or not isinstance(series, Mapping):
            raise FetchError(f"provider response missing expected monthly adjusted series for {symbol}")

        symbol_prices: dict[tuple[int, int], float] = {}
        symbol_dates: dict[tuple[int, int], str] = {}
        for observed_at, row in series.items():
            key = _month_key(observed_at)
            if key > cutoff:
                continue  # Current calendar month is not complete.
            if key in symbol_prices:
                raise FetchError(f"multiple monthly observations for {symbol}; no CSV written")
            if not isinstance(row, Mapping):
                raise FetchError(f"malformed monthly observation for {symbol}; no CSV written")
            raw = row.get("5. adjusted close")
            if isinstance(raw, bool):
                raise FetchError(f"invalid adjusted close for {symbol}; no CSV written")
            try:
                value = float(raw)
            except (TypeError, ValueError, OverflowError):
                raise FetchError(f"invalid adjusted close for {symbol}; no CSV written") from None
            if not (value > 0 and value < float("inf")):
                raise FetchError(f"non-positive or non-finite adjusted close for {symbol}; no CSV written")
            symbol_prices[key] = value
            symbol_dates[key] = observed_at
        if cutoff not in symbol_prices:
            raise FetchError(f"last completed month is unavailable for {symbol}; no CSV written")
        prices[symbol] = symbol_prices
        observed_dates[symbol] = symbol_dates[cutoff]

    common_months = set.intersection(*(set(prices[symbol]) for symbol in SYMBOLS))
    months = sorted(month for month in common_months if month <= cutoff)
    if len(months) < 13:
        raise FetchError(f"fewer than 13 aligned completed monthly observations; found {len(months)}")
    # Fail closed if any month between the first retained month and the cutoff is missing.
    for prior, current in zip(months, months[1:]):
        expected = (prior[0] + (prior[1] == 12), 1 if prior[1] == 12 else prior[1] + 1)
        if current != expected:
            raise FetchError("provider data contains a skipped calendar month; no CSV written")
    # Restrict each symbol to the same complete month range.
    aligned = {symbol: {month: prices[symbol][month] for month in months} for symbol in SYMBOLS}
    labels = [_month_end(year, month) for year, month in months]
    return labels, aligned, {
        "provider": "Alpha Vantage",
        "provider_function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "price_field": "5. adjusted close",
        "adjustment_basis": "provider-adjusted close; split and cash-dividend distributions per provider documentation",
        "symbols": list(SYMBOLS),
        "as_of_date": as_of.isoformat(),
        "last_completed_month": f"{cutoff[0]:04d}-{cutoff[1]:02d}",
        "calendar_month_labels": labels,
        "latest_provider_observation_dates": observed_dates,
        "retrieved_at_utc": retrieved_at,
        "data_note": "CSV Date values are calendar-month-end labels; each price is the provider's last available monthly adjusted close for that month.",
        "evidence_boundary": "Provider-backed signal input only; not an independent performance backtest or proof of price accuracy.",
    }


def write_outputs(csv_path: Path, labels: list[str], prices: dict[str, dict[tuple[int, int], float]], manifest: Mapping[str, object]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = csv_path.with_suffix(csv_path.suffix + ".tmp")
    try:
        with temp_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["Date", *OFFENSIVE, "SHY", "IEF"])
            for label in labels:
                key = _month_key(label)
                writer.writerow([label, *(f"{prices[symbol][key]:.10f}" for symbol in (*OFFENSIVE, "SHY", "IEF"))])
        temp_path.replace(csv_path)
        manifest_data = dict(manifest)
        manifest_data["csv_sha256"] = hashlib.sha256(csv_path.read_bytes()).hexdigest()
        manifest_path = csv_path.with_suffix(csv_path.suffix + ".manifest.json")
        manifest_path.write_text(json.dumps(manifest_data, indent=2) + "\n", encoding="utf-8")
    finally:
        if temp_path.exists():
            temp_path.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/vaa_monthly_adjusted_close.csv"))
    parser.add_argument("--as-of-date", type=date.fromisoformat, default=date.today(), help="date used to exclude the current incomplete month (YYYY-MM-DD)")
    parser.add_argument("--min-interval-seconds", type=float, default=13.0, help="delay between requests; default 13s for conservative pacing")
    args = parser.parse_args(argv)
    api_key = os.environ.get("ORION_ALPHA_VANTAGE_API_KEY", "").strip()
    if not api_key:
        print("NOT RUN: ORION_ALPHA_VANTAGE_API_KEY is not configured.")
        return 2
    try:
        labels, prices, manifest = fetch_monthly_prices(
            api_key, args.as_of_date, min_interval_seconds=args.min_interval_seconds
        )
        write_outputs(args.output, labels, prices, manifest)
    except FetchError as exc:
        print(f"VAA PRICE FETCH FAILED: {exc}")
        return 1
    except Exception:
        print("VAA PRICE FETCH FAILED: unexpected error (details suppressed).")
        return 1
    print("VAA MONTHLY PRICE CSV: PASS")
    print(f"Rows: {len(labels)}; symbols: {len(SYMBOLS)}")
    print(f"Latest completed month: {manifest['last_completed_month']}")
    print(f"CSV: {args.output}")
    print(f"Manifest: {args.output}.manifest.json")
    print("Note: no VAA signal or execution decision was made by this command.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
