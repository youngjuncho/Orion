# Orion Moon/ADM Sync Bundle — 2026-10-15 (v20)

## Contents

- Cumulative Orion repository snapshot based on `Orion_1013.zip`, Git commit `fea05ba`, including the previously accumulated Moon/ADM changes, PCD-15 readiness audit, G-01 status reconciliation, G-02 runtime cross-check audit, and this step's leased-drain argument validation hardening.
- Per user preference, this is the single cumulative ZIP bundle; no standalone patch files are included. Compare it with the local working tree and merge selectively.

## Included changes

0c. v20 validates `lease_seconds` at entry to `drain_leased_acceptances()`, even when the acceptance journal is empty; regression tests cover zero, negative, NaN, infinity, booleans, and strings.

0b. v19 adds a source-checked G-02 runtime cross-check documenting the generic validator's permissive envelope/scope behavior versus the stricter proposed Supernova domain validator. Documentation-only; G-02 remains blocking.

0. v17 added a PCD-15 readiness audit showing that production binding remains blocked by unapproved authority, payload, cryptographic trust, freshness/anti-rollback, recovery, and consumer-ownership decisions.
0a. v18 reconciles stale G-01 status references in the G-01 decision brief and G-02 audit with the current D-060 `DEFERRED — BLOCKING` disposition. Documentation-only; no runtime integration is made.

1. Governance decision-record validation rejects malformed status types.
2. PCD-15 governance-binding contract proposal remains proposal-only; production integration is not approved or implemented.
3. G-01 registry-authority decision brief documents options without selecting an authority; D-060 records G-01 as deferred and blocking.
4. G-02 payload/scope contract audit records unresolved schema and canonicalization questions.
5. Alpha Vantage timeout validation rejects non-finite, non-positive, boolean, and non-numeric values; offline tests only.
6. PCD-08/PCD-11/PCD-12 implementation audits and PCD-11 digest canonicalization, consumer, semantics, and object-integrity reviews.
7. D-055 monthly assessment and signal guard enforce the approved strict-greater-than operator.
8. ADM readiness and signal-guard result objects validate tuple contracts and remain fail-closed where required.
9. v12 validates optional `policy_id` and `operator` provenance on unavailable comparison results, with regression tests and an audit note.
10. v13 validates that `absolute_freshness_by_symbol` is a mapping before inspecting its keys, with malformed-input regression tests and an audit note.
11. v14 enforces the approved seven-day maximum in the readiness constructor.
12. v15 enforces the same D-058 maximum in the public observation-pair freshness validator, with a regression test and audit note.
13. v16 rejects malformed, empty, or string-like `required_ids` inputs in the governance decision resolver, with regression tests and an audit note.

## Validation

- v20 full test suite: **460 passed in 4.01s**, Python **3.13.5**.

- Full test suite: see `SYNC_BUNDLE_MANIFEST.json`; executed with the recorded interpreter version.
- This is not a verification in the project's designated Conda Python 3.12.13 environment unless the manifest explicitly says so. After merging, run:

  `"$HOME/anaconda3/envs/orion/python.exe" -m pytest -q -p no:cacheprovider`

- UTF-8 policy and archive integrity are checked when producing this bundle.

## Synchronization precautions

- Baseline: `Orion_1013.zip`, commit `fea05ba`. The bundle may not include edits made in the local working tree after that snapshot was produced.
- Do not replace the working repository wholesale. Back up local changes, inspect `git status` and `git diff`, and merge selectively. Preserve local and VAA work.

## Safety and scope

- No live Alpha Vantage API calls were made.
- `config/moon.yaml` must keep `active_strategies: []`.
- No investment or trading logic was changed. PCD-15 authoritative governance binding remains incomplete; signal assembly stays fail-closed.
