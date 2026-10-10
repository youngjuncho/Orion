# Moon ADM Authoritative Decision Record Schema & Validator

Version: 1.0  
Status: Local structural validator implemented; authoritative governance integration not implemented  
Date: 2026-10-09  
Baseline: Step 45 — Provider Governance Gate Specification

## 1. Purpose and limits

This contract defines a versioned decision record and a fail-closed local validator for fixture-backed governance tests. It does **not** establish who is authorized to approve a decision, authenticate a record, read a trusted registry, grant provider access, approve investment policy, or activate Moon ADM.

`src/data/governance.py` implements structural validation, content-digest verification, exact requested-scope checks, dependency resolution, and rejection of unapproved, invalidated, superseded, unknown, malformed, or cyclic records. The registry is passed by the caller; its authority is not cryptographically or operationally established by this module. Therefore G5 remains closed.

## 2. Required record fields

| Field | Requirement |
|---|---|
| `decision_id` | Stable non-empty identifier, e.g. PCD-01 |
| `record_version` | Non-empty version identifier |
| `status` | `Open`, `Partially defined`, `Approved`, `Rejected`, or `Deferred` |
| `scope` | Non-empty mapping identifying exact provider/use/instruments/fields as applicable |
| `authority` | `owner` and `basis`; descriptive only until trusted authority binding exists |
| `decided_at` | ISO-8601 timestamp with timezone offset |
| `evidence` | List of evidence objects with `ref`, `version`, and `evidence_date` |
| `rationale` | Non-empty decision rationale and limitations |
| `dependencies` | List of decision IDs that must resolve and be approved |
| `contract_changes` | List of linked contract/change references |
| `test_refs` | List of deterministic verification references |
| `content_digest` | SHA-256 of canonical JSON for all record fields except `content_digest` itself |
| `invalidated` | Optional boolean; when true, use is rejected |
| `superseded_by` | Optional replacement identifier; when present, use is rejected |

An `Approved` record must have at least one evidence entry. Digest verification detects accidental or unapproved content edits relative to the supplied digest; it does not prove authorship, authority, or evidence truth.

## 3. Python API

- `canonical_digest(record)` computes the canonical SHA-256 digest.
- `validate_decision_record(record)` validates schema, timestamp, evidence, collection types, and digest.
- `resolve_approved_decisions(registry, required_ids, requested_scope)` resolves required IDs and dependencies from a caller-supplied registry snapshot. Every required record must be Approved, valid, not invalidated/superseded, and match each requested scope key exactly.
- `DecisionRecordError` is raised on every rejected path. Callers must treat it as a blocked gate, not downgrade it to a warning.

The resolver returns records in deterministic decision-ID order. It detects missing IDs, registry key/record ID mismatch, dependency cycles, and non-approved dependencies. This is a local contract utility, not a runtime policy decision or Core Runtime integration.

## 4. Example fixture

```python
record = {
    "decision_id": "PCD-TEST-01",
    "record_version": "1",
    "status": "Approved",
    "scope": {"provider": "fixture", "use": "test"},
    "authority": {"owner": "fixture-owner", "basis": "test only"},
    "decided_at": "2026-10-09T12:00:00Z",
    "evidence": [{"ref": "fixture://evidence", "version": "1", "evidence_date": "2026-10-09"}],
    "rationale": "Fixture-only validation; not investment approval.",
    "dependencies": [],
    "contract_changes": ["fixture-contract"],
    "test_refs": ["tests/data/test_governance.py"],
    "content_digest": "<computed with canonical_digest>",
}
```

This is illustrative fixture data only. It must not be copied as an actual approval.

## 5. Fail-closed rules

Reject a record or resolution when any required field is missing or malformed, the timestamp has no timezone, the digest mismatches, an Approved record lacks evidence, a required ID is unknown, registry key and record ID differ, the status is not Approved, the record is invalidated/superseded, the requested scope does not match, a dependency is missing/unapproved, or a dependency cycle exists.

A digest must be recalculated after any content change. Recalculating a digest is not approval; it merely creates a self-consistent record. Production use needs an independently trusted registry/signature or equivalent authority mechanism and a governed process for versioning, revocation, expiry, and audit history.

## 6. Gate mapping and current state

- G1–G4 remain closed because provider, data semantics, operational policy, and investment methodology are not approved.
- G5 remains closed: local schema and resolution behavior exist, but authoritative registry identity, authorized signer/owner verification, durable audit history, and runtime binding do not.
- G6 remains closed: no actual Runtime-to-Moon end-to-end negative-path integration acceptance.
- G7 remains closed: no separate strategy activation authorization.

`config/moon.yaml` must continue to retain `active_strategies: []`. This implementation does not change Core Runtime or create a provider-specific adapter.

## 7. Tests

`tests/data/test_governance.py` covers valid fixture records, missing fields, digest tampering, timezone-less timestamps, missing evidence, unknown IDs, scope mismatch, non-approved status, invalidation/supersession, dependency failures/cycles, and deterministic valid dependency resolution.

Passing these tests establishes only the tested local validation behavior. It does not establish governance authority or approve any provider/investment decision.

## Related documents

- `Moon_ADM_Provider_Governance_Gate_Specification.md`
- `Moon_ADM_Provider_Contract_Decision_Register.md`
- `Moon_ADM_Provider_Decision_Evidence_and_Closure_Workflow.md`
- `Moon_ADM_Provider_Contract_Readiness_Audit.md`
