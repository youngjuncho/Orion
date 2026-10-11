# Orion Authoritative Registry Snapshot Contract

**Status:** Local integrity, trusted-authority allowlist, signature-verifier boundary, strict numeric version, file-backed SQLite high-water storage, and a recoverable acceptance journal implemented. External identity/key infrastructure, production consumer integration, remote latestness, and revocation remain unimplemented.

## Purpose

A structurally valid decision record is not sufficient to establish that its registry is the intended snapshot, current for the requested use, or issued by a trusted authority. This contract defines metadata and checks for a caller-supplied snapshot. It does not fetch, sign, authenticate, or discover a remote registry.

## Required snapshot fields

- `snapshot_id`: stable non-empty identifier for this snapshot.
- `snapshot_version`: positive integer; strings, booleans, zero, and negative values are invalid.
- `generated_at`: ISO-8601 timestamp with an explicit UTC offset.
- `scope`: non-empty mapping; every requested scope key must match exactly.
- `authority_ref`: non-empty reference to the claimed issuing authority; it must appear in caller-supplied `trusted_authorities`.
- `signature`, `key_id`, `signature_algorithm`: required non-empty strings used by the caller-supplied signature verifier.
- `records`: non-empty mapping of decision ID to decision record.
- `content_digest`: SHA-256 digest of canonical JSON for all snapshot fields except `content_digest`.

## Validation rules

1. Validate required metadata, types, and strict positive-integer `snapshot_version`.
2. Require exact matching for every caller-specified scope key.
3. Require an aware `now` value and aware `generated_at` timestamp.
4. Reject snapshots older than caller-supplied `max_age_seconds` or farther in the future than `max_future_skew_seconds`.
5. Verify the SHA-256 content digest over canonical JSON excluding `content_digest`. This establishes content integrity only, not issuer identity.
6. Require `authority_ref` to be in caller-supplied `trusted_authorities`.
7. Require signature/key metadata and a callable `signature_verifier`. The callback receives `(snapshot, signature, key_id, algorithm)` and must return exactly `True`; missing verifier, false/non-True result, or any exception fails closed. The callback is responsible for verifying a well-defined signed payload with an appropriate cryptographic implementation.
8. If `last_accepted_version` is supplied, require it to be a non-negative integer (not `bool`) and require `snapshot_version > last_accepted_version`. Equality is replay and lower versions are rollback. No implicit string-to-number conversion is performed.
9. Validate each decision record and all registry supersession links/cycles. Any failure rejects the entire snapshot.

`last_accepted_version` is an input high-water mark, not self-authenticating state. The caller must store and update it in a trusted, durable manner after acceptance; otherwise an attacker may reset it and defeat local anti-rollback.

## Trust model distinctions

- **Content integrity:** SHA-256 detects content changes relative to the digest. Anyone who can edit the snapshot can recompute it.
- **Signature authenticity:** a trusted verifier validates the signature against an accepted key and signed payload. A digest match alone never authenticates an issuer.
- **Freshness:** `generated_at` and caller-supplied age/skew limits constrain age relative to the caller's clock.
- **Latestness:** a fresh snapshot is not necessarily the newest snapshot available. Proving latestness requires a separate trusted source or protocol.
- **Anti-rollback:** a strictly increasing numeric version is compared with `last_accepted_version`; durable trusted retention of that high-water mark is essential.
- **Revocation:** local validation cannot learn that an authority/key/record was revoked remotely unless a separate trusted service or mechanism delivers that information.

Age limits and allowed future clock skew are caller-supplied engineering parameters, not approved Moon investment policy. This step implements a local contract, testable verifier boundary, and local durable storage primitive only; it does not implement an authentication service, network integration, key management infrastructure, remote latestness, or revocation delivery.

## Integration status and caller responsibilities

The validator is currently a callable governance API exported from `data`; repository search shows its direct call sites are tests, not the Core Runtime or a Framework execution path. This is intentional for this step: the local contract is available, but no production registry consumer has been selected or wired to it.

Before any production caller adopts this contract, that integration must explicitly provide and govern all of the following:

- the expected scope and freshness/skew policy for the specific consumer;
- the trusted authority allowlist and a cryptographic verifier that validates a documented signed payload against trusted key material;
- a durable, trusted `last_accepted_version` scoped to the relevant authority/registry/scope, updated atomically only after successful acceptance;
- a trusted mechanism for discovering newer snapshots and delivering authority/key/record revocations, if those guarantees are required.

Validation does not itself persist the high-water mark. The local SQLite acceptance primitive described below can atomically persist the high-water mark and a recovery journal, but no production caller currently uses it. Callers must not treat a successful validation return as proof of remote latestness, revocation status, or durable anti-rollback.

