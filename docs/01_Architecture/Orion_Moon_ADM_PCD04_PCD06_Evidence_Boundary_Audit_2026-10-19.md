# Orion Moon / ADM — PCD-04 and PCD-06 Evidence-Boundary Audit

**Date:** 2026-10-19  
**Scope:** Current repository evidence for adjusted-price semantics (PCD-04) and monthly evaluation target construction (PCD-06).  
**Disposition:** Both remain open. This is a documentation/source-inspection audit, not a policy approval or production-readiness decision.

## Executive result

The repository contains a deliberately bounded engineering implementation for monthly target dates and prior-observation selection. It does not establish that Alpha Vantage adjusted close is a provider-certified point-in-time total-return series, nor does it establish the operational signal date / next-trading-day execution mapping. No source code or strategy behavior was changed in this audit.

## PCD-04 — adjusted-price semantics

### Evidence found

- D-028 defines adjusted-price-based total-return measurement as ADM's calculation basis.
- D-057 maps Alpha Vantage `5. adjusted close` to canonical `adjusted_close` and excludes the separate monthly dividend field from the ADM calculation.
- The provider decision register records that provider materials describe split and cash-dividend adjustments, while exact adjustment-factor/reinvestment convention, empirical history parity, and revision schedule remain unverified.
- The provider adapter maps the named field and validates its response structure; mapping and validation do not independently prove economic semantics or history parity.

### Remaining blocker

No accepted reference series, documented parity tolerance/window, or approved interpretation of the provider's adjustment/reinvestment convention was found in the inspected decision register and workflow documents. Consequently, `adjusted_close` may be used only as the currently selected D-028 research proxy; do not describe it as verified point-in-time total return or use this audit to authorize a signal.

### Closure evidence required

1. Retain provider documentation supporting split/cash-dividend adjustment claims.
2. Specify the intended economic meaning and limitations of the adjusted series, including reinvestment and retrospective-revision behavior to the extent evidence permits.
3. Define an accepted comparison/reference series and deterministic empirical parity procedure, including date coverage, tolerances, and treatment of provider revisions.
4. Record the decision and scope explicitly. If exact semantics cannot be established, preserve the proxy-only limitation rather than asserting stronger guarantees.

## PCD-06 — evaluation endpoint and calendar

### Evidence found

- `derive_adm_monthly_target_dates(as_of_date)` excludes the calendar month containing `as_of_date`, uses the previous calendar month's final date as the current target, and uses the corresponding prior-year calendar month-end as the trailing target.
- `select_adm_price_observations_on_or_before(...)` selects the latest observation at or before each target and rejects missing targets or a pair resolving to the same date.
- The selector's own docstring explicitly states it does not prove that a selected observation is a valid trading-day bar and does not enforce maximum age; those checks are separate.
- PCD-05/06 documents still leave signal-date and next-trading-day execution mapping unresolved. A target date is a calendar boundary, while provider observations are labeled by the month's final trading day; these concepts must not be conflated.

### Remaining blocker

The helper is deterministic but does not define an operational scheduler, timezone, exchange-calendar source, publication-time SLA, or the date on which a signal is considered effective and executable. The seven-calendar-day selected-observation age gate (D-058) is a separate rule and does not close these questions. A successful target/observation selection is not signal authorization.

### Closure evidence required

1. Approve the authoritative evaluation-date/timezone convention.
2. Define the signal effective date and next-trading-day execution mapping, including weekends, exchange holidays, late provider publication, and unavailable/stale data.
3. Add deterministic fixtures for month boundaries, leap years, holidays, late publication, and boundary-age cases once the contract is approved.
4. Keep signal assembly blocked until PCD-15/PCD-16 and all other required gates are independently satisfied.

## Gate disposition

| Gate | Result in this audit | Runtime consequence |
|---|---|---|
| PCD-04 | Open — proxy mapping exists; semantics/parity not proven | No verified point-in-time total-return claim; signal remains blocked |
| PCD-06 | Partially specified engineering helper; operational date mapping open | Target selection does not authorize signal or execution |
| PCD-15 / PCD-16 | Unchanged, open/blocking under the current deferred-governance decision | Signal assembly remains fail-closed |

## Verification boundary

This audit was based on repository source and documentation inspection only. No live provider requests were made. No source code, tests, runtime defaults, or `config/moon.yaml` activation settings were changed. `active_strategies: []` must remain unchanged.
