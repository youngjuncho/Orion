from datetime import datetime, timezone

import pytest

from orion.frameworks.moon.adm_asof import (
    ADMAsOfResolutionError,
    resolve_adm_asof_boundary,
    validate_adm_availability_timestamp,
)


def test_date_only_boundary_includes_entire_seoul_date_and_normalizes_to_utc():
    result = resolve_adm_asof_boundary(through_date="2026-11-02")
    assert result.boundary_seoul.isoformat() == "2026-11-03T00:00:00+09:00"
    assert result.boundary_utc.isoformat() == "2026-11-02T15:00:00+00:00"
    assert result.requested_through_date == "2026-11-02"


def test_availability_immediately_before_boundary_is_eligible():
    result = resolve_adm_asof_boundary(through_date="2026-11-02")
    assert result.includes_availability("2026-11-02T14:59:59.999999Z")


def test_availability_exactly_at_boundary_is_excluded():
    result = resolve_adm_asof_boundary(through_date="2026-11-02")
    assert not result.includes_availability("2026-11-02T15:00:00Z")


def test_exact_asof_timestamp_is_not_expanded_to_end_of_day():
    result = resolve_adm_asof_boundary(as_of="2026-11-02T14:30:00+09:00")
    assert result.boundary_utc.isoformat() == "2026-11-02T05:30:00+00:00"


def test_equivalent_timestamp_offsets_resolve_to_same_instant():
    seoul = resolve_adm_asof_boundary(as_of="2026-11-02T14:30:00+09:00")
    utc = resolve_adm_asof_boundary(as_of="2026-11-02T05:30:00Z")
    assert seoul.boundary_utc == utc.boundary_utc


def test_naive_timestamp_is_rejected_without_explicit_timezone_policy():
    with pytest.raises(ADMAsOfResolutionError, match="naive as_of is ambiguous"):
        resolve_adm_asof_boundary(as_of="2026-11-02T14:30:00")


def test_naive_timestamp_can_be_explicitly_interpreted_as_seoul():
    result = resolve_adm_asof_boundary(
        as_of="2026-11-02T14:30:00", allow_naive_as_of_in_seoul=True
    )
    assert result.boundary_utc.isoformat() == "2026-11-02T05:30:00+00:00"


@pytest.mark.parametrize("value", ["2026-02-30", "26-11-02", "2026/11/02", ""])
def test_invalid_date_only_requests_are_rejected(value):
    with pytest.raises(ADMAsOfResolutionError):
        resolve_adm_asof_boundary(through_date=value)


@pytest.mark.parametrize("value", ["not-a-timestamp", "2026-11-02T25:61:00Z", ""])
def test_malformed_exact_timestamps_are_rejected(value):
    with pytest.raises(ADMAsOfResolutionError):
        resolve_adm_asof_boundary(as_of=value)


def test_exactly_one_target_argument_is_required():
    with pytest.raises(ADMAsOfResolutionError, match="exactly one"):
        resolve_adm_asof_boundary()
    with pytest.raises(ADMAsOfResolutionError, match="exactly one"):
        resolve_adm_asof_boundary(through_date="2026-11-02", as_of="2026-11-02T00:00:00Z")


def test_naive_availability_timestamps_are_rejected():
    with pytest.raises(ADMAsOfResolutionError, match="naive as_of is ambiguous"):
        validate_adm_availability_timestamp("2026-11-02T14:30:00")


def test_datetime_inputs_ignore_host_local_timezone_by_requiring_awareness():
    aware = datetime(2026, 11, 2, 5, 30, tzinfo=timezone.utc)
    result = resolve_adm_asof_boundary(as_of=aware)
    assert result.boundary_utc == aware


def test_leap_day_date_only_boundary_is_deterministic():
    result = resolve_adm_asof_boundary(through_date="2024-02-29")
    assert result.boundary_seoul.isoformat() == "2024-03-01T00:00:00+09:00"
    assert result.boundary_utc.isoformat() == "2024-02-29T15:00:00+00:00"
