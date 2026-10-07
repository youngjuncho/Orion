from pathlib import Path

import pytest

from data import MarketDataPoint, MarketDataSet
from orion.core import ExecutionMetadata, RuntimeContext, load_config


def test_runtime_context_preserves_shared_execution_inputs() -> None:
    config = load_config(Path(__file__).resolve().parents[3] / "config")
    execution = ExecutionMetadata("execution-001", "2026-08-01T09:00:00+09:00", "1.0")
    market_data = MarketDataSet(
        (MarketDataPoint("SPY", "close", "2026-07-31", 1.0, "test"),),
        "2026-07-31",
    )
    context = RuntimeContext(
        configuration=config,
        execution=execution,
        market_data=market_data,
        services={"Configuration": "service"},
        framework_results={"Moon": "result"},
        dashboard_data={"status": "ready"},
    )

    assert context.configuration is config
    assert context.market_data == market_data
    assert context.services["Configuration"] == "service"
    assert context.framework_results["Moon"] == "result"


def test_runtime_context_uses_read_only_mapping_snapshots() -> None:
    config = load_config(Path(__file__).resolve().parents[3] / "config")
    execution = ExecutionMetadata("execution-001", "2026-08-01", "1.0")
    framework_results = {"Moon": "initial"}
    dashboard_data = {"status": "ready"}

    context = RuntimeContext(
        config,
        execution,
        framework_results=framework_results,
        dashboard_data=dashboard_data,
    )
    framework_results["Moon"] = "changed"
    dashboard_data["status"] = "changed"

    assert context.framework_results["Moon"] == "initial"
    assert context.dashboard_data["status"] == "ready"
    with pytest.raises(TypeError):
        context.framework_results["Aurora"] = "result"


def test_runtime_context_rejects_duplicate_frameworks() -> None:
    config = load_config(Path(__file__).resolve().parents[3] / "config")
    execution = ExecutionMetadata("execution-001", "2026-08-01", "1.0")

    with pytest.raises(ValueError, match="unique"):
        RuntimeContext(config, execution, registered_frameworks=("Moon", "Moon"))


def test_runtime_context_rejects_empty_framework_registry() -> None:
    config = load_config(Path(__file__).resolve().parents[3] / "config")
    execution = ExecutionMetadata("execution-001", "2026-08-01", "1.0")

    with pytest.raises(ValueError, match="at least one"):
        RuntimeContext(config, execution, registered_frameworks=())


def test_default_frameworks_include_all_five_canonical_frameworks() -> None:
    from orion.core import DEFAULT_FRAMEWORKS
    assert DEFAULT_FRAMEWORKS == ("Aurora", "Moon", "Orbit", "Supernova", "Phoenix")
