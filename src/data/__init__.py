"""Orion OS data layer."""

from .contracts import MarketDataPoint, MarketDataSet, MarketDataProvider
from .pipeline import normalize_dataset, normalize_observation, validate_dataset
from .adapters import ProviderNeutralMarketDataAdapter, RawMarketDataSource
from .alphavantage import (
    AlphaVantageMonthlyAdjustedProvider,
    AlphaVantageMonthlyAdjustedSource,
    AlphaVantageProviderError,
)

__all__ = [
    "MarketDataPoint",
    "MarketDataSet",
    "MarketDataProvider",
    "ProviderNeutralMarketDataAdapter",
    "AlphaVantageMonthlyAdjustedProvider",
    "AlphaVantageMonthlyAdjustedSource",
    "AlphaVantageProviderError",
    "RawMarketDataSource",
    "normalize_dataset",
    "normalize_observation",
    "validate_dataset",
]
from .governance import (
    DecisionRecordError,
    canonical_digest,
    canonical_snapshot_digest,
    invalidate_dependents,
    resolve_approved_decisions,
    resolve_registry_approved_decisions,
    validate_authoritative_registry_snapshot,
    validate_decision_record,
    validate_registry_lineage,
)

__all__ += [
    "DecisionRecordError",
    "canonical_digest",
    "canonical_snapshot_digest",
    "invalidate_dependents",
    "resolve_approved_decisions",
    "resolve_registry_approved_decisions",
    "validate_authoritative_registry_snapshot",
    "validate_decision_record",
    "validate_registry_lineage",
]
