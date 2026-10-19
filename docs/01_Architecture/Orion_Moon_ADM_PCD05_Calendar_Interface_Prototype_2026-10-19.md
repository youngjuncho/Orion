# Orion Moon / ADM — PCD-05 Calendar Interface Prototype

- Date: 2026-10-19
- Status: **Prototype only; no production calendar source selected**
- Scope: Deterministic, injected calendar interface and month-end cutoff resolver

## Implemented

`src/orion/frameworks/moon/adm_calendar.py` defines:

- `ADMMarketCalendar`: `calendar_id`, `calendar_version`, and `is_session(date)` contract.
- `resolve_adm_month_end_cutoff(year, month, calendar=...)`: use calendar month-end when it is a session; otherwise walk backward to the immediately preceding session in that month.
- `ADMResolvedEvaluationCutoff`: immutable result recording the calendar month-end, resolved cutoff, calendar identifier, and version.
- Fail-closed validation for invalid input, missing calendar identity/version, lookup exceptions, non-boolean lookup results, and no session in the requested month.

Deterministic tests use a fixture calendar and do not require a live market calendar or network access.

## Explicit non-goals

- No production calendar provider or library is selected.
- The resolver is **not wired into** `derive_adm_monthly_target_dates()` or the ADM signal pipeline.
- It does not resolve the prior-year comparison endpoint, provider publication time, data freshness, timezone, signal validity, or execution time.
- It does not approve the proposed per-instrument multi-market policy or all-required-instruments readiness rule.
- It does not alter `config/moon.yaml`, activate strategies, or bypass PCD-15/PCD-16 governance gates.

## Verification

Focused command:

```text
python -m pytest -q -p no:cacheprovider tests/orion/frameworks/moon/test_adm_calendar.py tests/orion/frameworks/moon/test_adm_data.py
```

Result in the available container runtime: **92 passed in 1.45s**.

The complete test suite and designated Windows Conda Python 3.12.13 were not run in this step. No live API calls were made.

## Remaining decisions

1. Approve/reject the instrument-specific calendar policy and portfolio-level fail-closed recommendation.
2. Select authoritative calendar source/package and supported exchange identifiers.
3. Decide dependency pinning, calendar-version recording, update policy, and outage behavior.
4. Define evidence for provider publication/availability time.
5. Define how the prior-year comparison cutoff is resolved with the same market calendar.

PCD-05 and PCD-06 remain open. PCD-02 and PCD-04 remain open. PCD-15/PCD-16 remain blocking; G-01 remains `DEFERRED — BLOCKING`; `config/moon.yaml` must retain `active_strategies: []`; signal assembly remains fail-closed.
