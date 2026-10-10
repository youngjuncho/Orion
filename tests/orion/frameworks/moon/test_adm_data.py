import pytest

from data import MarketDataPoint, MarketDataSet
from orion.frameworks.moon.adm_data import (
    derive_adm_monthly_target_dates,
    calculate_adm_asset_return,
    calculate_adm_observation_pair_return,
    select_adm_price_observations,
)


def make_dataset(*points: MarketDataPoint) -> MarketDataSet:
    return MarketDataSet(tuple(points), as_of="2026-10-09")


def test_monthly_target_dates_use_the_latest_completed_month() -> None:
    targets = derive_adm_monthly_target_dates("2026-10-10")

    assert targets.current_target_date == "2026-09-30"
    assert targets.trailing_target_date == "2025-09-30"
    assert targets.policy_id == "last-completed-month-end-v1"


def test_monthly_target_dates_align_leap_month_ends() -> None:
    targets = derive_adm_monthly_target_dates("2025-03-01")

    assert targets.current_target_date == "2025-02-28"
    assert targets.trailing_target_date == "2024-02-29"


def test_monthly_target_dates_exclude_current_month_on_first_day() -> None:
    targets = derive_adm_monthly_target_dates("2026-10-01")

    assert targets.current_target_date == "2026-09-30"


def test_adm_asset_return_uses_exact_caller_selected_observations() -> None:
    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 112.0, "fixture"),
        # Another field must not be substituted implicitly.
        MarketDataPoint("VTI", "close", "2026-10-09", 999.0, "fixture"),
    )

    result = calculate_adm_asset_return(
        dataset,
        symbol="VTI",
        field="adjusted_close",
        current_observed_at="2026-10-09",
        trailing_observed_at="2025-10-09",
    )

    assert result == pytest.approx(0.12)


def test_adm_asset_return_rejects_missing_exact_endpoint() -> None:
    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 112.0, "fixture"),
    )
    with pytest.raises(ValueError, match="missing observation"):
        calculate_adm_asset_return(
            dataset,
            symbol="VTI",
            field="adjusted_close",
            current_observed_at="2026-10-09",
            trailing_observed_at="2025-10-09",
        )


@pytest.mark.parametrize("value", [None, "112", 0, -1])
def test_adm_asset_return_rejects_invalid_price_values(value: object) -> None:
    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09", value, "fixture"),  # type: ignore[arg-type]
    )
    with pytest.raises(ValueError):
        calculate_adm_asset_return(
            dataset,
            symbol="VTI",
            field="adjusted_close",
            current_observed_at="2026-10-09",
            trailing_observed_at="2025-10-09",
        )


def test_adm_asset_return_does_not_choose_a_different_date_implicitly() -> None:
    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 112.0, "fixture"),
    )
    with pytest.raises(ValueError, match="missing observation"):
        calculate_adm_asset_return(
            dataset,
            symbol="VTI",
            field="adjusted_close",
            current_observed_at="2026-10-09",
            trailing_observed_at="2025-10-09",
        )


def test_market_data_contract_rejects_infinite_price_before_adm_calculation() -> None:
    with pytest.raises(ValueError, match="finite"):
        MarketDataPoint(
            "VTI", "adjusted_close", "2026-10-09", float("inf"), "fixture"
        )


def test_observation_selector_preserves_explicit_selection_and_policy_provenance() -> None:
    current = MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 112.0, "fixture")
    trailing = MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture")
    dataset = make_dataset(current, trailing)

    selected = select_adm_price_observations(
        dataset,
        symbol="VTI",
        field="adjusted_close",
        current_observed_at="2026-10-09",
        trailing_observed_at="2025-10-08",
        selection_policy_id="test-explicit-endpoints-v1",
    )

    assert selected.current is current
    assert selected.trailing is trailing
    assert selected.selection_policy_id == "test-explicit-endpoints-v1"


def test_observation_selector_does_not_choose_nearest_trailing_date() -> None:
    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 112.0, "fixture"),
    )
    with pytest.raises(ValueError, match="missing observation"):
        select_adm_price_observations(
            dataset,
            symbol="VTI",
            field="adjusted_close",
            current_observed_at="2026-10-09",
            trailing_observed_at="2025-10-09",
            selection_policy_id="unapproved-calendar-policy",
        )


