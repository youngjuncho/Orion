import importlib.util
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "baa" / "compare_monthly_price_exports.py"
spec = importlib.util.spec_from_file_location("baa_price_compare", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)

HEADER = "source,symbol,month,observed_at,adjusted_close,currency\n"


def write_csv(path: Path, rows: str) -> Path:
    path.write_text(HEADER + rows, encoding="utf-8")
    return path


def test_matching_monthly_exports_pass(tmp_path):
    a = write_csv(tmp_path / "a.csv", "av,SPY,2026-08,2026-08-31,100,USD\nav,SPY,2026-09,2026-09-30,101,USD\n")
    b = write_csv(tmp_path / "b.csv", "yf,SPY,2026-08,2026-08-31,100.01,USD\nyf,SPY,2026-09,2026-09-30,101.01,USD\n")
    result = module.compare(module.load_csv(a, "av"), module.load_csv(b, "yf"), tolerance_pct=0.05, expected_symbols=("SPY",))
    assert result.passed
    assert result.matched_observations == 2


def test_missing_month_fails_closed(tmp_path):
    a = write_csv(tmp_path / "a.csv", "av,SPY,2026-08,2026-08-31,100,USD\nav,SPY,2026-09,2026-09-30,101,USD\n")
    b = write_csv(tmp_path / "b.csv", "yf,SPY,2026-08,2026-08-31,100,USD\n")
    result = module.compare(module.load_csv(a, "av"), module.load_csv(b, "yf"), tolerance_pct=0.05, expected_symbols=("SPY",))
    assert not result.passed
    assert result.missing_right == ("SPY 2026-09",)


def test_observation_date_mismatch_fails(tmp_path):
    a = write_csv(tmp_path / "a.csv", "av,SPY,2026-08,2026-08-31,100,USD\n")
    b = write_csv(tmp_path / "b.csv", "yf,SPY,2026-08,2026-08-28,100,USD\n")
    result = module.compare(module.load_csv(a, "av"), module.load_csv(b, "yf"), tolerance_pct=0.05, expected_symbols=("SPY",))
    assert not result.passed
    assert result.date_mismatches


def test_price_difference_above_tolerance_fails(tmp_path):
    a = write_csv(tmp_path / "a.csv", "av,SPY,2026-08,2026-08-31,100,USD\n")
    b = write_csv(tmp_path / "b.csv", "yf,SPY,2026-08,2026-08-31,101,USD\n")
    result = module.compare(module.load_csv(a, "av"), module.load_csv(b, "yf"), tolerance_pct=0.05, expected_symbols=("SPY",))
    assert not result.passed
    assert result.price_mismatches


def test_duplicate_symbol_month_rejected(tmp_path):
    a = write_csv(tmp_path / "a.csv", "av,SPY,2026-08,2026-08-31,100,USD\nav,SPY,2026-08,2026-08-31,100,USD\n")
    with pytest.raises(ValueError, match="duplicate symbol/month"):
        module.load_csv(a, "av")


def test_non_usd_currency_rejected(tmp_path):
    a = write_csv(tmp_path / "a.csv", "av,SPY,2026-08,2026-08-31,100,KRW\n")
    with pytest.raises(ValueError, match="currency must be USD"):
        module.load_csv(a, "av")
