"""Offline integration coverage for the BAA provider CSV pipeline.

The test exercises collector -> normalizer -> comparator with synthetic data;
it deliberately makes no network requests and does not read provider secrets.
"""
from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SYMBOLS = ("SPY", "QQQ", "IWM", "VGK", "EWJ", "VWO", "VNQ", "DBC", "GLD", "TLT", "HYG", "LQD", "TIP", "BIL", "IEF", "BND", "VEA")


def _load(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


collector = _load("baa_pipeline_collector", "scripts/baa/collect_provider_price_exports.py")
normalizer = _load("baa_pipeline_normalizer", "scripts/baa/normalize_provider_price_exports.py")
comparator = _load("baa_pipeline_comparator", "scripts/baa/compare_monthly_price_exports.py")


@pytest.mark.parametrize("symbol_index", [0, 8, 16])
def test_offline_collector_normalizer_comparator_pipeline_passes(tmp_path, monkeypatch, symbol_index):
    """Sample representative symbols across the universe; all 17 flow through each run."""
    monkeypatch.setattr(collector, "_request_bytes", lambda *args, **kwargs: pytest.fail("network must not be called"))
    left_raw = tmp_path / "av_raw"
    right_raw = tmp_path / "yahoo_raw"
    left_norm = tmp_path / "av_normalized.csv"
    right_norm = tmp_path / "yahoo_normalized.csv"
    left_raw.mkdir()
    right_raw.mkdir()

    def price(symbol: str, month_index: int) -> float:
        return 80.0 + SYMBOLS.index(symbol) + month_index * 1.25

    def av_fetch(symbol: str, _secret: str) -> str:
        return (
            "timestamp,adjusted close,close\n"
            f"2026-08-31,{price(symbol, 0)},100\n"
            f"2026-09-30,{price(symbol, 1)},101\n"
        )

    def yahoo_fetch(symbol: str) -> str:
        return (
            "Date,Open,High,Low,Close,Adj Close,Volume\n"
            f"2026-08-31,100,101,99,100,{price(symbol, 0)},1000\n"
            f"2026-09-29,100,101,99,100,{price(symbol, 1) - 0.5},1000\n"
            f"2026-09-30,100,101,99,101,{price(symbol, 1)},1000\n"
        )

    collector.collect("alpha_vantage", SYMBOLS, left_raw, api_key="synthetic-test-secret", delay_seconds=0, fetch_av=av_fetch, sleep=lambda _: None)
    collector.collect("yahoo_finance", SYMBOLS, right_raw, fetch_yahoo=yahoo_fetch)

    left_rows = []
    right_rows = []
    for symbol in SYMBOLS:
        left_rows.extend(normalizer.normalize_file(left_raw / f"{symbol}.csv", "alpha_vantage", "alpha_vantage", symbol))
        right_rows.extend(normalizer.normalize_file(right_raw / f"{symbol}.csv", "yahoo_finance", "yahoo_finance", symbol))

    def write_normalized(path: Path, rows: list[dict[str, str]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=normalizer.OUTPUT_COLUMNS)
            writer.writeheader()
            writer.writerows(sorted(rows, key=lambda row: (row["symbol"], row["month"])))

    write_normalized(left_norm, left_rows)
    write_normalized(right_norm, right_rows)
    left = comparator.load_csv(left_norm, "alpha_vantage")
    right = comparator.load_csv(right_norm, "yahoo_finance")
    result = comparator.compare(left, right, tolerance_pct=0.000001, expected_symbols=SYMBOLS)

    assert result.passed
    assert result.symbols == len(SYMBOLS)
    assert result.months == 2
    assert result.matched_observations == len(SYMBOLS) * 2
    assert not result.date_mismatches
    assert not result.price_mismatches
    assert SYMBOLS[symbol_index] in {symbol for symbol, _ in left}
