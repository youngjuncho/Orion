from datetime import date
from types import SimpleNamespace

import pytest

from orion.frameworks.moon import adm_exchange_calendar as adapter
from orion.frameworks.moon.adm_calendar import ADMCalendarResolutionError


class FakeCalendar:
    def __init__(self, result=True, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def is_session(self, session_date):
        self.calls.append(session_date)
        if self.error:
            raise self.error
        return self.result


def install_fake_package(monkeypatch, calendar, installed_version="4.13.2"):
    monkeypatch.setattr(adapter, "version", lambda package: installed_version)
    monkeypatch.setattr(adapter, "import_module", lambda name: SimpleNamespace(get_calendar=lambda calendar_id: calendar))


def test_adapter_exposes_stable_identity_and_normalizes_boolean(monkeypatch):
    fake = FakeCalendar(result=True)
    install_fake_package(monkeypatch, fake)
    cal = adapter.ExchangeCalendarsAdapter("XNYS")
    assert cal.calendar_id == "XNYS"
    assert cal.calendar_version == "exchange-calendars==4.13.2"
    assert cal.is_session(date(2026, 10, 30)) is True
    assert fake.calls == ["2026-10-30"]


def test_unapproved_calendar_id_fails_closed(monkeypatch):
    with pytest.raises(ADMCalendarResolutionError, match="not in the approved"):
        adapter.ExchangeCalendarsAdapter("ARCX")


def test_unapproved_instrument_fails_closed(monkeypatch):
    with pytest.raises(ADMCalendarResolutionError, match="no approved market calendar mapping"):
        adapter.calendar_for_instrument("SPY")


@pytest.mark.parametrize("ticker", ["VTI", "VEU", "SGOV", " vti "])
def test_approved_instrument_mapping_is_explicit(monkeypatch, ticker):
    fake = FakeCalendar(result=True)
    install_fake_package(monkeypatch, fake)
    assert adapter.calendar_for_instrument(ticker).calendar_id == "XNYS"


def test_missing_dependency_fails_closed(monkeypatch):
    from importlib.metadata import PackageNotFoundError

    def missing(_):
        raise PackageNotFoundError("exchange-calendars")

    monkeypatch.setattr(adapter, "version", missing)
    with pytest.raises(ADMCalendarResolutionError, match="is not installed"):
        adapter.ExchangeCalendarsAdapter("XNYS")


def test_version_mismatch_fails_closed(monkeypatch):
    monkeypatch.setattr(adapter, "version", lambda _: "4.14.0")
    with pytest.raises(ADMCalendarResolutionError, match="unsupported"):
        adapter.ExchangeCalendarsAdapter("XNYS")


def test_calendar_construction_failure_fails_closed(monkeypatch):
    monkeypatch.setattr(adapter, "version", lambda _: "4.13.2")

    def broken_import(_):
        raise RuntimeError("broken calendar package")

    monkeypatch.setattr(adapter, "import_module", broken_import)
    with pytest.raises(ADMCalendarResolutionError, match="could not be loaded"):
        adapter.ExchangeCalendarsAdapter("XNYS")


def test_session_lookup_failure_fails_closed(monkeypatch):
    fake = FakeCalendar(error=RuntimeError("calendar unavailable"))
    install_fake_package(monkeypatch, fake)
    cal = adapter.ExchangeCalendarsAdapter("XNYS")
    with pytest.raises(ADMCalendarResolutionError, match="lookup failed"):
        cal.is_session(date(2026, 10, 30))


def test_invalid_session_result_fails_closed(monkeypatch):
    fake = FakeCalendar(result=1)
    install_fake_package(monkeypatch, fake)
    cal = adapter.ExchangeCalendarsAdapter("XNYS")
    with pytest.raises(ADMCalendarResolutionError, match="invalid result"):
        cal.is_session(date(2026, 10, 30))
