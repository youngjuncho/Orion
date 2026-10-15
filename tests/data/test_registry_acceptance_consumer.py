import time

import pytest

from data.registry_acceptance_consumer import (
    AcceptanceDrainError,
    drain_pending_acceptances,
    drain_leased_acceptances,
)
from data.registry_high_water_store import SQLiteHighWaterMarkStore


SCOPE = {"framework": "Supernova", "domain": "approved_company_state", "review_cycle": "2026-H2"}
AUTHORITY = "test-authority"
REGISTRY = "supernova.approved_company_state"
DIGEST = "a" * 64


def new_store(tmp_path):
    return SQLiteHighWaterMarkStore(tmp_path / "registry-state.sqlite3")


def accept(store, expected, version, *, scope=SCOPE):
    return store.accept_snapshot(
        authority_ref=AUTHORITY,
        registry_type=REGISTRY,
        scope=scope,
        expected_current_version=expected,
        snapshot_version=version,
        snapshot_id=f"snapshot-{version}",
        content_digest=DIGEST,
    )


def test_drain_applies_and_acknowledges_pending_events(tmp_path):
    store = new_store(tmp_path)
    first = accept(store, None, 1)
    second = accept(store, 1, 2)
    applied = []

    result = drain_pending_acceptances(store, lambda event: applied.append(event.event_id))

    assert applied == [first.event_id, second.event_id]
    assert result.applied_count == 2
    assert result.remaining_count == 0
    assert store.list_pending_acceptances() == []


def test_application_failure_leaves_event_pending_and_retry_succeeds(tmp_path):
    store = new_store(tmp_path)
    event = accept(store, None, 1)
    calls = 0

    def flaky_apply(received):
        nonlocal calls
        calls += 1
        assert received.event_id == event.event_id
        if calls == 1:
            raise OSError("temporary downstream outage")

    with pytest.raises(AcceptanceDrainError, match="downstream application") as caught:
        drain_pending_acceptances(store, flaky_apply)
    assert caught.value.event_id == event.event_id
    assert caught.value.completed_count == 0
    assert [item.event_id for item in store.list_pending_acceptances()] == [event.event_id]

    result = drain_pending_acceptances(store, flaky_apply)
    assert calls == 2
    assert result.applied_count == 1
    assert result.remaining_count == 0


def test_acknowledgement_failure_redelivers_same_idempotency_key(tmp_path, monkeypatch):
    store = new_store(tmp_path)
    event = accept(store, None, 1)
    downstream_effects = set()
    calls = []

    def idempotent_apply(received):
        calls.append(received.event_id)
        downstream_effects.add(received.event_id)  # unique-key upsert semantics

    original_mark_applied = store.mark_applied
    fail_once = True

    def flaky_mark_applied(event_id):
        nonlocal fail_once
        if fail_once:
            fail_once = False
            raise OSError("temporary journal acknowledgement failure")
        original_mark_applied(event_id)

    monkeypatch.setattr(store, "mark_applied", flaky_mark_applied)
    with pytest.raises(AcceptanceDrainError, match="journal acknowledgement"):
        drain_pending_acceptances(store, idempotent_apply)
    assert [item.event_id for item in store.list_pending_acceptances()] == [event.event_id]
    assert downstream_effects == {event.event_id}

    result = drain_pending_acceptances(store, idempotent_apply)
    assert result.applied_count == 1
    assert result.remaining_count == 0
    assert calls == [event.event_id, event.event_id]
    assert downstream_effects == {event.event_id}  # no duplicate durable effect


def test_drain_stops_at_first_failed_event(tmp_path):
    store = new_store(tmp_path)
    first = accept(store, None, 1)
    second = accept(store, 1, 2)
    attempted = []

    def fail_first(event):
        attempted.append(event.event_id)
        if event.event_id == first.event_id:
            raise RuntimeError("blocked")

    with pytest.raises(AcceptanceDrainError):
        drain_pending_acceptances(store, fail_first)

    assert attempted == [first.event_id]
    assert [event.snapshot_version for event in store.list_pending_acceptances()] == [1, 2]
    assert second.event_id != first.event_id


