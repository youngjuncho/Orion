# Moon ADM Readiness Maximum-Age Contract Audit

Date: 2026-10-15
Bundle: v14

## Finding

The readiness construction helper already rejects `max_age_days` above the approved D-058 limit of seven calendar days. However, `ADMDataAssemblyReadiness` is also a directly constructible frozen dataclass. Before this change, its own constructor accepted a value above seven if the remaining nested freshness objects were constructed consistently. That allowed a readiness object to describe a freshness policy wider than the approved monthly ADM limit.

## Change

`ADMDataAssemblyReadiness.__post_init__` now independently rejects `max_age_days > ADM_MONTHLY_MAX_OBSERVATION_AGE_DAYS`, using the same D-058 seven-day limit as the construction helper. A regression test attempts to replace a valid readiness object's limit with eight days and verifies rejection.

## Scope and safety

- No comparison operator, asset-selection rule, return calculation, or strategy activation was changed.
- `config/moon.yaml` retains `active_strategies: []`.
- PCD-15 authoritative governance binding remains unimplemented; `ADMMonthlyDataAssessment.signal_assembly_ready` remains fail-closed.
- No live Alpha Vantage calls were made.

## Validation

The full test suite passed: `445 passed in 3.97s` using the available Python 3.13.5 runtime. This does not replace the required post-merge test run in the project's designated Python 3.12.13 environment.
