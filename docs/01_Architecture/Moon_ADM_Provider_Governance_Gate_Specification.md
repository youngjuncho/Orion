# Moon ADM Provider Governance Gate Specification

Version: 1.0
Status: Specification — no provider, signal integration, or activation approved; D-055 methodology approved
Date: 2026-10-10
Baseline: Step 44 — Provider Contract Readiness Audit

## 1. Purpose

Define explicit, cumulative gates for moving from the provider-neutral adapter to any provider-specific use, selected-observation calculation, Moon signal integration, and eventual strategy activation. This document specifies required evidence and behavior; it does not implement a gate evaluator or constitute approval.

The current implementation must continue to treat caller-supplied approval references as attestations, not authoritative validation. A gate is not open merely because a document says `Approved`, a reference string is non-empty, or generic tests pass.

## 2. Gate model

| Gate | Name | Minimum prerequisite | Permitted scope after approval | Does not authorize |
|---|---|---|---|---|
| G0 | Provider-neutral boundary | Existing generic contract and fixture tests | Generic normalization and deterministic fixture testing | Network access or provider selection |
| G1 | Provider and instrument identity | PCD-01, PCD-02 | Provider-specific contract/mapping design within the approved scope | Treating prices as valid ADM inputs |
| G2 | Observation interpretation | PCD-03–PCD-07 | Provider-specific observation parsing and approved temporal/price interpretation | Production quality or signal generation by itself |
| G3 | Quality, provenance, operations | PCD-08–PCD-12, scoped to the intended deployment | Implementation of explicitly approved failure, revision, provenance and operational behaviors | Choosing investment methodology |
| G4 | Investment methodology | PCD-13 and PCD-14 approved by D-055 | D-055 SGOV/strict-greater-than comparison behavior | Provider access or strategy activation by itself |
| G5 | Governance binding | PCD-15 plus a tested authoritative-record resolver | Runtime/configuration may verify decision IDs, versions, scope and status against an authoritative record | Signal integration or activation by itself |
| G6 | Signal integration acceptance | G1–G5 prerequisites; PCD-16 evidence; end-to-end negative tests | A separately reviewed integration proposal | Enabling ADM in configuration |
| G7 | Strategy activation | Separate explicit activation authorization after G6 review | Only the exact approved scope and configuration change | Broader provider use or unrelated strategy activation |

G0 describes the current provider-neutral engineering boundary. G1–G7 are not currently passed. Gates are cumulative; later gates cannot waive earlier ones.

## 3. Required approval record contract

A decision can satisfy a gate only if an authoritative, versioned record contains all applicable fields:

- stable decision ID matching PCD-01–PCD-16;
- outcome and exact scope, including provider, instruments, fields, period and intended use as applicable;
- authorized decision owner/authority and decision timestamp;
- immutable or versioned evidence references and evidence version/date;
- rationale, limitations, review trigger/expiry where relevant;
- dependent decision IDs and downstream gates;
- linked contract changes and deterministic positive/negative tests;
- record version or content digest so a later edit cannot silently reuse prior approval.

A future resolver must verify that the record exists, is authoritative, is in an accepted status, matches the requested scope, satisfies dependencies, and has not been superseded or invalidated. Missing, malformed, unknown, out-of-scope, expired, or conflicting records must fail closed. No resolver is implemented by this specification.

## 4. Decision-to-gate mapping

- **G1:** PCD-01 and PCD-02 must be explicitly approved. Rejection or deferral keeps G1 closed.
- **G2:** PCD-03–PCD-07 must be approved for the exact data use. Generic field names do not prove financial semantics.
- **G3:** PCD-08–PCD-12 must be approved to the scope being deployed. An explicit, evidence-backed `Not applicable` decision is required for any intentionally omitted operational behavior; it cannot be inferred from absence.
- **G4:** PCD-13 and PCD-14 are approved by D-055. Their implementation does not approve provider semantics, data quality, or strategy activation.
- **G5:** PCD-15 requires an implemented resolver and tests for unknown IDs, wrong versions, scope mismatch, revoked/superseded records, missing dependencies, and valid approvals.
- **G6:** PCD-16 requires actual orchestration-path tests showing that provider exceptions, malformed/partial data, missing or stale observations, invalid provenance, and unavailable/unapproved policy cannot yield a valid accepted Moon signal.
- **G7:** Requires a separate activation record naming the exact strategy, configuration diff, effective time, rollback steps, verification checks, and owner. G6 is necessary but not sufficient.

