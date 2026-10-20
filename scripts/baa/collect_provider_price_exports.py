#!/usr/bin/env python3
"""Opt-in local collector for BAA provider CSV exports.

This script is intentionally inert by default. Without --confirm-live-data-fetch
it prints a plan and performs no network requests and does not read API keys.
Collected files are raw provider exports; normalize them with
normalize_provider_price_exports.py before comparison.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_SYMBOLS = (
    "SPY", "QQQ", "IWM", "VGK", "EWJ", "VWO", "VNQ", "DBC", "GLD",
    "TLT", "HYG", "LQD", "TIP", "BIL", "IEF", "BND", "VEA",
)
_SYMBOL_RE = re.compile(r"^[A-Z][A-Z0-9.\-^=]{0,19}$")
_USER_AGENT = "Orion-BAA-Research/1.0 (user-initiated local data validation)"


class CollectionError(RuntimeError):
    """Raised when a provider response cannot be safely persisted."""


def _request_bytes(url: str, timeout: float = 30.0) -> bytes:
    request = Request(url, headers={"User-Agent": _USER_AGENT, "Accept": "application/json,text/csv,*/*"})
    try:
        with urlopen(request, timeout=timeout) as response:  # nosec - fixed provider hosts below
            status = getattr(response, "status", 200)
            if status != 200:
                raise CollectionError(f"provider returned HTTP {status}")
            return response.read()
    except HTTPError as exc:
        raise CollectionError(f"provider returned HTTP {exc.code}") from None
    except URLError as exc:
        raise CollectionError(f"provider request failed: {exc.reason}") from None
    except TimeoutError:
        raise CollectionError("provider request timed out") from None


def fetch_alpha_vantage_csv(symbol: str, api_key: str, timeout: float = 30.0) -> str:
    query = urlencode({
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": symbol,
        "apikey": api_key,
    })
    payload = _request_bytes(f"https://www.alphavantage.co/query?{query}", timeout).decode("utf-8-sig")
    # Alpha Vantage can return JSON errors/throttle notices with HTTP 200.
    if payload.lstrip().startswith("{"):
        try:
            response = json.loads(payload)
        except json.JSONDecodeError:
            response = {}
        message = response.get("Error Message") or response.get("Note") or response.get("Information")
        if message:
            raise CollectionError(f"Alpha Vantage rejected {symbol}: {message}")
        raise CollectionError(f"Alpha Vantage returned JSON instead of CSV for {symbol}")
    reader = csv.DictReader(io.StringIO(payload))
    normalized_headers = {str(name).strip().lower() for name in (reader.fieldnames or [])}
    if not {"timestamp", "adjusted close"}.issubset(normalized_headers):
        raise CollectionError(f"Alpha Vantage CSV for {symbol} is missing timestamp/adjusted close columns")
    if not next(iter(reader), None):
        raise CollectionError(f"Alpha Vantage CSV for {symbol} has no observations")
    return payload


def fetch_yahoo_finance_csv(symbol: str, timeout: float = 30.0) -> str:
    # Use daily observations so the normalizer can select the last available
    # trading observation per calendar month rather than relying on monthly
    # chart timestamp conventions.
    query = urlencode({"range": "max", "interval": "1d", "events": "div,splits"})
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?{query}"
    try:
        payload = json.loads(_request_bytes(url, timeout).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise CollectionError(f"Yahoo Finance returned invalid JSON for {symbol}") from None
    chart = payload.get("chart") or {}
    if chart.get("error"):
        raise CollectionError(f"Yahoo Finance rejected {symbol}: {chart['error']}")
    results = chart.get("result") or []
    if not results:
        raise CollectionError(f"Yahoo Finance returned no observations for {symbol}")
    result = results[0]
    timestamps = result.get("timestamp") or []
    indicators = result.get("indicators") or {}
    quote_rows = (indicators.get("quote") or [{}])[0]
    adjusted_rows = (indicators.get("adjclose") or [{}])[0].get("adjclose") or []
    if not timestamps or not adjusted_rows or len(timestamps) != len(adjusted_rows):
        raise CollectionError(f"Yahoo Finance adjusted-close series is incomplete for {symbol}")
    fields = ("Date", "Open", "High", "Low", "Close", "Adj Close", "Volume")
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    import datetime as _datetime
    for index, timestamp in enumerate(timestamps):
        adjusted = adjusted_rows[index]
        if adjusted is None:
            continue
        observed = _datetime.datetime.fromtimestamp(int(timestamp), tz=timezone.utc).date().isoformat()
        row = {"Date": observed, "Adj Close": adjusted}
        for field, key in (("Open", "open"), ("High", "high"), ("Low", "low"),
                           ("Close", "close"), ("Volume", "volume")):
            values = quote_rows.get(key) or []
            row[field] = values[index] if index < len(values) else ""
        writer.writerow(row)
    if output.tell() <= len(",".join(fields)) + 2:
        raise CollectionError(f"Yahoo Finance returned no valid adjusted-close observations for {symbol}")
    return output.getvalue()


def collect(
    provider: str,
    symbols: Iterable[str],
    output_dir: Path,
    *,
    api_key: str | None = None,
    overwrite: bool = False,
    delay_seconds: float = 15.0,
    fetch_av: Callable[[str, str], str] = fetch_alpha_vantage_csv,
    fetch_yahoo: Callable[[str], str] = fetch_yahoo_finance_csv,
    sleep: Callable[[float], None] = time.sleep,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    symbols = list(symbols)
    paths = [output_dir / f"{symbol}.csv" for symbol in symbols]
    existing = [path.name for path in paths if path.exists()]
    if existing and not overwrite:
        raise CollectionError("refusing to overwrite existing exports: " + ", ".join(existing) + "; pass --overwrite to replace")
    # Fetch and minimally validate every symbol before touching destination files.
    # This prevents a mid-run provider failure from leaving a misleading partial
    # set that could be mistaken for a complete universe export.
    contents: list[tuple[Path, str]] = []
    for index, (symbol, path) in enumerate(zip(symbols, paths)):
        if provider == "alpha_vantage":
            if not api_key:
                raise CollectionError("ORION_ALPHA_VANTAGE_API_KEY is required for Alpha Vantage collection")
            content = fetch_av(symbol, api_key)
        elif provider == "yahoo_finance":
            content = fetch_yahoo(symbol)
        else:
            raise CollectionError(f"unsupported provider: {provider}")
        rows = list(csv.reader(io.StringIO(content)))
        if len(rows) < 2 or not rows[0] or any(not cell.strip() for cell in rows[0]):
            raise CollectionError(f"provider returned an empty or malformed CSV for {symbol}")
        contents.append((path, content))
        if provider == "alpha_vantage" and index < len(symbols) - 1 and delay_seconds > 0:
            sleep(delay_seconds)

    # Stage all bytes beside their final paths, then publish only after every
    # provider response has passed the basic CSV check.
    staged: list[tuple[Path, Path]] = []
    try:
        for path, content in contents:
            temp_path = path.with_name(f".{path.name}.orion-tmp")
            if temp_path.exists():
                temp_path.unlink()
            temp_path.write_text(content, encoding="utf-8", newline="")
            staged.append((temp_path, path))
        for temp_path, path in staged:
            temp_path.replace(path)
    except OSError as exc:
        for temp_path, _ in staged:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise CollectionError(f"could not safely persist provider exports: {exc}") from None
    return paths


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("alpha_vantage", "yahoo_finance"), required=True)
    parser.add_argument("--output-dir", type=Path, required=True, help="directory for raw per-ticker CSV exports")
    parser.add_argument("--symbols", nargs="+", default=list(DEFAULT_SYMBOLS), help="tickers; defaults to the 17-symbol BAA comparison universe")
    parser.add_argument("--delay-seconds", type=float, default=15.0, help="delay between Alpha Vantage requests (default: 15 seconds)")
    parser.add_argument("--timeout-seconds", type=float, default=30.0, help="per-request timeout")
    parser.add_argument("--overwrite", action="store_true", help="replace existing SYMBOL.csv files")
    parser.add_argument("--confirm-live-data-fetch", action="store_true", help="explicitly authorize live provider requests; absent means plan-only")
    args = parser.parse_args(argv)
    symbols = [symbol.strip().upper() for symbol in args.symbols]
    if not symbols or len(set(symbols)) != len(symbols) or any(not _SYMBOL_RE.fullmatch(s) for s in symbols):
        print("error: symbols must be valid, unique ticker symbols", file=sys.stderr)
        return 2
    if args.delay_seconds < 0 or args.timeout_seconds <= 0:
        print("error: delays must be nonnegative and timeout must be positive", file=sys.stderr)
        return 2
    if not args.confirm_live_data_fetch:
        print("PLAN ONLY — no network requests made and no API key read.")
        print(f"Provider: {args.provider}; symbols: {', '.join(symbols)}")
        print(f"Output directory: {args.output_dir}; existing files will {'be replaced' if args.overwrite else 'not be overwritten'}.")
        print("To fetch live data later, rerun with --confirm-live-data-fetch after approval.")
        return 0
    try:
        key = os.environ.get("ORION_ALPHA_VANTAGE_API_KEY") if args.provider == "alpha_vantage" else None
        if args.provider == "alpha_vantage" and not key:
            raise CollectionError("ORION_ALPHA_VANTAGE_API_KEY is not set; configure it locally, never paste it into chat")
        # Keep collection testable without network access while honoring the
        # caller's timeout setting for real provider requests.
        saved = collect(
            args.provider, symbols, args.output_dir, api_key=key,
            overwrite=args.overwrite, delay_seconds=args.delay_seconds,
            fetch_av=lambda symbol, secret: fetch_alpha_vantage_csv(symbol, secret, args.timeout_seconds),
            fetch_yahoo=lambda symbol: fetch_yahoo_finance_csv(symbol, args.timeout_seconds),
        )
    except (OSError, CollectionError) as exc:
        print(f"collection error: {exc}", file=sys.stderr)
        return 2
    print(f"Saved {len(saved)} raw provider CSV exports to {args.output_dir}")
    print("Next: normalize offline with scripts/baa/normalize_provider_price_exports.py, then compare.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
