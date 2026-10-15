# Orion Step 50 G-02 Payload and Scope Contract Audit

**Status:** Audit only; G-02 remains `OPEN — BLOCKING`
**Date:** 2026-10-14
**Evidence baseline:** `Orion_1013.zip` repository snapshot
**Decision boundary:** This document records implementation behavior and unresolved contract choices. It does not approve a production schema, registry authority, signature scheme, or consumer integration.

## 1. Executive result

The repository has useful local primitives for canonical JSON digests and snapshot validation, and a domain-specific Supernova registry proposal. It does not yet have one approved, versioned payload contract that governs all prospective registry consumers. The current `Orion_Step50_Production_Approval_Gates.md` records D-060 as `DEFERRED — BLOCKING`: no registry domain or issuer is selected, and the gate remains blocking rather than waived. G-02 must not be closed by treating the Supernova proposal or generic validator as an approved authority contract.

Keep G-02 `OPEN — BLOCKING`. Do not wire the validator into Moon or Supernova based on this audit.

## 2. Observed behavior in the generic validator

Source: `src/data/governance.py` and `docs/01_Architecture/Orion_Authoritative_Registry_Snapshot_Contract.md`.

- `canonical_digest()` and `canonical_snapshot_digest()` serialize mappings using `json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)` and UTF-8, excluding `content_digest` from the hash input.
- The snapshot validator requires a base set of envelope fields and requires non-empty `signature`, `key_id`, and `signature_algorithm` metadata.
- `expected_scope` is matched key-by-key: each requested key must have the expected value. The validator does not require the snapshot scope to contain exactly the same set of keys.
- The generic snapshot validator does not reject additional envelope fields. The decision-record validator also does not reject unknown fields.
- `record_version` is currently required to be non-empty text; the validator does not define a numeric schema-version migration policy.
- Duplicate JSON object keys cannot be detected after a payload has already been decoded into a normal mapping. Duplicate-key rejection must be enforced at the raw JSON parsing boundary before canonicalization.
- Canonical JSON hashing does not, by itself, define all cross-language canonicalization requirements or prove signature authenticity. The signature callback and its input contract are separate from the digest calculation.

## 3. Observed behavior in the Supernova proposal

Source: `docs/01_Architecture/Supernova_Approved_Company_Registry_Contract_Proposal.md`.

- The proposal suggests `registry_type = supernova.approved_company_state`, `schema_version = 1`, and an exact three-key scope (`framework`, `domain`, `review_cycle`).
- It proposes a domain-specific record schema and rejection of unknown security-relevant fields unless a schema version explicitly permits them.
- It explicitly states that the proposal is not approved for production integration and leaves issuer, company identity rules, canonicalization/signature format, freshness, and operational policy unresolved.
- The proposal's stricter unknown-field and exact-scope rules are not currently enforced by the generic validator alone.

## 4. Contract gaps to resolve before G-02 closure

| Gap | Why it matters | Required evidence |
|---|---|---|
| Schema ownership and domain binding | A generic envelope cannot determine whether Moon/ADM or Supernova-specific records are semantically valid | Approved registry type and consumer-specific schema owner; G-01/G-09 disposition |
| Exact scope-key set | Subset matching may accept extra scope dimensions that the domain contract intended to reject | Explicit exact-key policy and tests for both missing and additional keys |
| Unknown-field policy | Silently accepting unknown security-relevant fields can create version-skew ambiguity | Explicit reject/allow policy at envelope and record levels, with versioned compatibility tests |
| Schema versioning | `record_version` text is not equivalent to a registry `schema_version` and does not define migration behavior | Separate schema version from record revision; compatibility and migration rules |
| Canonicalization boundary | Duplicate-key rejection must occur before a mapping exists; serializer behavior must be pinned across implementations | Raw JSON duplicate-key tests, canonicalization vectors, UTF-8 and number/timestamp test vectors |
| Digest/signature composition | Digest proves consistency with its value, not authenticity; signed bytes must be unambiguous | Approved signed-payload definition and concrete verifier test vectors under G-03 |
| Scope and version identity | High-water marks are keyed by authority, registry type, and canonical scope; scope changes can partition rollback state | Approved scope identity and explicit migration/reset policy |

## 5. Recommended disposition

1. Keep G-02 `OPEN — BLOCKING`; do not claim contract approval from existing code or the Supernova proposal.
2. Treat the generic snapshot validator as an isolated validation primitive, not the final domain schema.
3. Once G-01 identifies a real registry consumer and authority, define a versioned envelope/record schema for that consumer. Avoid a premature one-size-fits-all schema.
4. For a future strict domain contract, add an explicit strict wrapper or schema validator that rejects unknown fields and enforces the exact scope-key set. Do not silently change generic-validator behavior without a compatibility review.
5. Add tests for extra scope keys, unknown envelope/record fields, malformed or unsupported schema versions, duplicate raw JSON keys, and canonicalization test vectors before requesting G-02 closure.
6. Keep G-03 signature policy and runtime integration as separate gates. G-02 closure must not imply trust establishment or production authorization.

## 6. Non-changes

This audit makes no source-code or runtime changes, selects no cryptographic algorithm or key, does not close G-01/G-02/G-03, and does not authorize Moon/ADM or Supernova integration. `config/moon.yaml` must remain `active_strategies: []` until the separate activation decision is approved.
