"""Canonical investable-asset reference data."""
from dataclasses import dataclass
from enum import Enum
from ..ids import AssetId

class AssetType(str, Enum):
    EQUITY = "equity"
    ETF = "etf"
    BOND = "bond"
    COMMODITY = "commodity"
    CASH = "cash"
    CRYPTO = "crypto"
    OTHER = "other"

@dataclass(frozen=True)
class Asset:
    asset_id: AssetId
    symbol: str
    name: str
    asset_type: AssetType
    currency: str

    def __post_init__(self) -> None:
        for field in ("symbol", "name", "currency"):
            if not isinstance(getattr(self, field), str) or not getattr(self, field).strip():
                raise ValueError(f"{field} must be a non-empty string")
