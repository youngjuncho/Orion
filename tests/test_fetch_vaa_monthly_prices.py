"""Offline tests for the opt-in VAA monthly price acquisition CLI."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "fetch_vaa_monthly_prices.py"


def load_module():
    spec = importlib.util.spec_from_file_location("fetch_vaa_monthly_prices_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fake_transport_factory(module, *, missing_symbol=None):
    calls = []
    def transport(url, timeout):
        from urllib.parse import parse_qs, urlparse
        query = parse_qs(urlparse(url).query)
        symbol = query["symbol"][0]
        calls.append(symbol)
        series = {}
        for year, month in ((2025, m) for m in range(9, 13)):
            series[f"{year}-{month:02d}-28"] = {"5. adjusted close": "100.0"}
        for month in range(1, 10):
            series[f"2026-{month:02d}-28"] = {"5. adjusted close": "101.0"}
        if symbol == missing_symbol:
            series.pop("2026-09-28")
        payload = {"Meta Data": {"2. Symbol": symbol}, "Monthly Adjusted Time Series": series}
        return json.dumps(payload).encode()
    return transport, calls


def test_fetch_builds_aligned_completed_month_data_without_real_network():
    module = load_module()
    transport, calls = fake_transport_factory(module)
    sleeps = []
    labels, prices, manifest = module.fetch_monthly_prices(
        "secret", date(2026, 10, 20), transport=transport,
        sleep=sleeps.append, min_interval_seconds=13,
    )
    assert len(calls) == 14
    assert len(set(calls)) == 14
    assert len(sleeps) == 13
    assert len(labels) == 13
    assert labels[0] == "2025-09-30"
    assert labels[-1] == "2026-09-30"
    assert set(prices) == set(module.SYMBOLS)
    assert manifest["last_completed_month"] == "2026-09"
    assert manifest["latest_provider_observation_dates"]["SPY"] == "2026-09-28"


def test_fetch_fails_closed_if_any_symbol_lacks_last_completed_month():
    module = load_module()
    transport, _ = fake_transport_factory(module, missing_symbol="EWJ")
    try:
        module.fetch_monthly_prices(
            "secret", date(2026, 10, 20), transport=transport,
            sleep=lambda _: None, min_interval_seconds=0,
        )
    except module.FetchError as exc:
        assert "EWJ" in str(exc)
        assert "no CSV written" in str(exc)
    else:
        raise AssertionError("missing last completed month must fail closed")


def test_write_outputs_creates_expected_csv_and_provenance_manifest(tmp_path):
    module = load_module()
    transport, _ = fake_transport_factory(module)
    labels, prices, manifest = module.fetch_monthly_prices(
        "secret", date(2026, 10, 20), transport=transport,
        sleep=lambda _: None, min_interval_seconds=0,
    )
    output = tmp_path / "prices.csv"
    module.write_outputs(output, labels, prices, manifest)
    with output.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    assert rows[0] == ["Date", *module.OFFENSIVE, "SHY", "IEF"]
    assert len(rows) == 14
    sidecar = json.loads((tmp_path / "prices.csv.manifest.json").read_text(encoding="utf-8"))
    assert sidecar["provider"] == "Alpha Vantage"
    assert sidecar["adjustment_basis"].startswith("provider-adjusted")
    assert sidecar["csv_sha256"] == hashlib.sha256(output.read_bytes()).hexdigest()


def test_cli_exits_before_network_when_api_key_is_missing():
    env = os.environ.copy()
    env.pop("ORION_ALPHA_VANTAGE_API_KEY", None)
    result = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=ROOT, env=env,
        capture_output=True, text=True, check=False, timeout=10,
    )
    assert result.returncode == 2
    assert result.stdout.strip() == "NOT RUN: ORION_ALPHA_VANTAGE_API_KEY is not configured."
    assert result.stderr == ""
    assert "https://" not in result.stdout
    assert "apikey" not in result.stdout.lower()