def test_pending_events_are_ordered_by_version_within_scope(tmp_path):
    store = new_store(tmp_path)
    first = accept(store, None, 1)
    second = accept(store, 1, 2)
    third = accept(store, 2, 3)
    assert [event.event_id for event in store.list_pending_acceptances()] == [
        first.event_id, second.event_id, third.event_id
    ]


def test_non_callable_consumer_is_rejected(tmp_path):
    store = new_store(tmp_path)
    with pytest.raises(TypeError, match="callable"):
        drain_pending_acceptances(store, None)  # type: ignore[arg-type]


# Lease protocol tests: the lease controls concurrent work, while the callback
# still owns the downstream idempotency guarantee.
def test_two_workers_cannot_claim_the_same_live_lease(tmp_path):
    store = new_store(tmp_path)
    event = accept(store, None, 1)
    first = store.claim_pending_acceptances(worker_id="worker-a", now=100.0, lease_seconds=10)
    second = store.claim_pending_acceptances(worker_id="worker-b", now=100.0, lease_seconds=10)
    assert len(first) == 1 and first[0].event.event_id == event.event_id
    assert second == []


def test_expired_lease_can_be_reclaimed_with_new_token(tmp_path):
    store = new_store(tmp_path)
    event = accept(store, None, 1)
    first = store.claim_pending_acceptances(worker_id="worker-a", now=100.0, lease_seconds=10)[0]
    second = store.claim_pending_acceptances(worker_id="worker-b", now=110.0, lease_seconds=10)[0]
    assert second.event.event_id == event.event_id
    assert second.lease_token != first.lease_token
    with pytest.raises(Exception, match="lease is stale"):
        store.acknowledge_claim(first, now=111.0)
    store.acknowledge_claim(second, now=111.0)
    assert store.list_pending_acceptances() == []


def test_expired_worker_cannot_acknowledge_even_before_reclaim(tmp_path):
    store = new_store(tmp_path)
    accept(store, None, 1)
    lease = store.claim_pending_acceptances(worker_id="worker-a", now=10.0, lease_seconds=5)[0]
    with pytest.raises(Exception, match="lease is stale"):
        store.acknowledge_claim(lease, now=15.0)
    assert len(store.list_pending_acceptances()) == 1


def test_later_version_is_blocked_until_earlier_event_is_applied(tmp_path):
    store = new_store(tmp_path)
    first = accept(store, None, 1)
    second = accept(store, 1, 2)
    claim = store.claim_pending_acceptances(worker_id="worker-a", now=100.0, lease_seconds=10)
    assert [item.event.event_id for item in claim] == [first.event_id]
    assert store.claim_pending_acceptances(worker_id="worker-b", now=100.0, lease_seconds=10) == []
    store.acknowledge_claim(claim[0], now=101.0)
    next_claim = store.claim_pending_acceptances(worker_id="worker-b", now=102.0, lease_seconds=10)
    assert [item.event.event_id for item in next_claim] == [second.event_id]




@pytest.mark.parametrize("lease_seconds", [0, -1, float("nan"), float("inf"), True, "30"])
def test_leased_drain_validates_lease_duration_even_when_queue_is_empty(tmp_path, lease_seconds):
    store = new_store(tmp_path)

    with pytest.raises(ValueError, match="lease_seconds must be a finite positive number"):
        drain_leased_acceptances(
            store, "worker-a", lambda _event: None, lease_seconds=lease_seconds,
        )

    assert store.list_pending_acceptances() == []


def test_leased_drain_applies_events_and_acknowledges_them(tmp_path):
    store = new_store(tmp_path)
    first = accept(store, None, 1)
    second = accept(store, 1, 2)
    calls = []
    result = drain_leased_acceptances(store, "worker-a", lambda event: calls.append(event.event_id))
    assert calls == [first.event_id, second.event_id]
    assert result.applied_count == 2
    assert result.remaining_count == 0


