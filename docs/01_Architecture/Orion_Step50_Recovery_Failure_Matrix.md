# Orion Step 50 Recovery and Failure Matrix

**Status:** Engineering evidence and unresolved recovery requirements; not production approval  
**Date:** 2026-10-11  
**Scope:** SQLite HWM, acceptance journal, leased consumer delivery, and restart behavior

## 1. Purpose

This matrix separates recovery properties exercised by the isolated test suite from properties that require an operational policy or an external trust anchor. Passing a unit test does not authorize Runtime/Supernova wiring, Moon activation, or changes to Core Runtime lifecycle.

## 2. Evidence matrix

| Failure or recovery scenario | Current behavior / invariant | Test evidence | Disposition |
|---|---|---|---|
| Process/store recreation after accepted version | HWM and pending event remain in the file-backed SQLite database | `test_high_water_mark_is_durable_across_store_recreation`; `test_pending_acceptance_survives_recreation_and_can_be_replayed` | Covered for local file-backed restart |
| Journal insert fails during acceptance | Transaction rolls back HWM and event together | `test_event_insert_failure_rolls_back_high_water_mark` | Covered by failure injection |
| Stale concurrent acceptance | CAS conflict rejects stale expected version without inserting an event | `test_acceptance_cas_conflict_does_not_create_an_event`; concurrent initial acceptance test | Covered for SQLite transaction concurrency |
| Downstream callback fails before acknowledgement | Event remains pending for retry | `test_application_failure_leaves_event_pending_and_retry_succeeds`; leased drain failure test | Covered; downstream effect semantics remain consumer-owned |
| Side effect succeeds but acknowledgement fails | Same stable event ID is redelivered; consumer must deduplicate | `test_acknowledgement_failure_redelivers_same_idempotency_key` | Delivery recovery covered; exactly-once external effects are not guaranteed by this store |
| Worker lease expires or store is recreated | Expired lease can be reclaimed with a new token; stale token cannot acknowledge | Lease expiry/restart tests in `tests/data/test_registry_acceptance_consumer.py` | Covered for local SQLite and supplied timestamps |
| Lease claim/acknowledgement storage update fails | Transaction preserves all-or-nothing lease state | Claim and acknowledgement failure-injection tests | Covered by failure injection |
| SQLite file is unreadable/corrupt at initialization | Store initialization must raise a storage error instead of silently accepting an empty state | `test_corrupt_database_fails_closed_instead_of_reinitializing_state` | Fail-closed initialization covered; repair/recovery procedure still required |
| Operator restores an older but valid database backup | The database may expose an older HWM and cannot independently prove it was rolled back | No in-process test can establish protection without a trusted external monotonic anchor | **OPEN — BLOCKING** |
| Power-loss durability and storage hardware behavior | Depends on SQLite/filesystem settings, storage device, OS, and deployment environment | Not established by unit tests | **OPEN — requires deployment-specific validation** |
| Recovery from missing database, WAL/SHM mishandling, disk-full, or filesystem corruption in production | Current code reports initialization/read/write failures, but there is no approved recovery runbook or measured RPO/RTO | Unit-level injected errors do not establish an operational recovery plan | **OPEN — BLOCKING** |

## 3. Anti-rollback limitation: valid stale backup

The HWM and acceptance journal are stored in the same SQLite database. Atomic transactions protect against partial acceptance writes, and a stale compare-and-swap cannot overwrite newer state while the database's current state is intact. Neither property detects that an operator has replaced the entire database with an older, internally valid copy.

Detecting that event requires a separately protected monotonic reference or an independently controlled audit/replication system whose state cannot be rolled back together with the SQLite file. The design, authority, availability, and recovery behavior of such an anchor are not selected here. Do not add an unreviewed remote dependency or claim rollback detection until that decision is approved.

## 3A. Independent rollback-detection contract

`Orion_Step50_Independent_Rollback_Detection_Contract.md` now defines the requirements for any future independently protected monotonic anchor, including strict positive-integer versions, strict increase, fail-closed behavior, cross-store crash consistency, and required fault-injection cases. It deliberately does not choose a provider or claim that valid-stale-backup rollback detection is implemented. This scenario remains OPEN — BLOCKING.

## 4. Consumer retry semantics

The store provides at-least-once delivery semantics around a durable pending journal. It cannot atomically commit a side effect in an external system and update the SQLite acknowledgement in one transaction. Consumers must make the operation idempotent using the event ID or another approved stable business key. If a callback times out after applying its effect, treat the result as ambiguous and retry only under that idempotency contract.

Leases limit concurrent attempts; they do not prevent duplicate external effects after a worker pauses beyond expiry. A replacement worker may reclaim an expired lease while the original worker is still executing. Therefore, lease ownership alone is not a substitute for downstream idempotency or downstream fencing where required.

## 5. Required operational decisions before closure

1. Select and document an independently protected rollback-detection strategy, or explicitly accept the residual risk with a named owner and review date.
2. Define database backup consistency requirements, including SQLite WAL handling and a restore procedure that verifies HWM/journal consistency before serving writes.
3. Define recovery point/time objectives, disk-full behavior, corruption escalation, monitoring, and restore authorization.
4. Define consumer idempotency/fencing semantics for callbacks that may outlive a lease or whose completion is ambiguous.
5. Run deployment-specific crash/power-loss and restore drills before any production wiring.

**Decision:** isolated recovery and failure-injection coverage is useful but insufficient for production approval. All production approval gates remain unchanged and blocking.
