# Orion Moon / ADM PCD-05 — Full Regression Test Result

**Date:** 2026-10-19  
**Bundle:** v44  
**Evidence type:** User-reported command output from designated Windows Conda environment

## Command

```bash
"$HOME/anaconda3/envs/orion/python.exe" -m pytest -q -p no:cacheprovider
```

## Result

```text
497 passed in 10.50s
```

All 497 tests in the existing Orion `orion` environment passed. The previously reported focused ADM calendar/data tests also passed (92 passed in 0.99s); those tests are part of the full suite and are not an additional set of 92 unique tests.

## Evidence boundaries

- This supports that the current repository test suite passes in the user's existing Windows 11 Conda Python 3.12.13 `orion` environment.
- `exchange-calendars==4.13.2` was installed and exercised only in the separate `orion-calendar-audit` environment. It was **not** installed into the existing `orion` environment and is not added to repository dependency declarations.
- The isolated XNYS session/cutoff probe passed, but this does not approve any instrument-to-calendar mapping, historical session equivalence, provider data freshness, execution timing, or production runtime integration.
- No source, test, configuration, or dependency code was changed for this step. No live market-data API calls were made.
- `config/moon.yaml` must continue to retain `active_strategies: []`. G-01 remains `DEFERRED — BLOCKING`; PCD-15/PCD-16 remain blocking and PCD-05/PCD-06 remain open.

## Next gate

Before adopting a calendar dependency, separately review and approve instrument-calendar mappings (including the SGOV listing-venue change), calendar coverage/version pinning, dependency compatibility policy, and operational handling for unsupported dates and calendar errors. Runtime integration must remain fail-closed and is not authorized by this test result.
