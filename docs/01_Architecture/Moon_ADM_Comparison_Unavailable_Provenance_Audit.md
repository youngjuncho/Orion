# Moon ADM — Unavailable Comparison Provenance Audit

Date: 2026-10-15

## Finding

`ADMAbsoluteMomentumComparisonResult` validates `policy_id` and `operator` strictly for available results, but the unavailable-result branch previously only required a non-empty reason. A manually constructed unavailable result could therefore carry malformed optional policy provenance (for example, a list-valued policy ID or a string-valued operator).

## Change

Optional provenance is now validated regardless of comparison status: a supplied `policy_id` must be a non-empty string, and a supplied `operator` must be an `ADMAbsoluteMomentumComparisonOperator`. `None` remains valid for either field on an unavailable result. The unavailable result still requires a non-empty reason; available-result semantics and comparison behavior are unchanged.

## Validation and scope

Regression tests cover malformed optional provenance on unavailable results. No investment rules, provider behavior, live API calls, or Moon strategy activation settings were changed. The PCD-15 authoritative governance binding remains incomplete and signal assembly remains fail-closed. Full-suite results and interpreter version are recorded in the sync bundle manifest.