def test_observation_selector_rejects_identical_endpoints() -> None:
    point = MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 112.0, "fixture")
    dataset = make_dataset(point)
    with pytest.raises(ValueError, match="different timestamps"):
        select_adm_price_observations(
            dataset,
            symbol="VTI",
            field="adjusted_close",
            current_observed_at="2026-10-09",
            trailing_observed_at="2026-10-09",
            selection_policy_id="test-explicit-endpoints-v1",
        )


def test_prior_observation_selector_uses_latest_available_date_on_or_before_target() -> None:
    from orion.frameworks.moon.adm_data import select_adm_price_observations_on_or_before

    current_prior = MarketDataPoint("VTI", "adjusted_close", "2026-10-30", 112.0, "fixture")
    trailing_prior = MarketDataPoint("VTI", "adjusted_close", "2025-10-30", 100.0, "fixture")
    dataset = MarketDataSet(
        (
            MarketDataPoint("VTI", "adjusted_close", "2026-10-29", 111.0, "fixture"),
            current_prior,
            MarketDataPoint("VTI", "adjusted_close", "2025-10-29", 99.0, "fixture"),
            trailing_prior,
            # Future observations must never be selected for either target.
            MarketDataPoint("VTI", "adjusted_close", "2026-11-02", 999.0, "fixture"),
        ),
        as_of="2026-11-02",
    )

    selected = select_adm_price_observations_on_or_before(
        dataset,
        symbol="VTI",
        field="adjusted_close",
        current_target_date="2026-10-31",  # Saturday
        trailing_target_date="2025-10-31",  # Friday target not present in fixture
    )

    assert selected.current is current_prior
    assert selected.trailing is trailing_prior
    assert selected.current_target_date == "2026-10-31"
    assert selected.trailing_target_date == "2025-10-31"
    assert selected.selection_policy_id == "prior-observation-on-or-before-v1"


def test_prior_observation_selector_rejects_no_observation_before_target() -> None:
    from orion.frameworks.moon.adm_data import select_adm_price_observations_on_or_before

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2026-10-10", 112.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2025-10-10", 100.0, "fixture"),
    )
    with pytest.raises(ValueError, match="missing observation on or before"):
        select_adm_price_observations_on_or_before(
            dataset,
            symbol="VTI",
            field="adjusted_close",
            current_target_date="2026-10-09",
            trailing_target_date="2025-10-09",
        )


def test_prior_observation_selector_rejects_timestamp_formats_outside_date_contract() -> None:
    from orion.frameworks.moon.adm_data import select_adm_price_observations_on_or_before

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09T00:00:00Z", 112.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2025-10-09", 100.0, "fixture"),
    )
    with pytest.raises(ValueError, match="observed_at must use YYYY-MM-DD format"):
        select_adm_price_observations_on_or_before(
            dataset,
            symbol="VTI",
            field="adjusted_close",
            current_target_date="2026-10-09",
            trailing_target_date="2025-10-09",
        )


def test_adm_pair_return_calculates_from_selected_observations() -> None:
    from orion.frameworks.moon.adm_data import select_adm_price_observations_on_or_before

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 112.0, "fixture"),
    )
    pair = select_adm_price_observations_on_or_before(
        dataset,
        symbol="VTI",
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
    )
    assert calculate_adm_observation_pair_return(pair) == pytest.approx(0.12)


def test_adm_pair_return_rejects_invalid_selected_price() -> None:
    from orion.frameworks.moon.adm_data import ADMPriceObservationPair

    pair = ADMPriceObservationPair(
        symbol="VTI",
        field="adjusted_close",
        current=MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 0, "fixture"),
        trailing=MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100, "fixture"),
        selection_policy_id="fixture-policy-v1",
    )
    with pytest.raises(ValueError, match="finite and positive"):
        calculate_adm_observation_pair_return(pair)