## 5. Failure and invalidation semantics

The following conditions close or re-close the affected gate:

1. Any required decision is Open, Partially defined, Deferred, Rejected, missing, superseded, expired, or not authoritative.
2. A required evidence link cannot be resolved or no longer supports the approved claim.
3. Provider instrument identifiers, schema, price adjustment methodology, calendar/timestamp semantics, revision behavior, usage terms, or relevant operational behavior changes.
4. The running adapter/configuration version is outside the scope recorded in the approval.
5. Required tests fail or an end-to-end negative path can produce a success-shaped result.

On invalidation, downstream use must be suspended or remain disabled pending review. The required operational suspension mechanism is not implemented here; do not claim runtime enforcement until it is built and tested.

## 6. Minimum acceptance test families before G6

- Approval resolver: valid record; unknown record; malformed record; stale/superseded version; scope mismatch; missing dependency; rejected/deferred status.
- Provider contract: explicit mapping, unsupported field rejection, stable instrument identity, adjustment semantics, temporal/calendar boundaries.
- Data quality: missing symbols/fields/sessions, partial batches, duplicate/conflicting records, stale and delayed publication, corrected history.
- Provenance/reproducibility: required fields, selected observation identity, adapter/contract version, repeat-run determinism within the approved revision policy.
- Orchestration: inject each failure into the actual runtime-to-Moon path and assert no accepted signal/state transition/event is produced from invalid inputs.
- Activation: configuration remains disabled absent G7 authorization; exact approved activation change and rollback are verified in a separate review.

Passing tests establishes only the tested contract and fixture behavior. It does not independently approve a decision or provider.

## 7. Current gate status

| Gate | Status | Reason |
|---|---|---|
| G0 | Available for generic fixture use | Provider-neutral adapter exists; existing suite is not provider certification |
| G1 | Closed | Provider/use and stable instrument identity are not approved |
| G2 | Closed | Price semantics and temporal contract are not approved |
| G3 | Closed | Provider-specific quality, revision, provenance and operations decisions remain open |
| G4 | Methodology approved by D-055 | Provider/data gates and authoritative runtime binding remain open |
| G5 | Closed | Local schema/digest/dependency validator exists, but trusted authoritative registry and runtime binding are not implemented |
| G6 | Closed | No approved live provider and no end-to-end Runtime-to-Moon fail-closed integration evidence |
| G7 | Closed | No activation authorization; `config/moon.yaml` keeps `active_strategies: []` |

## 8. Explicit non-goals

This specification does not choose a provider, approve any adjusted-price series, select a configured defensive holding, set freshness thresholds, add networking/retry/cache/fallback/persistence/scheduling, assemble `ADMSignalInput`, activate ADM, or modify Core Runtime. Moon's `active_strategies: []` must remain unchanged unless a separate, authorized activation decision is made and verified.

## Related documents

- `Moon_ADM_Authoritative_Decision_Record_Schema_and_Validator.md`

- `Moon_ADM_Provider_Contract_Decision_Register.md`
- `Moon_ADM_Provider_Decision_Evidence_and_Closure_Workflow.md`
- `Moon_ADM_Provider_Contract_Readiness_Audit.md`
- `Moon_ADM_Provider_Adapter_Acceptance_Test_Matrix.md`
- `Moon_ADM_Provider_Neutral_Adapter_Contract.md`
- `docs/05_Decisions/Decision_Log.md`
