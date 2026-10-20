#!/usr/bin/env python3
"""Independent VAA-G12 signal oracle from a provider-exported monthly price CSV.

Input CSV: Date,SPY,IWM,QQQ,VGK,EWJ,VWO,VNQ,GSG,GLD,TLT,HYG,LQD,SHY,IEF
Rows are oldest-to-newest monthly observations; prices must be total-return adjusted
close values from one provider, with one consistent observation convention.
This module intentionally does not import or call Orion's VAA implementation.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

OFFENSIVE = ("SPY", "IWM", "QQQ", "VGK", "EWJ", "VWO", "VNQ", "GSG", "GLD", "TLT", "HYG", "LQD")
DEFENSIVE = ("SHY", "IEF", "LQD")
ALL_ASSETS = tuple(dict.fromkeys(OFFENSIVE + DEFENSIVE))
WEIGHTS = ((1, 12), (3, 4), (6, 2), (12, 1))


def previous_month(as_of: date) -> tuple[int, int]:
    return (as_of.year - 1, 12) if as_of.month == 1 else (as_of.year, as_of.month - 1)


def read_prices(path: Path, as_of: date) -> tuple[list[str], dict[str, list[float]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "Date" not in reader.fieldnames:
            raise ValueError("CSV must contain a Date column")
        missing = [asset for asset in ALL_ASSETS if asset not in reader.fieldnames]
        if missing:
            raise ValueError("CSV missing required asset columns: " + ", ".join(missing))
        dates: list[date] = []
        values = {asset: [] for asset in ALL_ASSETS}
        for line_number, row in enumerate(reader, start=2):
            try:
                observed = date.fromisoformat((row.get("Date") or "").strip())
            except ValueError as exc:
                raise ValueError(f"line {line_number}: Date must be YYYY-MM-DD") from exc
            if dates and observed <= dates[-1]:
                raise ValueError(f"line {line_number}: dates must be strictly increasing")
            if dates:
                prior = dates[-1]
                expected = (prior.year + (prior.month == 12), 1 if prior.month == 12 else prior.month + 1)
                if (observed.year, observed.month) != expected:
                    raise ValueError(f"line {line_number}: skipped or duplicate calendar month")
            dates.append(observed)
            for asset in ALL_ASSETS:
                raw = (row.get(asset) or "").strip()
                try:
                    price = float(raw)
                except ValueError as exc:
                    raise ValueError(f"line {line_number}: {asset} price is missing/non-numeric") from exc
                if not math.isfinite(price) or price <= 0:
                    raise ValueError(f"line {line_number}: {asset} price must be finite and positive")
                values[asset].append(price)
    if len(dates) < 13:
        raise ValueError(f"need at least 13 monthly observations; found {len(dates)}")
    expected_year, expected_month = previous_month(as_of)
    latest = dates[-1]
    if (latest.year, latest.month) != (expected_year, expected_month):
        raise ValueError("latest row must belong to the last completed calendar month relative to --as-of-date")
    return [d.isoformat() for d in dates], values


def independent_score(prices: list[float]) -> float:
    """Reference formula, implemented separately from src/orion/.../vaa.py."""
    if len(prices) < 13:
        raise ValueError("13612W requires 13 prices")
    now = prices[-1]
    return sum(multiplier * (now / prices[-lag - 1] - 1.0) for lag, multiplier in WEIGHTS)


def reproduce(dates: list[str], prices: dict[str, list[float]]) -> dict[str, Any]:
    scores = {asset: independent_score(series) for asset, series in prices.items()}
    offensive_rank = sorted(OFFENSIVE, key=lambda asset: (-scores[asset], OFFENSIVE.index(asset)))
    defensive_rank = sorted(DEFENSIVE, key=lambda asset: (-scores[asset], DEFENSIVE.index(asset)))
    breadth = sum(scores[asset] <= 0.0 for asset in OFFENSIVE)
    cash_fraction = min(1.0, math.floor((breadth / 4.0) * 2.0) / 2.0)
    if cash_fraction == 0.0:
        selected, allocation, state = offensive_rank[:2], [0.5, 0.5], "Offensive"
    elif cash_fraction == 0.5:
        defensive_pick = next(asset for asset in defensive_rank if asset != offensive_rank[0])
        selected, allocation, state = [offensive_rank[0], defensive_pick], [0.5, 0.5], "Mixed"
    else:
        selected, allocation, state = [defensive_rank[0]], [1.0], "Defensive"
    return {
        "signal_date": dates[-1],
        "formula": "12*(P0/P1-1)+4*(P0/P3-1)+2*(P0/P6-1)+(P0/P12-1)",
        "scores": {asset: scores[asset] for asset in ALL_ASSETS},
        "offensive_ranked": offensive_rank,
        "defensive_ranked": defensive_rank,
        "offensive_nonpositive_count": breadth,
        "breadth_threshold_B": 4,
        "easy_trading_T": 2,
        "defensive_fraction": cash_fraction,
        "state": state,
        "selected_assets": selected,
        "weights": allocation,
        "evidence_boundary": "Independent formula oracle only; not a performance backtest or proof of provider data correctness.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="provider-exported monthly adjusted-close CSV")
    parser.add_argument("--as-of-date", required=True, type=date.fromisoformat, help="YYYY-MM-DD date used to enforce completed-month cutoff")
    parser.add_argument("--output", type=Path, help="write JSON report to this path; otherwise print to stdout")
    args = parser.parse_args()
    try:
        dates, prices = read_prices(args.csv, args.as_of_date)
        report = reproduce(dates, prices)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, indent=2, sort_keys=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
