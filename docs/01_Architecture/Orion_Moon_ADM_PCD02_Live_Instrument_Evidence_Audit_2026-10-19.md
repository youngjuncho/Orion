# Orion Moon/ADM PCD-02 Live Instrument Evidence Audit

- Date: 2026-10-19
- Status: Partial inherited evidence; PCD-02 remains OPEN
- Scope: Exact live coverage and response identity for Alpha Vantage monthly adjusted data for VTI, VEU, and SGOV
- Code changes: None
- Live API calls during this audit: None

## 1. Decision

Do not close PCD-02 based on the evidence currently available. The inherited live-check record reports successful individual responses for VTI and SGOV, while the sequential three-symbol check failed at VEU with the sanitized diagnostic `API_RATE_LIMIT`. The original response payload and independent provider-side cause have not been established in this audit. The diagnostic therefore must not be reinterpreted as proof that VEU is unsupported, that the API key is invalid, or that a specific quota was exceeded.

The current evidence is partial: VTI and SGOV individual successes do not demonstrate that the required all-symbol batch succeeds, and they do not establish the current response contract for VEU.

## 2. Current implementation contract

`src/data/alphavantage.py` configures the exact symbols `VTI`, `VEU`, and `SGOV` and the endpoint `TIME_SERIES_MONTHLY_ADJUSTED`. It checks provider-reported symbol identity, the monthly adjusted series, valid positive adjusted-close values, unique month keys, and at least 13 observations per symbol. The provider fails the entire load on a required-symbol failure and performs no retries, caching, or persistence.

`scripts/check_alpha_vantage_live_contract.py` is an explicit live-check entry point. It requires `ORION_ALPHA_VANTAGE_API_KEY`, performs the provider load, and prints sanitized coverage metadata only after the complete batch has passed its checks. The offline tests use deterministic fixtures; they establish software behavior, not live instrument coverage.

## 3. Evidence status

| Evidence item | Status | What it supports | What it does not support |
|---|---|---|---|
| VTI individual live response | Previously reported success; not reproduced here | A prior request reportedly returned a valid-looking monthly response | Current live availability, full-batch success, price accuracy, or adjustment suitability |
| SGOV individual live response | Previously reported success; not reproduced here | A prior request reportedly returned a valid-looking monthly response | Current live availability, full-batch success, price accuracy, or adjustment suitability |
| VEU in the all-symbol run | Failed with `API_RATE_LIMIT` in inherited record | The sequential all-symbol run did not complete | Root cause, permanent coverage failure, or key/plan diagnosis |
| Fixture tests | Available in repository | Deterministic response parsing, identity checks, malformed-data rejection, and fail-closed behavior | Live endpoint coverage or provider data semantics |
| Official endpoint documentation review | Recorded separately | Monthly adjusted endpoint shape and general endpoint description | Account-specific access or actual symbol-level availability |

## 4. Safe next verification

When a live check is explicitly authorized and API capacity is available:

1. Confirm `ORION_ALPHA_VANTAGE_API_KEY` is configured in the intended environment without printing or copying the key.
2. Run the existing full contract script once; do not add retries or bypass VEU.
3. Record only sanitized exit status, diagnostic code, symbol, response observation counts, and date coverage. Do not store raw payloads or credentials in the bundle.
4. If the run fails at VEU again, investigate the cause using provider-side evidence or a separately approved diagnostic plan. Do not infer a root cause from the generic notice classification alone.
5. Close PCD-02 only after all three exact identities and minimum history requirements pass in one complete run and the evidence is reviewed. PCD-02 closure alone does not close PCD-04 through PCD-07, approve adjusted-price suitability, authorize signal assembly, or activate ADM.

No live call was made for this audit because the available task context does not establish that fresh provider capacity and credentials are ready. Do not interpret this documentation update as a live verification.

## 5. Related gates remain unchanged

- PCD-01/PCD-02 provider and instrument gates remain open until their evidence is approved.
- D-028 continues to specify adjusted-price-based total-return measurement, but provider-specific suitability remains a separate question.
- D-058's seven-calendar-day freshness limit does not validate symbol identity or adjustment semantics.
- PCD-15/PCD-16 remain blocked; `config/moon.yaml` must retain `active_strategies: []` and ADM signal assembly remains fail-closed.

## Related documents

- `Moon_ADM_Provider_Contract_Decision_Register.md`
- `Moon_ADM_Alpha_Vantage_Endpoint_Entitlement_Audit.md`
- `Moon_ADM_Provider_Contract_Readiness_Audit.md`
- `Orion_Moon_ADM_Provider_Response_Contract_Verification.md`
- `Moon_ADM_Latest_Git_Audit_2026-10-18.md`
