# Orion Moon ADM PCD-05 — Calendar Dependency Validation Plan

Date: 2026-10-19  
Status: Evaluation plan only; no dependency adopted  
Scope: Offline dependency/environment audit and proposed validation sequence

## 1. Findings from the current repository

### Dependency declaration

- `requirements.txt` currently contains only unpinned `pyyaml` and `pytest` entries.
- There is no `pyproject.toml`, lockfile, or dedicated constraints file at the repository root in this bundle.
- `docs/07_Coding/Dependency_Management.md` requires dependencies to be explicit, minimal, replaceable, reviewed for maintenance/documentation/community/license, pinned, and tested with the full suite before upgrades.
- `docs/06_Implementation/Environment_Setup.md` is still marked Draft and says Python 3.10+ / conda environment `orion`; its environment description predates the separately designated Windows Conda Python 3.12.13 validation target.

### Architectural fit

- `src/orion/frameworks/moon/adm_calendar.py` already defines a provider-neutral `ADMMarketCalendar` protocol and a fail-closed month-end resolver.
- A third-party calendar library should be implemented as an adapter behind that protocol; framework/domain code should not depend directly on the package API.
- The prototype is not connected to the ADM runtime. No package should be added to `requirements.txt` until package behavior and installation are validated.

## 2. Candidate and current decision

`exchange_calendars` remains the first candidate for evaluation because the immediate need is trading-session membership and month-end cutoff resolution. This is a test candidate, not an approved dependency or calendar-source decision. `pandas_market_calendars` remains an alternative if the required scope expands to exchange schedules, open/close times, breaks, or interruption handling.

No version is pinned in this plan. Before selecting one, record the exact release, Python support metadata, runtime dependency set, license, release notes, and any relevant calendar corrections from the upstream release/tag metadata. Do not infer compatibility solely from a broad Python version classifier.

## 3. Validation sequence

### Gate A — reproducible environment inventory

On the designated Windows machine, activate the actual `orion` Conda environment and record:

```powershell
conda activate orion
python -c "import sys; print(sys.version); print(sys.executable)"
python -m pip --version
python -m pip freeze
```

Confirm whether the designated interpreter is Python 3.12.13 and capture the existing environment before changing it. Do not use the global Python or another environment as a substitute.

### Gate B — isolated installability probe

Create a disposable Conda environment using the designated Python version, then install the exact candidate release there (not into the working `orion` environment). Record the complete resolver output and installed transitive versions. Verify import, version reporting, and representative calendar construction for the required exchange identifiers. If the candidate cannot install cleanly, stop and document the failure; do not silently loosen pins or substitute a different package.

### Gate C — deterministic contract tests

Using fixture-driven tests and no network calls, verify:

1. Month-end that is a session returns that date.
2. Month-end that is not a session resolves to the immediately preceding session.
3. A missing calendar, unknown calendar identifier, or calendar lookup exception fails closed.
4. Instrument-to-calendar mappings are explicit and reviewed; listing venue names are not treated as package identifiers without verified mapping.
5. VTI, VEU, and SGOV test dates cover ordinary sessions, weekends, known exchange holidays, and the SGOV listing-venue transition period where relevant.
6. Calendar package adapter behavior conforms to the existing `ADMMarketCalendar` protocol without importing package types into domain/runtime code.

Expected dates must come from reviewed calendar evidence or fixed approved fixtures, not from the package under test alone; otherwise tests would only reproduce the package's own assumptions.

### Gate D — compatibility and regression

In the disposable environment, run the focused calendar/data tests and then the complete test suite. Separately run the repository UTF-8 policy check. Record interpreter path, package versions, commands, exit codes, and counts. Do not claim Windows/Conda validation until it has actually run there.

### Gate E — adoption review

Only after Gates A–D pass, propose a separate change that pins the chosen package version and justified transitive constraints, adds a small adapter plus focused tests, and documents calendar identifier mapping and data-update responsibility. Review the dependency diff and full test evidence before merging. Keep package adoption and runtime wiring as separate decisions.

## 4. Non-goals and safety constraints

- No package installation or dependency-file modification is performed by this document.
- No live market-data API calls are authorized or required.
- No authoritative calendar provider, asset-calendar mapping, freshness policy, timezone policy, or prior-year comparison cutoff is approved here.
- No ADM runtime integration or strategy activation is authorized.
- `config/moon.yaml` must retain `active_strategies: []`; signal assembly remains fail-closed.
- PCD-05 and PCD-06 remain open. PCD-15/PCD-16 remain blocking; G-01 remains `DEFERRED — BLOCKING`.

## 5. Acceptance record template

For any later execution, attach an evidence record with: date/time and operator; OS; Conda environment name; `sys.version` and `sys.executable`; exact candidate and transitive package versions; install command/output; focused/full test commands and results; UTF-8 check result; calendar fixtures and their independent source; known limitations; and explicit pass/fail for each gate. Missing evidence means the gate remains unpassed.