def test_adm_relative_momentum_calculates_vti_and_veu_with_shared_policy() -> None:
    from orion.frameworks.moon.adm_data import calculate_adm_relative_momentum

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 112.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2025-10-08", 200.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2026-10-08", 218.0, "fixture"),
    )

    result = calculate_adm_relative_momentum(
        dataset,
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        selection_policy_id="fixture-prior-bar-v1",
    )

    assert result.relative_momentum["VTI"] == pytest.approx(0.12)
    assert result.relative_momentum["VEU"] == pytest.approx(0.09)
    assert result.observation_pairs["VTI"].current.observed_at == "2026-10-08"
    assert result.observation_pairs["VEU"].trailing.observed_at == "2025-10-08"
    assert result.selection_policy_id == "fixture-prior-bar-v1"


def test_adm_relative_momentum_is_immutable_and_contains_only_risk_assets() -> None:
    from orion.frameworks.moon.adm_data import calculate_adm_relative_momentum

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 110.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2026-10-08", 105.0, "fixture"),
    )
    result = calculate_adm_relative_momentum(
        dataset,
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
    )

    assert set(result.relative_momentum) == {"VTI", "VEU"}
    with pytest.raises(TypeError):
        result.relative_momentum["VTI"] = 0.0  # type: ignore[index]


def test_adm_relative_momentum_fails_if_either_asset_is_missing() -> None:
    from orion.frameworks.moon.adm_data import calculate_adm_relative_momentum

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 110.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2025-10-08", 100.0, "fixture"),
    )
    with pytest.raises(ValueError, match="different dates"):
        calculate_adm_relative_momentum(
            dataset,
            field="adjusted_close",
            current_target_date="2026-10-09",
            trailing_target_date="2025-10-09",
        )


def test_adm_relative_momentum_does_not_construct_signal_or_absolute_momentum() -> None:
    from orion.frameworks.moon.adm_data import calculate_adm_relative_momentum

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 110.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2026-10-08", 105.0, "fixture"),
    )
    result = calculate_adm_relative_momentum(
        dataset,
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
    )

    assert not hasattr(result, "absolute_momentum_positive")
    assert not hasattr(result, "signal_input")


def test_adm_freshness_audit_accepts_explicit_max_age_and_records_ages() -> None:
    from orion.frameworks.moon.adm_data import (
        select_adm_price_observations_on_or_before,
        validate_adm_observation_pair_freshness,
    )

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 112.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
    )
    pair = select_adm_price_observations_on_or_before(
        dataset,
        symbol="VTI",
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        selection_policy_id="fixture-prior-bar-v1",
    )

    result = validate_adm_observation_pair_freshness(pair, max_age_days=1)
    assert result.current_age_days == 1
    assert result.trailing_age_days == 1
    assert result.max_age_days == 1
    assert result.selection_policy_id == "fixture-prior-bar-v1"


def test_adm_freshness_audit_rejects_observation_older_than_explicit_limit() -> None:
    from orion.frameworks.moon.adm_data import (
        select_adm_price_observations_on_or_before,
        validate_adm_observation_pair_freshness,
    )

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2026-10-06", 112.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
    )
    pair = select_adm_price_observations_on_or_before(
        dataset,
        symbol="VTI",
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
    )
    with pytest.raises(ValueError, match="maximum age"):
        validate_adm_observation_pair_freshness(pair, max_age_days=1)


@pytest.mark.parametrize("max_age_days", [-1, True, 1.5])
def test_adm_freshness_audit_requires_explicit_nonnegative_integer(max_age_days: object) -> None:
    from orion.frameworks.moon.adm_data import (
        select_adm_price_observations_on_or_before,
        validate_adm_observation_pair_freshness,
    )

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 112.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
    )
    pair = select_adm_price_observations_on_or_before(
        dataset,
        symbol="VTI",
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
    )
    with pytest.raises(ValueError, match="max_age_days must be a non-negative integer"):
        validate_adm_observation_pair_freshness(pair, max_age_days=max_age_days)  # type: ignore[arg-type]


def test_adm_freshness_audit_requires_target_dates() -> None:
    from orion.frameworks.moon.adm_data import (
        ADMPriceObservationPair,
        validate_adm_observation_pair_freshness,
    )

    pair = ADMPriceObservationPair(
        symbol="VTI",
        field="adjusted_close",
        current=MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 112.0, "fixture"),
        trailing=MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        selection_policy_id="fixture-policy-v1",
    )
    with pytest.raises(ValueError, match="must retain target dates"):
        validate_adm_observation_pair_freshness(pair, max_age_days=1)