def test_leased_drain_leaves_failed_event_for_expiry_and_recovery(tmp_path):
    store = new_store(tmp_path)
    event = accept(store, None, 1)
    with pytest.raises(AcceptanceDrainError, match="downstream application"):
        drain_leased_acceptances(store, "worker-a", lambda _event: (_ for _ in ()).throw(OSError("offline")))
    assert [pending.event_id for pending in store.list_pending_acceptances()] == [event.event_id]
    # Use deterministic timestamps directly to model the lease expiration/reclaim.
    future = time.time() + 100.0
    first = store.claim_pending_acceptances(worker_id="worker-a", now=future, lease_seconds=10)[0]
    replacement = store.claim_pending_acceptances(worker_id="worker-b", now=future + 10.0, lease_seconds=10)[0]
    store.acknowledge_claim(replacement, now=future + 11.0)
    assert first.event.event_id == event.event_id
    assert store.list_pending_acceptances() == []


def test_invalid_lease_inputs_are_rejected(tmp_path):
    store = new_store(tmp_path)
    for kwargs in (
        {"worker_id": " ", "now": 1.0},
        {"worker_id": "worker", "limit": True, "now": 1.0},
        {"worker_id": "worker", "lease_seconds": 0, "now": 1.0},
        {"worker_id": "worker", "now": float("nan")},
    ):
        with pytest.raises(ValueError):
            store.claim_pending_acceptances(**kwargs)


def test_simultaneous_workers_only_one_obtains_the_live_lease(tmp_path):
    from concurrent.futures import ThreadPoolExecutor

    store = new_store(tmp_path)
    event = accept(store, None, 1)

    def claim(worker):
        return store.claim_pending_acceptances(
            worker_id=worker, now=500.0, lease_seconds=30,
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(claim, ("worker-a", "worker-b")))
    winners = [lease for result in results for lease in result]
    assert len(winners) == 1
    assert winners[0].event.event_id == event.event_id


def test_legacy_acknowledgement_cannot_bypass_a_live_lease(tmp_path):
    from data.registry_high_water_store import HighWaterMarkConflict

    store = new_store(tmp_path)
    event = accept(store, None, 1)
    lease = store.claim_pending_acceptances(worker_id="worker-a", now=500.0, lease_seconds=30)[0]
    with pytest.raises(HighWaterMarkConflict, match="leased"):
        store.mark_applied(event.event_id)
    store.acknowledge_claim(lease, now=501.0)
    assert store.list_pending_acceptances() == []


# Failure-injection and state-transition invariants.
def test_claim_transaction_rolls_back_all_leases_when_one_update_fails(tmp_path):
    from contextlib import closing
    from data.registry_high_water_store import HighWaterMarkStorageError

    store = new_store(tmp_path)
    first = accept(store, None, 1, scope={**SCOPE, "partition": "a"})
    second = accept(store, None, 1, scope={**SCOPE, "partition": "b"})
    with closing(store._connect()) as connection:
        connection.execute(
            "CREATE TRIGGER fail_one_claim BEFORE UPDATE OF lease_owner ON registry_acceptance_event "
            f"WHEN OLD.event_id = '{second.event_id}' "
            "BEGIN SELECT RAISE(ABORT, 'injected claim failure'); END"
        )
    with pytest.raises(HighWaterMarkStorageError, match="claim"):
        store.claim_pending_acceptances(worker_id="worker-fault", limit=2, now=100.0, lease_seconds=10)
    # The transaction is all-or-nothing, regardless of which event sorted first.
    with closing(store._connect()) as connection:
        rows = connection.execute(
            "SELECT event_id, lease_owner, lease_token, lease_expires_at "
            "FROM registry_acceptance_event WHERE status = 'pending'"
        ).fetchall()
    assert {row[0] for row in rows} == {first.event_id, second.event_id}
    assert all(row[1:] == (None, None, None) for row in rows)
    # The queue remains usable after the injected fault is removed.
    with closing(store._connect()) as connection:
        connection.execute("DROP TRIGGER fail_one_claim")
    leases = store.claim_pending_acceptances(worker_id="worker-retry", limit=2, now=100.0, lease_seconds=10)
    assert {lease.event.event_id for lease in leases} == {first.event_id, second.event_id}


