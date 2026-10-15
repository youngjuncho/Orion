# Orion Step 50 Production Approval Gates

**Status:** Decision register; no production approval granted  
**Date:** 2026-10-11  
**Scope:** Authoritative registry acceptance and downstream materialization only

## 1. Purpose and decision rule

This document turns the Step 50 integration exit criteria into explicit decisions and evidence requirements. It does not select a registry domain, trust authority, cryptographic algorithm, freshness window, recovery-point objective, or consumer behavior on behalf of the project owner.

**Default disposition for every unresolved gate: BLOCK production wiring.** Existing validation and persistence components may continue to be tested in isolation. No item in this document authorizes Runtime or Supernova integration, Moon strategy activation, order execution, or a Core Runtime lifecycle change.

A gate is complete only when the decision is explicit, the decision owner is identified, supporting evidence is recorded, and the relevant tests pass. A code default, an example configuration, or a passing unit test is not itself policy approval.

## 2. Required decision register

| ID | Decision required | Minimum decision content | Evidence required before closure | Current status |
|---|---|---|---|---|
| G-01 | Registry domain and authority | Exact registry type, authoritative issuer identity, ownership, and authority to publish/revoke records | Approved domain contract and issuer ownership evidence | DEFERRED — BLOCKING (D-060) |
| G-02 | Payload and scope contract | Required fields, schema/version evolution, canonical serialization, exact scope keys, and whether unknown fields are rejected | Versioned schema/contract plus positive and negative fixtures | OPEN — BLOCKING |
| G-03 | Signature and key policy | Signature scheme, signed bytes/canonicalization, key identifiers, trusted-key source, key rotation, expiry, revocation, and compromise response | Reviewed verifier implementation, key lifecycle procedure, test vectors, invalid-signature and revoked-key tests | OPEN — BLOCKING |
| G-04 | Freshness and replay policy | Maximum snapshot age, tolerated future clock skew, handling of delayed but valid snapshots, and recovery behavior after extended outage | Explicit numeric policy with boundary tests and documented clock assumptions | OPEN — BLOCKING |
| G-05 | Anti-rollback persistence | HWM database location/permissions, transaction durability assumptions, backup frequency, restore procedure, and detection of a restored older database | Recovery runbook and tests demonstrating stale-backup detection or an explicitly accepted residual risk | OPEN — BLOCKING |
| G-06 | Acceptance orchestration | Mandatory use of `RegistryAcceptanceService`; ownership of validator configuration; prohibition of direct HWM-only advancement in production paths | Call-site audit, boundary tests, and a production composition test showing approved options are injected | OPEN — BLOCKING |
| G-07 | Consumer materialization | Downstream state changes, stable idempotency/deduplication key, duplicate delivery behavior, ordering, and poison-event handling | Consumer contract and crash/retry tests around side-effect-before-acknowledgement | OPEN — BLOCKING |
| G-08 | Lease and concurrency operations | Lease duration, renewal/reclaim policy, clock assumptions, multi-process expectations, and alerting on repeated failures | Concurrency/recovery tests and operational thresholds/runbook | OPEN — BLOCKING |
| G-09 | Domain-specific integration | First approved consumer and its exact read/write boundary; whether Supernova is in scope | Integration design review and isolated end-to-end tests against the approved schema | OPEN — BLOCKING |
| G-10 | Operational ownership | Who can publish, approve, revoke, restore, and respond to key or database incidents; audit retention and monitoring | Named role/owner matrix, incident procedure, and observable health/error signals | OPEN — BLOCKING |

## 3. Non-negotiable invariants

1. **Fail closed:** missing or ambiguous trust configuration must not accept a snapshot.
2. **Verify before persistence:** authenticity, digest, scope, freshness, schema, and anti-rollback checks must complete before acceptance is committed.
3. **Atomic acceptance:** HWM advancement and acceptance-journal insertion must remain one SQLite transaction.
4. **CAS conflict means revalidation:** reload current durable state and validate again; never blindly retry a snapshot validated against a stale HWM.
5. **Idempotent downstream effects:** a crash after applying an event but before acknowledgement must not duplicate a non-idempotent business effect.
6. **No hidden policy defaults:** numeric freshness/lease settings, trusted authorities, key sources, and recovery assumptions must be explicit reviewed configuration.
7. **No implicit integration authorization:** closing a technical gate does not itself authorize Runtime/Supernova wiring or Moon activation; integration approval is a separate explicit decision.

## 4. Verification required when a gate is proposed for closure

For each gate, record:

- decision ID and exact approved value(s);
- decision owner and approval date;
- contract/policy document version;
- implementation/configuration path;
- test names and results, including negative and failure-injection cases;
- operational procedure and responsible role, where applicable;
- unresolved risks and explicit acceptance owner, if any.

If any required field is missing, retain `OPEN — BLOCKING`. Do not infer approval from silence or from the presence of an implementation.

## 5. Current engineering disposition

- **G-01 disposition (D-060): DEFERRED — BLOCKING.** No authoritative registry domain or issuer is selected. This is not a waiver and does not permit production wiring. Reopen when a concrete consumer requirement and accountable issuer/operational owner are identified.
- `RegistryAcceptanceService` is the intended guarded acceptance entry point for isolated use.
- `SQLiteHighWaterMarkStore.accept_snapshot()` and `advance()` remain callable APIs; source-level tests discourage bypasses but do not create a security boundary against arbitrary external callers.
- The signature verifier and trusted-authority/key policy are supplied externally and have not been approved here.
- The SQLite store does not independently protect against an operator restoring an older database image; see `Orion_Step50_Recovery_Failure_Matrix.md` for the evidence boundary and unresolved operational requirements.
- The downstream consumer callback cannot be transactionally coupled to acknowledgement; idempotency remains a consumer contract.
- No production Runtime, Moon, or Supernova call site is authorized by this document.

## 6. Recovery evidence reference

`Orion_Step50_Independent_Rollback_Detection_Contract.md` defines the required invariants and cross-store recovery evidence for future independent rollback detection; it is a requirements document, not an implementation or provider decision.


`docs/01_Architecture/Orion_Step50_Recovery_Failure_Matrix.md` distinguishes covered process/store recovery and failure-injection scenarios from unresolved valid-stale-backup rollback detection, deployment-specific durability, and operational restore requirements. Corrupt database initialization is required to fail closed rather than silently initialize fresh state.

## 7. Release gate

Production wiring remains **NO-GO** until G-01 through G-10 have explicit dispositions and the project owner separately approves the precise integration target. If a gate is intentionally waived, the waiver must state its scope, residual risk, owner, and expiry/review date; a waiver must not silently broaden the authority or scope of the registry.
