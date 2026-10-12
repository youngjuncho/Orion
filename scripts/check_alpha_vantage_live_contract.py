"""Run an explicit, sanitized live contract check for the Moon ADM pilot.

Requires ORION_ALPHA_VANTAGE_API_KEY. Makes one request per configured symbol,
performs no retries, and prints only response shape/coverage metadata—not prices,
API credentials, request URLs, or raw provider payloads.
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data.alphavantage import (
    AlphaVantageMonthlyAdjustedProvider,
    AlphaVantageMonthlyAdjustedSource,
    AlphaVantageProviderError,
)


def main() -> int:
    if not os.environ.get("ORION_ALPHA_VANTAGE_API_KEY", "").strip():
        print("NOT RUN: ORION_ALPHA_VANTAGE_API_KEY is not configured.")
        return 2

    try:
        dataset = AlphaVantageMonthlyAdjustedProvider(
            AlphaVantageMonthlyAdjustedSource()
        ).load()
    except (AlphaVantageProviderError, ValueError) as exc:
        # Provider exceptions are sanitized by the provider; never print URLs or payloads.
        print(f"LIVE CONTRACT CHECK FAILED: {exc}")
        return 1
    except Exception:
        print("LIVE CONTRACT CHECK FAILED: unexpected error (details suppressed).")
        return 1

    expected_symbols = ("VTI", "VEU", "SGOV")
    by_symbol: dict[str, list[str]] = defaultdict(list)
    for point in dataset.observations:
        if point.field != "adjusted_close" or point.source != "alpha_vantage":
            print("LIVE CONTRACT CHECK FAILED: unexpected normalized field or source.")
            return 1
        if point.symbol not in expected_symbols:
            print("LIVE CONTRACT CHECK FAILED: unexpected symbol coverage.")
            return 1
        by_symbol[point.symbol].append(point.observed_at)

    if set(by_symbol) != set(expected_symbols):
        print("LIVE CONTRACT CHECK FAILED: unexpected symbol coverage.")
        return 1
    try:
        if date.fromisoformat(dataset.as_of).isoformat() != dataset.as_of:
            raise ValueError
    except (TypeError, ValueError):
        print("LIVE CONTRACT CHECK FAILED: invalid batch date.")
        return 1

    # Validate the entire batch before printing any PASS status so a later
    # symbol failure cannot leave a misleading partial-success report.
    batch_date = date.fromisoformat(dataset.as_of)
    validated: dict[str, list[str]] = {}
    for symbol in expected_symbols:
        dates = by_symbol[symbol]
        if len(dates) < 13:
            print(f"LIVE CONTRACT CHECK FAILED: insufficient history for {symbol} (minimum=13).")
            return 1
        try:
            normalized_dates = [date.fromisoformat(value).isoformat() for value in dates]
        except (TypeError, ValueError):
            print(f"LIVE CONTRACT CHECK FAILED: invalid observation date for {symbol}.")
            return 1
        if normalized_dates != dates:
            print(f"LIVE CONTRACT CHECK FAILED: invalid observation date for {symbol}.")
            return 1
        if len(set(normalized_dates)) != len(normalized_dates):
            print(f"LIVE CONTRACT CHECK FAILED: duplicate observation dates for {symbol}.")
            return 1
        if any(date.fromisoformat(value) > batch_date for value in normalized_dates):
            print(f"LIVE CONTRACT CHECK FAILED: observation date is later than batch date for {symbol}.")
            return 1
        month_keys = [value[:7] for value in normalized_dates]
        if len(set(month_keys)) != len(month_keys):
            print(f"LIVE CONTRACT CHECK FAILED: multiple monthly bars for {symbol}.")
            return 1
        validated[symbol] = sorted(normalized_dates)

    print("LIVE RESPONSE CONTRACT CHECK: PASS")
    print(f"Batch as_of: {dataset.as_of}")
    for symbol in expected_symbols:
        dates = validated[symbol]
        print(
            f"{symbol}: PASS (observations={len(dates)}, "
            f"oldest={dates[0]}, latest={dates[-1]})"
        )
    print("Note: this checks response shape and history coverage, not price accuracy or investment suitability.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
