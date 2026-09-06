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
        framework_results={"Moon": "result"},
        dashboard_data={"status": "ready"},
    )

    assert context.configuration is config
    assert context.market_data == market_data
    assert context.framework_results["Moon"] == "result"


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
