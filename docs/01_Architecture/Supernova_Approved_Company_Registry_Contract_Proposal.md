# Supernova Approved-Company Registry Contract Proposal

**Status:** Design proposal only; not implemented or approved for production integration  
**Date:** 2026-10-11  
**Decision baseline:** D-049 (2026-10-05)  
**Related contract:** `Orion_Authoritative_Registry_Snapshot_Contract.md`

## 1. Purpose and decision boundary

This proposal defines a narrow first registry domain: the **Supernova approved-company governance state**. It does not define the broader research candidate universe, calculate company scores, produce portfolio transition recommendations, or authorize trades. The purpose is to make a signed, versioned representation of a governance decision consumable without treating configuration or a research document as an authoritative approval record.

This proposal does not authorize runtime integration. A local SQLite high-water store and recoverable acceptance journal now exist as storage primitives, but the registry owner, signing-key policy, canonicalization implementation, freshness limits, production consumer integration, and operational deployment remain to be approved before any consumer may rely on it.

## 2. Domain separation

Maintain distinct concepts and payloads:

1. **Approved-company state registry** — records an explicit governance decision for a company within a named review cycle.
2. **Research candidate universe** — an exploratory/research input and never proof of approval.
3. **Runtime configuration** — may select a source or configure behavior, but is not itself an authority-signed governance record.

A company appearing in the candidate universe or `config/supernova.yaml` does not establish approval. D-049 approves the five-company baseline for its review cycle; it is not a standing blanket approval for future cycles or a trading instruction.

## 3. Proposed snapshot envelope

The envelope MUST satisfy the generic snapshot contract. The following domain values are proposed in addition to its required metadata:

| Field | Proposed rule |
|---|---|
| `registry_type` | Exact constant `supernova.approved_company_state` |
| `schema_version` | Positive integer; initial proposal `1` |
| `scope` | Exact keys `framework=Supernova`, `domain=approved_company_state`, and `review_cycle=<explicit cycle identifier>` |
| `records` | Mapping keyed by stable decision-record ID; no implicit records derived from config or candidate-universe documents |
| `source_decision_refs` | Explicit Decision Log references supporting the snapshot, including D-049 for the 2026-10-05 baseline |

The generic envelope fields remain required: `snapshot_id`, strict positive integer `snapshot_version`, timezone-aware `generated_at`, `authority_ref`, `signature`, `key_id`, `signature_algorithm`, `content_digest`, and `records`. A consumer must request the exact expected scope; it must not accept a broader or merely similar scope.

## 4. Proposed record schema

Each record is a governance assertion, not a computed score:

- `record_id`: stable, unique identifier within the registry.
- `company_id`: canonical identifier; initially an uppercase ticker only for the five D-049 baseline entries, with exchange/security identity rules to be defined before supporting ambiguous tickers.
- `decision_ref`: immutable Decision Log identifier such as `D-049`.
- `review_cycle`: explicit cycle identifier matching snapshot scope.
- `governance_status`: controlled enum, initially `approved`; future states require an explicit schema/governance decision.
- `effective_at`: timezone-aware timestamp for when the decision takes effect.
- `supersedes_record_id`: nullable explicit predecessor reference; no inferred supersession based only on timestamp or ordering.
- `decision_payload_digest`: digest of the canonical decision facts represented by this record, to make mapping to the underlying decision auditable.

The D-049 baseline maps to NVDA, GOOGL, ISRG, PLTR, and CEG as approved for the recorded review cycle. Company Score, leadership role, Replacement Risk, and Action are contextual decision fields in D-049; they must not be silently interpreted as order instructions or used as substitutes for `governance_status`. If those fields are carried in a later schema, their enum/range semantics and binding to the decision record must be explicit.

## 5. Canonicalization and signature boundary

Before implementation, specify one canonical serialization algorithm and pin it in tests. The canonical signed payload MUST:

- use UTF-8 without BOM;
- reject duplicate JSON object keys;
- define object-key ordering, string escaping, number representation, and timestamp normalization;
- include all security-relevant envelope and record fields except the detached signature and fields explicitly excluded by the generic digest contract;
- define whether the signature covers the `content_digest` and ensure the digest/signature relationship has no circular dependency;
- reject unknown security-relevant fields unless the schema version explicitly allows them.

The SHA-256 `content_digest` detects accidental or malicious content changes only relative to the digest. The signature verifier must validate the canonical payload against trusted key material associated with the allowlisted `authority_ref` and `key_id`. A verifier callback returning `True` is not, by itself, proof that the callback was correctly configured; production integration must test the concrete cryptographic implementation and key-binding policy.

## 6. Authority and key trust policy

The registry authority must be named and governed separately from the data host or file location. Before production use, define:

- who may issue and supersede Supernova approval records;
- the allowlisted authority identifiers and their permitted scopes;
- accepted signature algorithms and minimum key parameters;
- how `key_id` maps to trusted public-key material;
- key rotation, compromise, expiry, and revocation handling;
- whether multiple approvals or dual control are required for sensitive transitions.

No authority name, public key, signature algorithm, or external provider is selected by this proposal.

## 7. Versioning, freshness, and durable anti-rollback

`snapshot_version` is a monotonically increasing positive integer for the exact authority/registry/scope tuple. The consumer must compare it strictly against a trusted high-water mark for that tuple. Equal versions are replay; lower versions are rollback. A changed review cycle is a distinct scope and must not accidentally reset trust state without an explicit migration policy.

