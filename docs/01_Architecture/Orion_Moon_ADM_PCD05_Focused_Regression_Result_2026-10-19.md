# Orion Moon ADM PCD-05 Focused Regression Result — 2026-10-19

## Scope

This record captures the user-reported focused test run in the designated Windows Conda `orion` environment after the isolated `exchange-calendars==4.13.2` probe. The focused run does not install or import the candidate package as a repository dependency; it tests the existing ADM calendar prototype and ADM data tests in the original environment.

## Environment and command

Interpreter: `C:\Users\yj44c\anaconda3\envs\orion\python.exe`

Python version previously confirmed in this environment: 3.12.13 (Anaconda, Windows 64-bit).

Command:

```bash
"$HOME/anaconda3/envs/orion/python.exe" -m pytest -q -p no:cacheprovider tests/orion/frameworks/moon/test_adm_calendar.py tests/orion/frameworks/moon/test_adm_data.py
```

## User-reported result

```text
92 passed in 0.99s
```

Result: all 92 focused tests passed.

## Interpretation and limits

- Existing focused ADM calendar and data tests pass in the original `orion` environment.
- The isolated `exchange-calendars==4.13.2` session/cutoff probe also passed in the separate `orion-calendar-audit` environment, as recorded in the preceding probe result document.
- This is not a full-suite regression run.
- The candidate package is not added to `requirements.txt`, is not installed into the original `orion` environment, and is not wired into ADM runtime.
- XNYS checks do not approve instrument-to-calendar mappings for VTI, VEU, or SGOV.
- PCD-05/PCD-06 remain open. The common-run multi-market policy and operational freshness/time semantics remain unresolved.
- G-01 remains `DEFERRED — BLOCKING`; PCD-15/PCD-16 remain open/blocking; `config/moon.yaml` must retain `active_strategies: []`; signal assembly remains fail-closed.
- No live market-data API calls were made.
