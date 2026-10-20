import pytest

from orion.frameworks.moon.baa import (
    BAA_CANARY_ASSETS,
    BAA_DEFENSIVE_ASSETS,
    BAA_OFFENSIVE_ASSETS,
    BAA_REQUIRED_ASSETS,
    BAASignalInput,
    BAAStrategy,
    calculate_13612w_momentum,
    calculate_sma12_momentum,
)


def make_prices(*, canary_negative=(), latest_by_asset=None):
    latest_by_asset = latest_by_asset or {}
    prices = {}
    for asset in BAA_REQUIRED_ASSETS:
        latest = latest_by_asset.get(asset, 110.0)
        if asset in canary_negative:
            latest = 90.0
        prices[asset] = [100.0] * 12 + [latest]
    return prices


def make_input(*, canary_negative=(), latest_by_asset=None):
    return BAASignalInput(
        "2026-09-30",
        make_prices(canary_negative=canary_negative, latest_by_asset=latest_by_asset),
    )


def test_13612w_uses_weighted_1_3_6_12_month_returns():
    prices = [100.0] * 13
    prices[-1] = 110.0
    assert calculate_13612w_momentum(prices) == pytest.approx(1.9)


def test_sma12_momentum_uses_current_and_prior_twelve_months():
    prices = [100.0] * 12 + [130.0]
    assert calculate_sma12_momentum(prices) == pytest.approx(130.0 / (1330.0 / 13) - 1.0)


def test_momentum_rejects_insufficient_or_invalid_prices():
    with pytest.raises(ValueError, match="13 monthly prices"):
        calculate_13612w_momentum([100.0] * 12)
    with pytest.raises(ValueError, match="finite positive"):
        calculate_sma12_momentum([100.0] * 12 + [float("nan")])


def test_baa_g12_universes_are_explicit_and_distinct():
    assert BAA_CANARY_ASSETS == ("SPY", "VWO", "VEA", "BND")
    assert len(BAA_OFFENSIVE_ASSETS) == 12
    assert len(BAA_DEFENSIVE_ASSETS) == 7
    assert "QQQ" in BAA_OFFENSIVE_ASSETS and "QQQ" not in BAA_CANARY_ASSETS


def test_all_nonnegative_canary_scores_select_six_offensive_assets():
    result = BAAStrategy().calculate_signal(make_input())
    assert result.state == "Risk On"
    assert len(result.selected_assets) == 6
    assert result.weights == pytest.approx((1 / 6,) * 6)
    assert sum(result.weights) == pytest.approx(1.0)
    assert result.metadata["execution_status"] == "research-only-not-executable"


@pytest.mark.parametrize("negative_asset", BAA_CANARY_ASSETS)
def test_any_negative_canary_score_selects_defensive_assets(negative_asset):
    result = BAAStrategy().calculate_signal(make_input(canary_negative=(negative_asset,)))
    assert result.state == "Risk Off"
    assert sum(result.weights) == pytest.approx(1.0)
    assert len(result.selected_assets) <= 3


def test_zero_canary_momentum_is_not_negative():
    prices = make_prices()
    prices["SPY"] = [100.0] * 13
    result = BAAStrategy().calculate_signal(BAASignalInput("2026-09-30", prices))
    assert result.state == "Risk On"


def test_defensive_bil_floor_uses_13612w_after_sma12_ranking():
    prices = make_prices(latest_by_asset={
        "TIP": 160.0, "DBC": 140.0, "IEF": 130.0, "BIL": 110.0,
        "TLT": 105.0, "LQD": 104.0, "BND": 103.0, "SPY": 90.0,
    })
    # TIP has strong SMA12 rank but weak 13612W absolute momentum vs BIL.
    prices["TIP"] = [100.0] * 11 + [213.0, 160.0]
    result = BAAStrategy().calculate_signal(BAASignalInput("2026-09-30", prices))
    assert result.state == "Risk Off"
    assert result.selected_assets == ("BIL", "DBC", "IEF")
    assert result.weights == pytest.approx((1 / 3, 1 / 3, 1 / 3))
    assert result.metadata["bil_replacements"] == "TIP"


