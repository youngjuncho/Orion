"""Actual asset positions held inside an Account."""
from dataclasses import dataclass
from ..ids import AccountId, AssetId, PositionId

@dataclass(frozen=True)
class Position:
    position_id: PositionId
    account_id: AccountId
    asset_id: AssetId
    quantity: float

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("position quantity must be non-negative")
