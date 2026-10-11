# Orion Step 50 — Stateless Data Path Audit

**Status:** Source-level architecture audit; no production behavior changed  
**Decision:** Stateless fetch-and-validate remains the simplest current-MVP candidate; no evidence found that the isolated SQLite registry persistence prototype is needed by the active data path.

## 1. Scope

This audit traces the current repository's data entry points and distinguishes implemented code from an automatically wired production workflow. It does not assert that external sources are always available, that their responses are always current, or that stateless operation prevents cross-session replay.

## 2. Observed data path

### Canonical market-data path

1. `src/data/alphavantage.py` defines `AlphaVantageMonthlyAdjustedSource` and `AlphaVantageMonthlyAdjustedProvider`.
2. The source performs network requests only when `fetch()` is explicitly called. It fetches monthly adjusted data for VTI, VEU, and SGOV and fails closed on transport, response, identity, and minimum-history errors.
3. `src/data/adapters.py` wraps a raw source and calls `normalize_dataset()`.
4. `src/data/contracts.py` defines immutable `MarketDataPoint` and `MarketDataSet` contracts; `src/data/pipeline.py` normalizes fields and rejects duplicate observation identities.
5. `src/orion/core/runtime_engine.py` accepts either a prebuilt `MarketDataSet` or an injected `MarketDataProvider`. If a provider is supplied, it calls `load()` once for that runtime call and checks the returned type.

The provider boundary is dependency-injected. The Runtime does not select a provider, store fetched data, or automatically retry. The Alpha Vantage implementation documents that it has no retries, cache, or persistence.

### Current CLI wiring

The current CLI does **not** automatically construct or inject `AlphaVantageMonthlyAdjustedProvider` into `OrionRuntime`. `orion.cli.runtime.run_framework_report()` invokes report factories without a market-data provider. The `orion data update` and `orion data status` handlers currently print “not yet implemented”. Thus, a canonical provider path exists as an injectable component, but a complete user-facing data-update workflow is not yet wired.

### Step 50 registry persistence path

`SQLiteHighWaterMarkStore`, `RegistryAcceptanceService`, and the acceptance consumer helpers remain separate modules. Source inspection found no import/call site from the active Runtime or framework source. Their tests prove the prototype's local behavior; they do not demonstrate that an active product workflow needs it.

## 3. What the code currently validates

- Provider-neutral normalization checks required text fields, immutable data contracts, and duplicate observation identities.
- The Alpha Vantage source checks response structure, instrument identity, error/notice responses, and minimum history needed by its current ADM research use.
- Runtime checks that an injected provider returns `MarketDataSet` and disallows passing both direct data and a provider.
- Source comments explicitly leave freshness and source-specific semantic policy outside the provider-neutral MVP pipeline.

These are structural/contract checks, not a complete freshness or trust policy. A non-empty `observed_at` or `as_of` value is not by itself proof that data is sufficiently fresh. A successful refetch is not by itself proof that an earlier accepted version cannot be replayed.

## 4. Persistence conclusion

The active data handoff is designed around a provider returning a canonical in-memory `MarketDataSet`. The current provider implementation neither writes a local cache nor persists fetched observations. The Runtime's StateStore/EventStore are execution-scoped in-memory stores, and durable Runtime persistence is outside the current MVP boundary.

Consequently, the repository does not currently demonstrate a product need to operate the Step 50 SQLite HWM, acceptance journal, or leases. Keep the prototype isolated; do not add it to the market-data provider path. Prefer fetch-and-validate for current execution data unless a concrete requirement proves that cache, cross-session anti-replay state, or durable asynchronous delivery is needed.

## 5. Known limits and revisit triggers

Stateless fetch-and-validate is appropriate only for requirements that do not demand durable cross-session state, or where a trusted authority provides sufficient freshness/version guarantees. Revisit the decision if Orion must:

- reject an older registry version previously accepted in an earlier session;
- continue asynchronous work across process/host restart;
- durably deduplicate an external side effect;
- satisfy measured source latency, availability, rate-limit, or offline constraints with a rebuildable cache;
- introduce durable Runtime StateStore/EventStore as a separate approved workstream.

If a revisit is needed, first define the threat model, source guarantees, failure semantics, ownership, and tests. Persist only state that cannot safely be re-fetched or recomputed.

## 6. Data workflow readiness

The follow-up decision in `Orion_Data_Workflow_Readiness_Decision.md` records that a general `orion data update` workflow is premature until each framework/source pair has approved scope, semantics, freshness, failure behavior, and CLI success criteria. Keep provider injection explicit and do not treat the currently available Alpha Vantage provider as an implicitly approved system-wide source.

## 7. Non-goals and invariants

This audit changes no Python source or runtime behavior. It does not select a new provider, change investment logic, execute orders, alter Moon configuration (`active_strategies: []`), or connect the Step 50 prototype to Runtime/Supernova.