def test_multiple_bil_replacements_are_aggregated_into_unique_asset_weights():
    prices = make_prices(latest_by_asset={
        "TIP": 150.0, "DBC": 140.0, "IEF": 130.0, "BIL": 110.0,
        "TLT": 105.0, "LQD": 104.0, "BND": 103.0, "SPY": 90.0,
    })
    # All three top-ranked defensive assets have 13612W below BIL.
    for asset, previous_month_price in (("TIP", 300.0), ("DBC", 300.0), ("IEF", 300.0)):
        prices[asset] = [100.0] * 11 + [previous_month_price, prices[asset][-1]]
    result = BAAStrategy().calculate_signal(BAASignalInput("2026-09-30", prices))
    assert result.state == "Risk Off"
    assert result.selected_assets == ("BIL",)
    assert result.weights == pytest.approx((1.0,))
    assert result.metadata["bil_replacements"] == "TIP,DBC,IEF"


def test_missing_required_asset_fails_closed():
    prices = make_prices()
    del prices["BND"]
    with pytest.raises(ValueError, match="missing required assets: BND"):
        BAASignalInput("2026-09-30", prices)


def _monthly_dataset(*, missing=None, duplicate=None, currency="USD", field="adjusted_close",
                     verified=True, date_mismatch=None):
    from data.contracts import MarketDataPoint, MarketDataSet

    # Verified last US trading-session dates for the synthetic 2025-09..2026-09 panel.
    session_dates = (
        "2025-09-30", "2025-10-31", "2025-11-28", "2025-12-31",
        "2026-01-30", "2026-02-27", "2026-03-31", "2026-04-30",
        "2026-05-29", "2026-06-30", "2026-07-31", "2026-08-31",
        "2026-09-30",
    )
    observations = []
    for offset, observed_at in enumerate(session_dates):
        month_key = observed_at[:7]
        for asset in BAA_REQUIRED_ASSETS:
            if missing == (asset, month_key):
                continue
            observations.append(MarketDataPoint(
                symbol=asset,
                field=field,
                observed_at=(
                    f"{month_key}-29" if date_mismatch == (asset, month_key) else observed_at
                ),
                value=100.0 + offset,
                source="fixture-provider",
                currency=currency,
                metadata={
                    "provider_field": "5. adjusted close",
                    **({"month_end_session_verified": "true"} if verified else {}),
                },
            ))
            if duplicate == (asset, month_key):
                observations.append(MarketDataPoint(
                    symbol=asset,
                    field=field,
                    observed_at=f"{month_key}-15",
                    value=101.0 + offset,
                    source="fixture-provider",
                    currency=currency,
                    metadata={
                        "provider_field": "5. adjusted close",
                        "month_end_session_verified": "true",
                    },
                ))
    return MarketDataSet(tuple(observations), as_of="2026-10-20")


def test_build_baa_input_aligns_thirteen_months_in_oldest_to_newest_order():
    from orion.frameworks.moon.baa import build_baa_signal_input

    inputs = build_baa_signal_input(_monthly_dataset(), signal_month="2026-09")
    assert inputs.signal_date == "2026-09-30"
    assert inputs.monthly_prices["SPY"] == tuple(100.0 + i for i in range(13))
    assert all(len(prices) == 13 for prices in inputs.monthly_prices.values())


def test_build_baa_input_fails_closed_on_a_missing_month():
    from orion.frameworks.moon.baa import build_baa_signal_input

    dataset = _monthly_dataset(missing=("VWO", "2026-02"))
    with pytest.raises(ValueError, match="VWO is missing adjusted_close months: 2026-02"):
        build_baa_signal_input(dataset, signal_month="2026-09")


def test_build_baa_input_rejects_multiple_observations_in_one_month():
    from orion.frameworks.moon.baa import build_baa_signal_input

    dataset = _monthly_dataset(duplicate=("SPY", "2026-04"))
    with pytest.raises(ValueError, match="multiple adjusted_close observations for SPY in 2026-04"):
        build_baa_signal_input(dataset, signal_month="2026-09")


def test_build_baa_input_rejects_unverified_month_end_session():
    from orion.frameworks.moon.baa import build_baa_signal_input

    with pytest.raises(ValueError, match="lacks verified final US trading-session metadata"):
        build_baa_signal_input(_monthly_dataset(verified=False), signal_month="2026-09")


def test_build_baa_input_rejects_misaligned_final_session_dates():
    from orion.frameworks.moon.baa import build_baa_signal_input

    dataset = _monthly_dataset(date_mismatch=("SPY", "2026-09"))
    with pytest.raises(ValueError, match="must share one verified final US trading-session date"):
        build_baa_signal_input(dataset, signal_month="2026-09")


