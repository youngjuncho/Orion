# Moon/ADM Readiness-Gate Type Integrity Audit

Date: 2026-10-15

## Finding

`ADMDataAssemblyReadiness.unresolved_policy_gates` is declared as a tuple of strings, but Python does not enforce the annotation at runtime. The previous validation iterated the supplied value directly. An empty string therefore passed the element validation vacuously and was retained as an empty tuple, making `signal_ready` evaluate to `True` even though the caller had not supplied the required gate collection type.

The independent signal-assembly guard still unconditionally blocks on `authoritative_governance_binding_not_implemented`, so this did not bypass the current production signal gate. It could nevertheless misrepresent the intermediate readiness state and weaken future callers that rely on `signal_ready`.

## Change

- Require `unresolved_policy_gates` to be a tuple before inspecting its members.
- Keep the existing non-empty-string validation for each gate identifier.
- Add regression coverage for both an empty string and a non-empty string passed through `dataclasses.replace()`.
- Do not alter the default unresolved gates, D-055 comparison behavior, strategy activation, or governance status.

## Validation

- Full test suite: `439 passed in 4.13s` on Python `3.13.5`.
- This is not a run in the designated project environment (Conda Python `3.12.13`); rerun the standard test command after merging locally.
- No live API calls were made.
- `config/moon.yaml` must remain `active_strategies: []`.

## Remaining boundary

The authoritative PCD-15 governance binding is still not implemented. The signal guard remains fail-closed regardless of caller-supplied approval status/reference.
