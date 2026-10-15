# Orion PCD-15 Implementation Readiness Gate Audit

**Status:** Implementation blocked pending explicit project-owner decisions  
**Date:** 2026-10-15  
**Scope:** Determine whether the current governance acceptance prototype can safely be bound to Moon/ADM.

## Finding

The current repository does not contain enough approved trust-policy input to implement a production PCD-15 binding without inventing authority or security policy. This is a governance decision blocker, not a missing Python validation helper. Do not add a production caller from registry acceptance to the Moon signal guard in this state.

The existing guard's unconditional `authoritative_governance_binding_not_implemented` reason is the correct safe behavior. A locally valid record, a matching SHA-256 digest, a caller-provided approval label, or a durable SQLite high-water mark is not proof that a record came from an authorized issuer or that the snapshot is current and rollback-resistant.

## Readiness by dependency

| Dependency | Evidence needed before production binding | Current state | Required action |
|---|---|---|---|
| G-01 authority/domain | Named registry domain, issuer identity, accountable owner, publish/revoke powers, exact scope | Deferred/blocking; no authority selected | Project owner selects an operating model and records the decision |
| G-02 payload/scope | Frozen schema/version, canonical byte representation, unknown-field and scope-key behavior | Unresolved contract questions documented | Approve one schema and compatibility policy before signing/verifying production payloads |
| G-03 cryptographic trust | Concrete signature algorithm, verifier, issuer-to-key binding, key custody/rotation/revocation | Callback interface only; no production trust configuration | Approve and implement a verifiable trust configuration with positive and negative vectors |
| G-04/G-05 freshness and rollback | Trusted clock/freshness rules and an anti-rollback anchor independent of a restorable local SQLite backup | Blocking design gap | Approve outage, recovery, and rollback behavior; test restoration of a valid but stale backup |
| G-06/G-08 acceptance and consumer recovery | Atomicity, idempotency, concurrent acceptance, crash recovery, durable consumer acknowledgement | Prototype primitives exist; Moon-specific production consumer absent | Specify and test transaction/recovery boundaries before integration |
| G-09/G-10 consumer ownership | One concrete consumer, operational owner, monitoring and incident response | Not established for production binding | Name consumer and owner; define incident and re-authorization procedures |
| PCD-15 Moon binding | Typed verified-resolution result tied to accepted snapshot and exact required decision versions/scope | Proposal only; guard intentionally blocks | Implement only after the preceding decisions are approved and evidenced |
| PCD-16 activation | Separate authorization to activate a strategy | Not approved | Keep separate from PCD-15; retain `active_strategies: []` |

## Safe work that can continue without owner decisions

- Offline schema and malformed-input tests for the existing local prototype.
- Documentation of unresolved decisions and acceptance criteria.
- Unit tests for fail-closed behavior and deterministic integrity checks.
- Static inspection to ensure no active runtime path consumes an unverified registry result.

## Work that must not proceed yet

- Selecting or hard-coding an issuer, signing key, cryptographic algorithm, production freshness threshold, or external anti-rollback provider without approval.
- Treating SQLite persistence as an independent anti-rollback anchor.
- Connecting a caller-supplied `APPROVED` value or reference string directly to the ADM guard.
- Clearing `authoritative_governance_binding_not_implemented`, constructing an eligible signal, or activating Moon.

## Exit criteria

PCD-15 implementation may be proposed for review only after the owner-approved G-01/G-02/G-03/G-04/G-05 inputs are recorded and the acceptance/recovery model has testable requirements. The resulting resolver must produce a typed immutable evidence object; the guard must validate that object and clear only the governance blocker. All unrelated data-quality, provider, comparison, and strategy-activation gates remain independent.

Until then, no source-code integration change is warranted. The next meaningful project action is an explicit owner decision on the registry operating model, not another speculative implementation patch.
