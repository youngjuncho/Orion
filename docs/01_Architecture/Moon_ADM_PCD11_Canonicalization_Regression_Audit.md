# Moon ADM PCD-11 — Canonicalization Regression Audit

- Date: 2026-10-15
- Status: Regression test added; digest semantics remain unchanged
- Baseline: Orion_1013.zip, commit `fea05ba`, plus accumulated Sync Bundle v5 work
- Scope: deterministic serialization property only; no investment logic or policy change

## Finding

`assess_adm_monthly_dataset()` serializes the selected-input digest payload with sorted JSON object keys and compact separators before hashing it with SHA-256. That design should make a mapping's insertion order irrelevant while still binding the actual metadata key/value content.

The previous digest test checked repeatability for identical fixtures and sensitivity to a selected price change. It did not isolate mapping insertion order as its own property.

## Change

Added `test_monthly_assessment_digest_ignores_mapping_insertion_order` in `tests/orion/frameworks/moon/test_adm_data.py`. It constructs equivalent selected observation metadata in different insertion orders and asserts the digest remains identical.

This test does **not** decide whether volatile fields such as `retrieved_at` belong in `selected_input_digest`. That semantic question remains open as documented in `Moon_ADM_PCD11_Digest_Semantics_Decision_Brief.md`.

## Validation

- Full suite: `435 passed in 3.59s`
- Interpreter: Python 3.13.5
- Command: `python -m pytest -q -p no:cacheprovider`
- No live provider/API calls
- `config/moon.yaml` remains `active_strategies: []`

The project's designated Python 3.12.13 environment still needs to run the full suite after local synchronization.