def test_build_baa_input_requires_usd_prices():
    from orion.frameworks.moon.baa import build_baa_signal_input

    with pytest.raises(ValueError, match="SPY observation in 2025-09 must use USD currency"):
        build_baa_signal_input(_monthly_dataset(currency="KRW"), signal_month="2026-09")


def test_build_baa_input_does_not_silently_substitute_raw_close():
    from orion.frameworks.moon.baa import build_baa_signal_input

    with pytest.raises(ValueError, match="SPY is missing adjusted_close months"):
        build_baa_signal_input(_monthly_dataset(field="close"), signal_month="2026-09")


def test_build_baa_input_rejects_invalid_signal_month():
    from orion.frameworks.moon.baa import build_baa_signal_input

    with pytest.raises(ValueError, match="signal_month must use YYYY-MM format"):
        build_baa_signal_input(_monthly_dataset(), signal_month="2026-13")


def test_build_baa_input_rejects_current_incomplete_month():
    from orion.frameworks.moon.baa import build_baa_signal_input

    with pytest.raises(ValueError, match="signal_month must be earlier than the dataset.as_of month"):
        build_baa_signal_input(_monthly_dataset(), signal_month="2026-10")


def test_offensive_ranking_selects_exact_top_six_in_descending_order():
    latest = {
        asset: 140.0 - index
        for index, asset in enumerate(BAA_OFFENSIVE_ASSETS)
    }
    # Keep every canary asset positive so the offensive branch is selected.
    latest.update({asset: max(latest.get(asset, 110.0), 110.0) for asset in BAA_CANARY_ASSETS})
    result = BAAStrategy().calculate_signal(make_input(latest_by_asset=latest))
    expected_rank = sorted(
        BAA_OFFENSIVE_ASSETS,
        key=lambda asset: (-latest.get(asset, 110.0), BAA_OFFENSIVE_ASSETS.index(asset)),
    )
    assert result.state == "Risk On"
    assert result.metadata["offensive_sma12_ranked"].split(",") == expected_rank
    assert result.selected_assets == tuple(expected_rank[:6])
    assert result.weights == pytest.approx((1 / 6,) * 6)


def test_equal_sma12_scores_use_declared_universe_order_deterministically():
    inputs = make_input()
    first = BAAStrategy().calculate_signal(inputs)
    second = BAAStrategy().calculate_signal(inputs)
    assert first == second
    assert first.metadata["offensive_sma12_ranked"].split(",") == list(BAA_OFFENSIVE_ASSETS)
    assert first.selected_assets == BAA_OFFENSIVE_ASSETS[:6]


def test_risk_off_equal_defensive_scores_preserve_order_and_do_not_replace_equal_bil():
    # SPY's negative canary momentum switches the regime. All defensive assets
    # have identical SMA12 and 13612W scores, so tie-breaking must be stable;
    # the strict '< BIL' floor must not replace assets on equality.
    result = BAAStrategy().calculate_signal(make_input(canary_negative=("SPY",)))
    assert result.state == "Risk Off"
    assert result.metadata["defensive_sma12_ranked"].split(",") == list(BAA_DEFENSIVE_ASSETS)
    assert result.metadata["selected_slots"].split(",") == ["TIP", "DBC", "BIL"]
    assert result.selected_assets == ("TIP", "DBC", "BIL")
    assert result.metadata["bil_replacements"] == ""
    assert result.weights == pytest.approx((1 / 3,) * 3)


def test_canary_zero_boundary_is_risk_on_and_repeatable():
    prices = make_prices()
    prices["SPY"] = [100.0] * 13
    inputs = BAASignalInput("2026-09-30", prices)
    strategy = BAAStrategy()
    first = strategy.calculate_signal(inputs)
    second = strategy.calculate_signal(inputs)
    assert first.state == "Risk On"
    assert first == second
    assert first.metadata["canary_13612w"].startswith("SPY:0;")


def test_signal_output_is_unique_fully_weighted_and_research_only_in_both_regimes():
    for inputs, expected_state in (
        (make_input(), "Risk On"),
        (make_input(canary_negative=("VWO",)), "Risk Off"),
    ):
        result = BAAStrategy().calculate_signal(inputs)
        assert result.state == expected_state
        assert len(result.selected_assets) == len(set(result.selected_assets))
        assert all(weight >= 0 for weight in result.weights)
        assert sum(result.weights) == pytest.approx(1.0)
        assert result.metadata["execution_status"] == "research-only-not-executable"
