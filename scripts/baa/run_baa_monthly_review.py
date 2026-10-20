#!/usr/bin/env python3
"""Run the manually initiated monthly BAA data review.

Default behavior is plan-only: no network requests, no API-key reads, and no
filesystem writes. Live collection is attempted only when the operator supplies
--confirm-live-data-fetch. This is not a scheduler and does not activate BAA or
place orders.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
COLLECTOR = ROOT / "scripts" / "baa" / "collect_provider_price_exports.py"
VALIDATOR = ROOT / "scripts" / "baa" / "run_baa_price_validation.py"


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-month", default=date.today().strftime("%Y-%m"), help="label for this manual review, YYYY-MM (default: current month)")
    parser.add_argument("--output-root", type=Path, default=Path("./data/baa/monthly"), help="root directory for this review's raw exports and report")
    parser.add_argument("--minimum-months", type=int, default=13)
    parser.add_argument("--tolerance-pct", type=float, default=0.05)
    parser.add_argument("--confirm-live-data-fetch", action="store_true", help="explicitly authorize live requests to both providers")
    parser.add_argument("--overwrite", action="store_true", help="allow replacing existing raw ticker exports for this run-month")
    args = parser.parse_args(argv)

    import re
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", args.run_month):
        parser.error("--run-month must be YYYY-MM")
    if args.minimum_months < 1 or args.tolerance_pct < 0:
        parser.error("--minimum-months must be positive and --tolerance-pct nonnegative")

    run_root = args.output_root / args.run_month
    av_dir = run_root / "raw" / "alpha_vantage"
    yahoo_dir = run_root / "raw" / "yahoo_finance"
    report_dir = run_root / "validation"

    if not args.confirm_live_data_fetch:
        print("PLAN ONLY — no network requests, API-key reads, or filesystem writes.")
        print(f"Review label: {args.run_month}")
        print("Planned steps: collect Alpha Vantage exports; collect Yahoo Finance exports; normalize and compare offline; write a validation report.")
        print(f"Output root (not created): {run_root}")
        print("No scheduler, BAA activation, or order execution is involved.")
        print("Live collection requires a separate explicit invocation with --confirm-live-data-fetch.")
        return 0

    # Check the secret before starting either provider so a missing key cannot
    # cause an unnecessary first-provider request followed by a predictable stop.
    if not os.environ.get("ORION_ALPHA_VANTAGE_API_KEY"):
        print("error: ORION_ALPHA_VANTAGE_API_KEY is not set locally; no collection started", file=sys.stderr)
        return 2

    commands = [
        [sys.executable, str(COLLECTOR), "--provider", "alpha_vantage", "--output-dir", str(av_dir), "--confirm-live-data-fetch"],
        [sys.executable, str(COLLECTOR), "--provider", "yahoo_finance", "--output-dir", str(yahoo_dir), "--confirm-live-data-fetch"],
    ]
    if args.overwrite:
        commands = [command + ["--overwrite"] for command in commands]
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            print("error: collection stopped; do not treat this month's dataset as complete", file=sys.stderr)
            print("Any already-collected raw exports are retained for inspection; no validation report was produced.", file=sys.stderr)
            return result.returncode or 1

    validation_command = [
        sys.executable, str(VALIDATOR),
        "--alpha-vantage-dir", str(av_dir),
        "--yahoo-finance-dir", str(yahoo_dir),
        "--output-dir", str(report_dir),
        "--minimum-months", str(args.minimum_months),
        "--tolerance-pct", str(args.tolerance_pct),
    ]
    result = subprocess.run(validation_command, cwd=ROOT, check=False)
    if result.returncode != 0:
        print("Review completed with validation failure; inspect the report before any provider decision.", file=sys.stderr)
    print(f"Monthly review output: {run_root}")
    print("This workflow only collects and validates provider data; it does not activate BAA or trade.")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
