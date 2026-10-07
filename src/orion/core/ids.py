"""Typed identifiers for Orion's common domain."""
from typing import NewType

AssetId = NewType("AssetId", str)
PortfolioId = NewType("PortfolioId", str)
AccountId = NewType("AccountId", str)
PositionId = NewType("PositionId", str)
TargetId = NewType("TargetId", str)
OrderId = NewType("OrderId", str)
TransferId = NewType("TransferId", str)
FrameworkId = NewType("FrameworkId", str)
