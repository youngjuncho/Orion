# Moon ADM Readiness Mapping Type Audit — 2026-10-15

## Finding

`ADMDataAssemblyReadiness.__post_init__` validated the contents of `absolute_freshness_by_symbol` after attempting to iterate its keys, but did not first validate that the supplied object implemented the mapping contract. Malformed values such as `None` or a list could therefore fail with incidental runtime exceptions rather than the contract's explicit `ValueError`.

## Change

The readiness object now checks `isinstance(absolute_freshness_by_symbol, Mapping)` before examining expected symbols. The mapping is still normalized into an immutable mapping proxy after the existing symbol and observation consistency checks.

## Regression coverage

Tests replace a valid readiness object's mapping with `None` and a list, and assert the explicit validation error. Existing valid mapping and freshness consistency tests remain in the full suite.

## Scope and safety

This is input-contract validation only. It does not change momentum calculations, D-055 comparison semantics, strategy activation, or governance status. PCD-15 authoritative governance binding remains incomplete, so signal assembly remains fail-closed. No live Alpha Vantage API calls were made.
