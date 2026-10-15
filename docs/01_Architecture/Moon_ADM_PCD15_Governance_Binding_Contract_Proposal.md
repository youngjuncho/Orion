# Moon ADM PCD-15 Governance Binding Contract Proposal

**Status:** Design proposal only — not approved for production integration  
**Date:** 2026-10-14  
**Scope:** Contract boundary between authoritative decision-registry acceptance and the Moon ADM comparison guard

## 1. Decision

Keep `authoritative_governance_binding_not_implemented` as a blocking reason. Do not connect the current snapshot validator or acceptance service directly to the ADM guard until the trust-policy decisions in §4 are approved and the acceptance criteria in §6 pass.

This proposal defines the shape of a future integration boundary. It does not choose an issuer, key, cryptographic algorithm, registry owner, freshness threshold, remote revocation mechanism, or independent anti-rollback service. It does not authorize provider use, signal assembly, or strategy activation.

## 2. Current code boundary

The repository currently has separate components:

- `data.governance.validate_authoritative_registry_snapshot()` validates a supplied snapshot using caller-supplied trust configuration and a signature-verifier callback.
- `data.RegistryAcceptanceService` validates before accepting a version into `SQLiteHighWaterMarkStore` and its acceptance journal.
- `data.registry_acceptance_consumer` supplies at-least-once journal-consumption helpers.
- `guard_adm_comparison_for_signal_assembly()` in `orion.frameworks.moon.adm_data` still unconditionally blocks on `authoritative_governance_binding_not_implemented`.

There is no approved production caller connecting these components to Moon. The SQLite high-water mark is durable local state, but by itself it cannot detect restoration of an older, internally valid copy of that same database. The acceptance journal is not an independent trust anchor.

## 3. Proposed integration contract

A future implementation should introduce a dedicated resolver/binding interface between registry acceptance and the Moon guard. The guard must not accept a caller-provided status/reference pair as proof of approval.

The resolver must accept only the exact request needed by the consumer:

- the required decision IDs and required record versions, where version pinning is part of the policy;
- the exact canonical Moon/ADM scope;
- the expected authority and registry identity;
- the current time and the approved freshness policy, supplied by trusted application configuration rather than the request payload.

On success, the resolver should return an immutable verified-resolution value containing at least:

- accepted snapshot identity and version;
- authority and registry identity;
- canonical scope identity/digest;
- resolved decision IDs and record versions;
- validation/acceptance evidence sufficient to correlate the result with the durable acceptance journal;
- an explicit indication that every required decision and dependency was approved, in scope, not invalidated, and not superseded.

On any error, missing configuration, unavailable trust source, unknown or unapproved decision, version mismatch, scope mismatch, invalid signature, stale snapshot, revocation uncertainty, missing dependency, or rollback uncertainty, resolution must fail closed. No partially verified result may be returned as successful.

The resolver result is evidence for the governance-binding gate only. It must not override independent data-quality, provider-contract, comparison-availability, or activation gates. A successful result must not itself construct `ADMSignalInput`, emit a Moon signal, or enable a strategy.

## 4. Trust and policy decisions that remain open

These are required inputs to production integration; this proposal intentionally does not invent their values.

| Decision | Required owner-approved answer | Current disposition |
|---|---|---|
| Registry authority | Named authority/owner, registry identity, issuance and change-control responsibility | Open; no production authority selected |
| Cryptographic trust | Signed-payload canonicalization, signature algorithm, key source, key rotation/revocation and verifier implementation | Open; callback interface alone is insufficient |
| Moon scope | Exact scope keys/values and which PCD decision IDs are required for each use | Open; no production Moon registry scope approved |
| Freshness and clock | Maximum age, future skew, clock source and behavior when time cannot be trusted | Open; no Moon production threshold approved |
| Revocation/currentness | How latest snapshots and authority/key/record revocations are discovered and authenticated | Open; local snapshot validation cannot prove remote latestness |
| Anti-rollback | Independently protected monotonic state, its operator, recovery protocol and outage behavior | Open and blocking; local SQLite alone is not independent of its own backup/restore |
| Acceptance recovery | How journal events are applied idempotently and how downstream state is reconciled after a crash | Prototype primitives exist; Moon-specific production consumer is not implemented |
| Operational ownership | Monitoring, alerting, incident response, key compromise, backup restore and re-authorization process | Open |

A decision is not closed by a passing fixture test or by setting a configuration value. The owner-approved answer and supporting evidence must be recorded in the appropriate decision record before production wiring.

## 5. Fail-closed invariants

1. No trusted resolver/binding configured → block.
2. Caller-provided `APPROVED`, reference strings, record IDs, or booleans without resolver-produced evidence → block.
3. Resolver exception, malformed result, or incomplete decision set → block.
4. Snapshot acceptance event pending or not durably materialized for the consumer → do not claim the consumer has applied it.
5. Unknown latestness/revocation status where policy requires it → block.
6. Rollback anchor unavailable, inconsistent, or unable to prove monotonic state → block; never silently fall back to the local SQLite HWM.
7. Governance approval cannot clear unrelated readiness blockers.
8. `config/moon.yaml` must retain `active_strategies: []` until a separate G7 activation authorization is approved and verified.

## 6. Required tests before considering PCD-15 complete

### Resolver contract

- valid approval for the exact required IDs, versions, authority, registry and scope;
- unknown ID, unapproved/deferred/rejected record, missing dependency, dependency cycle;
- wrong record or snapshot version, invalidated/superseded record, broken lineage;
- wrong authority, unknown key, invalid signature, unsupported algorithm and verifier exception;
- wrong scope, stale snapshot, excessive future timestamp, malformed or missing metadata;
- revoked authority/key/record and inability to obtain required revocation/currentness evidence;
- malformed resolver output and resolver exception.

### Durable acceptance and recovery

- same-version replay and lower-version rollback rejected;
- concurrent acceptors cannot both advance the same scoped version;
- failure between validation, HWM/journal commit, consumer application and acknowledgement;
- duplicate event delivery has idempotent downstream effect;
- restore of an older but valid SQLite backup is detected by the separately approved anti-rollback mechanism;
- unavailable or contradictory anti-rollback state fails closed.

### Moon guard integration

- caller attestation alone remains blocked;
- verified governance resolution clears only the governance-binding blocker, never independent provider/data/readiness blockers;
- invalid, missing, stale, mismatched or unavailable resolution yields no eligible guard result;
- no invalid path constructs `ADMSignalInput`, produces an accepted signal/state transition, or activates a strategy;
- `config/moon.yaml` continues to have `active_strategies: []` throughout PCD-15 and PCD-16 work.

## 7. Implementation sequence

1. Obtain explicit owner decisions for the open inputs in §4 and record the evidence.
2. Implement the concrete signature verifier and trusted authority/key configuration from those approved inputs.
3. Resolve the independent anti-rollback and acceptance-recovery design; do not treat the existing SQLite HWM as sufficient against valid-stale backup restoration.
4. Implement the resolver as a separately testable component returning a typed verified-resolution value.
5. Add the resolver/guard integration tests in §6 while keeping all other Moon gates closed.
6. Review PCD-15 evidence separately. Only then may a distinct G6 integration proposal be considered; G7 remains a separate activation decision.

## 8. Non-goals

This proposal does not implement the resolver, cryptographic infrastructure, remote registry fetching, revocation service, independent rollback anchor, Moon signal assembly, provider selection, investment policy, Runtime lifecycle changes, order execution, or strategy activation. It changes no investment logic and does not alter `config/moon.yaml`.
