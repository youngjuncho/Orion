"""Offline tests for the one-command BAA price-validation runner."""
from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SYMBOLS = ("SPY", "VWO", "VEA")
spec = importlib.util.spec_from_file_location("baa_price_validation_runner", ROOT / "scripts/baa/run_baa_price_validation.py")
assert spec is not None and spec.loader is not None
runner = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)


def _write_provider_files(directory: Path, provider: str, symbols=SYMBOLS, months=("2026-08-31", "2026-09-30")) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    if provider == "alpha_vantage":
        header = "timestamp,adjusted close,close\n"
        for index, symbol in enumerate(symbols):
            rows = "".join(f"{month},{100 + index + month_i},{101 + index + month_i}\n" for month_i, month in enumerate(months))
            (directory / f"{symbol}.csv").write_text(header + rows, encoding="utf-8")
    else:
        header = "Date,Open,High,Low,Close,Adj Close,Volume\n"
        for index, symbol in enumerate(symbols):
            rows = "".join(f"{month},100,102,99,101,{100 + index + month_i},1000\n" for month_i, month in enumerate(months))
            (directory / f"{symbol}.csv").write_text(header + rows, encoding="utf-8")


def test_runner_passes_complete_offline_panel_and_writes_audit_report(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "DEFAULT_SYMBOLS", SYMBOLS)
    left, right, output = tmp_path / "av", tmp_path / "yahoo", tmp_path / "out"
    _write_provider_files(left, "alpha_vantage")
    _write_provider_files(right, "yahoo_finance")

    report = runner.run(left, right, output, tolerance_pct=0.000001, minimum_months=2, expected=SYMBOLS)

    assert report["passed"] is True
    assert report["network_requests"] == 0
    assert report["api_keys_read"] is False
    assert report["left_panel"]["month_count"] == 2
    assert (output / "alpha_vantage_normalized.csv").is_file()
    assert (output / "yahoo_finance_normalized.csv").is_file()
    assert (output / "baa_price_validation_report.json").is_file()
    summary = (output / "baa_price_validation_summary.md").read_text(encoding="utf-8")
    assert "Overall screening result: PASS" in summary
    assert "Manual review still required" in summary
    assert "does not approve a provider" in summary


def test_runner_fails_when_any_provider_has_incomplete_month_panel(tmp_path):
    left, right, output = tmp_path / "av", tmp_path / "yahoo", tmp_path / "out"
    _write_provider_files(left, "alpha_vantage")
    _write_provider_files(right, "yahoo_finance", months=("2026-08-31",))

    report = runner.run(left, right, output, tolerance_pct=0.05, minimum_months=2, expected=SYMBOLS)

    assert report["passed"] is False
    assert report["right_panel"]["passed"] is False
    assert report["right_panel"]["month_count"] == 1
    summary = (output / "baa_price_validation_summary.md").read_text(encoding="utf-8")
    assert "Overall screening result: FAIL" in summary
    assert "Yahoo Finance symbol/month panel" in summary


def test_runner_rejects_missing_expected_symbol_before_writing_outputs(tmp_path):
    left, right, output = tmp_path / "av", tmp_path / "yahoo", tmp_path / "out"
    _write_provider_files(left, "alpha_vantage", symbols=SYMBOLS[:-1])
    _write_provider_files(right, "yahoo_finance")

    with pytest.raises(ValueError, match="symbol coverage mismatch"):
        runner.run(left, right, output, tolerance_pct=0.05, minimum_months=2, expected=SYMBOLS)

    assert not output.exists()
