"""Pinned exchange-calendars adapter for approved ADM evaluation calendars.

This module is intentionally not imported by the ADM runtime. Callers must opt
in explicitly; there is no fallback calendar or inferred ticker mapping.
"""
from __future__ import annotations

from datetime import date
from importlib import import_module
from importlib.metadata import PackageNotFoundError, version
from typing import Any

from .adm_calendar import ADMCalendarResolutionError, ADMMarketCalendar

PINNED_PACKAGE_VERSION = "4.13.2"
PACKAGE_NAME = "exchange-calendars"
APPROVED_INSTRUMENT_CALENDAR_IDS: dict[str, str] = {
    "VTI": "XNYS",
    "VEU": "XNYS",
    "SGOV": "XNYS",
}


class ExchangeCalendarsAdapter:
    """Adapt a canonical package calendar to the ADMMarketCalendar protocol."""

    def __init__(self, calendar_id: str) -> None:
        if not isinstance(calendar_id, str) or not calendar_id.strip():
            raise ADMCalendarResolutionError("calendar_id must be a non-empty string")
        if calendar_id != "XNYS":
            raise ADMCalendarResolutionError(
                f"calendar_id {calendar_id!r} is not in the approved calendar set"
            )
        try:
            installed_version = version(PACKAGE_NAME)
        except PackageNotFoundError as exc:
            raise ADMCalendarResolutionError(
                f"required dependency {PACKAGE_NAME}=={PINNED_PACKAGE_VERSION} is not installed"
            ) from exc
        except Exception as exc:
            raise ADMCalendarResolutionError("calendar dependency version lookup failed") from exc
        if installed_version != PINNED_PACKAGE_VERSION:
            raise ADMCalendarResolutionError(
                f"unsupported {PACKAGE_NAME} version {installed_version!r}; "
                f"expected {PINNED_PACKAGE_VERSION!r}"
            )
        try:
            module = import_module("exchange_calendars")
            self._calendar = module.get_calendar(calendar_id)
        except Exception as exc:
            raise ADMCalendarResolutionError(
                f"market calendar {calendar_id!r} could not be loaded"
            ) from exc
        self._calendar_id = calendar_id
        self._calendar_version = f"{PACKAGE_NAME}=={installed_version}"

    @property
    def calendar_id(self) -> str:
        return self._calendar_id

    @property
    def calendar_version(self) -> str:
        return self._calendar_version

    def is_session(self, session_date: date) -> bool:
        if not isinstance(session_date, date):
            raise ADMCalendarResolutionError("session_date must be a datetime.date")
        try:
            result: Any = self._calendar.is_session(session_date.isoformat())
        except Exception as exc:
            raise ADMCalendarResolutionError("market calendar lookup failed") from exc
        if not isinstance(result, (bool,)) and type(result).__name__ != "bool_":
            raise ADMCalendarResolutionError("calendar is_session() returned an invalid result")
        return bool(result)


def calendar_for_instrument(instrument: str) -> ADMMarketCalendar:
    """Create the explicitly approved calendar adapter for an instrument."""
    if not isinstance(instrument, str):
        raise ADMCalendarResolutionError("instrument must be a string ticker")
    ticker = instrument.strip().upper()
    calendar_id = APPROVED_INSTRUMENT_CALENDAR_IDS.get(ticker)
    if calendar_id is None:
        raise ADMCalendarResolutionError(f"no approved market calendar mapping for {ticker!r}")
    return ExchangeCalendarsAdapter(calendar_id)
