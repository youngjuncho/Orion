# Orion Moon / ADM PCD-05 — US ETF Calendar Mapping Decision Brief

- Date: 2026-10-19
- Status: **APPROVED — mapping policy only; runtime integration not approved**
- Approval recorded: 2026-10-19, explicit user confirmation in Orion project conversation (“넵”) following presentation of the exact mapping policy.
- Candidate package: `exchange-calendars==4.13.2`
- Scope: Evaluation-cutoff session calendar only; not signal, provider-data, or execution semantics

## Proposed mapping

| Instrument | Listing evidence in existing audit | Proposed calendar | Status |
|---|---|---|---|
| VTI | Vanguard product page and SEC prospectus identify NYSE Arca | `XNYS` | **Approved** |
| VEU | Vanguard product page identifies NYSE Arca | `XNYS` | **Approved** |
| SGOV | SEC-hosted supplement says primary listing changes from NYSE Arca to NYSE on/around 2026-02-23 | `XNYS` | **Approved** |

## Technical evidence

1. On the user's Windows Conda Python 3.12.13 isolated environment, `exchange-calendars==4.13.2` installed successfully and `pip check` reported no broken requirements.
2. The adapter probe passed the sampled XNYS session checks and month-end cutoffs (May 2026: May 29; October 2026: October 30; November 2026: November 30).
3. Existing Orion focused tests passed: 92; full regression suite passed: 497.
4. Upstream package calendar dispatch code lists `ARCX` as an alias of `XNYS`. This is evidence of the library's own canonicalization policy, not an independent exchange-authority attestation that the venues' complete historical schedules are identical.
5. Added `scripts/validate_adm_calendar_alias_mapping.py` to verify the installed 4.13.2 alias behavior and sample session results in the isolated environment. The user ran it in the isolated Windows Conda environment and reported: `exchange-calendars: 4.13.2`; `resolve_alias(XNYS): XNYS`; `resolve_alias(ARCX): XNYS`; both identifiers resolved to the same XNYS calendar object; sampled session checks for 2026-02-16, 2026-02-20, 2026-02-21, 2026-02-23, and 2026-02-27 all matched expectations. Result: package alias and sample-session checks passed. Limitation: this verifies package alias behavior and sampled dates only, not independent official schedule equivalence.

## Rationale and boundaries

For this ADM use case, the calendar is proposed to select the latest eligible US session at or before calendar month-end. The current candidate implementation treats NYSE Arca's `ARCX` code as an alias of `XNYS`, and the listed ETFs are all US-listed. A single `XNYS` mapping is therefore operationally plausible and simpler than time-dependent SGOV mapping.

However, this is a **policy choice**, not a proof that all exchange-specific exceptional closures are identical. If Orion requires exact venue-specific historical schedules, the package alias is insufficient evidence and a source that models ARCX independently would be required.

Calendar membership does not establish:
- provider publication/availability time or freshness;
- monthly-bar date semantics or adjusted-price correctness;
- prior-year comparison endpoint policy;
- signal timestamp or execution timestamp;
- live-trading readiness.

## Proposed fail-closed behavior

- If the pinned package/version or required calendar cannot be loaded, block cutoff resolution.
- If session lookup fails or returns invalid data, block cutoff resolution; never fall back to weekday arithmetic.
- Record calendar ID and package version with the resolved cutoff.
- Do not use the mapping to infer data freshness or provider completeness.

## Approved decision

The user explicitly approved this exact policy on 2026-10-19:

- `VTI -> XNYS`
- `VEU -> XNYS`
- `SGOV -> XNYS` (including dates before and after the documented listing change)
- `exchange-calendars==4.13.2` as the pinned calendar implementation candidate
- mapping scope limited to month-end evaluation-cutoff session resolution
- unresolved calendar/version/data readiness remains fail-closed

This approval **does not** approve dependency integration, runtime activation, PCD-06 freshness/time policy, PCD-04 adjusted-price semantics, PCD-02 live provider behavior, PCD-15/PCD-16, or G-01. `config/moon.yaml` must continue to keep `active_strategies: []`.

## Sources

- `exchange_calendars` 4.13.2 on PyPI: https://pypi.org/project/exchange_calendars/4.13.2/
- Package calendar alias implementation (upstream source): https://github.com/gerrymanoim/exchange_calendars/blob/master/exchange_calendars/calendar_utils.py
- Existing instrument evidence audit: `Orion_Moon_ADM_PCD05_Instrument_Calendar_Mapping_Audit_2026-10-19.md`

No runtime source, tests, configuration, or dependency declarations were changed in this step. No live market-data API calls were made.
