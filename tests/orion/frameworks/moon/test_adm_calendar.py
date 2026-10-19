from datetime import date

import pytest

from orion.frameworks.moon.adm_calendar import (
    ADMCalendarResolutionError,
    resolve_adm_month_end_cutoff,
)


class FixtureCalendar:
    calendar_id = "TEST-X"
    calendar_version = "fixture-1"

    def __init__(self, sessions: set[date]):
        self.sessions = sessions

    def is_session(self, session_date: date) -> bool:
        return session_date in self.sessions


def test_month_end_session_is_used_as_cutoff() -> None:
    cutoff = resolve_adm_month_end_cutoff(
        2026, 9, calendar=FixtureCalendar({date(2026, 9, 30)})
    )

    assert cutoff.calendar_month_end == date(2026, 9, 30)
    assert cutoff.evaluation_cutoff == date(2026, 9, 30)
    assert cutoff.calendar_id == "TEST-X"
    assert cutoff.calendar_version == "fixture-1"


def test_non_session_month_end_uses_immediately_preceding_session() -> None:
    cutoff = resolve_adm_month_end_cutoff(
        2026,
        10,
        calendar=FixtureCalendar({date(2026, 10, 29), date(2026, 10, 30)}),
    )

    assert cutoff.calendar_month_end == date(2026, 10, 31)
    assert cutoff.evaluation_cutoff == date(2026, 10, 30)


def test_cutoff_uses_market_calendar_not_weekday_heuristics() -> None:
    # A Friday can be a market holiday; the injected calendar remains authoritative.
    cutoff = resolve_adm_month_end_cutoff(
        2026,
        7,
        calendar=FixtureCalendar({date(2026, 7, 29), date(2026, 7, 30)}),
    )

    assert cutoff.evaluation_cutoff == date(2026, 7, 30)


def test_missing_calendar_identity_fails_closed() -> None:
    class UnidentifiedCalendar:
        calendar_id = " "
        calendar_version = "fixture-1"

        def is_session(self, session_date: date) -> bool:
            return True

    with pytest.raises(ADMCalendarResolutionError, match="calendar_id"):
        resolve_adm_month_end_cutoff(2026, 9, calendar=UnidentifiedCalendar())


def test_calendar_lookup_exception_fails_closed_without_fallback() -> None:
    class BrokenCalendar:
        calendar_id = "TEST-X"
        calendar_version = "fixture-1"

        def is_session(self, session_date: date) -> bool:
            raise RuntimeError("source unavailable")

    with pytest.raises(ADMCalendarResolutionError, match="lookup failed"):
        resolve_adm_month_end_cutoff(2026, 9, calendar=BrokenCalendar())


def test_non_boolean_calendar_result_fails_closed() -> None:
    class InvalidCalendar:
        calendar_id = "TEST-X"
        calendar_version = "fixture-1"

        def is_session(self, session_date: date):
            return 1

    with pytest.raises(ADMCalendarResolutionError, match="must return bool"):
        resolve_adm_month_end_cutoff(2026, 9, calendar=InvalidCalendar())


def test_no_session_in_month_fails_closed() -> None:
    with pytest.raises(ADMCalendarResolutionError, match="no market session"):
        resolve_adm_month_end_cutoff(2026, 9, calendar=FixtureCalendar(set()))


@pytest.mark.parametrize("year,month", [(0, 1), (2026, 0), (2026, 13), (True, 1)])
def test_invalid_month_arguments_are_rejected(year, month) -> None:
    with pytest.raises(ADMCalendarResolutionError):
        resolve_adm_month_end_cutoff(year, month, calendar=FixtureCalendar(set()))
