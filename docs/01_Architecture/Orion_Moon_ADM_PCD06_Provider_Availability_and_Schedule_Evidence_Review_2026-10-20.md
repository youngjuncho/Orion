# Orion Moon / ADM — PCD-06 Provider Availability and Schedule Evidence Review

- Date: 2026-10-20
- Status: **PUBLIC DOCUMENTATION REVIEW COMPLETE — request-triggered evaluation selected; no recurring schedule proposed**
- Scope: Determine whether public Alpha Vantage documentation establishes a dependable monthly-bar publication SLA for PCD-06 scheduling.
- No live API calls were made. No credentials were accessed.

## Finding

The official Alpha Vantage API documentation describes `TIME_SERIES_MONTHLY_ADJUSTED` as returning monthly adjusted time series with each month's last trading day as the date label. It documents the required request parameters and response fields, but the reviewed endpoint section does **not** specify a guaranteed publication time after the final trading session, a monthly data-delivery SLA, a revision-finalization time, or a maximum latency for the completed month.

Source: Alpha Vantage official API documentation, `TIME_SERIES_MONTHLY_ADJUSTED` section: https://www.alphavantage.co/documentation/ (reviewed 2026-10-20).

This is a documentation-bound finding only. It does not prove actual delivery behavior for the user's API key, symbols VTI/VEU/SGOV, or any particular month. The prior PCD-02 evidence remains relevant: one three-symbol run failed at VEU with `API_RATE_LIMIT`, cause unknown. No conclusion is drawn about entitlement, quota, or ticker validity.

## Schedule implications

1. Keep `Asia/Seoul` as the approved operational timezone and use an explicit operator evaluation request as the trigger; do not assume a fixed monthly date or wall-clock time.
2. Do not treat a chosen wall-clock time as a provider availability guarantee.
3. A schedule trigger only starts an assessment attempt; all required input, target-selection, calendar, and D-058 freshness checks must pass independently.
4. If data is unavailable or fails validation at the snapshot boundary, fail closed. Do not silently use older bars, invent a grace window, or automatically retry.
5. Preserve the approved manual-reprocessing policy: operator-requested reprocessing is a distinct run with a new run ID and snapshot boundary; all gates rerun.
6. No recurring schedule time/frequency is required under the selected request-triggered model. The request instant is an operational trigger, not a publication-SLA claim.

## Proposed deterministic test cases

- Trigger instants immediately before, at, and after a configured `Asia/Seoul` wall-clock schedule.
- Equivalent UTC representation preserves the same instant and Seoul operational date.
- US DST transition dates do not change the configured Seoul wall-clock time or rely on a fixed Seoul/New York offset.
- Month-end on session, weekend, and exchange holiday; year rollover; leap-year February.
- Required data present at snapshot boundary versus arriving afterward.
- Provider publication timestamp absent: record it as unknown; do not substitute retrieval time.
- Missing/late/stale/malformed/duplicate/future-dated observation blocks assessment.
- Failed/missed run is recorded and not automatically replayed.

## Decision still needed

The user clarified that evaluations should be triggered on the date/time an evaluation is requested, since requests may happen at month-end, early next month, or other times and are not guaranteed to occur in the morning. Do not recommend a recurring monthly schedule. The request instant is only a trigger; assessment still fails closed when required data is not ready. If evidence about actual account/symbol delivery timing is needed, it requires explicit authorization for a limited live provider contract check; this review did not make such requests.

## Non-actions and governance

- No live Alpha Vantage API requests or credential access.
- No source, test, dependency, scheduler, runtime, or configuration changes.
- No signal assembly, strategy activation, or execution behavior.
- `config/moon.yaml` must retain `active_strategies: []`.
- G-01 remains `DEFERRED — BLOCKING`; PCD-04 adjusted-price semantics, PCD-02 live provider contract, and PCD-06 R5 remain open.
