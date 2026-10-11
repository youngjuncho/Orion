# Orion Moon ADM In-Memory Workflow Experiment

**Status:** Isolated engineering experiment; not production integration approval  
**Date:** 2026-10-11

## Scope

`src/orion/frameworks/moon/adm_workflow.py` adds a thin orchestration boundary for the existing Moon ADM data contract. A caller must inject a provider. The function calls `load()` once, requires a canonical `MarketDataSet`, applies the existing ADM monthly assessment (including the approved D-058 seven-calendar-day selected-observation age limit), and returns the dataset plus typed assessment in memory.

## Explicit non-goals

- No default provider and no network call unless the caller explicitly supplies a configured provider.
- No retries, scheduling, cache, SQLite, HWM, journal, Lease, or persistence.
- No `ADMSignalInput` construction, signal assembly, portfolio allocation, order execution, or strategy activation.
- No CLI command and no Core Runtime integration.
- No change to `config/moon.yaml`; `active_strategies: []` remains the activation boundary.

## Failure behavior

Provider exceptions propagate. Non-`MarketDataSet` provider results are rejected. Missing or stale selected endpoints cause the assessment to fail rather than returning a partial result. The workflow does not silently substitute another observation or merge multiple provider invocations.

## Evidence and remaining gates

Unit tests use deterministic fixtures only. They demonstrate orchestration behavior, not live Alpha Vantage coverage, adjusted-price parity, point-in-time validity, provider entitlement, or governance approval. Those gates remain open as listed in `Orion_Data_Workflow_Pilot_Selection.md`.

## Exit criteria for this experiment

- One explicit provider load per invocation.
- Canonical dataset required.
- Existing freshness/assessment contract applied.
- Provider and assessment failures fail closed.
- No signal object is returned or constructed.
- No persistence or Runtime/framework activation path is introduced.
