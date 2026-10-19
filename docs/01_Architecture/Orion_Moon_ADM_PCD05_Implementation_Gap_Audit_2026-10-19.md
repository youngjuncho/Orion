# Orion Moon / ADM — PCD-05 Implementation Gap Audit

- Date: 2026-10-19
- Status: Evidence audit; implementation change not authorized by this document
- Scope: Compare the user-confirmed month-end evaluation-date convention with the existing ADM date helper and observation selector.

## Finding

The approved convention is:

- If calendar month-end is a trading day for the relevant instrument/market, use that date as the evaluation cutoff.
- Otherwise, use the immediately preceding trading day for that instrument/market.
- This evaluation cutoff is not an execution timestamp.

The current implementation in `src/orion/frameworks/moon/adm_data.py` does not yet compute that convention. `derive_adm_monthly_target_dates(as_of_date)` constructs the previous **calendar** month-end and the prior-year corresponding **calendar** month-end. `select_adm_price_observations_on_or_before(...)` then chooses the latest observation on or before those calendar targets. The selected observation can therefore be a prior trading-day bar, but the helper does not establish that the target itself is the approved market-specific evaluation cutoff.

This difference matters because the approved policy refers to a market trading calendar, whereas the current helper intentionally has no calendar dependency. A passing prior-observation selection test is not evidence that the new user-confirmed cutoff rule has been implemented.

## What is established

1. The date helper excludes the calendar month containing `as_of_date`.
2. It derives calendar month-end targets, including the prior-year comparison target.
3. The observation selector uses only observations dated on or before each supplied target.
4. Freshness, valid trading-bar identity, actual publication time, and execution timing are separate gates.

## What remains undefined

Before changing runtime behavior, the following implementation contract must be specified:

- Authoritative trading-calendar source and versioning/update policy.
- Whether the evaluation cutoff is instrument-specific or based on one portfolio-wide calendar when instruments trade in different markets.
- Behavior when the calendar is unavailable or does not contain a date.
- Whether the trailing comparison endpoint uses the same market-specific month-end rule independently for the prior year.
- How date-only provider observations relate to the actual close and publication/availability timestamp.

## Recommended next engineering slice

After those inputs are approved, introduce a calendar abstraction that resolves the evaluation cutoff separately from the raw calendar month-end target. Add deterministic tests for month-end on a trading day, weekends, one or more consecutive holidays, year boundaries, leap-year February, and instruments with different market calendars. Keep the existing as-of observation constraint and D-058 freshness gate independently tested.

Do not infer a calendar package, data vendor, timezone, or multi-market policy from common practice. Do not silently change the current helper's meaning under its existing `last-completed-month-end-v1` policy ID; a behavior change should have an explicit policy/version transition and regression coverage.

## Governance and runtime consequence

This audit does not close PCD-05, PCD-06, PCD-04, PCD-02, PCD-15, or PCD-16. It does not authorize signal assembly or execution. G-01 remains `DEFERRED — BLOCKING`; `config/moon.yaml` must retain `active_strategies: []`; Moon/ADM remains fail-closed.

## Verification boundary

Documentation/source inspection only. No source code, tests, runtime defaults, or strategy configuration changed. No live provider requests were made. The full test suite was not run for this documentation-only step.
