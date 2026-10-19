# Orion Moon / ADM — PCD-05 Multi-Market Policy Proposal

- Date: 2026-10-19
- Status: **Proposal for user review; not an approved governance decision**
- Scope: Resolve the multi-market policy question before calendar implementation

## 1. Context

The approved evaluation-date convention is: use calendar month-end when it is a trading day; otherwise use the immediately preceding trading day. The existing implementation does not yet resolve the cutoff against an authoritative exchange calendar. This document proposes the multi-market behavior only; it does not select a production calendar provider or library.

## 2. Recommended policy

**Use an instrument-specific market calendar for each instrument, under one portfolio evaluation run.** A shared run ID and run timestamp provide orchestration identity, but do not force every instrument to share one market's trading calendar.

For each instrument:

1. Resolve the evaluation cutoff as calendar month-end if that instrument's market is open; otherwise use that market's immediately preceding trading session.
2. Select observations no later than that instrument-specific cutoff.
3. Independently validate observation availability and freshness. Calendar membership does not prove the provider had published the observation by a given time.
4. Resolve the prior-year comparison endpoint using the same market calendar and the corresponding prior-year month.
5. Record the calendar identifier/version, cutoff session date, selected observation timestamp, and data-availability evidence when available.

## 3. Portfolio readiness recommendation

For the initial fail-closed MVP, **do not finalize the portfolio-level ADM signal assembly unless every required instrument's data and calendar resolution pass validation**. An instrument that is missing, stale, unresolved, or not yet available should block finalization of the run rather than silently allowing a partial allocation.

This is a conservative proposal, not a confirmed business rule. A future decision could explicitly allow per-strategy partial results, but that requires defined downstream consensus behavior and must not be inferred here.

## 4. Why not one portfolio-wide market calendar?

A single calendar can incorrectly treat a US market holiday as a Korean market holiday (or vice versa). It can also conceal stale observations when one market has traded and another has not. Per-instrument calendars make market-session eligibility explicit; the common run ID still allows results to be grouped and audited together.

## 5. Required decisions before implementation

- Approve or reject instrument-specific calendars.
- Approve or reject all-required-instruments readiness as the initial fail-closed behavior.
- Select authoritative calendar source/package and supported exchange identifiers.
- Approve dependency pinning, calendar version recording, updates, and failure behavior.
- Define how provider publication/availability time is evidenced; do not treat session date as publication time.
- Confirm how instruments without a reliable exchange mapping are handled (recommended: fail closed).

## 6. Implementation constraints

- Do not add a runtime dependency or implement calendar lookup until the source and supported markets are approved.
- Keep evaluation cutoff, bar timestamp, provider availability time, run timestamp, signal timestamp, and execution timestamp distinct.
- Never substitute a later observation for an unavailable cutoff observation.
- Preserve the D-058 freshness check independently of calendar resolution.
- No source/test/config/dependency changes are made by this proposal.

## 7. Governance status

This proposal does not close PCD-05, PCD-06, PCD-04, PCD-02, PCD-15, or PCD-16. G-01 remains `DEFERRED — BLOCKING`; `config/moon.yaml` must retain `active_strategies: []`; signal assembly remains fail-closed. No live provider requests were made and no tests were run for this documentation-only step.
