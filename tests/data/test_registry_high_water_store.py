from concurrent.futures import ThreadPoolExecutor

import pytest

from data.registry_high_water_store import (
    HighWaterMarkConflict,
    HighWaterMarkStorageError,
    SQLiteHighWaterMarkStore,
)


SCOPE = {"framework": "Supernova", "domain": "approved_company_state", "review_cycle": "2026-H2"}
AUTHORITY = "test-authority"
REGISTRY = "supernova.approved_company_state"


def store_at(tmp_path):
    return SQLiteHighWaterMarkStore(tmp_path / "registry-state.sqlite3")


def get(store, *, scope=SCOPE, authority=AUTHORITY, registry=REGISTRY):
    return store.get_version(authority_ref=authority, registry_type=registry, scope=scope)


def advance(store, expected, new, *, scope=SCOPE, authority=AUTHORITY, registry=REGISTRY):
    return store.advance(
        authority_ref=authority,
        registry_type=registry,
        scope=scope,
        expected_current_version=expected,
        new_version=new,
    )


def test_high_water_mark_is_durable_across_store_recreation(tmp_path):
    first = store_at(tmp_path)
    assert get(first) is None
    assert advance(first, None, 1) == 1
    assert get(store_at(tmp_path)) == 1
    assert advance(store_at(tmp_path), 1, 4) == 4
    assert get(store_at(tmp_path)) == 4


def test_scope_authority_and_registry_are_isolated(tmp_path):
    store = store_at(tmp_path)
    advance(store, None, 2)
    assert get(store, scope={**SCOPE, "review_cycle": "2027-H1"}) is None
    assert get(store, authority="other-authority") is None
    assert get(store, registry="other.registry") is None


def test_scope_key_is_canonical_not_mapping_insertion_order(tmp_path):
    store = store_at(tmp_path)
    reversed_scope = dict(reversed(list(SCOPE.items())))
    advance(store, None, 3)
    assert get(store, scope=reversed_scope) == 3


def test_stale_compare_and_swap_cannot_overwrite_newer_version(tmp_path):
    store = store_at(tmp_path)
    advance(store, None, 1)
    advance(store, 1, 2)
    with pytest.raises(HighWaterMarkConflict, match="changed"):
        advance(store, 1, 3)
    assert get(store) == 2


def test_equal_or_lower_version_is_rejected(tmp_path):
    store = store_at(tmp_path)
    advance(store, None, 5)
    with pytest.raises(ValueError, match="strictly greater"):
        advance(store, 5, 5)
    with pytest.raises(ValueError, match="strictly greater"):
        advance(store, 5, 4)
    assert advance(store, 5, 6) == 6


def test_concurrent_initial_acceptance_allows_only_one_writer(tmp_path):
    path = tmp_path / "registry-state.sqlite3"
    stores = [SQLiteHighWaterMarkStore(path) for _ in range(2)]

    def attempt(store, version):
        try:
            return ("accepted", advance(store, None, version))
        except HighWaterMarkConflict:
            return ("conflict", version)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda pair: attempt(*pair), [(stores[0], 1), (stores[1], 2)]))
    assert sum(result[0] == "accepted" for result in results) == 1
    assert get(stores[0]) in {1, 2}


def test_invalid_versions_and_memory_database_fail_closed(tmp_path):
    store = store_at(tmp_path)
    for invalid in (True, -1, 1.5, "2"):
        with pytest.raises(ValueError):
            advance(store, None, invalid)
    with pytest.raises(ValueError, match="file-backed"):
        SQLiteHighWaterMarkStore(":memory:")


def test_storage_failure_is_not_reported_as_success(tmp_path):
    directory = tmp_path / "not-a-database-file"
    directory.mkdir()
    with pytest.raises(HighWaterMarkStorageError):
        SQLiteHighWaterMarkStore(directory)


