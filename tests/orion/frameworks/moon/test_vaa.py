from calendar import monthrange
from datetime import date

import pytest

from data import MarketDataPoint, MarketDataSet

from orion.frameworks.moon.vaa import (
    VAA_DEFENSIVE_ASSETS,
    VAA_OFFENSIVE_ASSETS,
    VAASignalInput,
    VAAStrategy,
    calculate_13612w_momentum,
    build_vaa_signal_input,
    build_vaa_signal_input_from_dataset,
)


def make_input(breadth, *, defensive_top="SHY", offensive_top=None):
    offensive = {asset: 1.0 for asset in VAA_OFFENSIVE_ASSETS}
    for asset in VAA_OFFENSIVE_ASSETS[:breadth]:
        offensive[asset] = 0.0
    if offensive_top is None and breadth < len(VAA_OFFENSIVE_ASSETS):
        offensive_top = VAA_OFFENSIVE_ASSETS[breadth]
    if offensive_top is not None and breadth < len(VAA_OFFENSIVE_ASSETS):
        offensive[offensive_top] = 10.0
    defensive = {asset: 1.0 for asset in VAA_DEFENSIVE_ASSETS}
    defensive[defensive_top] = 10.0
    return VAASignalInput("2026-09-30", offensive, defensive)


def test_13612w_momentum_uses_weighted_1_3_6_12_month_returns():
    prices = [100.0] * 13
    prices[-1] = 110.0
    expected = 0.1 * (12 + 4 + 2 + 1)  # each trailing base is 100
    assert calculate_13612w_momentum(prices) == pytest.approx(expected)


def test_13612w_requires_thirteen_positive_finite_prices():
    with pytest.raises(ValueError, match="13 monthly prices"):
        calculate_13612w_momentum([100.0] * 12)
    with pytest.raises(ValueError, match="finite positive"):
        calculate_13612w_momentum([100.0] * 12 + [0.0])


@pytest.mark.parametrize(
    ("breadth", "expected_state", "expected_weights"),
    [(0, "Offensive", (0.5, 0.5)), (1, "Offensive", (0.5, 0.5)),
     (2, "Mixed", (0.5, 0.5)), (3, "Mixed", (0.5, 0.5)),
     (4, "Defensive", (1.0,)), (12, "Defensive", (1.0,))],
)
def test_easy_trading_breadth_boundaries(breadth, expected_state, expected_weights):
    result = VAAStrategy().calculate_signal(make_input(breadth))
    assert result.state == expected_state
    assert result.weights == expected_weights
    assert sum(result.weights) == pytest.approx(1.0)
    assert len(result.selected_assets) == len(set(result.selected_assets))
    assert result.metadata["offensive_nonpositive_count"] == str(breadth)


def test_mixed_mode_deduplicates_lqd_overlap():
    result = VAAStrategy().calculate_signal(make_input(2, offensive_top="LQD", defensive_top="LQD"))
    assert result.selected_assets == ("LQD", "SHY")
    assert result.weights == (0.5, 0.5)


def test_missing_universe_score_fails_closed():
    offensive = {asset: 1.0 for asset in VAA_OFFENSIVE_ASSETS[:-1]}
    defensive = {asset: 1.0 for asset in VAA_DEFENSIVE_ASSETS}
    with pytest.raises(ValueError, match="missing: LQD"):
        VAASignalInput("2026-09-30", offensive, defensive)


def test_ties_follow_configured_universe_order():
    inputs = VAASignalInput(
        "2026-09-30",
        {asset: 1.0 for asset in VAA_OFFENSIVE_ASSETS},
        {asset: 1.0 for asset in VAA_DEFENSIVE_ASSETS},
    )
    assert VAAStrategy().calculate_signal(inputs).selected_assets == ("SPY", "IWM")


def dated_series(start_year=2025, start_month=9, count=13, price=100.0):
    result = []
    year, month = start_year, start_month
    for _ in range(count):
        result.append((date(year, month, monthrange(year, month)[1]).isoformat(), price))
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    return result


def complete_dated_mapping():
    return {asset: dated_series() for asset in set(VAA_OFFENSIVE_ASSETS + VAA_DEFENSIVE_ASSETS)}


def test_build_vaa_signal_input_from_complete_aligned_monthly_series():
    inputs = build_vaa_signal_input(complete_dated_mapping(), as_of_date="2026-10-18")
    assert inputs.signal_date == "2026-09-30"
    assert set(inputs.offensive_momentum) == set(VAA_OFFENSIVE_ASSETS)
    assert set(inputs.defensive_momentum) == set(VAA_DEFENSIVE_ASSETS)
    assert all(score == pytest.approx(0.0) for score in inputs.offensive_momentum.values())


def test_dated_builder_rejects_missing_asset_and_misaligned_dates():
    data = complete_dated_mapping()
    data.pop("SPY")
    with pytest.raises(ValueError, match="monthly_observations is missing: SPY"):
        build_vaa_signal_input(data, as_of_date="2026-10-18")
    data = complete_dated_mapping()
    data["SPY"] = data["SPY"][:-1] + [("2026-09-29", 100.0)]
    with pytest.raises(ValueError, match="same observation dates"):
        build_vaa_signal_input(data, as_of_date="2026-10-18")


def test_dated_builder_rejects_skipped_month_invalid_price_and_stale_month():
    data = complete_dated_mapping()
    data["SPY"] = data["SPY"][:2] + data["SPY"][3:]
    with pytest.raises(ValueError, match="at least 13"):
        build_vaa_signal_input(data, as_of_date="2026-10-18")
    data = complete_dated_mapping()
    data["SPY"][-1] = (data["SPY"][-1][0], float("nan"))
    with pytest.raises(ValueError, match="finite positive"):
        build_vaa_signal_input(data, as_of_date="2026-10-18")
    with pytest.raises(ValueError, match="last completed calendar month"):
        build_vaa_signal_input(complete_dated_mapping(), as_of_date="2026-11-18")


def test_market_dataset_adapter_accepts_complete_single_source_dataset():
    points = []
    for asset, observations in complete_dated_mapping().items():
        points.extend(MarketDataPoint(asset, "adjusted_close", observed, price, "fixture")
                      for observed, price in observations)
    dataset = MarketDataSet(tuple(points), as_of="2026-10-18")
    assert build_vaa_signal_input_from_dataset(dataset).signal_date == "2026-09-30"


def test_market_dataset_adapter_rejects_mixed_sources_and_missing_history():
    points = []
    for asset, observations in complete_dated_mapping().items():
        source = "provider-a" if asset == "SPY" else "provider-b"
        points.extend(MarketDataPoint(asset, "adjusted_close", observed, price, source)
                      for observed, price in observations)
    with pytest.raises(ValueError, match="single data source"):
        build_vaa_signal_input_from_dataset(MarketDataSet(tuple(points), as_of="2026-10-18"))

    points = [point for point in points if point.symbol != "SPY"]
    with pytest.raises(ValueError, match="missing adjusted_close observations for: SPY"):
        build_vaa_signal_input_from_dataset(MarketDataSet(tuple(points), as_of="2026-10-18"))


def test_public_moon_interface_exposes_vaa_and_preserves_adm():
    from orion.frameworks.moon import ADMStrategy as PublicADMStrategy
    from orion.frameworks.moon import VAAStrategy as PublicVAAStrategy
    assert PublicADMStrategy.__name__ == "ADMStrategy"
    assert PublicVAAStrategy is VAAStrategy
