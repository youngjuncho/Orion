"""Safety checks for the opt-in Alpha Vantage live-contract CLI."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_alpha_vantage_live_contract.py"


def test_live_contract_script_exits_before_network_when_key_is_missing() -> None:
    env = os.environ.copy()
    env.pop("ORION_ALPHA_VANTAGE_API_KEY", None)

    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )

    assert result.returncode == 2
    assert result.stdout.strip() == (
        "NOT RUN: ORION_ALPHA_VANTAGE_API_KEY is not configured."
    )
    assert result.stderr == ""
    assert "https://" not in result.stdout
    assert "apikey" not in result.stdout.lower()


def _load_script_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "check_alpha_vantage_live_contract_under_test", SCRIPT
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_live_contract_script_success_output_contains_only_coverage_metadata(
    monkeypatch, capsys
) -> None:
    from data.contracts import MarketDataPoint, MarketDataSet

    module = _load_script_module()
    monkeypatch.setenv("ORION_ALPHA_VANTAGE_API_KEY", "test-secret-key")

    observations = tuple(
        MarketDataPoint(
            symbol=symbol,
            field="adjusted_close",
            observed_at=f"{2025 + (month - 1) // 12}-{((month - 1) % 12) + 1:02d}-28",
            value=100.0 + month,
            source="alpha_vantage",
            currency="USD",
        )
        for symbol in ("VTI", "VEU", "SGOV")
        for month in range(1, 14)
    )
    dataset = MarketDataSet(observations=observations, as_of="2026-10-12")

    class FakeProvider:
        def __init__(self, _source):
            pass

        def load(self):
            return dataset

    monkeypatch.setattr(module, "AlphaVantageMonthlyAdjustedProvider", FakeProvider)
    assert module.main() == 0

    output = capsys.readouterr()
    assert output.err == ""
    assert "LIVE RESPONSE CONTRACT CHECK: PASS" in output.out
    assert "VTI: PASS (observations=13, oldest=2025-01-28, latest=2026-01-28)" in output.out
    assert "VEU: PASS (observations=13" in output.out
    assert "SGOV: PASS (observations=13" in output.out
    assert "test-secret-key" not in output.out
    assert "https://" not in output.out
    assert "100.0" not in output.out


def test_live_contract_script_suppresses_unexpected_exception_details(
    monkeypatch, capsys
) -> None:
    module = _load_script_module()
    monkeypatch.setenv("ORION_ALPHA_VANTAGE_API_KEY", "test-secret-key")

    class FakeProvider:
        def __init__(self, _source):
            pass

        def load(self):
            raise RuntimeError("credential=test-secret-key https://example.invalid")

    monkeypatch.setattr(module, "AlphaVantageMonthlyAdjustedProvider", FakeProvider)
    assert module.main() == 1

    output = capsys.readouterr()
    assert output.out == (
        "LIVE CONTRACT CHECK FAILED: unexpected error (details suppressed).\n"
    )
    assert output.err == ""
    assert "test-secret-key" not in output.out
    assert "https://" not in output.out


def test_live_contract_script_rejects_duplicate_observation_dates_without_partial_pass(
    monkeypatch, capsys
) -> None:
    from types import SimpleNamespace
    from data.contracts import MarketDataPoint

    module = _load_script_module()
    monkeypatch.setenv("ORION_ALPHA_VANTAGE_API_KEY", "test-secret-key")
    observations = []
    for symbol in ("VTI", "VEU", "SGOV"):
        for month in range(1, 14):
            year = 2025 + (month - 1) // 12
            month_number = ((month - 1) % 12) + 1
            day = 28
            if symbol == "VTI" and month == 13:
                year, month_number, day = 2025, 1, 28  # duplicate VTI date
            observations.append(
                MarketDataPoint(
                    symbol=symbol,
                    field="adjusted_close",
                    observed_at=f"{year}-{month_number:02d}-{day:02d}",
                    value=100.0 + month,
                    source="alpha_vantage",
                    currency="USD",
                )
            )
    # Use a deliberately malformed provider result to exercise the CLI's own
    # boundary check; the canonical MarketDataSet correctly rejects duplicates.
    dataset = SimpleNamespace(observations=tuple(observations), as_of="2026-10-12")

    class FakeProvider:
        def __init__(self, _source):
            pass

        def load(self):
            return dataset

    monkeypatch.setattr(module, "AlphaVantageMonthlyAdjustedProvider", FakeProvider)
    assert module.main() == 1
    output = capsys.readouterr()
    assert output.out == (
        "LIVE CONTRACT CHECK FAILED: duplicate observation dates for VTI.\n"
    )
    assert output.err == ""


def test_live_contract_script_rejects_invalid_batch_date(monkeypatch, capsys) -> None:
    from data.contracts import MarketDataPoint, MarketDataSet

    module = _load_script_module()
    monkeypatch.setenv("ORION_ALPHA_VANTAGE_API_KEY", "test-secret-key")
    observations = tuple(
        MarketDataPoint(
            symbol=symbol,
            field="adjusted_close",
            observed_at=f"{2025 + (month - 1) // 12}-{((month - 1) % 12) + 1:02d}-28",
            value=100.0 + month,
            source="alpha_vantage",
            currency="USD",
        )
        for symbol in ("VTI", "VEU", "SGOV")
        for month in range(1, 14)
    )
    dataset = MarketDataSet(observations=observations, as_of="not-a-date")

    class FakeProvider:
        def __init__(self, _source):
            pass

        def load(self):
            return dataset

    monkeypatch.setattr(module, "AlphaVantageMonthlyAdjustedProvider", FakeProvider)
    assert module.main() == 1
    output = capsys.readouterr()
    assert output.out == "LIVE CONTRACT CHECK FAILED: invalid batch date.\n"
    assert output.err == ""


def test_live_contract_script_rejects_observation_after_batch_date(
    monkeypatch, capsys
) -> None:
    from types import SimpleNamespace
    from data.contracts import MarketDataPoint

    module = _load_script_module()
    monkeypatch.setenv("ORION_ALPHA_VANTAGE_API_KEY", "test-secret-key")
    observations = tuple(
        MarketDataPoint(
            symbol=symbol,
            field="adjusted_close",
            observed_at=("2026-10-13" if symbol == "VTI" and month == 13 else
                         f"{2025 + (month - 1) // 12}-{((month - 1) % 12) + 1:02d}-28"),
            value=100.0 + month,
            source="alpha_vantage",
            currency="USD",
        )
        for symbol in ("VTI", "VEU", "SGOV")
        for month in range(1, 14)
    )
    dataset = SimpleNamespace(observations=observations, as_of="2026-10-12")

    class FakeProvider:
        def __init__(self, _source):
            pass

        def load(self):
            return dataset

    monkeypatch.setattr(module, "AlphaVantageMonthlyAdjustedProvider", FakeProvider)
    assert module.main() == 1
    output = capsys.readouterr()
    assert output.out == (
        "LIVE CONTRACT CHECK FAILED: observation date is later than batch date for VTI.\n"
    )
    assert output.err == ""


def test_live_contract_script_rejects_multiple_monthly_bars(monkeypatch, capsys) -> None:
    from types import SimpleNamespace
    from data.contracts import MarketDataPoint

    module = _load_script_module()
    monkeypatch.setenv("ORION_ALPHA_VANTAGE_API_KEY", "test-secret-key")
    observations = []
    for symbol in ("VTI", "VEU", "SGOV"):
        for month in range(1, 14):
            year = 2025 + (month - 1) // 12
            month_number = ((month - 1) % 12) + 1
            day = 28
            observations.append(
                MarketDataPoint(
                    symbol=symbol,
                    field="adjusted_close",
                    observed_at=f"{year}-{month_number:02d}-{day:02d}",
                    value=100.0 + month,
                    source="alpha_vantage",
                    currency="USD",
                )
            )
        if symbol == "VTI":
            observations.append(
                MarketDataPoint(
                    symbol=symbol,
                    field="adjusted_close",
                    observed_at="2025-01-29",
                    value=101.5,
                    source="alpha_vantage",
                    currency="USD",
                )
            )
    dataset = SimpleNamespace(observations=tuple(observations), as_of="2026-10-12")

    class FakeProvider:
        def __init__(self, _source):
            pass

        def load(self):
            return dataset

    monkeypatch.setattr(module, "AlphaVantageMonthlyAdjustedProvider", FakeProvider)
    assert module.main() == 1
    output = capsys.readouterr()
    assert output.out == "LIVE CONTRACT CHECK FAILED: multiple monthly bars for VTI.\n"
    assert output.err == ""