### Consumer discovery audit (Step 50 follow-up)

Repository search identifies governance-adjacent areas, but none is currently an approved production consumer of `validate_authoritative_registry_snapshot()`. The following are candidates to assess, not authorization to integrate:

| Area | Evidence in the current source | Audit conclusion |
|---|---|---|
| Moon ADM data/governance readiness | `src/orion/frameworks/moon/adm_data.py` includes `authoritative_governance_binding_not_implemented` and production-governance blocked reasons. | Closest governance integration candidate, but explicitly not bound to the authoritative registry contract. Do not activate ADM or infer policy approval. |
| Supernova universe/company configuration | `src/orion/core/config_loader.py` defines `candidate_universe.source` and `approved_companies`; `src/orion/frameworks/supernova/engine.py` builds the current approved-company input. | Candidate-universe source semantics and authoritative registry format are not established by these fields alone. Do not select a provider or change universe semantics. |
| Runtime framework/service registries | `src/orion/core/framework_registry.py` and `src/orion/services/registry.py` are in-memory registries of runtime objects/services. | These are not authoritative decision-record snapshot consumers and should not be wired to this validator. |
| Core Runtime decision lifecycle | `src/orion/core/runtime_session.py` and `src/orion/core/decision.py` implement runtime decisions/transitions, with no direct call to the snapshot validator. | No integration justified; preserve the frozen Runtime boundary. |

**Integration gate:** before selecting any candidate, document its exact registry payload and owner, consumer-specific scope/freshness rules, trusted authority/key policy, and durable atomic high-water storage. For Moon, existing blocked reasons are an explicit signal that authoritative governance binding remains incomplete; a successful snapshot validation alone must not clear those gates. For Supernova, a configured source name is not evidence that a provider or its semantics has been approved.

## Explicit non-goals

- No remote API, database, signature key, certificate, or identity provider.
- No provider selection or financial semantics approval.
- No approval of unresolved Moon ADM provider semantics, calendar, freshness, or activation gates. D-055 already approves the SGOV benchmark and strict comparison operator.
- No Runtime integration or strategy activation.
- Core Runtime remains frozen and Moon `active_strategies` remains empty.

## Tests

`tests/data/test_governance.py` covers a fresh valid snapshot, missing metadata, digest tampering, scope mismatch, staleness, missing timezone, and excessive future timestamps. The broader suite verifies that decision record and supersession lineage validation remain in force.

## Local durable high-water mark implementation

`data.registry_high_water_store.SQLiteHighWaterMarkStore` provides a local, file-backed SQLite implementation of the monotonic-version storage contract. Its key is the tuple `(authority_ref, registry_type, canonical scope)`. Scope keys are canonicalized as sorted, compact UTF-8 JSON and hashed with SHA-256; the canonical JSON is also retained to detect an unexpected digest collision.

`advance()` is a compare-and-swap operation. The caller supplies `expected_current_version` (or `None` for first acceptance) and a strictly higher positive `new_version`. A SQLite `BEGIN IMMEDIATE` transaction serializes writers, compares the current value, and commits the advance before returning. A stale concurrent writer receives `HighWaterMarkConflict`; database errors fail closed as `HighWaterMarkStorageError`. Recreating the store over the same database preserves the value.

This is a local storage primitive, not a distributed consensus service. The database path, filesystem permissions, backup/restore procedure, and host integrity remain part of the trust boundary. Do not place the database on an unverified network filesystem or treat a restored older backup as trustworthy without an explicit recovery procedure. The implementation does **not** make a separate application StateStore update and this SQLite update one cross-system transaction. The recoverable acceptance journal below provides an atomic local outbox with idempotent downstream replay, but exactly-once effects in a separate store are not guaranteed.

Recommended call sequence for a future consumer:

1. Read the stored high-water mark for the exact authority/registry/scope tuple.
2. Validate snapshot authenticity, digest, scope, freshness, lineage, and `snapshot_version > stored_version`.
3. Commit the version using `advance(expected_current_version=stored_version, new_version=snapshot_version)`.
4. If the compare-and-swap conflicts or persistence fails, do not report acceptance; reload state and revalidate from the beginning.
5. Only then expose the accepted snapshot to downstream logic, subject to the consumer's separate governance gates.

This module is not wired into Runtime or Supernova engine execution. It does not implement signature cryptography, authority/key distribution, remote latestness, revocation, or cross-system transactional acceptance.

### Recoverable acceptance journal (Step 50 follow-up)

