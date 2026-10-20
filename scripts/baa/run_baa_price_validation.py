#!/usr/bin/env python3
"""Run the offline BAA provider CSV validation pipeline.

This command only reads existing provider CSV exports. It never fetches data,
reads API keys, or activates BAA. It normalizes both source directories,
checks panel completeness, compares month-end observation dates and adjusted
prices, and writes a JSON report for auditability.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SYMBOLS = ("SPY", "VWO", "VEA", "BND", "QQQ", "IWM", "VGK", "EWJ", "VNQ", "DBC", "GLD", "TLT", "HYG", "LQD", "TIP", "BIL", "IEF")


def _load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validation module: {relative}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


normalizer = _load_module("baa_validation_normalizer", "scripts/baa/normalize_provider_price_exports.py")
comparator = _load_module("baa_validation_comparator", "scripts/baa/compare_monthly_price_exports.py")


def _normalize_directory(directory: Path, provider: str, label: str, expected: tuple[str, ...]) -> list[dict[str, str]]:
    if not directory.is_dir():
        raise ValueError(f"provider input directory does not exist: {directory}")
    files = sorted(directory.glob("*.csv"))
    if not files:
        raise ValueError(f"no CSV files found in {directory}")
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in files:
        symbol = normalizer._symbol_from_filename(path)
        if symbol in seen:
            raise ValueError(f"duplicate input ticker {symbol} in {directory}")
        seen.add(symbol)
        rows.extend(normalizer.normalize_file(path, provider, label, symbol, "USD"))
    unexpected = sorted(seen - set(expected))
    missing = sorted(set(expected) - seen)
    if unexpected or missing:
        raise ValueError(f"{label} symbol coverage mismatch; missing={missing}, unexpected={unexpected}")
    return sorted(rows, key=lambda row: (row["symbol"], row["month"]))


def _write_normalized(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=normalizer.OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _panel_check(rows: list[dict[str, str]], expected: tuple[str, ...], minimum_months: int) -> dict[str, object]:
    months_by_symbol: dict[str, set[str]] = {symbol: set() for symbol in expected}
    for row in rows:
        months_by_symbol[row["symbol"]].add(row["month"])
    month_sets = {tuple(sorted(months)) for months in months_by_symbol.values()}
    common_months = sorted(set.intersection(*(months_by_symbol[symbol] for symbol in expected))) if expected else []
    incomplete = {symbol: sorted(months_by_symbol[symbol]) for symbol in expected if len(months_by_symbol[symbol]) < minimum_months}
    same_month_panel = len(month_sets) == 1
    return {
        "symbols": len(months_by_symbol),
        "months": common_months,
        "month_count": len(common_months),
        "minimum_months_required": minimum_months,
        "same_month_panel": same_month_panel,
        "symbols_below_minimum_months": incomplete,
        "passed": same_month_panel and len(common_months) >= minimum_months and not incomplete,
    }


def _write_markdown_report(path: Path, report: dict[str, object]) -> None:
    """Write a concise human-readable summary alongside the machine report."""
    comparison = report["comparison"]
    left_panel = report["left_panel"]
    right_panel = report["right_panel"]
    assert isinstance(comparison, dict) and isinstance(left_panel, dict) and isinstance(right_panel, dict)

    def status(passed: bool) -> str:
        return "PASS" if passed else "FAIL"

    checks = [
        ("Alpha Vantage symbol/month panel", bool(left_panel["passed"])),
        ("Yahoo Finance symbol/month panel", bool(right_panel["passed"])),
        ("Cross-provider observation coverage", not comparison["missing_left"] and not comparison["missing_right"]),
        ("Observation-date alignment", not comparison["date_mismatches"]),
        ("Currency consistency", not comparison["currency_mismatches"]),
        (f"Adjusted-price difference <= {report['tolerance_pct']}%", not comparison["price_mismatches"]),
    ]
    lines = [
        "# BAA Monthly Price-Data Validation",
        "",
        f"**Overall screening result: {status(bool(report['passed']))}**",
        "",
        "This is an offline comparison of supplied exports. It does not approve a provider, establish total-return equivalence, activate BAA, or authorize trading.",
        "",
        "## Coverage",
        "",
        f"- Required symbols: {len(report['expected_symbols'])}",
        f"- Alpha Vantage: {left_panel['symbols']} symbols, {left_panel['month_count']} common months (minimum {left_panel['minimum_months_required']})",
        f"- Yahoo Finance: {right_panel['symbols']} symbols, {right_panel['month_count']} common months (minimum {right_panel['minimum_months_required']})",
        f"- Matched observations: {comparison['matched_observations']}",
        f"- Maximum absolute relative adjusted-price difference: {comparison['max_abs_pct_difference']}%",
        f"- Configured price-difference tolerance: {report['tolerance_pct']}%",
        "",
        "## Automated quality gates",
        "",
        "| Check | Result |",
        "|---|---|",
    ]
    lines.extend(f"| {name} | **{status(ok)}** |" for name, ok in checks)
    lines.extend(["", "## Exceptions", ""])
    exception_groups = (
        ("Missing from Alpha Vantage", comparison["missing_left"]),
        ("Missing from Yahoo Finance", comparison["missing_right"]),
        ("Observation-date mismatches", comparison["date_mismatches"]),
        ("Currency mismatches", comparison["currency_mismatches"]),
        ("Adjusted-price mismatches", comparison["price_mismatches"]),
    )
    any_exception = False
    for heading, values in exception_groups:
        if values:
            any_exception = True
            lines.append(f"### {heading}")
            lines.extend(f"- {value}" for value in values)
            lines.append("")
    if not any_exception:
        lines.append("No automated comparison exceptions were detected.")
        lines.append("")
    lines.extend([
        "## Manual review still required",
        "",
        "- Confirm the latest included month is a completed month; do not use the current partial month as a signal month.",
        "- Confirm provider access terms, endpoint entitlement, and quota before any live collection.",
        "- Review known split/dividend events and verify adjustment semantics against an independently documented reference.",
        "- Investigate every FAIL; do not silently drop symbols, fill missing values, mix providers within a signal window, or relax thresholds without a documented decision.",
        "- A PASS is only a screening result, not proof of total-return equivalence or provider approval.",
        "",
        "## Execution provenance",
        "",
        f"- Mode: `{report['mode']}`",
        f"- Network requests by validator: {report['network_requests']}",
        f"- API keys read by validator: {report['api_keys_read']}",
        f"- Provider approved by this report: {report['provider_approval']}",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(left_dir: Path, right_dir: Path, output_dir: Path, *, tolerance_pct: float, minimum_months: int, expected: tuple[str, ...]) -> dict[str, object]:
    left_rows = _normalize_directory(left_dir, "alpha_vantage", "alpha_vantage", expected)
    right_rows = _normalize_directory(right_dir, "yahoo_finance", "yahoo_finance", expected)
    left_panel = _panel_check(left_rows, expected, minimum_months)
    right_panel = _panel_check(right_rows, expected, minimum_months)
    output_dir.mkdir(parents=True, exist_ok=True)
    left_path = output_dir / "alpha_vantage_normalized.csv"
    right_path = output_dir / "yahoo_finance_normalized.csv"
    _write_normalized(left_path, left_rows)
    _write_normalized(right_path, right_rows)
    comparison = comparator.compare(
        comparator.load_csv(left_path, "alpha_vantage"),
        comparator.load_csv(right_path, "yahoo_finance"),
        tolerance_pct=tolerance_pct,
        expected_symbols=expected,
    )
    report: dict[str, object] = {
        "mode": "offline_only",
        "network_requests": 0,
        "api_keys_read": False,
        "provider_approval": False,
        "expected_symbols": list(expected),
        "tolerance_pct": tolerance_pct,
        "left_panel": left_panel,
        "right_panel": right_panel,
        "comparison": asdict(comparison),
        "outputs": {"alpha_vantage_normalized_csv": str(left_path), "yahoo_finance_normalized_csv": str(right_path)},
        "passed": bool(left_panel["passed"] and right_panel["passed"] and comparison.passed),
        "limitations": [
            "Passing is a data-comparison screen, not proof of total-return equivalence or provider quality.",
            "Monthly last-observation alignment does not independently prove final exchange-session close.",
            "No live provider requests were made by this command.",
        ],
    }
    (output_dir / "baa_price_validation_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_markdown_report(output_dir / "baa_price_validation_summary.md", report)
    return report


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alpha-vantage-dir", type=Path, required=True, help="directory containing SYMBOL.csv raw Alpha Vantage exports")
    parser.add_argument("--yahoo-finance-dir", type=Path, required=True, help="directory containing SYMBOL.csv raw Yahoo Finance exports")
    parser.add_argument("--output-dir", type=Path, required=True, help="directory for normalized CSVs and JSON report")
    parser.add_argument("--tolerance-pct", type=float, default=0.05, help="maximum relative adjusted-price difference in percent")
    parser.add_argument("--minimum-months", type=int, default=13, help="minimum complete monthly observations per symbol (default: 13)")
    parser.add_argument("--expected-symbols", default=",".join(DEFAULT_SYMBOLS), help="comma-separated required symbols")
    args = parser.parse_args(argv)
    expected = tuple(symbol.strip().upper() for symbol in args.expected_symbols.split(",") if symbol.strip())
    if not expected or len(set(expected)) != len(expected):
        parser.error("--expected-symbols must contain unique, non-empty symbols")
    if args.minimum_months < 1 or not math.isfinite(args.tolerance_pct) or args.tolerance_pct < 0:
        parser.error("--minimum-months must be positive and --tolerance-pct finite and non-negative")
    try:
        report = run(args.alpha_vantage_dir, args.yahoo_finance_dir, args.output_dir, tolerance_pct=args.tolerance_pct, minimum_months=args.minimum_months, expected=expected)
    except (OSError, ValueError) as exc:
        print(f"validation error: {exc}", file=sys.stderr)
        return 2
    print(f"Offline BAA price validation: {'PASS' if report['passed'] else 'FAIL'}")
    print(f"JSON report: {args.output_dir / 'baa_price_validation_report.json'}")
    print(f"Human-readable summary: {args.output_dir / 'baa_price_validation_summary.md'}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
