"""Retryable consumer loop for the durable registry acceptance journal.

The journal is at-least-once delivery. The supplied apply callback MUST make
its downstream effect idempotent using event.event_id (or an equivalent unique
key committed atomically with the downstream state change).
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import math
from typing import NoReturn

from data.registry_high_water_store import RegistryAcceptanceEvent, SQLiteHighWaterMarkStore


@dataclass(frozen=True)
class AcceptanceDrainResult:
    """Summary of one successful drain pass."""

    applied_count: int
    remaining_count: int


class AcceptanceDrainError(RuntimeError):
    """A pending event could not be applied or acknowledged."""

    def __init__(self, event_id: str, phase: str, completed_count: int) -> None:
        self.event_id = event_id
        self.phase = phase
        self.completed_count = completed_count
        super().__init__(
            f"acceptance event {event_id!r} failed during {phase}; "
            f"{completed_count} earlier event(s) completed in this pass"
        )


def _raise_drain_error(event: RegistryAcceptanceEvent, phase: str, completed: int, cause: Exception) -> NoReturn:
    error = AcceptanceDrainError(event.event_id, phase, completed)
    raise error from cause


def drain_pending_acceptances(
    store: SQLiteHighWaterMarkStore,
    apply_event: Callable[[RegistryAcceptanceEvent], None],
    *,
    limit: int = 100,
) -> AcceptanceDrainResult:
    """Apply pending events in per-scope version order, acknowledging each.

    Processing stops at the first failure to avoid applying a later version
    after an earlier pending event in the ordered batch failed. The event stays
    pending if application or acknowledgement fails. Because acknowledgement
    follows the downstream side effect, a crash between them causes redelivery;
    therefore ``apply_event`` must be idempotent.
    """
    if not callable(apply_event):
        raise TypeError("apply_event must be callable")
    events = store.list_pending_acceptances(limit=limit)
    completed = 0
    for event in events:
        try:
            apply_event(event)
        except Exception as exc:
            _raise_drain_error(event, "downstream application", completed, exc)
        try:
            store.mark_applied(event.event_id)
        except Exception as exc:
            _raise_drain_error(event, "journal acknowledgement", completed, exc)
        completed += 1
    remaining = store.count_pending_acceptances()
    return AcceptanceDrainResult(applied_count=completed, remaining_count=remaining)


def drain_leased_acceptances(
    store: SQLiteHighWaterMarkStore,
    worker_id: str,
    apply_event: Callable[[RegistryAcceptanceEvent], None],
    *,
    limit: int = 100,
    lease_seconds: float = 30.0,
) -> AcceptanceDrainResult:
    """Drain events through an atomic claim/lease protocol.

    Claims one event at a time so a slow callback does not consume the lease
    lifetime of later events in a batch. A failed callback leaves its lease to
    expire naturally; the next worker can then reclaim it. Downstream effects
    still MUST be idempotent because a callback can commit and then lose its
    process before acknowledgement.
    """
    if not callable(apply_event):
        raise TypeError("apply_event must be callable")
    if not isinstance(worker_id, str) or not worker_id.strip():
        raise ValueError("worker_id must be a non-empty string")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 10000:
        raise ValueError("limit must be an integer between 1 and 10000")
    if (
        not isinstance(lease_seconds, (int, float))
        or isinstance(lease_seconds, bool)
        or not math.isfinite(lease_seconds)
        or lease_seconds <= 0
    ):
        raise ValueError("lease_seconds must be a finite positive number")
    completed = 0
    while completed < limit:
        leases = store.claim_pending_acceptances(
            worker_id=worker_id, limit=1, lease_seconds=lease_seconds,
        )
        if not leases:
            break
        lease = leases[0]
        try:
            apply_event(lease.event)
        except Exception as exc:
            _raise_drain_error(lease.event, "downstream application", completed, exc)
        try:
            store.acknowledge_claim(lease)
        except Exception as exc:
            _raise_drain_error(lease.event, "lease acknowledgement", completed, exc)
        completed += 1
    remaining = store.count_pending_acceptances()
    return AcceptanceDrainResult(applied_count=completed, remaining_count=remaining)