`SQLiteHighWaterMarkStore.accept_snapshot()` is the transactional acceptance primitive for a future consumer. It must be called **only after** the caller has successfully validated issuer authority, signature, content digest, scope, freshness, and lineage. It atomically advances the high-water mark and writes a `pending` acceptance event in the same SQLite transaction. If either write fails, both changes roll back. This closes the crash window between advancing the HWM and recording what must be materialized downstream.

A consumer recovery loop should:

1. Query `list_pending_acceptances()` on startup and periodically.
2. Apply each event to its downstream state using an idempotency key (`event_id`) or an equivalent unique key such as `(authority_ref, registry_type, scope, snapshot_version)`.
3. Call `mark_applied(event_id)` only after downstream application has durably succeeded.
4. Retry pending events after transient failure. If a crash occurs after downstream application but before acknowledgement, the event will be delivered again; therefore downstream application must be idempotent.
5. Treat a high-water CAS conflict as a concurrent state change: reload the HWM and re-run snapshot validation before attempting acceptance again.

The acceptance event is a durable local outbox/journal, not proof that a separate application StateStore has already been updated. The protocol provides atomicity between the SQLite HWM and journal only. Exactly-once effects across an independent downstream store are not claimed; the consumer must implement idempotency or transactional inbox/outbox semantics. `accept_snapshot()` also does not run the validator or authenticate its arguments; callers must preserve that validation-before-acceptance boundary.


### Consumer retry and idempotency contract

`data.registry_acceptance_consumer.drain_pending_acceptances()` is a small reference drain loop for the journal. It applies pending events in per-authority/registry/scope version order, acknowledges each event only after the callback returns successfully, and stops at the first application or acknowledgement error. The error identifies the event and phase; the event remains pending unless its acknowledgement was durably committed.

The callback is an **at-least-once** consumer boundary, not an exactly-once guarantee. It must use `event_id` (or the unique authority/registry/scope/version tuple) as an idempotency key and atomically record that key with its downstream state change where possible. If downstream application succeeds but journal acknowledgement fails, the same event is delivered again. A single drain loop's ordering does not provide a cross-process lease or prevent multiple workers from concurrently seeing the same pending event; use the leased drain path when multiple workers may run.

Transient failures are surfaced as `AcceptanceDrainError` and are not silently swallowed. The caller may retry with bounded backoff and operational alerting. Do not acknowledge failed application, skip an earlier failed event in the same ordered batch, or infer that a pending event has not already affected the downstream store.

### Consumer claim/lease recovery boundary

`SQLiteHighWaterMarkStore.claim_pending_acceptances()` atomically claims eligible pending events using a worker identity, opaque lease token, and expiration timestamp. Claiming is serialized by a SQLite write transaction. A live lease cannot be claimed by a second worker; after expiration, another worker may reclaim the event with a new token. Events are claimable in ascending snapshot-version order within each authority/registry/scope, and an earlier pending event blocks later versions even while leased.

`acknowledge_claim()` only acknowledges a pending event when the worker identity and lease token still match and the lease has not expired. The legacy `mark_applied()` path cannot bypass an active lease. A worker that loses its lease must not treat a completed callback as authoritative; it must allow recovery to redeliver the event. Because a callback can commit its downstream effect and then crash before acknowledgement, the effect still must be idempotent using the durable event ID (or an equivalent key committed atomically with the downstream effect).

Lease timestamps rely on the host wall clock and this SQLite design assumes workers share one local database and a sufficiently consistent clock. It is not a distributed lease service or consensus mechanism. Lease expiry does not stop a stale process from executing external side effects; downstream idempotency and, where available, fencing tokens remain necessary. The runtime and Supernova engine are not wired to this reference consumer.


### Failure-injection and state-transition checks

The test suite injects SQLite trigger failures during multi-event claim and acknowledgement. A failed multi-event claim must roll back every lease update in that transaction; a failed acknowledgement must leave the event pending and preserve its current lease until retry or expiry. Tests also recreate the store between claim and recovery to verify that a live lease remains effective across process/store restarts and that an expired lease can be reclaimed with a new token.

The state invariants are:

- `pending` events may be unleased or have a complete lease tuple (`lease_owner`, `lease_token`, `lease_expires_at`); partial lease tuples are invalid states.
- `applied` events have a durable `applied_at` timestamp and no lease fields.
- Only the current owner/token with an unexpired lease can acknowledge a leased event.
- A stale lease cannot acknowledge after lease expiry or after a different worker reclaims the event.
- Failure before transaction commit must not leave a partial claim or a partial acknowledgement.
- Version ordering remains per authority/registry/scope; an earlier pending event blocks later versions even when its lease has expired and awaits reclaim.

These tests exercise local SQLite transaction semantics and deterministic lease-time boundaries. They do not simulate power-loss durability on every filesystem, distributed hosts sharing a database, or atomic commits with an external consumer state store.
