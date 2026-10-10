"""Actual asset positions held inside an Account."""
from dataclasses import dataclass
from math import isfinite
from ..ids import AccountId, AssetId, PositionId

@dataclass(frozen=True)
class Position:
    position_id: PositionId
    account_id: AccountId
    asset_id: AssetId
    quantity: float

    def __post_init__(self) -> None:
        if isinstance(self.quantity, bool) or not isinstance(self.quantity, (int, float)):
            raise ValueError("position quantity must be a finite number")
        if not isfinite(self.quantity):
            raise ValueError("position quantity must be a finite number")
        if self.quantity < 0:
            raise ValueError("position quantity must be non-negative")
