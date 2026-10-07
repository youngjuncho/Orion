"""Portfolio allocation value objects."""
from dataclasses import dataclass
from decimal import Decimal
from ..ids import AssetId

@dataclass(frozen=True)
class Allocation:
    asset_id: AssetId
    weight: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.asset_id, str) or not str(self.asset_id).strip():
            raise ValueError("asset_id must be a non-empty string")
        if isinstance(self.weight, bool):
            raise ValueError("allocation weight must be a Decimal or real number")
        if not isinstance(self.weight, Decimal):
            try:
                object.__setattr__(self, "weight", Decimal(str(self.weight)))
            except Exception as exc:
                raise ValueError("allocation weight must be a Decimal or real number") from exc
        if self.weight < Decimal("0") or self.weight > Decimal("1"):
            raise ValueError("allocation weight must be between 0 and 1")
