"""Deterministic PCD-06 as-of boundary helpers.

These pure helpers define request and snapshot-boundary semantics. They are not
wired into the ADM runtime, scheduler, provider, or signal assembly.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

OPERATIONAL_TIMEZONE = "Asia/Seoul"
UTC = timezone.utc


class ADMAsOfResolutionError(ValueError):
    """Raised when an as-of request or availability timestamp is ambiguous."""


def _seoul_zone() -> ZoneInfo:
    try:
        return ZoneInfo(OPERATIONAL_TIMEZONE)
    except ZoneInfoNotFoundError as exc:  # pragma: no cover - host tz database issue
        raise ADMAsOfResolutionError(
            f"required IANA timezone {OPERATIONAL_TIMEZONE!r} is unavailable"
        ) from exc


def _parse_date(value: str) -> date:
    if not isinstance(value, str) or len(value) != 10:
        raise ADMAsOfResolutionError("through_date must use YYYY-MM-DD format")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ADMAsOfResolutionError(
            "through_date must use YYYY-MM-DD format"
        ) from exc
    if parsed.isoformat() != value:
        raise ADMAsOfResolutionError("through_date must use YYYY-MM-DD format")
    return parsed


def _parse_datetime(value: str | datetime, *, allow_naive_seoul: bool) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str) and value.strip():
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError as exc:
            raise ADMAsOfResolutionError("as_of must be a valid ISO-8601 timestamp") from exc
    else:
        raise ADMAsOfResolutionError("as_of must be a valid ISO-8601 timestamp")

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        if not allow_naive_seoul:
            raise ADMAsOfResolutionError(
                "naive as_of is ambiguous; provide a timezone or explicitly allow Asia/Seoul"
            )
        parsed = parsed.replace(tzinfo=_seoul_zone())
    return parsed.astimezone(UTC)


@dataclass(frozen=True)
class ADMAsOfBoundary:
    """Exclusive UTC snapshot boundary and its Seoul-local representation."""

    boundary_utc: datetime
    boundary_seoul: datetime
    request_kind: str
    requested_through_date: str | None = None

    def __post_init__(self) -> None:
        if self.boundary_utc.tzinfo is None or self.boundary_utc.utcoffset() is None:
            raise ADMAsOfResolutionError("boundary_utc must be timezone-aware")
        if self.boundary_seoul.tzinfo is None or self.boundary_seoul.utcoffset() is None:
            raise ADMAsOfResolutionError("boundary_seoul must be timezone-aware")
        if self.boundary_utc.astimezone(UTC) != self.boundary_seoul.astimezone(UTC):
            raise ADMAsOfResolutionError("UTC and Seoul boundaries must identify the same instant")
        if self.request_kind not in {"through_date", "as_of"}:
            raise ADMAsOfResolutionError("request_kind must be through_date or as_of")

    def includes_availability(self, available_at: str | datetime) -> bool:
        """Return true only for an availability instant strictly before boundary."""
        available_utc = _parse_datetime(available_at, allow_naive_seoul=False)
        return available_utc < self.boundary_utc.astimezone(UTC)


def resolve_adm_asof_boundary(
    *,
    through_date: str | None = None,
    as_of: str | datetime | None = None,
    allow_naive_as_of_in_seoul: bool = False,
) -> ADMAsOfBoundary:
    """Resolve exactly one explicit request target to an exclusive UTC boundary.

    Date-only requests include the entire Seoul calendar date by using the
    following local midnight as an exclusive boundary. Exact timestamps remain
    exact instants. No target is inferred from the request arrival time.
    """
    if (through_date is None) == (as_of is None):
        raise ADMAsOfResolutionError("provide exactly one of through_date or as_of")

    if through_date is not None:
        target = _parse_date(through_date)
        boundary_local = datetime.combine(target + timedelta(days=1), time.min, _seoul_zone())
        return ADMAsOfBoundary(
            boundary_utc=boundary_local.astimezone(UTC),
            boundary_seoul=boundary_local,
            request_kind="through_date",
            requested_through_date=target.isoformat(),
        )

    exact_utc = _parse_datetime(as_of, allow_naive_seoul=allow_naive_as_of_in_seoul)
    return ADMAsOfBoundary(
        boundary_utc=exact_utc,
        boundary_seoul=exact_utc.astimezone(_seoul_zone()),
        request_kind="as_of",
    )


def validate_adm_availability_timestamp(value: str | datetime) -> datetime:
    """Parse a required availability timestamp and normalize it to UTC."""
    return _parse_datetime(value, allow_naive_seoul=False)
