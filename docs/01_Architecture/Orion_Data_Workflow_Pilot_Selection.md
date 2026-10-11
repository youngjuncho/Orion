# Orion Data Workflow Pilot Selection

**Status:** In-memory workflow experiment implemented; not a production-integration approval  
**Decision:** Use Moon ADM + Alpha Vantage monthly adjusted prices as the first *contract-evaluation candidate* if a data workflow is later authorized. Do not connect it to CLI, Runtime defaults, signal assembly, or strategy activation yet.  
**Date:** 2026-10-11

## 1. Why this is the most bounded candidate

Among the five frameworks, Moon ADM has the most concrete existing data contract and implementation path:

- Consumer and instruments are named: ADM uses VTI and VEU for relative momentum and SGOV for the approved absolute-momentum comparison.
- The canonical field is explicitly `adjusted_close`, mapped from Alpha Vantage `5. adjusted close`.
- The provider is implemented and performs network access only when explicitly invoked with a configured key.
- The provider requires all three instrument responses and at least 13 valid monthly observations per instrument; malformed, partial, or notice responses fail the complete load.
- D-055 approves SGOV and strict greater-than comparison; D-058 approves a seven-calendar-day maximum age for selected observations; D-059 defines per-invocation revision handling and fail-closed duplicate rejection.
- Existing selection, return, freshness, and assessment helpers have deterministic unit tests.

This makes Moon ADM the best-bounded candidate for an isolated, in-memory workflow experiment. It does **not** mean its data contract is fully closed or that a live signal is authorized.

## 2. Explicitly unresolved gates

| Gate | Evidence still required | While open |
|---|---|---|
| PCD-02 — live instrument coverage | Explicitly configured, authorized requests must return exact VTI, VEU, SGOV identities and sufficient valid monthly history | Do not claim live coverage; fail the entire batch on mismatch |
| PCD-04 — adjusted-price semantics | Evidence on adjustment/reinvestment conventions and empirical history parity against an accepted reference | Treat adjusted close only as the approved proxy; do not claim verified point-in-time total return |
| PCD-05/06 — time and calendar semantics | Close timezone/calendar interpretation and signal-date versus next-trading-day execution mapping | Do not convert observations into an activated signal or execution date |
| PCD-11 — reproducibility | Decide whether selected-input digests alone suffice for the intended private research workflow; a digest cannot recover source payloads | No claim of durable historical replay |
| PCD-12 — operational behavior | Reassess provider quota and entitlement before any repeated/scheduled use; retry/cache/outage behavior remains unapproved | No scheduling, retries, cache, or fallback source |
| PCD-15 — authoritative governance binding | Validate approval against an authoritative decision record, not only caller-supplied status/reference | Signal guard remains fail-closed |
| PCD-16 — end-to-end boundary | Demonstrate that provider/data failure cannot produce a valid `ADMSignalInput`, plus separate activation authorization | No signal assembly, activation, or Runtime integration |

PCD-13 and PCD-14 are already approved by D-055 and must not be reopened as a shortcut around data gates.

## 3. Allowed next experiment, if needed

A future, separately authorized engineering task may add a thin in-memory orchestration function that:

1. receives an explicitly injected provider;
2. calls `load()` once and validates the returned `MarketDataSet`;
3. applies only the already-approved seven-day age rule to the selected endpoints;
4. returns a typed data assessment and provenance for inspection;
5. fails the whole assessment on any required instrument, field, or endpoint failure.

The experiment must not construct `ADMSignalInput`, change `ADMStrategy`, select a configured defensive holding, create a default provider, schedule requests, retry, cache, persist, add a CLI command, or modify `config/moon.yaml`.

No network request is part of this decision. Provider coverage must not be represented as verified until an explicitly authorized request has actually succeeded.

## 4. Why not choose another framework now?

- **Aurora:** approved indicator set, source semantics, release/revision handling, and freshness requirements remain broader and less closed.
- **Orbit:** no concrete market-data consumer has been identified that justifies adding a collector.
- **Supernova:** registry/approved-company contracts are concrete, but current company data sourcing, reporting-period semantics, and fundamental field definitions are not yet a bounded live data workflow.
- **Phoenix:** source and entity identity contracts across market, on-chain, and ecosystem observations remain broader.

The selection is about boundedness of the existing data contract, not investment priority or strategy activation.

## 5. Invariants

- No SQLite HWM store, registry acceptance journal, lease consumer, cache, or other persistence is part of this candidate workflow.
- Core Runtime lifecycle and dependency-injection semantics remain unchanged.
- `config/moon.yaml` retains `active_strategies: []`.
- No investment logic, signal assembly, portfolio allocation, or order execution changes are authorized.
- A passing unit-test suite is not provider evidence, governance approval, or activation authorization.

## Related documents

- `Orion_Data_Workflow_Readiness_Decision.md`
- `Orion_Framework_Data_Contracts.md`
- `Moon_ADM_Data_Contract.md`
- `Moon_ADM_Data_Readiness_and_Closure.md`
- `Moon_ADM_Provider_Contract_Decision_Register.md`
- `Moon_ADM_Provider_Governance_Gate_Specification.md`


## Experiment implementation status (2026-10-11)

The isolated workflow is implemented in `src/orion/frameworks/moon/adm_workflow.py` and documented in `Orion_Moon_ADM_InMemory_Workflow_Experiment.md`. It requires an explicitly injected provider, calls `load()` once, runs the existing monthly assessment, and returns only the dataset and typed assessment. It does not create a signal, connect to Runtime/CLI, or persist data. Unit tests use fixtures; no live provider request was performed.
