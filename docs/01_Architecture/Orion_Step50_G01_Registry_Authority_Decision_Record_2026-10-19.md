# Orion Step 50 — G-01 Registry Authority Decision Record

**Decision ID:** G-01-DISP-2026-10-19-01  
**Decision date:** 2026-10-19  
**Decision owner:** Orion project owner (decision recorded from explicit project-owner confirmation in the working session)  
**Outcome:** **Option D selected for the current MVP; G-01 remains DEFERRED — BLOCKING**  
**Approval scope:** MVP disposition only; not production authority approval and not a waiver of any gate.

## Decision

For the current Orion MVP, do **not** designate or connect an authoritative registry to Moon/ADM. Keep the registry-acceptance prototype isolated from Moon/ADM until a concrete consumer requirement and an accountable registry owner are identified and the G-01 authority decision is reopened with supporting evidence.

This is an affirmative decision to defer authoritative registry adoption for the current MVP. It is **not** a decision that the prototype is authoritative, not approval of a stateless fetch-and-validate design, and not permission to treat repository contents, a hostname, a digest, a local database, or a test fixture as proof of authority.

## Rationale

- The current stateless-path audit has not established a concrete production consumer need for durable registry acceptance.
- No exact registry domain, issuer identity, accountable issuer owner, or publish/revoke authority has been approved.
- The signature/key lifecycle, freshness/revocation, replay and anti-rollback policy remain unresolved downstream dependencies.
- Connecting the prototype now would create an implicit trust decision without approved authority evidence.

## Required controls

1. Keep `config/moon.yaml` at `active_strategies: []`.
2. Keep PCD-15 / PCD-16 open and retain `authoritative_governance_binding_not_implemented` as a blocking reason.
3. Keep signal assembly fail-closed; registry acceptance alone must not make ADM ready.
4. Do not wire the acceptance service, consumer, SQLite HWM store, or registry events into Moon/ADM production signal assembly.
5. Do not mark G-01, G-03, or related Step 50 gates closed. Option D does not waive them.

## Reopen trigger

Reopen G-01 only when a concrete consumer requirement exists and a named accountable owner can propose the exact registry domain, issuer identity, ownership, publish/revoke authority, permitted scope, evidence/audit requirements, and operational responsibility. Cryptographic trust and key lifecycle must then be reviewed under G-03; G-01 selection alone does not authorize runtime integration.

**Review timing:** Trigger-based; no calendar deadline is assigned by this decision. Review when the consumer requirement and accountable owner are identified, or before any proposal to activate a Moon/ADM strategy or connect authoritative governance data.

## Consequences and status

- G-01: `DEFERRED — BLOCKING` (Option D is the chosen MVP disposition, not G-01 closure).
- PCD-15 / PCD-16: open; authoritative Moon/ADM binding not implemented.
- Runtime/production registry integration: not authorized.
- `active_strategies`: empty list required.
- Residual risk accepted for the MVP: authoritative governance-backed signal assembly remains unavailable; this is preferable to implying trust without an approved authority model.

## Approval boundary

This record captures the project owner's confirmation to use Option D for the current MVP. It does not identify a cryptographic issuer, approve keys or signatures, grant publish/revoke privileges, approve a production deployment, or authorize any strategy activation.
