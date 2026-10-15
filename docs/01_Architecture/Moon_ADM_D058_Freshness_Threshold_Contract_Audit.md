# Moon/ADM D-058 Freshness Threshold Contract Audit

Date: 2026-10-15

## Finding

`validate_adm_observation_pair_freshness()` accepted any non-negative integer threshold. A caller could pass `max_age_days=8` and receive a successful freshness result, even though D-058 caps monthly ADM observation age at seven calendar days. Higher-level readiness construction rejected the same threshold, leaving the public pair-level validator inconsistent with the approved cap.

## Change

The pair-level validator now rejects thresholds greater than `ADM_MONTHLY_MAX_OBSERVATION_AGE_DAYS` and raises a clear `ValueError`. A regression test confirms that an eight-day threshold is rejected even when the fixture observations themselves are fresh.

## Scope and safety

- The approved seven-day maximum is enforced; no threshold was loosened.
- No investment signal, asset allocation, or strategy activation logic changed.
- `config/moon.yaml` remains configured with `active_strategies: []`.
- No live provider/API calls were made.

## Verification

Full suite: 446 passed in 3.80s using Python 3.13.5. The designated Python 3.12.13 environment must still be run after local merge.
