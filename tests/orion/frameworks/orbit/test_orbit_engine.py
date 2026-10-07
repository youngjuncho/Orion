from datetime import date
from decimal import Decimal

from orion.core.ids import PortfolioId, TargetId
from orion.frameworks.orbit import OrbitEngine


def test_orbit_builds_static_common_portfolio_target() -> None:
    target = OrbitEngine().build_portfolio_target(
        PortfolioId("ORBIT"), target_id=TargetId("ORBIT-1"), effective_from=date(2026, 11, 2)
    )
    assert target.portfolio_id == PortfolioId("ORBIT")
    assert [(str(a.asset_id), a.weight) for a in target.allocations] == [
        ("SPYM", Decimal("0.30")), ("QQQM", Decimal("0.15")), ("VGIT", Decimal("0.20")),
        ("VGLT", Decimal("0.10")), ("GLDM", Decimal("0.10")), ("SIVR", Decimal("0.05")), ("SGOV", Decimal("0.10")),
    ]
