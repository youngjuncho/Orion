import importlib.util
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "baa" / "normalize_provider_price_exports.py"
spec = importlib.util.spec_from_file_location("baa_price_normalizer", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_alpha_vantage_monthly_adjusted_export_normalizes(tmp_path):
    path = write(tmp_path / "SPY.csv", "timestamp,open,high,low,close,adjusted close,volume,dividend amount\n2026-09-30,1,1,1,99,101,100,0.2\n2026-08-31,1,1,1,98,100,100,0.1\n")
    rows = module.normalize_file(path, "alpha_vantage", "av", "SPY")
    assert [(r["month"], r["observed_at"], r["adjusted_close"]) for r in rows] == [
        ("2026-08", "2026-08-31", "100"), ("2026-09", "2026-09-30", "101")]


def test_yahoo_daily_export_uses_last_adjusted_observation_in_month(tmp_path):
    path = write(tmp_path / "SPY.csv", "Date,Open,High,Low,Close,Adj Close,Volume\n2026-09-30,1,1,1,100,101,10\n2026-09-29,1,1,1,99,100,10\n2026-08-31,1,1,1,98,99,10\n")
    rows = module.normalize_file(path, "yahoo_finance", "yf", "SPY")
    assert [(r["month"], r["observed_at"], r["adjusted_close"]) for r in rows] == [
        ("2026-08", "2026-08-31", "99"), ("2026-09", "2026-09-30", "101")]


def test_raw_close_is_not_used_as_fallback(tmp_path):
    path = write(tmp_path / "SPY.csv", "Date,Close\n2026-09-30,100\n")
    with pytest.raises(ValueError, match="raw Close is not an acceptable fallback"):
        module.normalize_file(path, "yahoo_finance", "yf", "SPY")


def test_duplicate_observation_date_is_rejected(tmp_path):
    path = write(tmp_path / "SPY.csv", "Date,Adj Close\n2026-09-30,101\n2026-09-30,102\n")
    with pytest.raises(ValueError, match="duplicate observation date"):
        module.normalize_file(path, "yahoo_finance", "yf", "SPY")


def test_nonpositive_adjusted_close_is_rejected(tmp_path):
    path = write(tmp_path / "SPY.csv", "Date,Adj Close\n2026-09-30,0\n")
    with pytest.raises(ValueError, match="finite and positive"):
        module.normalize_file(path, "yahoo_finance", "yf", "SPY")


def test_non_usd_currency_is_rejected(tmp_path):
    path = write(tmp_path / "SPY.csv", "Date,Adj Close\n2026-09-30,100\n")
    with pytest.raises(ValueError, match="explicitly USD"):
        module.normalize_file(path, "yahoo_finance", "yf", "SPY", "KRW")


def test_invalid_date_is_rejected(tmp_path):
    path = write(tmp_path / "SPY.csv", "timestamp,adjusted close\n2026-09,100\n")
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        module.normalize_file(path, "alpha_vantage", "av", "SPY")
