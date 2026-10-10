# Moon ADM Provider Adapter Acceptance Test Matrix

Version: 1.0  
Status: Implemented — provider-neutral boundary acceptance; provider approval remains open  
Last Updated: 2026-10-10

## Purpose

This matrix defines the minimum acceptance evidence for the current provider-neutral adapter boundary and the additional gates required before a concrete provider can be approved. Passing these tests does not certify that a provider's prices, timestamps, calendars, or adjustment methodology are financially suitable.

## Acceptance matrix

| ID | Risk / contract | Acceptance evidence | Current result | Boundary / remaining work |
|---|---|---|---|---|
| A-01 | Implicit symbol or field mapping | Canonical symbol and field are preserved; `close` is not silently rewritten to `adjusted_close` | Covered by adapter acceptance test | Concrete provider must define and review explicit source-to-canonical mapping |
| A-02 | Timestamp/timezone reinterpretation | Timestamp and batch `as_of` labels pass through unchanged | Covered by adapter acceptance test | No timestamp parsing, timezone normalization, exchange-calendar validation, or date meaning approval |
| A-03 | Missing required asset/period | Moon relative-momentum calculation rejects a dataset lacking VEU or required endpoints | Covered by adapter acceptance test and existing ADM data tests | Adapter alone cannot know a strategy's required universe; freshness limits and missing-bar policy remain explicit inputs / open policy |
| A-04 | Duplicate or revised observations | Duplicate canonical identity fails closed, including two revision-tagged records for the same symbol/field/timestamp | Covered by adapter acceptance test | Historical correction selection, snapshot retention, and revision precedence are not implemented |
| A-05 | Provenance and reproducibility | Source and supplied string metadata are preserved; no missing provenance is fabricated | Covered by adapter acceptance test | A concrete provider must supply stable instrument IDs, field semantics, retrieval time, adapter version, and revision/snapshot identity where available |
| A-06 | Provider failure / partial signal path | Fetch exception propagates; guarded caller does not invoke downstream signal consumer | Covered as a boundary usage test | No end-to-end Runtime-to-Moon provider integration exists or is authorized |
| A-07 | Delayed/stale observations | Existing ADM freshness gates can reject observations using a caller-supplied maximum age | Existing ADM data tests | Threshold, calendar-aware age, timezone and source-delay policy are not approved by this matrix |
| A-08 | Invalid batch/value shape | Missing envelope fields, invalid required fields, unsupported values, and duplicate identities fail closed | Covered by Step 40 adapter tests | Provider-specific HTTP/API response validation and retry behavior are out of scope |

## Acceptance interpretation

- **Pass** means the current generic contract behaves as documented for deterministic fixtures.
- **Not validated** means the generic adapter intentionally lacks the provider context or approved policy needed to make that determination.
- A structurally valid `MarketDataSet` is not proof of fresh data, correct instrument identity, total-return adjusted prices, valid trading-calendar alignment, or governance approval.
- Provenance metadata is retained only when supplied. The generic adapter does not invent provider fields, normalize timestamps, select revisions, or infer an adjusted-price definition.
- A failed data load must be treated as a failed load by its caller. The test demonstrates the fail-closed calling pattern; it does not claim an existing production signal orchestration path.

## Exit criteria for a concrete provider adapter

Before provider-specific implementation or activation, governance must close and document:

1. Provider selection and source approval.
2. Stable instrument identity and explicit field mapping.
3. Adjusted-price methodology and suitability for D-028.
4. Timestamp meaning, timezone, trading calendar, evaluation-date and trailing-period selection.
5. Missing, delayed, stale, duplicate, conflicting and revised observation behavior.
6. Provenance and reproducibility requirements.
7. Timeout, rate-limit, retry, partial-response and provider-outage behavior.
8. D-055 comparison behavior plus independently closed source/data gates and signal-assembly review.

## Explicit non-goals

This step does not add a live provider, network access, retry/cache/fallback logic, provider precedence, persistent snapshots, new investment logic, `ADMSignalInput` assembly, strategy activation, or Core Runtime changes. Moon's `active_strategies` configuration remains unchanged.

## Related documents

- `Moon_ADM_Provider_Neutral_Adapter_Contract.md`
- `Moon_ADM_Provider_Adapter_Readiness_Review.md`
- `Moon_ADM_Provider_Contract_Decision_Register.md`
- `Moon_ADM_Data_Contract.md`
- `Orion_Data_Pipeline.md`
