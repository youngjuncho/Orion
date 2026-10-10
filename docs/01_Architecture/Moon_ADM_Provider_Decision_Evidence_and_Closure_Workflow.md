# Moon ADM Provider Decision Evidence and Closure Workflow

Version: 1.0
Status: Proposed workflow — no provider approved; D-055 methodology approved
Last Updated: 2026-10-10

## 1. Purpose and authority

This workflow defines the evidence required to move an item in `Moon_ADM_Provider_Contract_Decision_Register.md` from `Open` or `Partially defined` to a governed outcome. It is a process contract, not an approval, and it does not authorize live data access, provider-specific implementation, signal assembly, or strategy activation.

The decision register is an index. The authoritative decision record must live in the applicable governance artifact, identify the authorized decision owner, and link to the evidence. Editing a status label alone does not close a gate.

## 2. Permitted outcomes

Each decision ID must have exactly one current outcome:

- **Open** — required evidence or authorized decision is missing.
- **Partially defined** — a generic engineering behavior exists, but one or more provider-specific or policy-specific questions remain.
- **Approved** — the authorized owner explicitly accepted a defined outcome based on linked evidence.
- **Rejected** — the proposed outcome/provider/contract is explicitly disallowed; the rejection rationale and allowed alternatives or next steps are recorded.
- **Deferred** — an authorized owner explicitly postponed the decision, with reason, review trigger or date where available, and downstream gates left open.

`Not applicable` may be used only with a written rationale and approval from the authority responsible for the affected decision. It must not be used merely to bypass a dependency.

## 3. Required closure record

Every closure or deferral record must include:

1. Decision ID(s) from the register.
2. Outcome and exact scope: provider, instrument, field, timeframe, or policy version covered.
3. Decision authority/owner and decision date.
4. Rationale, assumptions, known limitations, and rejected alternatives where material.
5. Evidence links with version/date: official provider documentation, instrument identifiers, sample payloads, data dictionary, methodology notes, or investment-policy record.
6. Contract changes and deterministic fixture/test references, including negative cases.
7. Dependencies and downstream gates that remain open.
8. Review trigger/date for time-sensitive or changeable terms, such as licensing, provider schema, or API behavior.

A record must not claim evidence that has not been inspected. Where provider documentation is ambiguous, the decision remains open or is explicitly deferred.

## 4. Evidence standards by decision group

### Group A — Provider and identity (PCD-01 to PCD-03)

Required evidence:
- Provider identity, access method, permitted use and relevant usage/licensing constraints.
- Stable instrument identifiers for each canonical symbol; ticker text alone is insufficient where ambiguity exists.
- A deterministic source-to-canonical mapping for every supported field, with unsupported fields rejected explicitly.
- Fixtures for valid mappings, unknown identifiers, unsupported fields, and accidental aliasing.

Exit condition: the source and identity contract is reviewed and approved. No live adapter is implied by fixture success.

### Group B — Price and temporal semantics (PCD-04 to PCD-07)

Required evidence:
- Written adjustment methodology and evidence for the intended total-return proxy; the label `adjusted_close` alone is insufficient.
- Timestamp format, timezone, daily-bar timestamp meaning, session-close meaning, exchange calendar, and evaluation endpoint rules.
- Explicit trailing-period endpoint selection and approved freshness/late-publication behavior.
- Fixtures around month ends, holidays, missing sessions, stale data, and boundary timestamps where applicable.

Exit condition: price meaning and temporal interpretation are approved for the intended use. Engineering defaults do not substitute for these approvals.

### Group C — Data quality, revisions, provenance and operations (PCD-08 to PCD-12)

Required evidence:
- Defined completeness expectations and fail-closed behavior for missing/partial responses.
- Duplicate/conflict identity and deterministic handling rules.
- Revision/correction policy, including whether calculations use current revised history or retrieval-time snapshots.
- Provenance fields sufficient to identify source, requested/returned instrument, retrieval time, adapter version, selected observations, and revision/snapshot identity when available.
- Provider-specific timeout, rate-limit, retry, cache, partial failure and outage behavior, including tests proving failure cannot become a successful-looking dataset.

Exit condition: the relevant quality and operational contracts are specified and fixture-tested. Persistence and scheduling remain separate decisions if not in scope.

### Group D - Investment methodology (PCD-13 to PCD-14)

D-055 approves SGOV as the absolute-momentum benchmark and strict greater-than comparison, with equality false. PCD-13 and PCD-14 are closed for this methodology. Provider measurement semantics remain in Groups B/C, and D-055 does not authorize signal integration or activation.

### Group E — Governance binding and activation boundary (PCD-15 to PCD-16)

Required evidence:
- A verifiable link from implementation configuration to the authoritative decision record; arbitrary caller-supplied text is not sufficient validation.
- End-to-end negative tests showing provider failure, missing/stale observations, invalid provenance, or unverified production data/governance cannot produce an accepted Moon signal.
- A separate activation authorization identifying scope, configuration change, rollback plan, and post-change verification.

Exit condition: all prerequisite decisions are approved and verified. This workflow itself never activates ADM or changes `active_strategies`.

## 5. Dependency and release gates

The following gates are cumulative; a later gate cannot bypass an earlier unresolved dependency:

1. **G1 — Provider identity:** PCD-01 and PCD-02 approved.
2. **G2 — Interpretation contract:** PCD-03 through PCD-07 approved for the proposed use.
3. **G3 — Quality and operations:** PCD-08 through PCD-12 approved to the extent required by the proposed adapter scope.
4. **G4 — Investment policy:** PCD-13 and PCD-14 are approved by D-055; provider/data gates remain separate.
5. **G5 — Governance binding:** PCD-15 implemented and tested against authoritative records.
6. **G6 — Signal integration proposal:** PCD-16 evidence reviewed; explicit activation authorization still required before configuration changes.

A `Deferred` or `Rejected` prerequisite keeps dependent gates closed unless the authoritative owner records a justified dependency change. No gate may be inferred from passing generic adapter tests.

## 6. Change control and re-opening

Re-open the affected decision(s) when provider documentation, API schema, licensing, instrument identity, adjustment methodology, timestamp/calendar behavior, revision behavior, or the approved investment methodology changes. Record the detected change, impact assessment, affected fixtures/tests, and whether live use must be suspended pending review.

A provider adapter version change does not automatically re-approve the provider contract. Conversely, unchanged provider identity does not guarantee that historical data semantics or licensing remain unchanged.

## 7. Closure record template

Use this template for each decision or tightly coupled decision set:

```text
Decision ID(s):
Outcome: Open | Partially defined | Approved | Rejected | Deferred
Scope / exact contract version:
Decision authority / owner:
Decision date:
Rationale and assumptions:
Evidence links and versions:
Known limitations / rejected alternatives:
Contract and test changes:
Dependencies / downstream gates still open:
Review trigger or date:
```

Do not fill `Approved` unless the named authority has made that decision and the linked evidence is available.

## 8. Explicit non-goals

This workflow does not select a provider, approve Yahoo Finance or another source, approve adjusted-price semantics, set freshness thresholds, add network/retry/cache/fallback behavior, implement persistence, activate ADM, or modify Core Runtime. Moon's `active_strategies: []` remains unchanged.

## Related documents

- `Moon_ADM_Provider_Contract_Decision_Register.md`
- `Moon_ADM_Provider_Adapter_Acceptance_Test_Matrix.md`
- `Moon_ADM_Provider_Adapter_Readiness_Review.md`
- `Moon_ADM_Provider_Neutral_Adapter_Contract.md`
- `Moon_ADM_Data_Contract.md`
- `docs/05_Decisions/Decision_Log.md`