def _relative_momentum_fixture(*, stale_veu: bool = False):
    from orion.frameworks.moon.adm_data import calculate_adm_relative_momentum

    current_veu = "2026-10-07" if stale_veu else "2026-10-09"
    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 112.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", current_veu, 109.0, "fixture"),
    )
    return calculate_adm_relative_momentum(
        dataset,
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
    )


def test_adm_relative_momentum_freshness_gate_accepts_both_assets_under_same_limit() -> None:
    from orion.frameworks.moon.adm_data import validate_adm_relative_momentum_freshness

    result = validate_adm_relative_momentum_freshness(
        _relative_momentum_fixture(), max_age_days=1
    )

    assert result.max_age_days == 1
    assert set(result.freshness_by_symbol) == {"VTI", "VEU"}
    assert result.freshness_by_symbol["VTI"].current_age_days == 0
    assert result.freshness_by_symbol["VEU"].current_age_days == 0


def test_adm_relative_momentum_freshness_gate_fails_if_either_asset_is_stale() -> None:
    from orion.frameworks.moon.adm_data import validate_adm_relative_momentum_freshness

    with pytest.raises(ValueError, match="observation exceeds the configured maximum age"):
        validate_adm_relative_momentum_freshness(
            _relative_momentum_fixture(stale_veu=True), max_age_days=1
        )

def test_adm_relative_momentum_freshness_gate_requires_explicit_nonnegative_limit() -> None:
    from orion.frameworks.moon.adm_data import validate_adm_relative_momentum_freshness

    for invalid in (-1, True, 1.5):
        with pytest.raises(ValueError, match="max_age_days must be a non-negative integer"):
            validate_adm_relative_momentum_freshness(
                _relative_momentum_fixture(), max_age_days=invalid  # type: ignore[arg-type]
            )

def test_adm_relative_momentum_freshness_gate_is_not_an_investment_signal() -> None:
    from orion.frameworks.moon.adm_data import (
        ADMRelativeMomentumFreshnessResult,
        validate_adm_relative_momentum_freshness,
    )

    gate = validate_adm_relative_momentum_freshness(
        _relative_momentum_fixture(), max_age_days=1
    )
    assert isinstance(gate, ADMRelativeMomentumFreshnessResult)
    assert not hasattr(gate, "signal")
    assert not hasattr(gate, "absolute_momentum_positive")


def test_absolute_momentum_inputs_calculate_both_returns_without_comparing_them() -> None:
    from orion.frameworks.moon.adm_data import calculate_adm_absolute_momentum_inputs

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 112.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2026-10-08", 104.0, "fixture"),
    )
    result = calculate_adm_absolute_momentum_inputs(
        dataset,
        risk_asset_symbol="VTI",
        benchmark_symbol="SGOV",
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        selection_policy_id="fixture-prior-bar-v1",
    )
    assert result.risk_asset_return == pytest.approx(0.12)
    assert result.benchmark_return == pytest.approx(0.04)
    assert set(result.observation_pairs) == {"VTI", "SGOV"}
    assert not hasattr(result, "absolute_momentum_positive")


def test_absolute_momentum_inputs_require_explicit_benchmark() -> None:
    from orion.frameworks.moon.adm_data import calculate_adm_absolute_momentum_inputs

    with pytest.raises(TypeError, match="benchmark_symbol"):
        calculate_adm_absolute_momentum_inputs(  # type: ignore[call-arg]
            make_dataset(),
            risk_asset_symbol="VTI",
            field="adjusted_close",
            current_target_date="2026-10-09",
            trailing_target_date="2025-10-09",
        )


def test_absolute_momentum_inputs_reject_same_risk_asset_and_benchmark() -> None:
    from orion.frameworks.moon.adm_data import calculate_adm_absolute_momentum_inputs

    with pytest.raises(ValueError, match="different instruments"):
        calculate_adm_absolute_momentum_inputs(
            make_dataset(),
            risk_asset_symbol="VTI",
            benchmark_symbol="VTI",
            field="adjusted_close",
            current_target_date="2026-10-09",
            trailing_target_date="2025-10-09",
        )


