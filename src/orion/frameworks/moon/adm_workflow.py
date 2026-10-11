"""Isolated, in-memory Moon ADM data workflow experiment.

This module deliberately stops at a typed data assessment. It does not build
an ADMSignalInput, activate a strategy, access Runtime defaults, or persist data.
A provider is always supplied explicitly by the caller.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from data.contracts import MarketDataSet
from orion.frameworks.moon.adm_data import ADMMonthlyDataAssessment, assess_adm_monthly_dataset


class ADMWorkflowProvider(Protocol):
    """Explicitly injected source of one canonical market-data batch."""

    def load(self) -> MarketDataSet:
        """Load one complete batch or raise; partial batches are not accepted."""
        ...


@dataclass(frozen=True)
class ADMDataWorkflowResult:
    """In-memory workflow output, limited to source data and assessment."""

    dataset: MarketDataSet
    assessment: ADMMonthlyDataAssessment

    def __post_init__(self) -> None:
        if not isinstance(self.dataset, MarketDataSet):
            raise ValueError("dataset must be a MarketDataSet")
        if not isinstance(self.assessment, ADMMonthlyDataAssessment):
            raise ValueError("assessment must be an ADMMonthlyDataAssessment")
        if not self.assessment.readiness.data_quality_passed:
            raise ValueError("workflow result requires a passing data-quality assessment")


def run_adm_data_workflow(provider: ADMWorkflowProvider) -> ADMDataWorkflowResult:
    """Load once, validate the canonical batch, and return its ADM assessment.

    The function does not create a default provider, retry, cache, persist,
    construct a signal, or call Runtime. Provider and assessment errors
    propagate so callers cannot mistake a failed run for a successful result.
    """

    load = getattr(provider, "load", None)
    if not callable(load):
        raise ValueError("provider must expose a callable load() method")

    dataset = load()
    if not isinstance(dataset, MarketDataSet):
        raise ValueError("provider.load() must return a MarketDataSet")

    assessment = assess_adm_monthly_dataset(dataset)
    return ADMDataWorkflowResult(dataset=dataset, assessment=assessment)
