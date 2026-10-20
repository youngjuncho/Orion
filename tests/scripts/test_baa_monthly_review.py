"""Tests for the manual, plan-only-by-default BAA monthly review entrypoint."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("baa_monthly_review", ROOT / "scripts/baa/run_baa_monthly_review.py")
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_default_monthly_review_is_plan_only_and_does_not_write_or_call_subprocess(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("ORION_ALPHA_VANTAGE_API_KEY", raising=False)
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("subprocess must not run in plan-only mode")))
    output_root = tmp_path / "review-output"

    code = module.main(["--run-month", "2026-10", "--output-root", str(output_root)])

    output = capsys.readouterr().out
    assert code == 0
    assert "PLAN ONLY" in output
    assert "no network requests" in output
    assert not output_root.exists()


def test_live_mode_without_local_api_key_stops_before_any_collection(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("ORION_ALPHA_VANTAGE_API_KEY", raising=False)
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("collection must not start without key")))

    code = module.main(["--run-month", "2026-10", "--output-root", str(tmp_path), "--confirm-live-data-fetch"])

    assert code == 2
    assert "no collection started" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


def test_invalid_run_month_is_rejected(tmp_path):
    try:
        module.main(["--run-month", "2026-13", "--output-root", str(tmp_path)])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("invalid run month should be rejected")
    assert list(tmp_path.iterdir()) == []
