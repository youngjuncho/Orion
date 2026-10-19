"""Offline audit of exchange_calendars alias behavior for proposed US ETF mapping.

This checks package behavior only. It does not independently establish that two
listing venues have identical official schedules, and does not approve runtime use.
Run with the isolated audit environment and exchange-calendars==4.13.2 installed.
"""
from __future__ import annotations

from datetime import date
from importlib.metadata import version
import exchange_calendars as xc

EXPECTED_VERSION = "4.13.2"

def main() -> int:
    actual_version = version("exchange-calendars")
    print(f"exchange-calendars: {actual_version}")
    if actual_version != EXPECTED_VERSION:
        raise SystemExit(f"expected exchange-calendars=={EXPECTED_VERSION}, got {actual_version}")

    xnys_name = xc.resolve_alias("XNYS")
    arcx_name = xc.resolve_alias("ARCX")
    print(f"resolve_alias(XNYS): {xnys_name}")
    print(f"resolve_alias(ARCX): {arcx_name}")
    if xnys_name != "XNYS" or arcx_name != "XNYS":
        raise SystemExit("Unexpected canonical calendar resolution; proposed mapping needs re-review")

    xnys = xc.get_calendar("XNYS")
    arcx = xc.get_calendar("ARCX")
    if xnys is not arcx:
        raise SystemExit("XNYS and ARCX did not resolve to the same calendar object")
    print("PASS: XNYS and ARCX resolve to the same XNYS calendar object")

    # Deterministic sample around the documented SGOV listing-venue transition.
    samples = {
        date(2026, 2, 16): False,  # US Presidents Day
        date(2026, 2, 20): True,
        date(2026, 2, 21): False,
        date(2026, 2, 23): True,
        date(2026, 2, 27): True,
    }
    for day, expected in samples.items():
        got = bool(xnys.is_session(day.isoformat()))
        print(f"{day.isoformat()} XNYS session={got} expected={expected}")
        if got != expected:
            raise SystemExit(f"Unexpected XNYS session result for {day}: {got}")

    print("RESULT: package alias and sample-session checks passed")
    print("LIMIT: alias behavior is package policy, not independent proof of official ARCX/XNYS schedule equivalence")
    print("LIMIT: mapping policy is approved; this probe does not connect or modify ADM runtime")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