def accept(store, expected, version, *, snapshot_id=None, digest=None):
    return store.accept_snapshot(
        authority_ref=AUTHORITY,
        registry_type=REGISTRY,
        scope=SCOPE,
        expected_current_version=expected,
        snapshot_version=version,
        snapshot_id=snapshot_id or f"snapshot-{version}",
        content_digest=digest or ("a" * 64),
    )


def test_acceptance_record_and_high_water_mark_commit_atomically(tmp_path):
    store = store_at(tmp_path)
    event = accept(store, None, 1)
    assert get(store) == 1
    pending = store.list_pending_acceptances()
    assert pending == [event]
    assert pending[0].status == "pending"
    assert pending[0].snapshot_id == "snapshot-1"
    assert pending[0].content_digest == "a" * 64


def test_pending_acceptance_survives_recreation_and_can_be_replayed(tmp_path):
    store = store_at(tmp_path)
    event = accept(store, None, 1)
    recreated = store_at(tmp_path)
    assert recreated.list_pending_acceptances() == [event]
    # The HWM is already advanced, so replay is recovery of the durable event,
    # not re-acceptance of the same registry version.
    with pytest.raises(ValueError, match="strictly greater"):
        accept(recreated, 1, 1)
    recreated.mark_applied(event.event_id)
    assert recreated.list_pending_acceptances() == []
    recreated.mark_applied(event.event_id)  # idempotent acknowledgement


def test_acceptance_cas_conflict_does_not_create_an_event(tmp_path):
    store = store_at(tmp_path)
    accept(store, None, 1)
    with pytest.raises(HighWaterMarkConflict):
        accept(store, None, 2)
    assert get(store) == 1
    assert [event.snapshot_version for event in store.list_pending_acceptances()] == [1]


def test_acceptance_validation_rejects_bad_digest_and_identity(tmp_path):
    store = store_at(tmp_path)
    with pytest.raises(ValueError, match="SHA-256"):
        accept(store, None, 1, digest="not-a-digest")
    with pytest.raises(ValueError, match="snapshot_id"):
        accept(store, None, 1, snapshot_id=" ")
    assert get(store) is None
    assert store.list_pending_acceptances() == []


def test_event_insert_failure_rolls_back_high_water_mark(tmp_path):
    store = store_at(tmp_path)
    from contextlib import closing

    with closing(store._connect()) as connection:
        connection.execute(
            "CREATE TRIGGER fail_acceptance_insert BEFORE INSERT ON registry_acceptance_event "
            "BEGIN SELECT RAISE(ABORT, 'injected journal failure'); END"
        )
    with pytest.raises(HighWaterMarkStorageError):
        accept(store, None, 1)
    assert get(store) is None
    assert store.list_pending_acceptances() == []


def test_restoring_an_older_valid_database_can_roll_back_the_hwm(tmp_path):
    """Document the SQLite prototype's limit: local persistence is not an anti-rollback anchor."""
    import shutil

    path = tmp_path / "registry-state.sqlite3"
    store = SQLiteHighWaterMarkStore(path)
    advance(store, None, 1)
    backup = tmp_path / "older-valid-backup.sqlite3"
    shutil.copy2(path, backup)

    advance(store, 1, 2)
    assert get(store) == 2

    # Restoring a previously valid database restores its older HWM as well.
    # This is a documented security limitation, not an acceptable production trust design.
    shutil.copy2(backup, path)
    assert get(store_at(tmp_path)) == 1


def test_corrupt_database_fails_closed_instead_of_reinitializing_state(tmp_path):
    """A damaged state file must not be silently treated as a fresh registry."""
    path = tmp_path / "registry-state.sqlite3"
    path.write_bytes(b"not a valid sqlite database")

    with pytest.raises(HighWaterMarkStorageError):
        SQLiteHighWaterMarkStore(path)

    # The failed open must not replace the operator's evidence with a new DB.
    assert path.read_bytes() == b"not a valid sqlite database"
