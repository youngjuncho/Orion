# Orion Step 50 G-02 Runtime Cross-check Audit

**Status:** Audit only; G-02 remains `OPEN — BLOCKING`  
**Date:** 2026-10-15  
**Scope:** Compare the generic authoritative snapshot validator and the proposed Supernova domain validator against the unresolved G-02 payload/scope requirements.

## 1. Confirmed implementation behavior

This audit was checked against the source in this bundle, not inferred from earlier status notes.

- `src/data/governance.py::validate_authoritative_registry_snapshot` checks that required envelope fields exist, but it does not reject additional envelope fields. The required-field check is at lines 308–311; no unknown-field check follows.
- The same generic validator checks each key/value in `expected_scope` against the candidate scope (lines 331–337), but does not require exact equality between the two key sets. Additional candidate scope keys therefore remain possible.
- `src/data/governance.py::canonical_snapshot_digest` hashes the snapshot mapping excluding `content_digest`. This provides a deterministic digest for the decoded mapping; it cannot detect duplicate JSON object keys that were already collapsed by a parser before the mapping was created.
- `src/orion/frameworks/supernova/registry_contract.py::validate_approved_company_snapshot` is stricter for its proposed Supernova domain: it rejects unknown envelope fields and requires the exact scope-key set (`framework`, `domain`, `review_cycle`). It also rejects unknown record fields and unsupported schema versions.
- The Supernova validator's strictness is domain-specific. It is not evidence that the generic registry envelope has an approved universal schema, and the proposal is not production authorization.

## 2. Consequence

The generic and Supernova validators intentionally enforce different contracts. Silently making the generic validator stricter would be a compatibility and policy change; treating the generic validator as sufficient for Supernova would discard domain-specific checks. Neither path closes G-02 while registry ownership and the consumer's exact payload/scope contract remain unapproved.

## 3. Required closure evidence

Before G-02 can be considered closed, the accountable registry owner must approve:

1. Registry type and versioned envelope/record schemas for the selected consumer.
2. Exact scope-key and scope-value rules, including whether additional dimensions are rejected.
3. Unknown-field behavior and schema-evolution/migration policy.
4. Raw JSON parsing rules, including duplicate-key rejection before mapping construction.
5. Canonical serialization and digest/signature test vectors across supported implementations.

The chosen contract then needs positive and negative fixtures. G-03 cryptographic trust, freshness/rollback controls, and production consumer binding remain separate approval gates.

## 4. Disposition and non-changes

Keep G-02 `OPEN — BLOCKING`. This audit changes no runtime behavior, does not select an authority or schema, does not approve the Supernova proposal, and does not authorize Moon/ADM or Supernova integration. `config/moon.yaml` must remain `active_strategies: []`.