def test_absolute_momentum_inputs_fail_closed_when_benchmark_observation_missing() -> None:
    from orion.frameworks.moon.adm_data import calculate_adm_absolute_momentum_inputs

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 112.0, "fixture"),
    )
    with pytest.raises(ValueError, match="missing observation on or before"):
        calculate_adm_absolute_momentum_inputs(
            dataset,
            risk_asset_symbol="VTI",
            benchmark_symbol="SGOV",
            field="adjusted_close",
            current_target_date="2026-10-09",
            trailing_target_date="2025-10-09",
        )


def test_absolute_momentum_input_contract_requires_same_dates_and_policy() -> None:
    from dataclasses import replace
    from orion.frameworks.moon.adm_data import calculate_adm_absolute_momentum_inputs

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 112.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2026-10-08", 104.0, "fixture"),
    )
    result = calculate_adm_absolute_momentum_inputs(
        dataset,
        risk_asset_symbol="VTI",
        benchmark_symbol="SGOV",
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
    )
    bad_pair = replace(result.observation_pairs["SGOV"], selection_policy_id="different-policy")
    with pytest.raises(ValueError, match="same field and selection policy"):
        replace(result, observation_pairs={"VTI": result.observation_pairs["VTI"], "SGOV": bad_pair})


def test_adm_signal_assembly_readiness_passes_data_gates_but_not_policy_gates() -> None:
    from orion.frameworks.moon.adm_data import (
        calculate_adm_absolute_momentum_inputs,
        calculate_adm_relative_momentum,
        prepare_adm_signal_assembly_readiness,
        validate_adm_relative_momentum_freshness,
    )

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 110.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2026-10-09", 105.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2026-10-09", 104.0, "fixture"),
    )
    relative = calculate_adm_relative_momentum(
        dataset,
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        selection_policy_id="fixture-prior-bar-v1",
    )
    relative_gate = validate_adm_relative_momentum_freshness(relative, max_age_days=0)
    absolute = calculate_adm_absolute_momentum_inputs(
        dataset,
        risk_asset_symbol="VTI",
        benchmark_symbol="SGOV",
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        selection_policy_id="fixture-prior-bar-v1",
    )

    readiness = prepare_adm_signal_assembly_readiness(relative_gate, absolute, max_age_days=0)

    assert readiness.data_quality_passed is True
    assert readiness.signal_ready is False
    assert set(readiness.absolute_freshness_by_symbol) == {"VTI", "SGOV"}
    assert "absolute_momentum_benchmark_approval" not in readiness.unresolved_policy_gates
    assert "absolute_momentum_comparison_expression_and_equality_behavior" not in readiness.unresolved_policy_gates
    assert "adjusted_price_semantics_approval" in readiness.unresolved_policy_gates


def test_adm_signal_assembly_readiness_rejects_mismatched_target_dates() -> None:
    from orion.frameworks.moon.adm_data import (
        calculate_adm_absolute_momentum_inputs,
        calculate_adm_relative_momentum,
        prepare_adm_signal_assembly_readiness,
        validate_adm_relative_momentum_freshness,
    )

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 99.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 109.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 110.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2025-10-08", 99.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2026-10-08", 104.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2026-10-09", 105.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2026-10-08", 104.0, "fixture"),
    )
    relative = calculate_adm_relative_momentum(
        dataset,
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        selection_policy_id="fixture-prior-bar-v1",
    )
    relative_gate = validate_adm_relative_momentum_freshness(relative, max_age_days=0)
    absolute = calculate_adm_absolute_momentum_inputs(
        dataset,
        risk_asset_symbol="VTI",
        benchmark_symbol="SGOV",
        field="adjusted_close",
        current_target_date="2026-10-08",
        trailing_target_date="2025-10-08",
        selection_policy_id="fixture-prior-bar-v1",
    )
    with pytest.raises(ValueError, match="target dates must match"):
        prepare_adm_signal_assembly_readiness(relative_gate, absolute, max_age_days=0)


