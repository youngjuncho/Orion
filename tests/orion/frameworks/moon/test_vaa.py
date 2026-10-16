import pytest

from orion.frameworks.moon.vaa import (
    VAA_DEFENSIVE_ASSETS,
    VAA_OFFENSIVE_ASSETS,
    VAASignalInput,
    VAAStrategy,
    calculate_13612w_momentum,
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
