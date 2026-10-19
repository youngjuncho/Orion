# Orion Moon / ADM — PCD-05 Calendar Package Comparison

- Date: 2026-10-19
- Status: Evidence review and recommendation only; no package selected or installed
- Related: `Orion_Moon_ADM_PCD05_Calendar_Interface_Prototype_2026-10-19.md`, `Orion_Moon_ADM_PCD05_Instrument_Calendar_Mapping_Audit_2026-10-19.md`

## Decision context

The approved evaluation-date convention is: use calendar month-end when it is a trading session; otherwise use the immediately preceding trading session. The current `ADMMarketCalendar` protocol is deliberately provider-neutral and is not wired into the ADM pipeline. This document compares candidate libraries for that interface; it does not approve production use or resolve PCD-05/PCD-06.

## Candidate comparison

| Criterion | `exchange_calendars` | `pandas_market_calendars` |
|---|---|---|
| Primary API | Exchange session calendars, `get_calendar`, `is_session` and session schedules | Trading schedules and market open/close times, via `get_calendar` and `schedule` |
| Required US session calendar | `XNYS` is available; `XNAS`/`ARCX` are aliases mapped to `XNYS` in its current calendar registry | `XNYS` is available directly; it also exposes calendars mirrored from `exchange_calendars` |
| XKRX evidence | The release history records an XKRX 2026 calendar update in 4.13.1 | Its documentation demonstrates an `XKRX` schedule; its mirrored calendars inherit the installed underlying calendar data |
| Runtime data refresh | Calendar rules ship with the installed package; updating means a reviewed package/data update | Calendar rules ship with the installed package; it does not fetch live exchange hours at runtime |
| Dependency footprint | Current published metadata declares NumPy, Pandas, `pyluach`, `toolz`, `tzdata`, and `korean_lunar_calendar` | Depends on Pandas and `exchange_calendars`; adds a higher-level schedule API rather than eliminating the underlying calendar dependency |
| Fit for current requirement | Better fit for a small adapter whose only required primitive is session membership | Useful if Orion later needs market schedules, open/close times, breaks, or interruptions |

## Evidence sources

- `exchange_calendars` PyPI metadata and API examples: https://pypi.org/project/exchange_calendars/
- `exchange_calendars` release history, including the XKRX 2026 update in 4.13.1: https://github.com/gerrymanoim/exchange_calendars/releases
- `exchange_calendars` current calendar registry and aliases: https://github.com/gerrymanoim/exchange_calendars/blob/master/exchange_calendars/calendar_utils.py
- `exchange_calendars` current dependency metadata: https://github.com/gerrymanoim/exchange_calendars/blob/master/pyproject.toml
- `pandas_market_calendars` calendar data/update behavior and API: https://pandas-market-calendars.readthedocs.io/en/latest/
- `pandas_market_calendars` calendar status: https://pandas-market-calendars.readthedocs.io/en/stable/calendars.html

These are public project documentation/release sources, not independent validation of every historical session. The alias mapping in a package is a library implementation detail and must not be treated as proof that two venues have identical historical sessions in all periods.

## Recommendation

For the current PCD-05 scope, prefer evaluating `exchange_calendars` first behind the existing `ADMMarketCalendar` protocol. The reason is narrow fit: ADM needs deterministic session membership and month-end resolution, not intraday market-hours calculations. `pandas_market_calendars` remains a reasonable alternative if the scope expands to explicit schedules or market-hour operations, but it depends on `exchange_calendars` for mirrored calendars and therefore does not avoid the underlying calendar-data dependency.

This is a technical recommendation only. It is **not** approval to install a dependency, pin a version, bind a calendar code to an asset, or wire a provider into ADM.

## Required checks before any adoption

1. Confirm the repository's dependency policy and designated Windows Conda Python 3.12.13 compatibility in the actual project environment.
2. Select and record a reviewed exact package version and transitive dependency lock/constraints; do not use an unbounded version.
3. Confirm the actual package registry includes the selected identifiers in that exact version, including `XNYS` and `XKRX` if required.
4. Compare representative historical sessions and exceptional closures against an authoritative exchange calendar for the chosen date range. Package release notes alone are insufficient.
5. Define how to handle calendar coverage limits, ad-hoc closures, corrections, and reproducibility when a package upgrade changes historical data.
6. Keep calendar-session status distinct from price-data availability, adjusted-price parity, publication time, and freshness.
7. Add provider adapter tests using deterministic fixtures and package-backed tests only after dependency approval. Keep fail-closed behavior on unknown identifiers, out-of-range dates, or calendar errors.
8. Do not connect the adapter to the ADM signal path until the remaining PCD-05/PCD-06 decisions and governance requirements are resolved.

## Status invariants

- PCD-05 and PCD-06 remain open.
- Multi-market/per-instrument calendar handling remains a proposal, not an approved policy.
- No package was installed and no runtime code/configuration was changed in this step.
- `config/moon.yaml` must keep `active_strategies: []`.
- G-01 remains `DEFERRED — BLOCKING`; PCD-15/PCD-16 remain blocking.
- No live market-data API calls were made.