def test_adm_signal_assembly_readiness_fails_closed_when_absolute_input_is_stale() -> None:
    from orion.frameworks.moon.adm_data import (
        calculate_adm_absolute_momentum_inputs,
        calculate_adm_relative_momentum,
        prepare_adm_signal_assembly_readiness,
        validate_adm_relative_momentum_freshness,
    )

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 110.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2026-10-09", 105.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2026-10-08", 104.0, "fixture"),
    )
    relative = calculate_adm_relative_momentum(
        dataset,
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        selection_policy_id="fixture-prior-bar-v1",
    )
    relative_gate = validate_adm_relative_momentum_freshness(relative, max_age_days=0)
    absolute = calculate_adm_absolute_momentum_inputs(
        dataset,
        risk_asset_symbol="VTI",
        benchmark_symbol="SGOV",
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        selection_policy_id="fixture-prior-bar-v1",
    )
    with pytest.raises(ValueError, match="maximum age"):
        prepare_adm_signal_assembly_readiness(relative_gate, absolute, max_age_days=0)


def _absolute_inputs_for_comparison(risk_return: float = 0.12, benchmark_return: float = 0.04):
    from orion.frameworks.moon.adm_data import (
        ADMAbsoluteMomentumInputs,
        select_adm_price_observations_on_or_before,
    )

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-08", 100.0 * (1 + risk_return), "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2025-10-08", 100.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2026-10-08", 100.0 * (1 + benchmark_return), "fixture"),
    )
    pairs = {
        symbol: select_adm_price_observations_on_or_before(
            dataset,
            symbol=symbol,
            field="adjusted_close",
            current_target_date="2026-10-09",
            trailing_target_date="2025-10-09",
            selection_policy_id="fixture-prior-v1",
        )
        for symbol in ("VTI", "SGOV")
    }
    return ADMAbsoluteMomentumInputs(
        risk_asset_symbol="VTI",
        benchmark_symbol="SGOV",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        field="adjusted_close",
        selection_policy_id="fixture-prior-v1",
        risk_asset_return=risk_return,
        benchmark_return=benchmark_return,
        observation_pairs=pairs,
    )


def test_absolute_momentum_comparison_uses_d055_policy_without_override() -> None:
    from orion.frameworks.moon.adm_data import (
        ADMAbsoluteMomentumComparisonOperator,
        ADMAbsoluteMomentumComparisonStatus,
        compare_adm_absolute_momentum_returns,
    )

    result = compare_adm_absolute_momentum_returns(_absolute_inputs_for_comparison())
    assert result.status is ADMAbsoluteMomentumComparisonStatus.TRUE
    assert result.policy_id == "D-055"
    assert result.benchmark_symbol == "SGOV"
    assert result.operator is ADMAbsoluteMomentumComparisonOperator.RISK_RETURN_GT_BENCHMARK

    tied = compare_adm_absolute_momentum_returns(
        _absolute_inputs_for_comparison(0.04, 0.04)
    )
    assert tied.status is ADMAbsoluteMomentumComparisonStatus.FALSE


def test_absolute_momentum_comparison_uses_explicit_strict_operator() -> None:
    from orion.frameworks.moon.adm_data import (
        ADMAbsoluteMomentumComparisonOperator,
        ADMAbsoluteMomentumComparisonPolicy,
        ADMAbsoluteMomentumComparisonStatus,
        compare_adm_absolute_momentum_returns,
    )

    policy = ADMAbsoluteMomentumComparisonPolicy(
        policy_id="fixture-strict-comparison-v1",
        benchmark_symbol="SGOV",
        operator=ADMAbsoluteMomentumComparisonOperator.RISK_RETURN_GT_BENCHMARK,
    )
    assert compare_adm_absolute_momentum_returns(_absolute_inputs_for_comparison(0.12, 0.04), policy=policy).status is ADMAbsoluteMomentumComparisonStatus.TRUE
    assert compare_adm_absolute_momentum_returns(_absolute_inputs_for_comparison(0.04, 0.04), policy=policy).status is ADMAbsoluteMomentumComparisonStatus.FALSE


def test_absolute_momentum_comparison_operator_explicitly_controls_equality() -> None:
    from orion.frameworks.moon.adm_data import (
        ADMAbsoluteMomentumComparisonOperator,
        ADMAbsoluteMomentumComparisonPolicy,
        ADMAbsoluteMomentumComparisonStatus,
        compare_adm_absolute_momentum_returns,
    )

    policy = ADMAbsoluteMomentumComparisonPolicy(
        policy_id="fixture-inclusive-comparison-v1",
        benchmark_symbol="SGOV",
        operator=ADMAbsoluteMomentumComparisonOperator.RISK_RETURN_GTE_BENCHMARK,
    )
    result = compare_adm_absolute_momentum_returns(_absolute_inputs_for_comparison(0.04, 0.04), policy=policy)
    assert result.status is ADMAbsoluteMomentumComparisonStatus.TRUE


