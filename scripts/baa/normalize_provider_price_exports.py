#!/usr/bin/env python3
"""Normalize offline Alpha Vantage or Yahoo Finance CSV exports for BAA comparison.

No network access or API keys are used. Each input CSV must contain one ticker.
Input filenames should be SYMBOL.csv (or SYMBOL_anything.csv); alternatively,
pass --symbol when normalizing a single file. Output schema matches the offline
BAA comparator: source,symbol,month,observed_at,adjusted_close,currency.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Iterable

OUTPUT_COLUMNS = ("source", "symbol", "month", "observed_at", "adjusted_close", "currency")
_SYMBOL_RE = re.compile(r"^[A-Z][A-Z0-9.\-^=]{0,19}$")


def _column_map(fieldnames: list[str] | None) -> dict[str, str]:
    if not fieldnames:
        raise ValueError("CSV has no header row")
    return {re.sub(r"[^a-z0-9]", "", name.strip().lower()): name for name in fieldnames}


def _parse_date(raw: str, path: Path, line_no: int) -> date:
    try:
        return date.fromisoformat(raw.strip()[:10])
    except (TypeError, ValueError):
        raise ValueError(f"{path}:{line_no}: date/timestamp must start with YYYY-MM-DD") from None


def normalize_file(path: Path, provider: str, source: str, symbol: str, currency: str = "USD") -> list[dict[str, str]]:
    symbol = symbol.strip().upper()
    currency = currency.strip().upper()
    if not _SYMBOL_RE.fullmatch(symbol):
        raise ValueError(f"{path}: invalid ticker symbol {symbol!r}")
    if currency != "USD":
        raise ValueError(f"{path}: BAA US-listed ETF export currency must be explicitly USD")
    with path.open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        columns = _column_map(reader.fieldnames)
        date_col = columns.get("timestamp") if provider == "alpha_vantage" else columns.get("date")
        price_col = columns.get("adjustedclose") or columns.get("adjclose")
        if date_col is None:
            raise ValueError(f"{path}: missing {'timestamp' if provider == 'alpha_vantage' else 'Date'} column")
        if price_col is None:
            raise ValueError(f"{path}: missing adjusted close column; raw Close is not an acceptable fallback")
        by_month: dict[str, tuple[date, float]] = {}
        seen_dates: set[date] = set()
        for line_no, row in enumerate(reader, start=2):
            observed = _parse_date(row.get(date_col, ""), path, line_no)
            if observed in seen_dates:
                raise ValueError(f"{path}:{line_no}: duplicate observation date {observed.isoformat()}")
            seen_dates.add(observed)
            raw_price = (row.get(price_col) or "").strip()
            try:
                price = float(raw_price)
            except (TypeError, ValueError, OverflowError):
                raise ValueError(f"{path}:{line_no}: adjusted close must be numeric") from None
            if not math.isfinite(price) or price <= 0:
                raise ValueError(f"{path}:{line_no}: adjusted close must be finite and positive")
            month = observed.strftime("%Y-%m")
            current = by_month.get(month)
            if current is None or observed > current[0]:
                by_month[month] = (observed, price)
        if not by_month:
            raise ValueError(f"{path}: no price observations found")
    return [
        {"source": source, "symbol": symbol, "month": month,
         "observed_at": observed.isoformat(), "adjusted_close": format(price, ".12g"), "currency": currency}
        for month, (observed, price) in sorted(by_month.items())
    ]


def _symbol_from_filename(path: Path) -> str:
    # Prefer the first filename token, so SPY.csv and SPY_monthly.csv both work.
    return path.stem.split("_")[0].split("-")[0].upper()


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("alpha_vantage", "yahoo_finance"), required=True)
    parser.add_argument("--input", type=Path, required=True, help="single ticker CSV or directory of SYMBOL*.csv files")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", required=True, help="label recorded in the normalized CSV")
    parser.add_argument("--symbol", help="ticker symbol for a single input file; otherwise inferred from filename")
    parser.add_argument("--currency", default="USD", help="explicit data currency (BAA comparison currently requires USD)")
    args = parser.parse_args(argv)
    try:
        if args.input.is_dir():
            files = sorted(args.input.glob("*.csv"))
            if args.symbol:
                raise ValueError("--symbol is only valid when --input is a single file")
            if not files:
                raise ValueError(f"{args.input}: no CSV files found")
        elif args.input.is_file():
            files = [args.input]
        else:
            raise ValueError(f"input path does not exist: {args.input}")
        rows: list[dict[str, str]] = []
        seen_symbols: set[str] = set()
        for path in files:
            symbol = args.symbol.strip().upper() if args.symbol else _symbol_from_filename(path)
            if symbol in seen_symbols:
                raise ValueError(f"duplicate input ticker {symbol}; provide one CSV per symbol")
            seen_symbols.add(symbol)
            rows.extend(normalize_file(path, args.provider, args.source, symbol, args.currency))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=OUTPUT_COLUMNS)
            writer.writeheader()
            writer.writerows(sorted(rows, key=lambda row: (row["symbol"], row["month"])))
    except (OSError, ValueError) as exc:
        print(f"normalization error: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {len(rows)} monthly observations for {len(seen_symbols)} symbols to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