def test_acknowledgement_storage_failure_preserves_live_lease_for_retry(tmp_path):
    from contextlib import closing
    from data.registry_high_water_store import HighWaterMarkStorageError

    store = new_store(tmp_path)
    event = accept(store, None, 1)
    lease = store.claim_pending_acceptances(worker_id="worker-a", now=100.0, lease_seconds=10)[0]
    with closing(store._connect()) as connection:
        connection.execute(
            "CREATE TRIGGER fail_ack BEFORE UPDATE OF status ON registry_acceptance_event "
            "WHEN NEW.status = 'applied' "
            "BEGIN SELECT RAISE(ABORT, 'injected ack failure'); END"
        )
    with pytest.raises(HighWaterMarkStorageError, match="acknowledge"):
        store.acknowledge_claim(lease, now=101.0)
    with closing(store._connect()) as connection:
        row = connection.execute(
            "SELECT status, lease_owner, lease_token, lease_expires_at "
            "FROM registry_acceptance_event WHERE event_id = ?", (event.event_id,)
        ).fetchone()
    assert row[0] == "pending"
    assert row[1] == lease.worker_id
    assert row[2] == lease.lease_token
    assert row[3] == lease.lease_expires_at
    with closing(store._connect()) as connection:
        connection.execute("DROP TRIGGER fail_ack")
    store.acknowledge_claim(lease, now=102.0)
    assert store.list_pending_acceptances() == []


def test_lease_survives_store_recreation_and_expired_lease_is_reclaimable(tmp_path):
    store = new_store(tmp_path)
    event = accept(store, None, 1)
    original = store.claim_pending_acceptances(
        worker_id="worker-old", now=100.0, lease_seconds=10
    )[0]
    restarted = new_store(tmp_path)
    assert restarted.claim_pending_acceptances(
        worker_id="worker-new", now=109.0, lease_seconds=10
    ) == []
    replacement = restarted.claim_pending_acceptances(
        worker_id="worker-new", now=110.0, lease_seconds=10
    )[0]
    assert replacement.event.event_id == event.event_id
    assert replacement.lease_token != original.lease_token
    from data.registry_high_water_store import HighWaterMarkConflict
    with pytest.raises(HighWaterMarkConflict):
        restarted.acknowledge_claim(original, now=111.0)
    restarted.acknowledge_claim(replacement, now=111.0)
    assert restarted.list_pending_acceptances() == []


def test_applied_state_clears_all_lease_fields_and_pending_state_is_consistent(tmp_path):
    from contextlib import closing

    store = new_store(tmp_path)
    event = accept(store, None, 1)
    lease = store.claim_pending_acceptances(worker_id="worker-a", now=100.0, lease_seconds=10)[0]
    with closing(store._connect()) as connection:
        before = connection.execute(
            "SELECT status, lease_owner, lease_token, lease_expires_at "
            "FROM registry_acceptance_event WHERE event_id = ?", (event.event_id,)
        ).fetchone()
    assert before == ("pending", "worker-a", lease.lease_token, 110.0)
    store.acknowledge_claim(lease, now=101.0)
    with closing(store._connect()) as connection:
        after = connection.execute(
            "SELECT status, lease_owner, lease_token, lease_expires_at, applied_at "
            "FROM registry_acceptance_event WHERE event_id = ?", (event.event_id,)
        ).fetchone()
    assert after[0] == "applied"
    assert after[1:4] == (None, None, None)
    assert after[4]
