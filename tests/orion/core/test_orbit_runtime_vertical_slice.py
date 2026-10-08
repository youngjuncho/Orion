from datetime import date
from decimal import Decimal

from orion.core import FrameworkRegistry, ExecutionMetadata, OrionRuntime, make_orbit_portfolio_adapter
from orion.core.config_loader import load_config
from orion.core.ids import PortfolioId, TargetId


def _runtime() -> OrionRuntime:
    registry = FrameworkRegistry()
    registry.register("Orbit", object())
    return OrionRuntime(
        configuration=load_config(),
        execution=ExecutionMetadata(
            execution_id="orbit-vertical-001",
            start_time="2026-10-08T00:00:00+00:00",
            orion_version="v1",
        ),
        registry=registry,
    )


def test_orbit_adapter_exposes_canonical_portfolio_target_candidate() -> None:
    result = _runtime().run(
        {
            "Orbit": make_orbit_portfolio_adapter(
                PortfolioId("orbit-main"),
                target_id=TargetId("orbit-target-001"),
                effective_from=date(2026, 11, 2),
            )
        }
    )

    framework_result = result.framework_results[0]
    candidate = framework_result.decision_candidates[0]
    target = candidate.payload["portfolio_target"]

    assert candidate.framework_name == "Orbit"
    assert candidate.entity_type == "PortfolioTarget"
    assert candidate.entity_id == "orbit-target-001"
    assert target.portfolio_id == PortfolioId("orbit-main")
    assert target.target_id == TargetId("orbit-target-001")
    assert sum((allocation.weight for allocation in target.allocations), Decimal("0")) == Decimal("1")
    assert {str(allocation.asset_id) for allocation in target.allocations} == {
        "SPYM", "QQQM", "VGIT", "VGLT", "GLDM", "SIVR", "SGOV"
    }