def test_absolute_momentum_comparison_rejects_policy_benchmark_mismatch_as_unavailable() -> None:
    from orion.frameworks.moon.adm_data import (
        ADMAbsoluteMomentumComparisonOperator,
        ADMAbsoluteMomentumComparisonPolicy,
        ADMAbsoluteMomentumComparisonStatus,
        compare_adm_absolute_momentum_returns,
    )

    policy = ADMAbsoluteMomentumComparisonPolicy(
        policy_id="fixture-wrong-benchmark-v1",
        benchmark_symbol="BIL",
        operator=ADMAbsoluteMomentumComparisonOperator.RISK_RETURN_GT_BENCHMARK,
    )
    result = compare_adm_absolute_momentum_returns(_absolute_inputs_for_comparison(), policy=policy)
    assert result.status is ADMAbsoluteMomentumComparisonStatus.UNAVAILABLE
    assert result.reason == "policy_benchmark_does_not_match_input_benchmark"


def _readiness_for_comparison_guard():
    from orion.frameworks.moon.adm_data import (
        calculate_adm_absolute_momentum_inputs,
        calculate_adm_relative_momentum,
        prepare_adm_signal_assembly_readiness,
        validate_adm_relative_momentum_freshness,
    )

    dataset = make_dataset(
        MarketDataPoint("VTI", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VTI", "adjusted_close", "2026-10-09", 112.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("VEU", "adjusted_close", "2026-10-09", 109.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2025-10-09", 100.0, "fixture"),
        MarketDataPoint("SGOV", "adjusted_close", "2026-10-09", 104.0, "fixture"),
    )
    relative = calculate_adm_relative_momentum(
        dataset,
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        selection_policy_id="fixture-prior-v1",
    )
    relative_gate = validate_adm_relative_momentum_freshness(relative, max_age_days=0)
    absolute = calculate_adm_absolute_momentum_inputs(
        dataset,
        risk_asset_symbol="VTI",
        benchmark_symbol="SGOV",
        field="adjusted_close",
        current_target_date="2026-10-09",
        trailing_target_date="2025-10-09",
        selection_policy_id="fixture-prior-v1",
    )
    readiness = prepare_adm_signal_assembly_readiness(relative_gate, absolute, max_age_days=0)
    return readiness


def _comparison_for_readiness(readiness):
    from orion.frameworks.moon.adm_data import (
        ADMAbsoluteMomentumComparisonOperator,
        ADMAbsoluteMomentumComparisonPolicy,
        compare_adm_absolute_momentum_returns,
    )

    policy = ADMAbsoluteMomentumComparisonPolicy(
        policy_id="fixture-approved-policy-v1",
        benchmark_symbol="SGOV",
        operator=ADMAbsoluteMomentumComparisonOperator.RISK_RETURN_GT_BENCHMARK,
    )
    return compare_adm_absolute_momentum_returns(readiness.absolute_momentum_inputs, policy=policy)


def test_comparison_signal_guard_blocks_unknown_approval_and_open_data_gates() -> None:
    from orion.frameworks.moon.adm_data import (
        ADMAbsoluteMomentumComparisonStatus,
        ADMComparisonSignalGuardResult,
        ADMPolicyApprovalStatus,
        compare_adm_absolute_momentum_returns,
        guard_adm_comparison_for_signal_assembly,
    )

    readiness = _readiness_for_comparison_guard()
    comparison = compare_adm_absolute_momentum_returns(readiness.absolute_momentum_inputs)
    result = guard_adm_comparison_for_signal_assembly(comparison, readiness)
    assert isinstance(result, ADMComparisonSignalGuardResult)
    assert result.comparison_status is ADMAbsoluteMomentumComparisonStatus.TRUE
    assert result.policy_approval_status is ADMPolicyApprovalStatus.UNKNOWN
    assert result.eligible_for_signal_assembly is False
    assert "production_data_governance_not_approved" in result.blocked_reasons
    assert "unresolved_policy_gates" in result.blocked_reasons


