"""Framework-independent contracts for normalized external observations."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from typing import Mapping, Protocol


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
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        if self.currency is not None and (
            not isinstance(self.currency, str) or not self.currency.strip()
        ):
            raise ValueError("currency must be a non-empty string when provided")

        if self.value is not None:
            if isinstance(self.value, bool) or not isinstance(
                self.value, (float, int, str)
            ):
                raise ValueError("value must be a number, string, or None")
            if isinstance(self.value, float) and not isfinite(self.value):
                raise ValueError("value must be finite when it is a float")

        if not isinstance(self.metadata, Mapping):
            raise ValueError("metadata must be a mapping")
        metadata = dict(self.metadata)
        if any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in metadata.items()
        ):
            raise ValueError("metadata keys and values must be strings")
        object.__setattr__(self, "metadata", MappingProxyType(metadata))

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
        if not isinstance(self.as_of, str) or not self.as_of.strip():
            raise ValueError("as_of must be a non-empty string")

        observations = tuple(self.observations)
        if any(not isinstance(item, MarketDataPoint) for item in observations):
            raise ValueError("observations must contain MarketDataPoint values")
        identities = [observation.identity for observation in observations]
        if len(identities) != len(set(identities)):
            raise ValueError("observations must not contain duplicate identities")
        object.__setattr__(self, "observations", observations)


class MarketDataProvider(Protocol):
    """Runtime-facing provider that returns one canonical market-data batch."""

    def load(self) -> MarketDataSet:
        """Return validated canonical market data for the current execution."""
        ...
