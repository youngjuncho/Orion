# Orion Moon / ADM PCD-05 — Calendar Dependency Adoption Decision

- Date: 2026-10-19
- Status: **APPROVED — implementation isolated from ADM runtime**
- Depends on: `Orion_Moon_ADM_PCD05_US_ETF_Calendar_Mapping_Decision_Brief_2026-10-19.md`
- Scope: Add a pinned calendar dependency and a provider adapter behind the existing interface; **does not connect the adapter to the ADM signal/runtime path**.

## 1. Evidence already available

- The mapping policy has been explicitly approved: `VTI -> XNYS`, `VEU -> XNYS`, `SGOV -> XNYS`, only for month-end evaluation-cutoff session resolution.
- The user reports that an isolated Windows Conda environment with Python 3.12.13 and `exchange-calendars==4.13.2` installed successfully; `pip check` reported no broken requirements.
- The user ran `scripts/validate_adm_calendar_alias_mapping.py`: package version was 4.13.2; `XNYS` and `ARCX` canonicalized to the same XNYS calendar object; all listed sample-session expectations passed.
- The user reports 92 focused tests and 497 full-suite tests passing on the current repository snapshot.
- The package's `ARCX` alias is package behavior only. It is not an independent authoritative attestation of full historical NYSE Arca/NYSE schedule equivalence.

## 2. Proposed minimal change

If separately approved:

1. Add `exchange-calendars==4.13.2` to the repository's explicit dependency declaration, subject to a final review of the exact installed dependency metadata and the repository's current dependency-management convention.
2. Implement a small infrastructure adapter for `ADMMarketCalendar` in a separate module. The adapter must expose stable `calendar_id` and `calendar_version` values and normalize package session results to Python `bool`.
3. Keep `src/orion/frameworks/moon/adm_calendar.py` provider-neutral. It must not import `exchange_calendars` directly.
4. Add deterministic tests for missing/unknown calendar, import/lookup exceptions, invalid return values, month-end session/non-session, and the approved instrument map. Tests must not make network calls.
5. Keep the adapter unused by the ADM runtime in this change. No default calendar factory, implicit fallback, strategy activation, or runtime wiring.
6. Run focused tests, full test suite, and `scripts/check_utf8.py` in the designated Windows `orion` environment and record the exact results.

## 3. Fail-closed contract

- Missing dependency, unexpected dependency version, unknown calendar ID, construction failure, session lookup failure, invalid result type, or no valid session within the month must stop cutoff resolution with an explicit error.
- No weekday-only fallback, silent substitution, stale cached calendar, or default-to-XNYS behavior is permitted when the requested mapping cannot be resolved.
- The resolved cutoff must carry calendar ID and package version in its result/audit record.
- Calendar membership must remain separate from market-data availability, freshness, adjusted-price correctness, prior-year endpoint alignment, signal timestamp, and execution timestamp.
- The mapping table must be explicit and reviewed. The adapter must not infer package IDs from provider ticker metadata.

## 4. Dependency and maintenance considerations

- Pin the direct dependency exactly for reproducibility; do not manually pin transitive dependencies unless resolver evidence demonstrates a need and the constraints are documented.
- Record the actual installed versions from the isolated environment rather than treating a successful import as a complete dependency audit.
- Calendar data may be corrected between releases. Dependency upgrades therefore require release-note review, fixture review, focused tests, full regression, and an explicit change record.
- The current isolated install does not authorize installing this package into the main `orion` environment.

## 5. Explicit exclusions

This proposal does not authorize:

- wiring the adapter into the ADM runtime or signal assembly;
- changing `config/moon.yaml` (`active_strategies` must remain `[]`);
- closing PCD-06 freshness/time semantics, PCD-04 adjusted-price semantics, PCD-02 provider contract uncertainty, PCD-15/PCD-16 registry binding, or G-01 (`DEFERRED — BLOCKING`);
- any live market-data API calls;
- claiming independent official full-schedule equivalence for `ARCX` and `XNYS`.

## 6. Approval and implementation record

The user explicitly approved the narrow change on 2026-10-19:

> Add the pinned `exchange-calendars==4.13.2` dependency and a tested, fail-closed adapter behind `ADMMarketCalendar`, without connecting it to ADM runtime or signal assembly.

Implementation is isolated in `src/orion/frameworks/moon/adm_exchange_calendar.py`. The dependency is declared in `requirements.txt`. The adapter only permits the approved canonical `XNYS` calendar and explicit ticker map (`VTI`, `VEU`, `SGOV`); it checks the exact installed package version and raises `ADMCalendarResolutionError` on missing dependency, version mismatch, unknown mapping/calendar, construction failure, invalid input/result, or lookup failure.

This approval does not authorize ADM runtime wiring, strategy activation, live data calls, or closure of any other open/blocking governance item. Test and UTF-8 results must be recorded separately after execution in the designated Windows environment.
