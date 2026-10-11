from __future__ import annotations

from dataclasses import dataclass

import pytest

from data.contracts import MarketDataPoint, MarketDataSet
from orion.frameworks.moon.adm_data import ADMAbsoluteMomentumComparisonStatus
from orion.frameworks.moon.adm_workflow import run_adm_data_workflow


def fixture_dataset(*, as_of: str = "2026-10-10") -> MarketDataSet:
    return MarketDataSet(
        (
            MarketDataPoint("VTI", "adjusted_close", "2025-09-30", 100.0, "fixture"),
            MarketDataPoint("VTI", "adjusted_close", "2026-09-30", 115.0, "fixture"),
            MarketDataPoint("VEU", "adjusted_close", "2025-09-30", 100.0, "fixture"),
            MarketDataPoint("VEU", "adjusted_close", "2026-09-30", 110.0, "fixture"),
            MarketDataPoint("SGOV", "adjusted_close", "2025-09-30", 100.0, "fixture"),
            MarketDataPoint("SGOV", "adjusted_close", "2026-09-30", 104.0, "fixture"),
        ),
        as_of=as_of,
    )


@dataclass
class FakeProvider:
    dataset: MarketDataSet
    calls: int = 0

    def load(self) -> MarketDataSet:
        self.calls += 1
        return self.dataset


def test_workflow_loads_once_and_returns_assessment_only() -> None:
    dataset = fixture_dataset()
    provider = FakeProvider(dataset)

    result = run_adm_data_workflow(provider)

    assert provider.calls == 1
    assert result.dataset is dataset
    assert result.assessment.targets.current_target_date == "2026-09-30"
    assert result.assessment.selected_risk_asset == "VTI"
    assert result.assessment.comparison.status is ADMAbsoluteMomentumComparisonStatus.TRUE
    assert result.assessment.signal_assembly_ready is False
    assert not hasattr(result, "signal")


def test_workflow_fails_closed_on_provider_exception() -> None:
    class BrokenProvider:
        def load(self) -> MarketDataSet:
            raise RuntimeError("provider unavailable")

    with pytest.raises(RuntimeError, match="provider unavailable"):
        run_adm_data_workflow(BrokenProvider())


def test_workflow_rejects_noncanonical_provider_result() -> None:
    class InvalidProvider:
        def load(self) -> object:
            return {"observations": []}

    with pytest.raises(ValueError, match="must return a MarketDataSet"):
        run_adm_data_workflow(InvalidProvider())


def test_workflow_rejects_missing_provider() -> None:
    with pytest.raises(ValueError, match="callable load"):
        run_adm_data_workflow(object())


def test_workflow_rejects_stale_required_endpoint_without_result() -> None:
    stale = MarketDataSet(
        (
            MarketDataPoint("VTI", "adjusted_close", "2025-09-30", 100.0, "fixture"),
            MarketDataPoint("VTI", "adjusted_close", "2026-08-31", 115.0, "fixture"),
            MarketDataPoint("VEU", "adjusted_close", "2025-09-30", 100.0, "fixture"),
            MarketDataPoint("VEU", "adjusted_close", "2026-09-30", 110.0, "fixture"),
            MarketDataPoint("SGOV", "adjusted_close", "2025-09-30", 100.0, "fixture"),
            MarketDataPoint("SGOV", "adjusted_close", "2026-09-30", 104.0, "fixture"),
        ),
        as_of="2026-10-10",
    )
    provider = FakeProvider(stale)

    with pytest.raises(ValueError, match="maximum age"):
        run_adm_data_workflow(provider)
    assert provider.calls == 1
