# Registry Leased-Drain Argument Validation Audit

**Status:** Implemented and regression-tested; no production consumer binding approved
**Date:** 2026-10-15

## Finding

`drain_leased_acceptances()` delegated `lease_seconds` validation to `SQLiteHighWaterMarkStore.claim_pending_acceptances()`. The validation was therefore reached only when a pending event existed. With an empty queue, invalid lease durations (including zero, non-finite values, booleans, or strings) could return a successful empty drain result instead of rejecting invalid caller configuration.

## Change

The public drain function now validates `lease_seconds` at entry using the same contract as the store: a finite positive integer or float, excluding booleans. This makes argument validation independent of queue state and prevents configuration mistakes from being masked by an empty journal.

Parameterized regression tests cover zero, negative, NaN, infinity, boolean, and string values with an empty queue. No event is consumed and no downstream callback is invoked.

## Boundaries

This is input-contract hardening only. It does not change lease duration semantics, retry/acknowledgement ordering, investment logic, registry trust policy, G-01/G-02/G-03 status, or PCD-15. `config/moon.yaml` remains `active_strategies: []`; ADM signal assembly remains fail-closed.
