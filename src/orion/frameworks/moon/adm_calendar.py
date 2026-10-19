"""Calendar-injected ADM evaluation-cutoff resolution.

This module defines a deterministic interface and resolver only. It deliberately
ships no authoritative exchange-calendar implementation and is not wired into
the ADM signal pipeline until a calendar source and supported market mapping are
approved.
"""

from __future__ import annotations

from calendar import monthrange
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Protocol, runtime_checkable


class ADMCalendarResolutionError(ValueError):
    """Raised when the supplied market calendar cannot resolve a cutoff safely."""


@runtime_checkable
class ADMMarketCalendar(Protocol):
    """Minimal contract for a version-identifiable instrument-market calendar."""

    @property
    def calendar_id(self) -> str:
        """Stable identifier for the market calendar, e.g. an exchange code."""

    @property
    def calendar_version(self) -> str:
        """Version or immutable revision used for this resolution."""

    def is_session(self, session_date: date) -> bool:
        """Return whether the market has a regular trading session on this date."""


@dataclass(frozen=True)
class ADMResolvedEvaluationCutoff:
    """Resolved market-specific cutoff; not a signal or execution timestamp."""

    calendar_month_end: date
    evaluation_cutoff: date
    calendar_id: str
    calendar_version: str

    def __post_init__(self) -> None:
        if self.calendar_month_end.day != monthrange(
            self.calendar_month_end.year, self.calendar_month_end.month
        )[1]:
            raise ValueError("calendar_month_end must be the final calendar day of a month")
        if self.evaluation_cutoff > self.calendar_month_end:
            raise ValueError("evaluation_cutoff cannot be after calendar month-end")
        if (self.evaluation_cutoff.year, self.evaluation_cutoff.month) != (
            self.calendar_month_end.year,
            self.calendar_month_end.month,
        ):
            raise ValueError("evaluation_cutoff must be in the same month as calendar month-end")
        if not isinstance(self.calendar_id, str) or not self.calendar_id.strip():
            raise ValueError("calendar_id must be a non-empty string")
        if not isinstance(self.calendar_version, str) or not self.calendar_version.strip():
            raise ValueError("calendar_version must be a non-empty string")


def resolve_adm_month_end_cutoff(
    year: int,
    month: int,
    *,
    calendar: ADMMarketCalendar,
) -> ADMResolvedEvaluationCutoff:
    """Resolve month-end to that date or the immediately preceding market session.

    The calendar is injected by the caller. This function fails closed for an
    invalid/unidentifiable calendar or if no session is found in the month. It
    does not check data publication time, observation freshness, prior-year
    endpoint alignment, signal time, or execution time.
    """

    if isinstance(year, bool) or not isinstance(year, int) or not 1 <= year <= 9999:
        raise ADMCalendarResolutionError("year must be an integer from 1 through 9999")
    if isinstance(month, bool) or not isinstance(month, int) or not 1 <= month <= 12:
        raise ADMCalendarResolutionError("month must be an integer from 1 through 12")
    calendar_id = getattr(calendar, "calendar_id", None)
    calendar_version = getattr(calendar, "calendar_version", None)
    is_session = getattr(calendar, "is_session", None)
    if not isinstance(calendar_id, str) or not calendar_id.strip():
        raise ADMCalendarResolutionError("calendar_id must be provided by the calendar")
    if not isinstance(calendar_version, str) or not calendar_version.strip():
        raise ADMCalendarResolutionError("calendar_version must be provided by the calendar")
    if not callable(is_session):
        raise ADMCalendarResolutionError("calendar must provide callable is_session(date)")

    month_end = date(year, month, monthrange(year, month)[1])
    candidate = month_end
    while candidate.month == month:
        try:
            session = is_session(candidate)
        except Exception as exc:  # calendar errors must not silently fall back
            raise ADMCalendarResolutionError("market calendar lookup failed") from exc
        if not isinstance(session, bool):
            raise ADMCalendarResolutionError("calendar is_session() must return bool")
        if session:
            return ADMResolvedEvaluationCutoff(
                calendar_month_end=month_end,
                evaluation_cutoff=candidate,
                calendar_id=calendar_id,
                calendar_version=calendar_version,
            )
        candidate -= timedelta(days=1)

    raise ADMCalendarResolutionError("no market session found in the requested calendar month")
