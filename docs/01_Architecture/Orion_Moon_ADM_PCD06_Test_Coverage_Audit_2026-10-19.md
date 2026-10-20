# Orion Moon / ADM — PCD-06 Deterministic Test-Coverage Audit

**Date:** 2026-10-19  
**Scope:** Existing tests for monthly target construction, prior-observation selection, and observation-age validation.  
**Disposition:** Source/test inspection only. PCD-06 remains open for operational scheduling and signal/execution date mapping.

## Executive result

The current engineering helpers have useful deterministic unit coverage. The tests cover completed-month selection, a leap-year February boundary, exclusion of the in-progress month on its first day, selection of the latest observation on or before a calendar target (including a Saturday target), rejection when no prior observation exists, date-only timestamp format, and explicit observation-age checks.

This coverage validates the helpers' documented behavior; it does not establish an exchange calendar, provider publication SLA, timezone convention, signal effective date, or executable trading date. Those are policy/operational contract questions and should not be guessed in tests.

## Existing coverage confirmed

| Behavior | Evidence in tests | Assessment |
|---|---|---|
| Latest completed calendar month | `test_monthly_target_dates_use_the_latest_completed_month` | Covered |
| Leap-year February | `test_monthly_target_dates_align_leap_month_ends` | Covered for 2024-02-29 / 2025-02-28 |
| `as_of_date` on first day of month | `test_monthly_target_dates_exclude_current_month_on_first_day` | Covered |
| Latest prior observation; never select future bar | `test_prior_observation_selector_uses_latest_available_date_on_or_before_target` | Covered, including Saturday target |
| No observation at/before target | `test_prior_observation_selector_rejects_no_observation_before_target` | Covered |
| Observation timestamp is date-only ISO | `test_prior_observation_selector_rejects_timestamp_formats_outside_date_contract` | Covered |
| Explicit age calculation and stale rejection | freshness tests in `test_adm_data.py` | Covered in basic cases |
| Seven-day ceiling | tests reject a configured maximum greater than seven days | Covered as a configuration bound |

## Remaining test questions (do not silently convert into policy)

1. **Age boundary:** Add exact seven-calendar-day acceptance and eight-day rejection fixtures for both current and trailing observations if not already covered elsewhere. The configured limit and observed age are different things; both sides need explicit boundary assertions.
2. **Month/year rollover:** Add deterministic target-date fixtures around January 1 and December/January transitions to make the calendar arithmetic contract explicit.
3. **Target versus bar date:** Keep tests demonstrating that a calendar month-end may be a weekend and that the selected monthly bar can be earlier. Do not claim that this alone validates an exchange trading calendar.
4. **Late publication / missing completed-month bar:** Requires an approved policy for when the evaluation is considered ready. Until then, test only the existing fail-closed behavior; do not invent a grace period.
5. **Timezone and signal/execution mapping:** No implementation or tests should be added until the authoritative timezone, signal effective date, and next-trading-day rule are approved.
6. **Provider revisions and point-in-time history:** These are PCD-04 evidence questions, not calendar-helper unit tests.

## Recommended next test-only slice

After the relevant contract is approved, add small table-driven fixtures for:

- `as_of_date` at year rollover;
- current and trailing observation ages exactly at the allowed boundary and one day beyond it;
- a target on a weekend with the prior observation on Friday;
- missing/stale completed-month data producing a non-ready outcome rather than a signal.

Do not add a holiday calendar or signal/execution scheduler as part of this slice without a decision defining its authority and semantics.

## Gate disposition

- **PCD-06:** Deterministic helper coverage exists; operational date/calendar contract remains open.
- **PCD-04:** Adjusted-price semantics and empirical parity remain open, as recorded in the separate PCD-04/PCD-06 evidence-boundary audit.
- **PCD-15 / PCD-16:** Unchanged and blocking. No helper result or passing unit test authorizes signal assembly.
- `config/moon.yaml` must retain `active_strategies: []`.

## Verification boundary

This audit inspected existing source and tests only. No source, test, configuration, provider, or runtime behavior was changed. No live API requests were made.


## Addendum — as-of boundary helper implementation (2026-10-20)

A standalone pure helper was added in `src/orion/frameworks/moon/adm_asof.py` with deterministic unit tests in `tests/orion/frameworks/moon/test_adm_asof.py`. Covered cases include inclusive date-only target converted to an exclusive next-day `Asia/Seoul` boundary, UTC normalization, exact timestamp semantics, equivalent offset representations, explicit handling of naive timestamps, malformed input rejection, exclusive availability comparison, and leap-day boundary arithmetic.

Focused ADM calendar/data/as-of/adapter tests at v57: 122 passed. Full workspace test suite at v57: 527 passed. UTF-8 policy check passed (410 text files). This did not implement the complete PCD-06 matrix and did not connect helpers to ADM runtime, providers, scheduling, signal assembly, or execution.

## Addendum — D-058 boundary and real-calendar integration tests (2026-10-20, v58)

Added an explicit D-058 acceptance test showing that a current observation exactly seven calendar days old passes when the configured maximum is seven. The existing eight-day configuration test continues to reject a threshold above the approved cap. Added optional real-package integration tests for XNYS month-end/weekend cutoffs, November month-end session handling, February leap/non-leap cases, and sessions/non-sessions around US DST transition dates. These integration tests run only when `exchange-calendars==4.13.2` is installed; they were skipped in the current workspace because it has version 4.13.1.

Verification in the current workspace: focused tests 123 passed, 4 skipped; full suite 528 passed, 4 skipped; UTF-8 policy check passed (501 text files). The skipped real-package tests must be run in the user's isolated `orion-calendar-audit` environment. No live API calls were made, and no scheduler/runtime wiring was added.
