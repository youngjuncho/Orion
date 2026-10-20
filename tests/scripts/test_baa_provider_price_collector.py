import importlib.util
import json
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "baa" / "collect_provider_price_exports.py"
spec = importlib.util.spec_from_file_location("baa_provider_price_collector", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_plan_only_does_not_read_key_or_make_network_request(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("ORION_ALPHA_VANTAGE_API_KEY", raising=False)
    monkeypatch.setattr(module, "_request_bytes", lambda *args, **kwargs: pytest.fail("network must not be called"))
    code = module.main(["--provider", "alpha_vantage", "--output-dir", str(tmp_path), "--symbols", "SPY"])
    assert code == 0
    assert "PLAN ONLY" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_live_collection_requires_local_alpha_vantage_environment_key(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("ORION_ALPHA_VANTAGE_API_KEY", raising=False)
    code = module.main(["--provider", "alpha_vantage", "--output-dir", str(tmp_path), "--symbols", "SPY", "--confirm-live-data-fetch"])
    assert code == 2
    assert "not set" in capsys.readouterr().err


def test_alpha_vantage_json_throttle_response_is_rejected(monkeypatch):
    monkeypatch.setattr(module, "_request_bytes", lambda *args, **kwargs: b'{"Note":"API rate limit"}')
    with pytest.raises(module.CollectionError, match="rate limit"):
        module.fetch_alpha_vantage_csv("SPY", "dummy-local-test-key")


def test_yahoo_chart_json_is_exported_as_daily_adjusted_close_csv(monkeypatch):
    response = {
        "chart": {"result": [{
            "timestamp": [1790726400],
            "indicators": {
                "quote": [{"open": [10], "high": [12], "low": [9], "close": [11], "volume": [100]}],
                "adjclose": [{"adjclose": [10.5]}],
            },
        }], "error": None}
    }
    monkeypatch.setattr(module, "_request_bytes", lambda *args, **kwargs: json.dumps(response).encode())
    text = module.fetch_yahoo_finance_csv("SPY")
    assert "Date,Open,High,Low,Close,Adj Close,Volume" in text
    assert ",10.5,100" in text


def test_collector_refuses_to_overwrite_without_explicit_option(tmp_path):
    (tmp_path / "SPY.csv").write_text("old", encoding="utf-8")
    with pytest.raises(module.CollectionError, match="refusing to overwrite"):
        module.collect("yahoo_finance", ["SPY"], tmp_path, fetch_yahoo=lambda symbol: "Date,Adj Close\n2026-09-30,1\n")


def test_collector_writes_provider_csv_using_injected_offline_fetcher(tmp_path):
    saved = module.collect(
        "yahoo_finance", ["SPY", "BND"], tmp_path,
        fetch_yahoo=lambda symbol: f"Date,Adj Close\n2026-09-30,{100 if symbol == 'SPY' else 90}\n",
        sleep=lambda seconds: pytest.fail("Yahoo collection should not delay"),
    )
    assert [path.name for path in saved] == ["SPY.csv", "BND.csv"]
    assert "100" in (tmp_path / "SPY.csv").read_text(encoding="utf-8")


def test_duplicate_or_invalid_symbols_are_rejected_before_collection(tmp_path, capsys):
    code = module.main(["--provider", "yahoo_finance", "--output-dir", str(tmp_path), "--symbols", "SPY", "SPY"])
    assert code == 2
    assert "valid, unique ticker" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


def test_provider_failure_does_not_leave_partial_export_set(tmp_path):
    def fetch(symbol):
        if symbol == "BND":
            raise module.CollectionError("simulated provider failure")
        return "Date,Adj Close\n2026-09-30,100\n"

    with pytest.raises(module.CollectionError, match="simulated provider failure"):
        module.collect("yahoo_finance", ["SPY", "BND"], tmp_path, fetch_yahoo=fetch)
    assert list(tmp_path.iterdir()) == []


def test_malformed_header_is_rejected_before_any_export_is_written(tmp_path):
    def fetch(symbol):
        if symbol == "BND":
            return "Date,,Adj Close\n2026-09-30,100,99\n"
        return "Date,Adj Close\n2026-09-30,100\n"

    with pytest.raises(module.CollectionError, match="malformed CSV"):
        module.collect("yahoo_finance", ["SPY", "BND"], tmp_path, fetch_yahoo=fetch)
    assert list(tmp_path.iterdir()) == []
