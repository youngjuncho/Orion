"""Deterministic normalization and structural validation for Orion market data."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .contracts import MarketDataPoint, MarketDataSet


def normalize_observation(raw: Mapping[str, Any]) -> MarketDataPoint:
    """Normalize one source observation into the canonical data contract.

    This function deliberately performs only source-agnostic normalization:
    required textual fields are trimmed and optional text is normalized to
    ``None`` when absent. It does not infer financial meaning, freshness, or
    framework-specific fields.
    """

    if not isinstance(raw, Mapping):
        raise ValueError("observation must be a mapping")

    def text(name: str, *, required: bool = True) -> str | None:
        value = raw.get(name)
        if value is None and not required:
            return None
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")
        return value.strip()

    return MarketDataPoint(
        symbol=text("symbol"),
        field=text("field"),
        observed_at=text("observed_at"),
        value=raw.get("value"),
        source=text("source"),
        currency=text("currency", required=False),
        metadata=dict(raw.get("metadata") or {}),
    )


def normalize_dataset(
    observations: Iterable[Mapping[str, Any]],
    *,
    as_of: str,
) -> MarketDataSet:
    """Normalize and structurally validate one source batch.

    Duplicate identities and invalid observation values are rejected by the
    canonical ``MarketDataSet`` contract. Freshness and source-specific
    semantic validation remain outside this MVP because their policies are
    not yet closed.
    """

    if not isinstance(as_of, str) or not as_of.strip():
        raise ValueError("as_of must be a non-empty string")

    normalized = tuple(normalize_observation(item) for item in observations)
    return MarketDataSet(normalized, as_of.strip())


def validate_dataset(dataset: MarketDataSet) -> MarketDataSet:
    """Validate an already canonical dataset without mutating it."""

    if not isinstance(dataset, MarketDataSet):
        raise ValueError("dataset must be a MarketDataSet")
    return dataset