The high-water mark must be stored durably and atomically with a durable acceptance record. The local `SQLiteHighWaterMarkStore.accept_snapshot()` primitive advances the high-water mark and inserts a pending acceptance-journal event in one SQLite transaction; downstream consumers must apply pending events idempotently and acknowledge only after durable application. This primitive is not currently wired to the Supernova engine and does not make a separate downstream StateStore transaction atomic. If validation succeeds but persistence fails, the consumer must not report durable acceptance. Concurrent consumers must use compare-and-swap, a transaction, or an equivalent serialization mechanism so two snapshots cannot both advance from the same old value in an unsafe order. Storage rollback, restore from backup, and disaster recovery need an explicit trust procedure.

Freshness is a separate caller policy based on `generated_at`, clock assumptions, and a maximum age. A fresh snapshot is not proof of latestness. Detecting a newer snapshot and receiving remote revocations require a separate trusted service or distribution mechanism.

## 8. Consumer behavior and fail-closed rules

A future Supernova consumer may treat a record as approved only if all envelope, scope, digest, signature, freshness, lineage, schema, and anti-rollback checks succeed and the record maps to an explicit accepted governance decision. Missing records, unknown companies, duplicate company identities, unknown statuses, malformed lineage, invalid signatures, unknown authorities, stale snapshots, missing high-water state, or failed persistence must not create approval.

Validation success does **not** authorize:

- trading, broker submission, or execution;
- automatic portfolio transition or replacement;
- computing or trusting scores that are absent from the authoritative record;
- promoting every research candidate to approved status;
- bypassing Supernova's normal governance review or portfolio transition process.

A successful registry validation is one input to governance readiness, not a trade signal.

## 9. Required tests before implementation can be accepted

The future implementation should include at least:

- valid D-049 baseline snapshot with exact expected scope;
- candidate-universe-only company is not approved;
- missing, duplicate, unknown, or ambiguous company identity;
- wrong review cycle or wrong scope;
- digest tampering and signature tampering;
- unknown authority, unknown key ID, unsupported algorithm, key rotation/revocation;
- duplicate JSON keys and canonicalization edge cases;
- stale/future timestamps and timezone errors;
- equal-version replay, lower-version rollback, malformed version/high-water mark;
- missing high-water state, concurrent update, and persistence failure;
- malformed or cyclic supersession lineage;
- unknown status and unsupported schema version;
- proof that acceptance does not invoke execution or alter portfolio state.

## 10. Approval gates and non-goals

Before code integration, obtain explicit decisions for the record owner, company identity model, review-cycle naming, schema/version policy, canonicalization/signature format, trusted key distribution, freshness thresholds, high-water storage/transaction boundary, and revocation/latestness requirements. Then implement the schema and verifier tests in isolation before connecting any Framework consumer.

This proposal does not modify Core Runtime, any Framework, configuration, investment policy, provider selection, or `config/moon.yaml`. Moon ADM remains inactive with `active_strategies: []`. No network service, database, key management infrastructure, or broker integration is implemented here.

## 11. Isolated schema validator implementation status (2026-10-11)

An isolated local schema validator now exists at
`src/orion/frameworks/supernova/registry_contract.py`. It checks the proposed
envelope and record field sets, exact Supernova domain scope and review cycle,
positive integer versions, timezone-aware timestamps, explicit `approved`
status, uppercase ticker-shaped identifiers, digest string shape, source-decision
references, and duplicate company identities. Focused negative tests cover these
checks.

This implementation is **schema validation only**. It does not calculate or
verify the snapshot `content_digest`, verify signatures, establish authority/key
trust, enforce freshness or lineage, persist a high-water mark, or connect to the
Supernova engine. The fixture signature and authority values in tests are
placeholders and are not cryptographic evidence. The module's docstring and
API explicitly require the generic trust contract to be invoked separately
before any future consumer relies on a snapshot. This change does not approve
the proposal for production use.

## Local validator composition (implemented; not a runtime integration)

`validate_trusted_approved_company_snapshot()` composes the generic authoritative
snapshot checks with the Supernova-specific schema and predecessor-lineage checks.
It requires caller-supplied trusted authorities, a signature verifier, a timezone-aware
clock, freshness bounds, the expected review cycle, and the last accepted version.

The generic validator's decision-record lineage check is disabled only for this call,
because Supernova records have a different schema; the Supernova-specific predecessor
chain is checked after the generic digest, authority, signature, scope, freshness, and
anti-rollback checks. Other callers retain the generic lineage check by default.

This function is a local contract adapter, not a production integration. It does not
persist or atomically advance the high-water mark. Callers must persist the accepted
version durably and atomically with their own state transition; on persistence failure,
the snapshot must not be treated as committed. The supplied verifier must perform real
cryptographic verification against an independently configured key trust policy. Tests
use a fixture verifier and do not establish production authenticity. No Supernova engine,
Core Runtime, broker, or investment decision path calls this adapter.

### Durable high-water mark prototype

A file-backed SQLite compare-and-swap primitive is available in `data.registry_high_water_store.SQLiteHighWaterMarkStore`. It isolates state by authority, registry type, and canonical scope, rejects stale concurrent writers, and retains state across store recreation. It is a local implementation only and is not connected to the Supernova engine. In particular, the SQLite commit is not automatically atomic with any separate application StateStore or acceptance record; production integration must specify and test a recoverable transaction protocol before claiming end-to-end atomic acceptance.

#### Reference consumer concurrency and recovery

The local SQLite acceptance journal supports worker claims with expiring leases. Claims are atomic, a lease token is required for acknowledgement, and later snapshot versions in a scope remain blocked while an earlier version is pending. Expired work can be reclaimed after a process failure. This limits concurrent duplicate processing but does not make arbitrary external side effects exactly-once; downstream materialization must be idempotent and should use a durable event ID or equivalent idempotency key. This proposal does not authorize wiring the consumer into Supernova or changing Core Runtime lifecycle behavior.
