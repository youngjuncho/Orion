# Orion Data Workflow — Readiness Decision

**Status:** Architecture decision recommendation; no production collector or CLI behavior added  
**Decision:** Do not implement a general-purpose `orion data update` workflow yet.  
**Current supported boundary:** Explicit provider invocation, normalization, structural validation, and in-memory handoff.

## 1. Decision

The repository has reusable market-data contracts and a concrete Alpha Vantage monthly adjusted-price provider, but it does not yet have an approved product-level data-update workflow. The existing `orion data update` and `orion data status` commands are placeholders; they do not fetch data, report freshness, or inspect persisted state.

Do not connect a provider to the CLI or Runtime as an implicit default until the project has approved the consuming framework, source semantics, freshness rules, failure behavior, and operator expectations. The absence of a workflow is currently more honest than implementing a superficially generic command whose data scope and success criteria are undefined.

## 2. Evidence in the current source

- `src/data/alphavantage.py` implements one concrete provider for monthly adjusted closes of VTI, VEU, and SGOV. It requires `ORION_ALPHA_VANTAGE_API_KEY`, makes network calls only when explicitly invoked, and does not retry, cache, or persist.
- `src/data/adapters.py` and `src/data/pipeline.py` normalize a source batch into `MarketDataSet` and reject malformed or duplicate observation identities.
- `src/orion/core/runtime_engine.py` accepts a `MarketDataSet` or an injected `MarketDataProvider`; provider choice is dependency-injected, not selected by the Runtime.
- `src/orion/cli/runtime.py` builds framework reports without injecting a market-data provider.
- `src/orion/cli/main.py` currently registers `data update` and `data status` as placeholders that print “not yet implemented”.
- Framework contracts explicitly leave source-specific freshness, units, timestamp semantics, missing observations, revisions, and source precedence unresolved until approved per framework/source pair.

## 3. Why a generic workflow is premature

A single `update all data` command implies an authoritative list of datasets, sources, schedules, and success conditions. Those are not yet defined for all frameworks. Moon has a concrete adjusted-price use case, while Aurora, Supernova, Phoenix, and Orbit have different domains and unresolved source-specific contracts. Treating the one available Alpha Vantage provider as the system-wide default would silently make an unapproved scope decision.

Similarly, `data status` cannot truthfully report “fresh” or “stale” without an approved freshness policy and a definition of the relevant dataset set. A timestamp alone is not a freshness guarantee.

## 4. Minimal workflow contract required before implementation

For each approved framework/source pair, record:

1. **Consumer and scope:** which framework consumes which symbols/entities and fields.
2. **Source authority:** provider identity, credential handling, entitlement/rate limits, and source precedence.
3. **Semantics:** field meaning, units/currency, adjustment basis, timestamp/timezone, calendar, and revision behavior.
4. **Freshness:** maximum age, expected observation cadence, and treatment of market holidays or delayed publication.
5. **Failure semantics:** timeout, rate limit, partial response, missing symbol, malformed response, stale response, and retry policy.
6. **Delivery contract:** whether the result is passed only in-memory, written to a rebuildable cache, or persisted for a specific durable-state requirement.
7. **CLI behavior:** precise meaning of success, partial success, status, and non-zero exit codes.
8. **Verification:** deterministic fixtures, negative tests, and an end-to-end test that proves the selected dataset reaches only its approved consumer.

Do not fill these fields by inference. If one item is unresolved, keep the provider injectable and the end-user workflow unconnected for that framework/source pair.

## 5. Recommended incremental implementation plan

When an actual workflow is approved:

1. Start with one explicit framework/source pair rather than `update all data`.
2. Build a thin orchestration service that calls the approved provider, validates the returned `MarketDataSet`, applies the approved freshness policy, and returns an in-memory result.
3. Keep persistence out of the first version unless a requirement explicitly needs cache or durable state.
4. Add a CLI command only after its inputs, outputs, exit codes, and status semantics are specified.
5. Do not change investment signals, ranking, allocation, order execution, or Runtime lifecycle as part of data acquisition work.

## 6. Step 50 disposition

The SQLite HWM store, registry acceptance journal, and lease consumer remain isolated prototypes. They are not required to implement a simple market-data fetch-and-validate call and must not be introduced as a dependency of the data workflow. Registry trust and market-data freshness are separate concerns and must not be conflated.

## 8. Pilot candidate selection

`Orion_Data_Workflow_Pilot_Selection.md` identifies Moon ADM + Alpha Vantage monthly adjusted prices as the most bounded candidate for a future isolated in-memory experiment. This is not a production-integration approval: provider coverage, adjusted-price parity, temporal semantics, authoritative governance binding, and end-to-end failure gates remain open. No live provider request or Runtime/CLI wiring is authorized by that selection.

## 7. Non-goals and invariants

This decision adds no network calls, provider selection, credentials, retries, cache, persistence, CLI behavior, Runtime integration, or framework data injection. It does not change investment logic, order execution, Moon configuration (`active_strategies: []`), or Supernova production integration.
