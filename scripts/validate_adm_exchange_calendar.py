"""Offline validation probe for the optional exchange_calendars ADM adapter.

Run from the repository root with the candidate package installed in the active
interpreter. This script does not modify configuration or activate Moon ADM.
"""
from __future__ import annotations

import sys
from datetime import date
from importlib.metadata import version
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

try:
    import exchange_calendars as xc
except ImportError as exc:  # provide a clear, non-mutating failure
    raise SystemExit(
        "exchange_calendars is not installed in this interpreter; "
        "run this script using the isolated audit environment."
    ) from exc

from orion.frameworks.moon.adm_calendar import resolve_adm_month_end_cutoff


class ExchangeCalendarAdapter:
    """Small experiment implementing the existing provider-neutral protocol."""

    def __init__(self, calendar_name: str) -> None:
        self._calendar = xc.get_calendar(calendar_name)
        self.calendar_id = calendar_name
        self.calendar_version = f"exchange-calendars=={version('exchange-calendars')}"

    def is_session(self, session_date: date) -> bool:
        # ISO date labels avoid passing timezone-aware timestamps into the API.
        return bool(self._calendar.is_session(session_date.isoformat()))


def check(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")
    print(f"PASS {label}: {actual}")


def main() -> int:
    calendar = ExchangeCalendarAdapter("XNYS")
    print(f"calendar_id: {calendar.calendar_id}")
    print(f"calendar_version: {calendar.calendar_version}")

    known_sessions = {
        date(2026, 10, 30): True,
        date(2026, 10, 31): False,
        date(2026, 11, 26): False,
        date(2026, 11, 27): True,
        date(2026, 11, 30): True,
    }
    for session_date, expected in known_sessions.items():
        check(f"is_session({session_date.isoformat()})", calendar.is_session(session_date), expected)

    # May 2026 ends on Sunday; the immediately preceding XNYS session is Friday.
    may_cutoff = resolve_adm_month_end_cutoff(2026, 5, calendar=calendar)
    check("May calendar month-end", may_cutoff.calendar_month_end, date(2026, 5, 31))
    check("May evaluation cutoff", may_cutoff.evaluation_cutoff, date(2026, 5, 29))
    check("May cutoff calendar id", may_cutoff.calendar_id, "XNYS")
    check(
        "May cutoff calendar version",
        may_cutoff.calendar_version,
        calendar.calendar_version,
    )

    # October 2026 ends on Saturday; the immediately preceding session is Friday.
    october_cutoff = resolve_adm_month_end_cutoff(2026, 10, calendar=calendar)
    check("October evaluation cutoff", october_cutoff.evaluation_cutoff, date(2026, 10, 30))

    # November 2026 ends on a trading Monday, so the month-end itself is used.
    november_cutoff = resolve_adm_month_end_cutoff(2026, 11, calendar=calendar)
    check("November evaluation cutoff", november_cutoff.evaluation_cutoff, date(2026, 11, 30))

    print("RESULT: all adapter and cutoff checks passed")
    print("LIMIT: XNYS-only probe; not an approved instrument mapping or runtime integration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
