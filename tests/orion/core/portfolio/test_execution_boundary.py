from datetime import datetime, timezone
from decimal import Decimal

from orion.core.portfolio.execution import ExecutionSizingInput, build_execution_orders
from orion.core.portfolio.operations import RebalanceAction, RebalanceChange, RebalancePlan


def test_execution_order_materialization_is_not_execution():
    plan = RebalancePlan(
        portfolio_id="portfolio-1",
        target_id="target-1",
        as_of="2026-10-08T00:00:00Z",
        changes=(
            RebalanceChange(asset_id="asset-1", action=RebalanceAction.BUY, target_weight=Decimal("0.60"), current_weight=Decimal("0.50"), delta_weight=Decimal("0.10")),
        ),
    )
    sizing = ExecutionSizingInput(
        quantities={"asset-1": Decimal("2")},
        order_ids={"asset-1": "order-1"},
    )

    orders = build_execution_orders(
        plan,
        sizing,
        created_at=datetime.now(timezone.utc),
    )

    assert len(orders) == 1
    assert orders[0].status == "planned"
    assert orders[0].quantity == Decimal("2")
