"""Optional real-package acceptance tests for the pinned XNYS adapter.

These tests are skipped in environments without the exact approved dependency;
run them in the isolated `orion-calendar-audit` environment. They never call a
market-data provider and do not wire the calendar into ADM runtime.
"""
from datetime import date
from importlib.metadata import PackageNotFoundError, version

import pytest

from orion.frameworks.moon.adm_calendar import resolve_adm_month_end_cutoff
from orion.frameworks.moon.adm_exchange_calendar import (
    PINNED_PACKAGE_VERSION,
    ExchangeCalendarsAdapter,
)

try:
    installed_version = version("exchange-calendars")
except PackageNotFoundError:
    installed_version = None

pytestmark = pytest.mark.skipif(
    installed_version != PINNED_PACKAGE_VERSION,
    reason=f"requires exchange-calendars=={PINNED_PACKAGE_VERSION}; installed={installed_version!r}",
)


def test_real_xnys_month_end_weekend_cutoff():
    calendar = ExchangeCalendarsAdapter("XNYS")
    result = resolve_adm_month_end_cutoff(2026, 10, calendar=calendar)
    assert result.calendar_month_end == date(2026, 10, 31)
    assert result.evaluation_cutoff == date(2026, 10, 30)
    assert result.calendar_id == "XNYS"
    assert result.calendar_version == "exchange-calendars==4.13.2"


def test_real_xnys_month_end_session_is_preserved():
    calendar = ExchangeCalendarsAdapter("XNYS")
    result = resolve_adm_month_end_cutoff(2026, 11, calendar=calendar)
    assert result.calendar_month_end == date(2026, 11, 30)
    assert result.evaluation_cutoff == date(2026, 11, 30)


def test_real_xnys_february_weekend_and_leap_year_cutoffs():
    calendar = ExchangeCalendarsAdapter("XNYS")
    non_leap = resolve_adm_month_end_cutoff(2026, 2, calendar=calendar)
    leap = resolve_adm_month_end_cutoff(2024, 2, calendar=calendar)
    assert non_leap.calendar_month_end == date(2026, 2, 28)
    assert non_leap.evaluation_cutoff == date(2026, 2, 27)
    assert leap.calendar_month_end == date(2024, 2, 29)
    assert leap.evaluation_cutoff == date(2024, 2, 29)


def test_real_xnys_sessions_around_us_dst_transitions():
    calendar = ExchangeCalendarsAdapter("XNYS")
    for session_date in (date(2026, 3, 6), date(2026, 3, 9), date(2026, 10, 30), date(2026, 11, 2)):
        assert calendar.is_session(session_date) is True
    for non_session in (date(2026, 3, 7), date(2026, 3, 8), date(2026, 10, 31), date(2026, 11, 1)):
        assert calendar.is_session(non_session) is False
