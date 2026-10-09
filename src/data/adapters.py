"""Provider-neutral adapter boundary for raw market-data batches.

No network client or provider-specific field semantics live in this module.
A concrete source must return the documented raw batch shape, and all records
are normalized through the canonical data pipeline before they are exposed.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from .contracts import MarketDataSet
from .pipeline import normalize_dataset


class RawMarketDataSource(Protocol):
    """A source that fetches one raw batch using its own approved mechanism."""

    def fetch(self) -> Mapping[str, Any]:
        """Return a batch with ``as_of`` and ``observations`` keys."""
        ...


class ProviderNeutralMarketDataAdapter:
    """Normalize one source batch into the canonical ``MarketDataSet``.

    Expected raw shape::

        {
            "as_of": "YYYY-MM-DD or source-defined non-empty label",
            "observations": [
                {
                    "symbol": "VTI",
                    "field": "adjusted_close",
                    "observed_at": "YYYY-MM-DD",
                    "value": 123.45,
                    "source": "fixture-provider",
                    "currency": "USD",  # optional
                    "metadata": {"provider_field": "adjclose"},  # optional
                }
            ],
        }

    The adapter intentionally does not infer aliases, price-field semantics,
    dates, currencies, freshness, or missing-value substitutions. Source errors
    propagate to the caller; malformed or duplicate batches fail closed.
    """

    def __init__(self, source: RawMarketDataSource) -> None:
        if not callable(getattr(source, "fetch", None)):
            raise ValueError("source must provide a callable fetch() method")
        self._source = source

    def load(self) -> MarketDataSet:
        """Fetch and normalize one complete batch, or raise on any failure."""

        raw_batch = self._source.fetch()
        if not isinstance(raw_batch, Mapping):
            raise ValueError("provider batch must be a mapping")
        if "as_of" not in raw_batch:
            raise ValueError("provider batch must include as_of")
        if "observations" not in raw_batch:
            raise ValueError("provider batch must include observations")

        observations = raw_batch["observations"]
        if isinstance(observations, (str, bytes, Mapping)):
            raise ValueError("provider observations must be an iterable of mappings")
        try:
            return normalize_dataset(observations, as_of=raw_batch["as_of"])
        except TypeError as exc:
            raise ValueError("provider observations must be an iterable of mappings") from exc
