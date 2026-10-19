# Orion Moon / ADM — PCD-05 Calendar Source and Multi-Market Options

- Date: 2026-10-19
- Status: **Options analysis; no calendar source or multi-market policy approved**
- Scope: Engineering decision inputs for implementing the user-confirmed month-end evaluation cutoff

## 1. Fixed rule

For an instrument/market, use calendar month-end if it is a trading day; otherwise use the immediately preceding trading day. The evaluation cutoff is not an execution timestamp. Observations after the cutoff are forbidden, and required data must be available and pass readiness checks before a signal can be finalized.

## 2. Calendar-source options

| Option | Advantages | Risks / limitations | Assessment |
|---|---|---|---|
| A. Add a third-party exchange-calendar package | Provides named exchange sessions and holiday rules; deterministic offline tests are possible for supported markets | Adds dependency and version/update policy; exchange coverage and historical corrections must be checked; package calendar is not proof of provider publication time | Viable after explicit dependency and market coverage approval |
| B. Provider-supplied trading calendar | May align with provider's bars and symbol coverage | Availability and semantics are provider-specific; can be incomplete or change without an independent reference; current Alpha Vantage contract does not establish an authoritative calendar contract | Not currently evidenced |
| C. Maintain an Orion-owned holiday/session table | Explicit and reviewable; no runtime dependency | Ongoing maintenance burden; easy to miss special closures, emergency closures, and calendar corrections; requires ownership and release process | Not recommended without a designated maintainer and update SLA |
| D. Inject a calendar interface, but do not select a production implementation yet | Keeps ADM logic independent; allows deterministic test calendars; avoids guessing a vendor or package | Does not make production cutoff calculation ready until an implementation is selected and validated | **Recommended next engineering boundary** |

## 3. Multi-market policy options

| Option | Behavior | Consequence |
|---|---|---|
| Instrument-specific calendar | Resolve the cutoff independently using each instrument's market calendar | Correctly models local sessions, but different instruments can have different evaluation dates for one portfolio run |
| One portfolio-wide calendar | Resolve a single cutoff for all instruments | Operationally simpler, but may use stale prior bars for some markets or mishandle a market that traded when the chosen calendar was closed |
| Portfolio-wide run date plus per-instrument as-of cutoff | A common run identifier/date is retained, while each instrument's eligible observation cutoff is resolved against its own calendar | Separates orchestration from market-session eligibility; still needs explicit portfolio synchronization and missing/stale-data policy |

**Recommendation for discussion, not an approved decision:** prefer instrument-specific market calendars under one portfolio evaluation run, with a common run ID and an explicit rule for whether all instruments must be ready before any signal is finalized. This avoids silently treating a US holiday as a Korean-market holiday or vice versa. Do not implement this recommendation until approved.

## 4. Required decision inputs

Before runtime implementation, approve:

1. Calendar source/library and supported exchange identifiers for each ADM instrument.
2. Dependency pinning, calendar version recording, update cadence, and behavior when a calendar cannot be loaded.
3. Whether evaluation uses instrument-specific calendars or one portfolio-wide calendar.
4. Whether prior-year comparison endpoints independently resolve the corresponding month's last trading day using the same market calendar.
5. Portfolio behavior when one market's data is missing, stale, or not yet published: fail the whole run or withhold only the affected strategy result. Do not silently substitute a later observation.
6. The distinction between session date, bar timestamp, publication/availability timestamp, evaluation run timestamp, signal timestamp, and execution timestamp.

## 5. Implementation guardrails

- First add a narrow calendar protocol/interface and deterministic fake-calendar tests only after the API contract is approved.
- Do not add a package dependency merely because it is common in financial Python projects.
- Do not change `derive_adm_monthly_target_dates()` behavior under the existing `last-completed-month-end-v1` policy ID without an explicit version transition and regression tests.
- Preserve the as-of observation constraint and D-058 freshness gate as independent checks.
- Calendar membership alone does not prove data publication or availability.
- Calendar resolution failure must fail closed; never fall back silently to calendar month-end or latest available observation.

## 6. Governance status

This options analysis does not close PCD-05, PCD-06, PCD-04, PCD-02, PCD-15, or PCD-16. No authoritative governance binding is implemented. G-01 remains `DEFERRED — BLOCKING`; `config/moon.yaml` must retain `active_strategies: []`; signal assembly remains fail-closed.

## 7. Verification boundary

Documentation-only analysis. No source code, tests, runtime defaults, dependencies, or strategy configuration changed. No live provider requests were made. The full test suite was not run for this step.
