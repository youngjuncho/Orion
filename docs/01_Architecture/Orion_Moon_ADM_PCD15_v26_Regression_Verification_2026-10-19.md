# Orion Moon / ADM — v26 Regression Verification and Boundary Tests

**Date:** 2026-10-19  
**Baseline:** `Orion_Moon_ADM_Sync_Bundle_2026-10-19_v25.zip`  
**Purpose:** Record added regression tests for the isolated registry-acceptance prototype and the continuing PCD-15 fail-closed boundary.

## 1. Changes in this step

- Added a test demonstrating that restoring an older, valid SQLite database restores the older high-water mark too. This makes the prototype's anti-rollback limitation explicit; it is **not** a production security guarantee.
- Added an ADM boundary test demonstrating that the existence of a durable registry acceptance event does not clear the independent PCD-15 governance-binding blocker.
- No production source, trust policy, authority configuration, or strategy activation was changed.

## 2. Verification

Focused registry/ADM regression tests: **124 passed in 0.78s**.

Full test suite:

```bash
python -m pytest -q -p no:cacheprovider
```

Result: **479 passed in 3.55s** on the available container Python runtime. The designated Windows Conda Python 3.12.13 environment was not available for this run. No Alpha Vantage live API request was made.

## 3. Security and governance disposition

- The SQLite high-water mark is ordinary local persistence. Restoring an older valid database can roll it back; independent anti-rollback protection remains unresolved.
- Registry event acceptance and downstream event delivery are not the same as an authoritative Moon/ADM governance binding.
- PCD-15 remains incomplete; signal assembly must remain fail-closed.
- G-01 remains `DEFERRED — BLOCKING`; do not fabricate an authority, key, signature, approval, or currentness source.
- `config/moon.yaml` must retain `active_strategies: []`.
- The experimental SQLite HWM/journal/lease subsystem remains isolated and must not be wired into Moon/ADM as an approved production trust boundary.

## 4. Required next gate

Before implementing the production resolver, obtain explicit owner decisions on authority and revocation, signed payload/schema, key trust and rotation, scope and decision identifiers, freshness/currentness, independent rollback protection, and downstream idempotency/operational ownership. Then implement the typed resolver at an approved composition root and test that governance success clears only the governance blocker, never unrelated readiness gates.
