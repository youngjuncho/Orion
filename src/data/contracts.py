"""Framework-independent contracts for normalized external observations."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class MarketDataPoint:
    """One normalized observation supplied to a framework.

    The contract carries observations only. It does not assign signals,
    scores, rankings, or portfolio decisions.
    """

    symbol: str
    field: str
    observed_at: str
    value: float | int | str | None
    source: str
    currency: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, value in (
            ("symbol", self.symbol),
            ("field", self.field),
            ("observed_at", self.observed_at),
            ("source", self.source),
        ):
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        if self.currency is not None and not self.currency.strip():
            raise ValueError("currency must not be empty when provided")

        if isinstance(self.value, float) and not isfinite(self.value):
            raise ValueError("value must be finite when it is a float")

        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    @property
    def identity(self) -> tuple[str, str, str]:
        """Return the key used to detect duplicate observations."""

        return (self.symbol, self.field, self.observed_at)


@dataclass(frozen=True)
class MarketDataSet:
    """Validated collection of normalized observations for one input batch."""

    observations: tuple[MarketDataPoint, ...]
    as_of: str

    def __post_init__(self) -> None:
        if not self.as_of.strip():
            raise ValueError("as_of must not be empty")

        identities = [observation.identity for observation in self.observations]
        if len(identities) != len(set(identities)):
            raise ValueError("observations must not contain duplicate identities")

