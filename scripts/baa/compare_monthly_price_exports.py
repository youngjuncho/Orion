#!/usr/bin/env python3
"""Compare normalized monthly adjusted-price exports from two providers.

Input CSV schema: source,symbol,month,observed_at,adjusted_close,currency
This is an offline audit tool. It makes no network calls and never reads API keys.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

REQUIRED_COLUMNS = ("source", "symbol", "month", "observed_at", "adjusted_close", "currency")
BAA_G12_SYMBOLS = ("SPY", "VWO", "VEA", "BND", "QQQ", "IWM", "VGK", "EWJ", "VNQ", "DBC", "GLD", "TLT", "HYG", "LQD", "TIP", "BIL", "IEF")


@dataclass(frozen=True)
class Observation:
    source: str
    symbol: str
    month: str
    observed_at: str
    adjusted_close: float
    currency: str


@dataclass(frozen=True)
class Comparison:
    symbols: int
    months: int
    matched_observations: int
    missing_left: tuple[str, ...]
    missing_right: tuple[str, ...]
    date_mismatches: tuple[str, ...]
    currency_mismatches: tuple[str, ...]
    price_mismatches: tuple[str, ...]
    max_abs_pct_difference: float | None
    passed: bool


def load_csv(path: Path, source_label: str) -> dict[tuple[str, str], Observation]:
    rows: dict[tuple[str, str], Observation] = {}
    with path.open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or any(name not in reader.fieldnames for name in REQUIRED_COLUMNS):
            raise ValueError(f"{path}: CSV must include columns: {', '.join(REQUIRED_COLUMNS)}")
        for line_no, row in enumerate(reader, start=2):
            symbol = (row.get("symbol") or "").strip().upper()
            month = (row.get("month") or "").strip()
            observed_at = (row.get("observed_at") or "").strip()
            currency = (row.get("currency") or "").strip().upper()
            try:
                price = float(row.get("adjusted_close", ""))
            except (TypeError, ValueError, OverflowError):
                raise ValueError(f"{path}:{line_no}: adjusted_close must be numeric") from None
            if not symbol or len(month) != 7 or month[4] != "-" or observed_at[:7] != month:
                raise ValueError(f"{path}:{line_no}: invalid symbol/month/observed_at")
            if not math.isfinite(price) or price <= 0:
                raise ValueError(f"{path}:{line_no}: adjusted_close must be finite and positive")
            if currency != "USD":
                raise ValueError(f"{path}:{line_no}: currency must be USD")
            key = (symbol, month)
            if key in rows:
                raise ValueError(f"{path}:{line_no}: duplicate symbol/month {symbol} {month}")
            rows[key] = Observation(source_label, symbol, month, observed_at, price, currency)
    if not rows:
        raise ValueError(f"{path}: no observations found")
    return rows


def compare(left: dict[tuple[str, str], Observation], right: dict[tuple[str, str], Observation], *, tolerance_pct: float, expected_symbols: tuple[str, ...] = BAA_G12_SYMBOLS) -> Comparison:
    left_keys, right_keys = set(left), set(right)
    left_symbols = {symbol for symbol, _ in left_keys}
    right_symbols = {symbol for symbol, _ in right_keys}
    expected = set(expected_symbols)
    missing_expected_left = sorted(expected - left_symbols)
    missing_expected_right = sorted(expected - right_symbols)
    common = sorted(left_keys & right_keys)
    missing_left = tuple([f"{s} {m}" for s, m in sorted(right_keys - left_keys)] + [f"SYMBOL {s}" for s in missing_expected_left])
    missing_right = tuple([f"{s} {m}" for s, m in sorted(left_keys - right_keys)] + [f"SYMBOL {s}" for s in missing_expected_right])
    date_mismatches: list[str] = []
    currency_mismatches: list[str] = []
    price_mismatches: list[str] = []
    diffs: list[float] = []
    for key in common:
        a, b = left[key], right[key]
        if a.observed_at != b.observed_at:
            date_mismatches.append(f"{key[0]} {key[1]}: {a.observed_at} != {b.observed_at}")
        if a.currency != b.currency:
            currency_mismatches.append(f"{key[0]} {key[1]}: {a.currency} != {b.currency}")
        pct = abs(a.adjusted_close - b.adjusted_close) / max(abs(a.adjusted_close), abs(b.adjusted_close)) * 100.0
        diffs.append(pct)
        if pct > tolerance_pct:
            price_mismatches.append(f"{key[0]} {key[1]}: {a.adjusted_close:.8g} vs {b.adjusted_close:.8g} ({pct:.6f}%)")
    return Comparison(
        symbols=len({s for s, _ in left_keys | right_keys}),
        months=len({m for _, m in left_keys | right_keys}),
        matched_observations=len(common),
        missing_left=missing_left,
        missing_right=missing_right,
        date_mismatches=tuple(date_mismatches),
        currency_mismatches=tuple(currency_mismatches),
        price_mismatches=tuple(price_mismatches),
        max_abs_pct_difference=max(diffs) if diffs else None,
        passed=bool(common) and not (missing_left or missing_right or date_mismatches or currency_mismatches or price_mismatches),
    )


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left_csv", type=Path)
    parser.add_argument("right_csv", type=Path)
    parser.add_argument("--left-label", default="provider_a")
    parser.add_argument("--right-label", default="provider_b")
    parser.add_argument("--tolerance-pct", type=float, default=0.05, help="maximum permitted relative price difference in percent (default: 0.05%%)")
    parser.add_argument("--expected-symbols", default=",".join(BAA_G12_SYMBOLS), help="comma-separated required symbols; defaults to BAA-G12 universe")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)
    if not math.isfinite(args.tolerance_pct) or args.tolerance_pct < 0:
        parser.error("--tolerance-pct must be finite and non-negative")
    try:
        left = load_csv(args.left_csv, args.left_label)
        right = load_csv(args.right_csv, args.right_label)
        expected_symbols = tuple(symbol.strip().upper() for symbol in args.expected_symbols.split(",") if symbol.strip())
        if not expected_symbols or len(set(expected_symbols)) != len(expected_symbols):
            raise ValueError("--expected-symbols must contain unique, non-empty symbols")
        result = compare(left, right, tolerance_pct=args.tolerance_pct, expected_symbols=expected_symbols)
    except (OSError, ValueError) as exc:
        print(f"validation error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(f"Comparison: {'PASS' if result.passed else 'FAIL'}")
        print(f"Symbols: {result.symbols}; months: {result.months}; matched observations: {result.matched_observations}")
        print(f"Maximum absolute relative price difference: {result.max_abs_pct_difference}")
        for name in ("missing_left", "missing_right", "date_mismatches", "currency_mismatches", "price_mismatches"):
            values = getattr(result, name)
            if values:
                print(f"{name}:")
                for value in values:
                    print(f"  - {value}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
