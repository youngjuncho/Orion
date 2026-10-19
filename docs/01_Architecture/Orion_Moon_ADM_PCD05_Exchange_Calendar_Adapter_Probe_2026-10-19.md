# Orion Moon ADM PCD-05 — exchange_calendars Adapter Probe

Date: 2026-10-19  
Status: **isolated validation probe; not runtime integration or adoption approval**

## Evidence received from designated Windows environment

The user created a separate Conda environment using Python 3.12.13 and installed `exchange-calendars==4.13.2`. `pip check` reported `No broken requirements found`; imports succeeded for `exchange_calendars==4.13.2`, `pandas==3.0.6`, and `numpy==2.5.4`. The installed package's `XNYS` calendar returned the expected results for 2026-10-30 (session), 2026-10-31 (non-session), 2026-11-26 (Thanksgiving; non-session), 2026-11-27 (session), and 2026-11-30 (session).

Conda also emitted `conda-libmamba-solver (No module named 'conda.reporters')` on each invocation. Environment creation and the package probe nevertheless completed. This is a separate Conda installation/plugin warning and has not been repaired as part of this work.

## Added probe

`scripts/validate_adm_exchange_calendar.py` implements a tiny local adapter for the existing `ADMMarketCalendar` protocol. It uses `XNYS`, exposes the installed package version as the calendar version, and delegates session checks to `exchange_calendars`. It then exercises the existing resolver for May, October, and November 2026.

Run from the repository root using the isolated audit interpreter:

```bash
conda run --prefix "$HOME/anaconda3/envs/orion-calendar-audit" python scripts/validate_adm_exchange_calendar.py
```

The script adds the repository's `src` directory to `sys.path`, does not install packages, and does not write project files during execution.

## Acceptance checks in the probe

- Known XNYS session/non-session observations match the expected values.
- May 2026 month-end Sunday resolves to Friday 2026-05-29.
- October 2026 month-end Saturday resolves to Friday 2026-10-30.
- November 2026 month-end trading Monday resolves to Monday 2026-11-30.
- The resolved result carries `XNYS` and the installed package version.

## Boundaries and open items

- This probe has been authored but **has not yet been run in the user's Windows environment**. Do not report its assertions as passed until its output is returned.
- `XNYS` is used only as a test fixture; no VTI/VEU/SGOV production mapping is adopted.
- No package dependency is added or pinned in the repository requirements.
- No ADM runtime or signal assembly integration is performed; `config/moon.yaml` must keep `active_strategies: []`.
- Out-of-range behavior, previous-year comparison endpoints, publication timestamps, freshness, timezone conventions, and execution timing remain outside this probe.
- The existing `ADMMarketCalendar` contract and deterministic fixture tests remain unchanged.
- PCD-05/PCD-06 remain open; PCD-15/PCD-16 remain blocking; G-01 remains `DEFERRED — BLOCKING`.
- No live market-data API calls were made.
