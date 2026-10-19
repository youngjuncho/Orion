# Orion Moon / ADM — PCD-15 G-01 and Registry Acceptance/Recovery Audit

**Date:** 2026-10-19  
**Baseline:** `Orion_1018(1).zip`, cumulative bundle v23  
**Status:** Audit / decision-gap record only; no authority selected, no production approval, no runtime wiring

## 1. Executive finding

The repository already contains substantial isolated registry-acceptance and recovery primitives, but they do not establish an authoritative governance service and are not connected to Moon/ADM production execution. The blocking issue is not simply missing adapter code: G-01 remains `DEFERRED — BLOCKING` under D-060, and G-02 through G-10 remain open/blocking in the Step 50 production gate register.

Accordingly, this audit makes no production code change. It preserves the current fail-closed ADM behavior and `config/moon.yaml` `active_strategies: []`.

## 2. Evidence reviewed

- `Orion_Step50_G01_Registry_Authority_Decision_Brief.md`: no registry domain or issuer selected; requires an accountable owner and explicit publish/revoke authority.
- `Orion_Step50_Production_Approval_Gates.md`: G-01 is `DEFERRED — BLOCKING`; G-02 through G-10 are `OPEN — BLOCKING`; production wiring is NO-GO until gates and target approval are explicit.
- `Orion_Step50_Independent_Rollback_Detection_Contract.md`: the SQLite HWM cannot detect restoration of an older but internally valid database without an independently protected monotonic reference.
- `Orion_Step50_Recovery_Failure_Matrix.md`: local transaction, restart, lease, and retry paths have test evidence; valid-stale-backup rollback and deployment-specific recovery remain open.
- `Orion_Step50_Persistence_Necessity_Assessment.md`: no production call site currently demonstrates a need to operationalize the isolated HWM/journal/lease subsystem; persistence requirements remain a decision, not an assumption.
- `Moon_ADM_Governance_Binding_Implementation_Audit.md` and `Moon_ADM_PCD15_Governance_Binding_Contract_Proposal.md`: Moon/ADM authoritative binding is not implemented; a caller-supplied approval or reference is insufficient.

## 3. Acceptance and recovery path audit

| Boundary | Existing evidence | Finding | Production disposition |
|---|---|---|---|
| Snapshot acceptance | `RegistryAcceptanceService` validates before calling the HWM store; acceptance is atomic with journal insertion | Useful isolated acceptance primitive; does not itself define issuer authority or approved verifier configuration | Keep isolated |
| HWM compare-and-swap | Stale expected-version conflicts are rejected; callers must reload and revalidate | Protects concurrent writes against current stored state, not against whole-database rollback | Blocking for anti-rollback-dependent use |
| Pending-event journal | HWM advance and pending journal event share a SQLite transaction | Atomic local acceptance record; does not atomically commit a separate downstream side effect | Consumer must be idempotent |
| Consumer drain | At-least-once delivery, ordered processing, acknowledgement after callback success | Callback may be repeated after side effect / acknowledgement failure | No exactly-once claim; require durable downstream deduplication or transactional inbox/outbox |
| Lease-based drain | Claim token and expiry gate acknowledgement; failure injection covers multi-row transaction rollback | Local SQLite lease semantics only; wall-clock and stale-worker side effects remain relevant | Not a distributed lease/fencing service |
| Corrupt DB initialization | Tests require storage error rather than silent empty-state reinitialization | Fail-closed initialization is covered; operational restore procedure is not | Runbook/drill required |
| Valid stale backup restoration | HWM and journal reside in the same DB | Restored old DB can present internally consistent old state | OPEN — BLOCKING without independent anchor or explicit risk acceptance |
| Authority and signature trust | Validator relies on injected trust configuration and verifier callback | No approved issuer/key policy or proof of authority follows from the prototype alone | G-01/G-03 remain blocking |
| Moon/ADM binding | Guard unconditionally blocks with `authoritative_governance_binding_not_implemented` | Safe fail-closed behavior; no authoritative resolver is wired | PCD-15 remains open |

## 4. Decision gaps that must not be filled by implementation guesswork

### G-01 — authority and domain

The project owner must identify the exact registry domain/type, stable issuer identifier, accountable owner, authorized publishers/approvers, revoker and revocation propagation mechanism, permitted scope, audit evidence, and incident owner. A repository path, hostname, digest, or fixture is not proof of authority.

### G-02 / G-03 — payload and cryptographic trust

Freeze canonical payload bytes, schema evolution and unknown-field behavior before choosing/verifying signatures. Then approve the signature scheme, trusted-key source, issuer-to-key binding, rotation, expiry, revocation, and compromise response. A generic callback is an extension point, not an approved cryptographic trust policy.

### G-04 / G-05 — freshness and rollback

Specify maximum age, clock skew, delayed snapshots, replay rules, and recovery behavior. Decide whether cross-session monotonic acceptance is a real requirement. If it is, choose an independent rollback-resistant anchor and define outage behavior; never silently fall back to the SQLite HWM when the anchor is unavailable.

### G-06 through G-10 — orchestration and operations

Define the mandatory acceptance facade, the exact consumer/scope, downstream idempotency, poison-event handling, lease/clock assumptions, monitoring, recovery owner, and deployment validation. Passing unit tests does not close these policy or operational gates.

## 5. Recommended next engineering sequence

1. Keep G-01 and G-02 through G-10 in their recorded blocking states until a decision owner provides explicit approved values and evidence.
2. Resolve whether the current MVP actually requires cross-session anti-replay or durable downstream delivery. The existing persistence assessment recommends stateless fetch-and-validate as the default candidate absent a demonstrated requirement; do not operationalize SQLite merely because the prototype exists.
3. If durable anti-rollback is required, select and approve the independent anchor and failure semantics before implementing it. If not required, record the accepted threat boundary and avoid claiming cross-session rollback protection.
4. After G-01 through G-05 have approved contracts, implement a typed authoritative resolver that returns verified evidence rather than accepting caller-asserted approval flags.
5. Wire it only behind an explicit approved composition root, then add end-to-end negative tests for missing authority, wrong scope, invalid/revoked key, stale/future snapshot, replay, anchor outage, rollback, persistence failure, and consumer retry/idempotency.
6. Keep `config/moon.yaml` at `active_strategies: []` and retain `authoritative_governance_binding_not_implemented` as a blocking reason until integration and separate activation approval are complete.

## 6. Current disposition

- G-01: `DEFERRED — BLOCKING`.
- G-02 through G-10: `OPEN — BLOCKING`, unless separately changed by an explicit, evidenced decision record.
- PCD-15 / PCD-16: open; authoritative binding not implemented.
- Registry acceptance/HWM/journal/consumer: isolated reference implementation; not a production trust boundary.
- Moon signal assembly: remain fail-closed.
- Strategy activation: prohibited; `active_strategies: []` remains required.

This audit is not an approval, waiver, or implementation of authority, signature trust, remote revocation, independent rollback detection, or production integration.