def test_comparison_signal_guard_requires_explicit_approval_reference() -> None:
    from orion.frameworks.moon.adm_data import (
        ADMPolicyApprovalStatus,
        guard_adm_comparison_for_signal_assembly,
    )

    readiness = _readiness_for_comparison_guard()
    result = guard_adm_comparison_for_signal_assembly(
        _comparison_for_readiness(readiness),
        readiness,
        policy_approval_status=ADMPolicyApprovalStatus.APPROVED,
    )
    assert result.eligible_for_signal_assembly is False
    assert "unresolved_policy_gates" in result.blocked_reasons
    assert "production_governance_reference_missing" in result.blocked_reasons


def test_comparison_signal_guard_blocks_comparison_return_mismatch() -> None:
    from dataclasses import replace
    from orion.frameworks.moon.adm_data import (
        ADMAbsoluteMomentumComparisonStatus,
        ADMComparisonSignalGuardResult,
        ADMPolicyApprovalStatus,
        guard_adm_comparison_for_signal_assembly,
    )

    readiness = _readiness_for_comparison_guard()
    comparison = replace(_comparison_for_readiness(readiness), risk_asset_return=0.99)
    result = guard_adm_comparison_for_signal_assembly(
        comparison,
        readiness,
        policy_approval_status=ADMPolicyApprovalStatus.APPROVED,
        policy_approval_reference="decision-log:D-XXX",
    )
    assert isinstance(result, ADMComparisonSignalGuardResult)
    assert result.comparison_status is ADMAbsoluteMomentumComparisonStatus.TRUE
    assert result.eligible_for_signal_assembly is False
    assert "comparison_does_not_match_readiness_inputs" in result.blocked_reasons


def test_comparison_signal_guard_allows_only_explicitly_closed_hypothetical_contract() -> None:
    from dataclasses import replace
    from orion.frameworks.moon.adm_data import (
        ADMPolicyApprovalStatus,
        guard_adm_comparison_for_signal_assembly,
    )

    readiness = _readiness_for_comparison_guard()
    # Fixture-only simulation of future governance closure; no production policy
    # is being approved by this test.
    closed_readiness = replace(readiness, unresolved_policy_gates=())
    result = guard_adm_comparison_for_signal_assembly(
        _comparison_for_readiness(closed_readiness),
        closed_readiness,
        policy_approval_status=ADMPolicyApprovalStatus.APPROVED,
        policy_approval_reference="fixture-governance-record-v1",
    )
    assert result.eligible_for_signal_assembly is True
    assert result.blocked_reasons == ()
    # Guard emits a readiness decision only; it never constructs ADMSignalInput.


def test_adm_composed_data_pipeline_keeps_readiness_distinct_from_signal_approval() -> None:
    from orion.frameworks.moon.adm_data import (
        ADMAbsoluteMomentumComparisonStatus,
        ADMPolicyApprovalStatus,
        compare_adm_absolute_momentum_returns,
        guard_adm_comparison_for_signal_assembly,
    )

    readiness = _readiness_for_comparison_guard()
    relative = readiness.relative_momentum_freshness.relative_momentum_result

    # The relative-return stage retains both assets and the same measurement
    # contract used by the absolute-input stage.
    assert set(relative.relative_momentum) == {"VTI", "VEU"}
    assert relative.current_target_date == readiness.absolute_momentum_inputs.current_target_date
    assert relative.trailing_target_date == readiness.absolute_momentum_inputs.trailing_target_date
    assert relative.field == readiness.absolute_momentum_inputs.field
    assert relative.selection_policy_id == readiness.absolute_momentum_inputs.selection_policy_id
    assert readiness.data_quality_passed is True

    # D-055 provides the approved comparison rule; open data gates and the
    # missing caller approval attestation still prevent signal integration.
    comparison = compare_adm_absolute_momentum_returns(readiness.absolute_momentum_inputs)
    assert comparison.status is ADMAbsoluteMomentumComparisonStatus.TRUE
    guarded = guard_adm_comparison_for_signal_assembly(
        comparison,
        readiness,
        policy_approval_status=ADMPolicyApprovalStatus.UNKNOWN,
    )
    assert guarded.eligible_for_signal_assembly is False
    assert "production_data_governance_not_approved" in guarded.blocked_reasons
    assert "unresolved_policy_gates" in guarded.blocked_reasons
