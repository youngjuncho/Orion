"""Policy-explicit data lookup helpers for Moon's ADM return calculations.

These helpers consume an already normalized dataset. They intentionally do not
choose trading dates, resolve provider identities, infer adjusted-price
semantics, or decide freshness/missing-data policies.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from math import isfinite
from types import MappingProxyType
from typing import Mapping

from data.contracts import MarketDataPoint, MarketDataSet

from .adm import ADM_RISK_ASSETS, calculate_adjusted_price_return


def _exact_numeric_price(
    dataset: MarketDataSet,
    *,
    symbol: str,
    field: str,
    observed_at: str,
) -> float:
    """Return one positive numeric observation at an explicitly named key."""

    if not isinstance(dataset, MarketDataSet):
        raise ValueError("dataset must be a MarketDataSet")
    for name, value in (("symbol", symbol), ("field", field), ("observed_at", observed_at)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")

    matches = [
        point
        for point in dataset.observations
        if point.identity == (symbol, field, observed_at)
    ]
    if not matches:
        raise ValueError(
            f"missing observation for {symbol}/{field} at {observed_at}"
        )

    point: MarketDataPoint = matches[0]
    value = point.value
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(
            f"observation for {symbol}/{field} at {observed_at} must be numeric"
        )
    if not isfinite(value) or value <= 0:
        raise ValueError(
            f"observation for {symbol}/{field} at {observed_at} must be finite and positive"
        )
    return float(value)


@dataclass(frozen=True)
class ADMPriceObservationPair:
    """Two exact price observations selected under a named caller policy.

    ``selection_policy_id`` is provenance supplied by the caller; it does not
    imply that the policy has been approved by Orion governance.
    """

    symbol: str
    field: str
    current: MarketDataPoint
    trailing: MarketDataPoint
    selection_policy_id: str
    current_target_date: str | None = None
    trailing_target_date: str | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("symbol", self.symbol),
            ("field", self.field),
            ("selection_policy_id", self.selection_policy_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.current, MarketDataPoint) or not isinstance(
            self.trailing, MarketDataPoint
        ):
            raise ValueError("current and trailing must be MarketDataPoint values")
        expected_prefix = (self.symbol, self.field)
        if self.current.identity[:2] != expected_prefix:
            raise ValueError("current observation does not match symbol and field")
        if self.trailing.identity[:2] != expected_prefix:
            raise ValueError("trailing observation does not match symbol and field")
        if self.current.observed_at == self.trailing.observed_at:
            raise ValueError("current and trailing observations must have different timestamps")
        for name, value in (
            ("current_target_date", self.current_target_date),
            ("trailing_target_date", self.trailing_target_date),
        ):
            if value is not None:
                _parse_iso_date(value, name)


def select_adm_price_observations(
    dataset: MarketDataSet,
    *,
    symbol: str,
    field: str,
    current_observed_at: str,
    trailing_observed_at: str,
    selection_policy_id: str,
) -> ADMPriceObservationPair:
    """Select two exact observations and retain the caller's policy identifier.

    Date arithmetic, calendar interpretation, nearest-bar selection, freshness
    handling, and policy approval are deliberately outside this function.
    """

    # Reuse the same strict key and price validation as the return helper.
    current_value = _exact_numeric_price(
        dataset, symbol=symbol, field=field, observed_at=current_observed_at
    )
    trailing_value = _exact_numeric_price(
        dataset, symbol=symbol, field=field, observed_at=trailing_observed_at
    )
    del current_value, trailing_value  # Validation only; retain source observations.

    current = next(
        point for point in dataset.observations
        if point.identity == (symbol, field, current_observed_at)
    )
    trailing = next(
        point for point in dataset.observations
        if point.identity == (symbol, field, trailing_observed_at)
    )
    return ADMPriceObservationPair(
        symbol=symbol,
        field=field,
        current=current,
        trailing=trailing,
        selection_policy_id=selection_policy_id,
    )



def _parse_iso_date(value: str, name: str) -> date:
    """Parse the deliberately narrow YYYY-MM-DD date contract."""

    if not isinstance(value, str) or len(value) != 10:
        raise ValueError(f"{name} must use YYYY-MM-DD format")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{name} must use YYYY-MM-DD format") from exc
    if parsed.isoformat() != value:
        raise ValueError(f"{name} must use YYYY-MM-DD format")
    return parsed


def select_adm_price_observations_on_or_before(
    dataset: MarketDataSet,
    *,
    symbol: str,
    field: str,
    current_target_date: str,
    trailing_target_date: str,
    selection_policy_id: str = "prior-observation-on-or-before-v1",
) -> ADMPriceObservationPair:
    """Select the latest available observation on or before each target date.

    This is a deterministic, source-agnostic prior-observation rule. It does
    not prove that a selected observation is a valid trading-day bar, and it
    does not enforce a maximum age. Provider calendar, stale-data, adjusted-
    price semantics, and timezone policies remain the caller's responsibility.
    Observation timestamps must be date-only ``YYYY-MM-DD`` strings.
    """

    if not isinstance(dataset, MarketDataSet):
        raise ValueError("dataset must be a MarketDataSet")
    for name, value in (("symbol", symbol), ("field", field), ("selection_policy_id", selection_policy_id)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")

    current_target = _parse_iso_date(current_target_date, "current_target_date")
    trailing_target = _parse_iso_date(trailing_target_date, "trailing_target_date")
    if trailing_target >= current_target:
        raise ValueError("trailing_target_date must be earlier than current_target_date")

    candidates: list[tuple[date, MarketDataPoint]] = []
    for point in dataset.observations:
        if point.symbol != symbol or point.field != field:
            continue
        observed_date = _parse_iso_date(point.observed_at, "observed_at")
        candidates.append((observed_date, point))

    def choose(target: date, label: str) -> MarketDataPoint:
        eligible = [(observed, point) for observed, point in candidates if observed <= target]
        if not eligible:
            raise ValueError(f"missing observation on or before {target.isoformat()} for {symbol}/{field} ({label})")
        observed, point = max(eligible, key=lambda item: item[0])
        # Validate the chosen observation without substituting another date.
        _exact_numeric_price(
            dataset,
            symbol=symbol,
            field=field,
            observed_at=point.observed_at,
        )
        return point

    current = choose(current_target, "current")
    trailing = choose(trailing_target, "trailing")
    if current.observed_at == trailing.observed_at:
        raise ValueError("current and trailing observations must resolve to different dates")
    return ADMPriceObservationPair(
        symbol=symbol,
        field=field,
        current=current,
        trailing=trailing,
        selection_policy_id=selection_policy_id,
        current_target_date=current_target_date,
        trailing_target_date=trailing_target_date,
    )



def calculate_adm_observation_pair_return(pair: ADMPriceObservationPair) -> float:
    """Calculate return from a previously selected and auditable price pair."""

    if not isinstance(pair, ADMPriceObservationPair):
        raise ValueError("pair must be an ADMPriceObservationPair")
    current_value = pair.current.value
    trailing_value = pair.trailing.value
    for name, value in (("current", current_value), ("trailing", trailing_value)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} observation price must be numeric")
        if not isfinite(value) or value <= 0:
            raise ValueError(f"{name} observation price must be finite and positive")
    return calculate_adjusted_price_return(float(current_value), float(trailing_value))


def calculate_adm_asset_return(
    dataset: MarketDataSet,
    *,
    symbol: str,
    field: str,
    current_observed_at: str,
    trailing_observed_at: str,
) -> float:
    """Calculate a return from two exact, caller-selected observations.

    The caller must explicitly select the canonical field and both observation
    timestamps under an approved policy. This function does not interpret the
    timestamps or assume that ``field`` has total-return adjusted semantics.
    """

    current_price = _exact_numeric_price(
        dataset,
        symbol=symbol,
        field=field,
        observed_at=current_observed_at,
    )
    trailing_price = _exact_numeric_price(
        dataset,
        symbol=symbol,
        field=field,
        observed_at=trailing_observed_at,
    )
    return calculate_adjusted_price_return(current_price, trailing_price)


@dataclass(frozen=True)
class ADMRelativeMomentumResult:
    """Auditable relative-momentum returns for ADM's approved risk assets.

    This result contains only the two independently calculated asset returns.
    It intentionally does not calculate absolute momentum or construct
    ``ADMSignalInput``, whose benchmark and policy dependencies remain open.
    """

    current_target_date: str
    trailing_target_date: str
    field: str
    selection_policy_id: str
    relative_momentum: Mapping[str, float]
    observation_pairs: Mapping[str, ADMPriceObservationPair]

    def __post_init__(self) -> None:
        current_target = _parse_iso_date(self.current_target_date, "current_target_date")
        trailing_target = _parse_iso_date(self.trailing_target_date, "trailing_target_date")
        if trailing_target >= current_target:
            raise ValueError("trailing_target_date must be earlier than current_target_date")
        for name, value in (("field", self.field), ("selection_policy_id", self.selection_policy_id)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if set(self.relative_momentum) != set(ADM_RISK_ASSETS):
            raise ValueError("relative_momentum must contain exactly VTI and VEU")
        if set(self.observation_pairs) != set(ADM_RISK_ASSETS):
            raise ValueError("observation_pairs must contain exactly VTI and VEU")
        returns: dict[str, float] = {}
        pairs: dict[str, ADMPriceObservationPair] = {}
        for symbol in ADM_RISK_ASSETS:
            value = self.relative_momentum[symbol]
            pair = self.observation_pairs[symbol]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
                raise ValueError(f"relative momentum for {symbol} must be finite")
            if not isinstance(pair, ADMPriceObservationPair) or pair.symbol != symbol:
                raise ValueError(f"observation pair for {symbol} is invalid")
            if pair.field != self.field or pair.selection_policy_id != self.selection_policy_id:
                raise ValueError("observation pair field and policy must match result")
            if pair.current_target_date != self.current_target_date or pair.trailing_target_date != self.trailing_target_date:
                raise ValueError("observation pair target dates must match result")
            returns[symbol] = float(value)
            pairs[symbol] = pair
        object.__setattr__(self, "relative_momentum", MappingProxyType(returns))
        object.__setattr__(self, "observation_pairs", MappingProxyType(pairs))


def calculate_adm_relative_momentum(
    dataset: MarketDataSet,
    *,
    field: str,
    current_target_date: str,
    trailing_target_date: str,
    selection_policy_id: str = "prior-observation-on-or-before-v1",
) -> ADMRelativeMomentumResult:
    """Calculate VTI and VEU returns using one shared endpoint policy.

    This function deliberately stops before absolute-momentum calculation and
    ``ADMSignalInput`` construction. Both risk assets use the same target dates,
    field, and policy identifier, and the selected observations remain available
    for audit. Provider-specific calendars, stale-data limits, and adjusted-price
    semantics are not inferred here.
    """

    pairs = {
        symbol: select_adm_price_observations_on_or_before(
            dataset,
            symbol=symbol,
            field=field,
            current_target_date=current_target_date,
            trailing_target_date=trailing_target_date,
            selection_policy_id=selection_policy_id,
        )
        for symbol in ADM_RISK_ASSETS
    }
    returns = {
        symbol: calculate_adm_observation_pair_return(pair)
        for symbol, pair in pairs.items()
    }
    return ADMRelativeMomentumResult(
        current_target_date=current_target_date,
        trailing_target_date=trailing_target_date,
        field=field,
        selection_policy_id=selection_policy_id,
        relative_momentum=returns,
        observation_pairs=pairs,
    )

@dataclass(frozen=True)
class ADMObservationFreshnessResult:
    """Explicit freshness audit for the two observations in a selected pair."""

    symbol: str
    field: str
    selection_policy_id: str
    current_target_date: str
    trailing_target_date: str
    current_observed_at: str
    trailing_observed_at: str
    current_age_days: int
    trailing_age_days: int
    max_age_days: int

    def __post_init__(self) -> None:
        for name, value in (
            ("symbol", self.symbol),
            ("field", self.field),
            ("selection_policy_id", self.selection_policy_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        for name in ("current_target_date", "trailing_target_date", "current_observed_at", "trailing_observed_at"):
            _parse_iso_date(getattr(self, name), name)
        if self.trailing_target_date >= self.current_target_date:
            raise ValueError("trailing_target_date must be earlier than current_target_date")
        if isinstance(self.max_age_days, bool) or not isinstance(self.max_age_days, int) or self.max_age_days < 0:
            raise ValueError("max_age_days must be a non-negative integer")
        if self.current_age_days < 0 or self.trailing_age_days < 0:
            raise ValueError("observation age must be non-negative")
        if self.current_age_days > self.max_age_days or self.trailing_age_days > self.max_age_days:
            raise ValueError("observation exceeds the configured maximum age")


def validate_adm_observation_pair_freshness(
    pair: ADMPriceObservationPair,
    *,
    max_age_days: int,
) -> ADMObservationFreshnessResult:
    """Audit observation age against an explicit caller-supplied threshold.

    No threshold is defaulted or inferred. The selected observation must be on
    or before its target date, and both calendar-day ages must be within the
    supplied limit. This is a generic age check, not proof of exchange-calendar
    validity or provider data quality.
    """

    if not isinstance(pair, ADMPriceObservationPair):
        raise ValueError("pair must be an ADMPriceObservationPair")
    if isinstance(max_age_days, bool) or not isinstance(max_age_days, int) or max_age_days < 0:
        raise ValueError("max_age_days must be a non-negative integer")
    if pair.current_target_date is None or pair.trailing_target_date is None:
        raise ValueError("pair must retain target dates for freshness validation")

    current_target = _parse_iso_date(pair.current_target_date, "current_target_date")
    trailing_target = _parse_iso_date(pair.trailing_target_date, "trailing_target_date")
    current_observed = _parse_iso_date(pair.current.observed_at, "current observed_at")
    trailing_observed = _parse_iso_date(pair.trailing.observed_at, "trailing observed_at")
    if current_observed > current_target:
        raise ValueError("current observation must not be later than its target date")
    if trailing_observed > trailing_target:
        raise ValueError("trailing observation must not be later than its target date")

    current_age = (current_target - current_observed).days
    trailing_age = (trailing_target - trailing_observed).days
    if current_age > max_age_days or trailing_age > max_age_days:
        raise ValueError("observation exceeds the configured maximum age")
    return ADMObservationFreshnessResult(
        symbol=pair.symbol,
        field=pair.field,
        selection_policy_id=pair.selection_policy_id,
        current_target_date=pair.current_target_date,
        trailing_target_date=pair.trailing_target_date,
        current_observed_at=pair.current.observed_at,
        trailing_observed_at=pair.trailing.observed_at,
        current_age_days=current_age,
        trailing_age_days=trailing_age,
        max_age_days=max_age_days,
    )


@dataclass(frozen=True)
class ADMRelativeMomentumFreshnessResult:
    """Freshness gate result for both ADM risk-asset observation pairs.

    Passing this gate certifies only that both pairs meet the explicitly
    supplied calendar-day age limit. It does not approve the data source,
    adjusted-price semantics, or any investment signal.
    """

    relative_momentum_result: ADMRelativeMomentumResult
    max_age_days: int
    freshness_by_symbol: Mapping[str, ADMObservationFreshnessResult]

    def __post_init__(self) -> None:
        if not isinstance(self.relative_momentum_result, ADMRelativeMomentumResult):
            raise ValueError("relative_momentum_result must be an ADMRelativeMomentumResult")
        if isinstance(self.max_age_days, bool) or not isinstance(self.max_age_days, int) or self.max_age_days < 0:
            raise ValueError("max_age_days must be a non-negative integer")
        if set(self.freshness_by_symbol) != set(ADM_RISK_ASSETS):
            raise ValueError("freshness_by_symbol must contain exactly VTI and VEU")
        normalized: dict[str, ADMObservationFreshnessResult] = {}
        for symbol in ADM_RISK_ASSETS:
            freshness = self.freshness_by_symbol[symbol]
            pair = self.relative_momentum_result.observation_pairs[symbol]
            if not isinstance(freshness, ADMObservationFreshnessResult):
                raise ValueError(f"freshness result for {symbol} is invalid")
            if freshness.symbol != symbol or freshness.field != self.relative_momentum_result.field:
                raise ValueError(f"freshness result for {symbol} does not match relative-momentum input")
            if freshness.selection_policy_id != self.relative_momentum_result.selection_policy_id:
                raise ValueError("freshness policy provenance does not match relative-momentum result")
            if (
                freshness.current_target_date != self.relative_momentum_result.current_target_date
                or freshness.trailing_target_date != self.relative_momentum_result.trailing_target_date
            ):
                raise ValueError("freshness target dates do not match relative-momentum result")
            if freshness.current_observed_at != pair.current.observed_at or freshness.trailing_observed_at != pair.trailing.observed_at:
                raise ValueError(f"freshness observations for {symbol} do not match selected pair")
            if freshness.max_age_days != self.max_age_days:
                raise ValueError("all freshness results must use the same maximum age")
            normalized[symbol] = freshness
        object.__setattr__(self, "freshness_by_symbol", MappingProxyType(normalized))


def validate_adm_relative_momentum_freshness(
    result: ADMRelativeMomentumResult,
    *,
    max_age_days: int,
) -> ADMRelativeMomentumFreshnessResult:
    """Apply one explicit freshness threshold to both ADM risk assets.

    The operation is fail-closed: if either VTI or VEU fails freshness
    validation, no aggregate gate result is returned. This is a data-quality
    gate only; it does not create an ADM signal or validate source semantics.
    """

    if not isinstance(result, ADMRelativeMomentumResult):
        raise ValueError("result must be an ADMRelativeMomentumResult")
    if isinstance(max_age_days, bool) or not isinstance(max_age_days, int) or max_age_days < 0:
        raise ValueError("max_age_days must be a non-negative integer")
    freshness_by_symbol = {
        symbol: validate_adm_observation_pair_freshness(
            result.observation_pairs[symbol], max_age_days=max_age_days
        )
        for symbol in ADM_RISK_ASSETS
    }
    return ADMRelativeMomentumFreshnessResult(
        relative_momentum_result=result,
        max_age_days=max_age_days,
        freshness_by_symbol=freshness_by_symbol,
    )

@dataclass(frozen=True)
class ADMAbsoluteMomentumInputs:
    """Auditable return inputs for a future, policy-approved absolute test.

    This object deliberately does not define how the risk asset and benchmark
    returns are compared. The benchmark and comparison rule remain governance
    decisions; merely supplying a benchmark here does not approve it.
    """

    risk_asset_symbol: str
    benchmark_symbol: str
    current_target_date: str
    trailing_target_date: str
    field: str
    selection_policy_id: str
    risk_asset_return: float
    benchmark_return: float
    observation_pairs: Mapping[str, ADMPriceObservationPair]

    def __post_init__(self) -> None:
        for name, value in (
            ("risk_asset_symbol", self.risk_asset_symbol),
            ("benchmark_symbol", self.benchmark_symbol),
            ("field", self.field),
            ("selection_policy_id", self.selection_policy_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if self.risk_asset_symbol == self.benchmark_symbol:
            raise ValueError("risk asset and benchmark must be different instruments")
        current_target = _parse_iso_date(self.current_target_date, "current_target_date")
        trailing_target = _parse_iso_date(self.trailing_target_date, "trailing_target_date")
        if trailing_target >= current_target:
            raise ValueError("trailing_target_date must be earlier than current_target_date")
        for name, value in (("risk_asset_return", self.risk_asset_return), ("benchmark_return", self.benchmark_return)):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
                raise ValueError(f"{name} must be a finite number")
        expected_symbols = {self.risk_asset_symbol, self.benchmark_symbol}
        if set(self.observation_pairs) != expected_symbols:
            raise ValueError("observation_pairs must contain exactly the risk asset and benchmark")
        normalized: dict[str, ADMPriceObservationPair] = {}
        for symbol in expected_symbols:
            pair = self.observation_pairs[symbol]
            if not isinstance(pair, ADMPriceObservationPair) or pair.symbol != symbol:
                raise ValueError(f"observation pair for {symbol} is invalid")
            if pair.field != self.field or pair.selection_policy_id != self.selection_policy_id:
                raise ValueError("observation pairs must use the same field and selection policy")
            if pair.current_target_date != self.current_target_date or pair.trailing_target_date != self.trailing_target_date:
                raise ValueError("observation-pair target dates must match result")
            normalized[symbol] = pair
        object.__setattr__(self, "observation_pairs", MappingProxyType(normalized))


def calculate_adm_absolute_momentum_inputs(
    dataset: MarketDataSet,
    *,
    risk_asset_symbol: str,
    benchmark_symbol: str,
    field: str,
    current_target_date: str,
    trailing_target_date: str,
    selection_policy_id: str = "prior-observation-on-or-before-v1",
) -> ADMAbsoluteMomentumInputs:
    """Prepare comparable returns without deciding the absolute-momentum rule.

    Both instruments use the same field, target dates, and endpoint-selection
    policy. No benchmark identity is defaulted and no boolean signal is emitted.
    """

    for name, value in (("risk_asset_symbol", risk_asset_symbol), ("benchmark_symbol", benchmark_symbol)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")
    if risk_asset_symbol == benchmark_symbol:
        raise ValueError("risk asset and benchmark must be different instruments")
    pairs = {
        symbol: select_adm_price_observations_on_or_before(
            dataset,
            symbol=symbol,
            field=field,
            current_target_date=current_target_date,
            trailing_target_date=trailing_target_date,
            selection_policy_id=selection_policy_id,
        )
        for symbol in (risk_asset_symbol, benchmark_symbol)
    }
    returns = {symbol: calculate_adm_observation_pair_return(pair) for symbol, pair in pairs.items()}
    return ADMAbsoluteMomentumInputs(
        risk_asset_symbol=risk_asset_symbol,
        benchmark_symbol=benchmark_symbol,
        current_target_date=current_target_date,
        trailing_target_date=trailing_target_date,
        field=field,
        selection_policy_id=selection_policy_id,
        risk_asset_return=returns[risk_asset_symbol],
        benchmark_return=returns[benchmark_symbol],
        observation_pairs=pairs,
    )


class ADMAbsoluteMomentumComparisonStatus(str, Enum):
    """Three-state result for an absolute-momentum comparison.

    UNAVAILABLE is deliberately distinct from FALSE: missing or unresolved
    policy must never be interpreted as a negative investment signal.
    """

    TRUE = "true"
    FALSE = "false"
    UNAVAILABLE = "unavailable"


class ADMAbsoluteMomentumComparisonOperator(str, Enum):
    """Explicit comparison operators; neither is an Orion-approved default."""

    RISK_RETURN_GT_BENCHMARK = "risk_return_gt_benchmark"
    RISK_RETURN_GTE_BENCHMARK = "risk_return_gte_benchmark"


@dataclass(frozen=True)
class ADMAbsoluteMomentumComparisonPolicy:
    """Caller-supplied comparison contract, not governance approval.

    The operator encodes equality behavior: strict greater-than treats equal
    returns as false; greater-than-or-equal treats them as true. A policy ID is
    provenance only and does not prove that the policy was approved.
    """

    policy_id: str
    benchmark_symbol: str
    operator: ADMAbsoluteMomentumComparisonOperator

    def __post_init__(self) -> None:
        for name, value in (("policy_id", self.policy_id), ("benchmark_symbol", self.benchmark_symbol)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.operator, ADMAbsoluteMomentumComparisonOperator):
            raise ValueError("operator must be an ADMAbsoluteMomentumComparisonOperator")


@dataclass(frozen=True)
class ADMAbsoluteMomentumComparisonResult:
    """Auditable comparison outcome; UNAVAILABLE is not a negative signal."""

    status: ADMAbsoluteMomentumComparisonStatus
    risk_asset_symbol: str
    benchmark_symbol: str
    risk_asset_return: float
    benchmark_return: float
    policy_id: str | None
    operator: ADMAbsoluteMomentumComparisonOperator | None
    reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, ADMAbsoluteMomentumComparisonStatus):
            raise ValueError("status must be an ADMAbsoluteMomentumComparisonStatus")
        for name, value in (("risk_asset_symbol", self.risk_asset_symbol), ("benchmark_symbol", self.benchmark_symbol)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        for name, value in (("risk_asset_return", self.risk_asset_return), ("benchmark_return", self.benchmark_return)):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
                raise ValueError(f"{name} must be a finite number")
        if self.status is ADMAbsoluteMomentumComparisonStatus.UNAVAILABLE:
            if not isinstance(self.reason, str) or not self.reason.strip():
                raise ValueError("unavailable result requires a reason")
        else:
            if self.reason is not None or not isinstance(self.policy_id, str) or not self.policy_id.strip():
                raise ValueError("available comparison requires policy provenance and no reason")
            if not isinstance(self.operator, ADMAbsoluteMomentumComparisonOperator):
                raise ValueError("available comparison requires a valid operator")


def compare_adm_absolute_momentum_returns(
    inputs: ADMAbsoluteMomentumInputs,
    *,
    policy: ADMAbsoluteMomentumComparisonPolicy | None = None,
) -> ADMAbsoluteMomentumComparisonResult:
    """Compare explicit return inputs only when an explicit policy is supplied.

    No policy is inferred. A supplied policy is caller configuration and its
    presence does not itself constitute governance approval. The result does
    not construct ADMSignalInput or activate an ADM strategy.
    """

    if not isinstance(inputs, ADMAbsoluteMomentumInputs):
        raise ValueError("inputs must be an ADMAbsoluteMomentumInputs")
    if policy is not None and not isinstance(policy, ADMAbsoluteMomentumComparisonPolicy):
        raise ValueError("policy must be an ADMAbsoluteMomentumComparisonPolicy or None")

    common = dict(
        risk_asset_symbol=inputs.risk_asset_symbol,
        benchmark_symbol=inputs.benchmark_symbol,
        risk_asset_return=inputs.risk_asset_return,
        benchmark_return=inputs.benchmark_return,
    )
    if policy is None:
        return ADMAbsoluteMomentumComparisonResult(
            status=ADMAbsoluteMomentumComparisonStatus.UNAVAILABLE,
            **common,
            policy_id=None,
            operator=None,
            reason="comparison_policy_not_supplied",
        )
    if policy.benchmark_symbol != inputs.benchmark_symbol:
        return ADMAbsoluteMomentumComparisonResult(
            status=ADMAbsoluteMomentumComparisonStatus.UNAVAILABLE,
            **common,
            policy_id=policy.policy_id,
            operator=policy.operator,
            reason="policy_benchmark_does_not_match_input_benchmark",
        )

    if policy.operator is ADMAbsoluteMomentumComparisonOperator.RISK_RETURN_GT_BENCHMARK:
        matched = inputs.risk_asset_return > inputs.benchmark_return
    elif policy.operator is ADMAbsoluteMomentumComparisonOperator.RISK_RETURN_GTE_BENCHMARK:
        matched = inputs.risk_asset_return >= inputs.benchmark_return
    else:  # Defensive exhaustiveness guard for future enum extensions.
        return ADMAbsoluteMomentumComparisonResult(
            status=ADMAbsoluteMomentumComparisonStatus.UNAVAILABLE,
            **common,
            policy_id=policy.policy_id,
            operator=policy.operator,
            reason="unsupported_comparison_operator",
        )

    return ADMAbsoluteMomentumComparisonResult(
        status=(
            ADMAbsoluteMomentumComparisonStatus.TRUE
            if matched
            else ADMAbsoluteMomentumComparisonStatus.FALSE
        ),
        **common,
        policy_id=policy.policy_id,
        operator=policy.operator,
    )


@dataclass(frozen=True)
class ADMDataAssemblyReadiness:
    """Auditable data-gate status before ADM signal assembly.

    A successful instance means that relative-momentum freshness and the
    explicitly supplied absolute-momentum return inputs passed the requested
    age checks and share the same measurement endpoints. It is not an
    investment signal: benchmark approval, comparison expression, equality
    behavior, and adjusted-price semantics remain governance gates.
    """

    relative_momentum_freshness: ADMRelativeMomentumFreshnessResult
    absolute_momentum_inputs: ADMAbsoluteMomentumInputs
    max_age_days: int
    absolute_freshness_by_symbol: Mapping[str, ADMObservationFreshnessResult]
    unresolved_policy_gates: tuple[str, ...] = (
        "absolute_momentum_benchmark_approval",
        "absolute_momentum_comparison_expression_and_equality_behavior",
        "adjusted_price_semantics_approval",
        "provider_calendar_and_data_quality_policy_approval",
    )

    def __post_init__(self) -> None:
        if not isinstance(self.relative_momentum_freshness, ADMRelativeMomentumFreshnessResult):
            raise ValueError("relative_momentum_freshness must be an ADMRelativeMomentumFreshnessResult")
        if not isinstance(self.absolute_momentum_inputs, ADMAbsoluteMomentumInputs):
            raise ValueError("absolute_momentum_inputs must be an ADMAbsoluteMomentumInputs")
        if isinstance(self.max_age_days, bool) or not isinstance(self.max_age_days, int) or self.max_age_days < 0:
            raise ValueError("max_age_days must be a non-negative integer")
        relative = self.relative_momentum_freshness.relative_momentum_result
        absolute = self.absolute_momentum_inputs
        if (
            relative.current_target_date != absolute.current_target_date
            or relative.trailing_target_date != absolute.trailing_target_date
        ):
            raise ValueError("relative and absolute momentum target dates must match")
        if relative.field != absolute.field:
            raise ValueError("relative and absolute momentum fields must match")
        if relative.selection_policy_id != absolute.selection_policy_id:
            raise ValueError("relative and absolute momentum selection policies must match")
        if self.relative_momentum_freshness.max_age_days != self.max_age_days:
            raise ValueError("relative and absolute momentum must use the same maximum age")
        expected_symbols = {absolute.risk_asset_symbol, absolute.benchmark_symbol}
        if set(self.absolute_freshness_by_symbol) != expected_symbols:
            raise ValueError("absolute_freshness_by_symbol must cover risk asset and benchmark")
        normalized: dict[str, ADMObservationFreshnessResult] = {}
        for symbol in expected_symbols:
            freshness = self.absolute_freshness_by_symbol[symbol]
            pair = absolute.observation_pairs[symbol]
            if not isinstance(freshness, ADMObservationFreshnessResult):
                raise ValueError(f"freshness result for {symbol} is invalid")
            if freshness.symbol != symbol or freshness.field != absolute.field:
                raise ValueError(f"freshness result for {symbol} does not match absolute inputs")
            if freshness.selection_policy_id != absolute.selection_policy_id:
                raise ValueError("absolute freshness policy does not match absolute inputs")
            if freshness.current_observed_at != pair.current.observed_at or freshness.trailing_observed_at != pair.trailing.observed_at:
                raise ValueError(f"freshness observations for {symbol} do not match selected pair")
            if freshness.max_age_days != self.max_age_days:
                raise ValueError("all assembly freshness checks must use the same maximum age")
            normalized[symbol] = freshness
        if any(
            not isinstance(gate, str) or not gate.strip() for gate in self.unresolved_policy_gates
        ):
            raise ValueError("unresolved_policy_gates entries must be non-empty strings")
        object.__setattr__(self, "absolute_freshness_by_symbol", MappingProxyType(normalized))
        object.__setattr__(self, "unresolved_policy_gates", tuple(self.unresolved_policy_gates))

    @property
    def data_quality_passed(self) -> bool:
        """True only for a successfully constructed readiness result."""
        return True

    @property
    def signal_ready(self) -> bool:
        """True only when the caller has explicitly closed all policy gates."""
        return not self.unresolved_policy_gates


def prepare_adm_signal_assembly_readiness(
    relative_momentum_freshness: ADMRelativeMomentumFreshnessResult,
    absolute_momentum_inputs: ADMAbsoluteMomentumInputs,
    *,
    max_age_days: int,
) -> ADMDataAssemblyReadiness:
    """Validate cross-input consistency and freshness before signal assembly.

    This is deliberately a readiness audit, not a signal assembler. The same
    explicit calendar-day freshness limit is applied to both relative risk
    assets and the caller-supplied absolute risk/benchmark pair. Investment
    policy gates remain unresolved in the returned object; no boolean signal
    or ADMSignalInput is produced.
    """

    if not isinstance(relative_momentum_freshness, ADMRelativeMomentumFreshnessResult):
        raise ValueError("relative_momentum_freshness must be an ADMRelativeMomentumFreshnessResult")
    if not isinstance(absolute_momentum_inputs, ADMAbsoluteMomentumInputs):
        raise ValueError("absolute_momentum_inputs must be an ADMAbsoluteMomentumInputs")
    if isinstance(max_age_days, bool) or not isinstance(max_age_days, int) or max_age_days < 0:
        raise ValueError("max_age_days must be a non-negative integer")
    absolute_freshness = {
        symbol: validate_adm_observation_pair_freshness(pair, max_age_days=max_age_days)
        for symbol, pair in absolute_momentum_inputs.observation_pairs.items()
    }
    return ADMDataAssemblyReadiness(
        relative_momentum_freshness=relative_momentum_freshness,
        absolute_momentum_inputs=absolute_momentum_inputs,
        max_age_days=max_age_days,
        absolute_freshness_by_symbol=absolute_freshness,
    )


class ADMPolicyApprovalStatus(str, Enum):
    """Caller-attested governance status; not an automatic approval mechanism."""

    APPROVED = "approved"
    NOT_APPROVED = "not_approved"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ADMComparisonSignalGuardResult:
    """Guard decision for whether a comparison may enter signal assembly.

    This guard never creates ``ADMSignalInput`` and never activates a strategy.
    Approval status/reference are explicit caller-supplied provenance; the guard
    does not independently verify external governance records.
    """

    eligible_for_signal_assembly: bool
    comparison_status: ADMAbsoluteMomentumComparisonStatus
    policy_approval_status: ADMPolicyApprovalStatus
    policy_approval_reference: str | None
    blocked_reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.eligible_for_signal_assembly, bool):
            raise ValueError("eligible_for_signal_assembly must be boolean")
        if not isinstance(self.comparison_status, ADMAbsoluteMomentumComparisonStatus):
            raise ValueError("comparison_status must be an ADMAbsoluteMomentumComparisonStatus")
        if not isinstance(self.policy_approval_status, ADMPolicyApprovalStatus):
            raise ValueError("policy_approval_status must be an ADMPolicyApprovalStatus")
        if self.policy_approval_reference is not None and (
            not isinstance(self.policy_approval_reference, str) or not self.policy_approval_reference.strip()
        ):
            raise ValueError("policy_approval_reference must be a non-empty string when supplied")
        if any(not isinstance(reason, str) or not reason.strip() for reason in self.blocked_reasons):
            raise ValueError("blocked_reasons entries must be non-empty strings")
        object.__setattr__(self, "blocked_reasons", tuple(self.blocked_reasons))
        if self.eligible_for_signal_assembly != (len(self.blocked_reasons) == 0):
            raise ValueError("eligibility must exactly reflect whether blocked reasons are empty")


def guard_adm_comparison_for_signal_assembly(
    comparison: ADMAbsoluteMomentumComparisonResult,
    readiness: ADMDataAssemblyReadiness,
    *,
    policy_approval_status: ADMPolicyApprovalStatus = ADMPolicyApprovalStatus.UNKNOWN,
    policy_approval_reference: str | None = None,
) -> ADMComparisonSignalGuardResult:
    """Fail closed before a comparison is allowed into signal assembly.

    The comparison must be available, match the freshness-checked absolute
    return inputs, and have an explicit approval status/reference. Unresolved
    data/methodology gates block eligibility. No signal object is constructed.
    """

    if not isinstance(comparison, ADMAbsoluteMomentumComparisonResult):
        raise ValueError("comparison must be an ADMAbsoluteMomentumComparisonResult")
    if not isinstance(readiness, ADMDataAssemblyReadiness):
        raise ValueError("readiness must be an ADMDataAssemblyReadiness")
    if not isinstance(policy_approval_status, ADMPolicyApprovalStatus):
        raise ValueError("policy_approval_status must be an ADMPolicyApprovalStatus")
    if policy_approval_reference is not None and (
        not isinstance(policy_approval_reference, str) or not policy_approval_reference.strip()
    ):
        raise ValueError("policy_approval_reference must be a non-empty string when supplied")

    absolute = readiness.absolute_momentum_inputs
    reasons: list[str] = []
    if comparison.status is ADMAbsoluteMomentumComparisonStatus.UNAVAILABLE:
        reasons.append("comparison_unavailable")
    if (
        comparison.risk_asset_symbol != absolute.risk_asset_symbol
        or comparison.benchmark_symbol != absolute.benchmark_symbol
        or comparison.risk_asset_return != absolute.risk_asset_return
        or comparison.benchmark_return != absolute.benchmark_return
    ):
        reasons.append("comparison_does_not_match_readiness_inputs")
    if not readiness.data_quality_passed:
        reasons.append("data_quality_not_passed")
    if not readiness.signal_ready:
        reasons.append("unresolved_policy_gates")
    if policy_approval_status is not ADMPolicyApprovalStatus.APPROVED:
        reasons.append("comparison_policy_not_approved")
    if not policy_approval_reference:
        reasons.append("policy_approval_reference_missing")
    if comparison.status is not ADMAbsoluteMomentumComparisonStatus.UNAVAILABLE:
        if not comparison.policy_id:
            reasons.append("comparison_policy_provenance_missing")

    return ADMComparisonSignalGuardResult(
        eligible_for_signal_assembly=not reasons,
        comparison_status=comparison.status,
        policy_approval_status=policy_approval_status,
        policy_approval_reference=policy_approval_reference,
        blocked_reasons=tuple(dict.fromkeys(reasons)),
    )
