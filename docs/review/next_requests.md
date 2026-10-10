# Review Follow-up Requests

Version: 2.0

Date: 2026-10-10

## Core Architecture

No new Core architecture decision is currently requested. Before relying on the `CORE-001` through `CORE-020` closure claim as an auditable decision set, reconcile the missing topic-to-ID/evidence crosswalk and the D-029 gap. Do not manufacture historical decisions to fill missing records.

## Next Documentation / Decision Work

### 1. D-051 — ADM Signal-to-Execution Mapping (Implemented)

`ADM_Orion.md` specifies VTI and VEU as risk assets and SGOV as the defensive candidate. D-051 resolves the prior mapping gap with identity mappings. The current Moon configuration has `active_strategies: []`, so ADM remains inactive.

Choose whether ADM should:

* execute the signal instruments directly;
* use explicitly approved signal-to-execution equivalents; or
* remain unavailable for target construction until mappings are approved.

D-051 is approved and implemented: VTI->VTI, VEU->VEU, and SGOV->SGOV. Focused model and Runtime integration coverage passes. VEU->VXUS is not approved. Keep strategy activation separate because `active_strategies` remains empty.

### 2. Resolve Draft D-052 — Runtime Failure / Commit Semantics

The existing contract specifies commit-before-transition-event ordering but not rollback or residual side effects on failures. Define the failure outcome for framework events, StateStore publication, event-factory/EventStore failures, and reuse of an `OrionRuntime` with its existing stores and execution identity. Then reconcile `Orion_Runtime.md`, `Orion_Event_Model.md`, and `Codex_Handoff_Specification.md` before implementation.

Do not describe the in-memory lifecycle as all-or-nothing until that behavior is explicitly chosen and validated.

### 3. Resolve Draft D-053 — Portfolio Cash Valuation / Target Semantics

`PortfolioState` carries account cash, but the valuation function accepts a separate `cash_value` and the target model has no cash sleeve. Decide whether cash enters the total-value denominator, how it relates to a fully invested target, and which layer converts multi-currency balances into the valuation currency. Do not make raw cross-currency sums or silently omit cash.

## Next Implementation Work (after the decisions)

### Core Runtime

Public framework orchestration and the optional in-memory decision/state/event lifecycle are implemented. After D-052 is resolved, reconcile the implementation and Runtime/Event/Handoff contracts for failure status, residual side effects, commit validation, and Runtime reuse. Durable persistence and replay remain future scope.

### Data Pipeline

Canonical observation contracts, source-agnostic normalization, structural validation, and direct/provider `MarketDataSet` Runtime handoff are implemented. Remaining work is production collection, source-specific semantic validation, freshness thresholds, and source failure/fallback behavior.

### Moon

The common domain provides PortfolioState/Snapshot records, caller-supplied valuation, deterministic weight-based RebalancePlan construction, and ExecutionOrder materialization from explicit sizing inputs. Keep ADM inactive until its data/runtime handoff is implemented; resolve D-053 before integrating cash into valuation. Then implement Account aggregation/current-state projection and the Moon Runtime rebalance handoff.

### Framework-Specific Work

When each Framework is ready, use its own governance/specification documents. Do not move those decisions into Core.
## Closed Historical Questions

The following no longer require Core-level user decisions:

* canonical Portfolio object separation — D-027 / CORE-019
* Runtime lifecycle — CORE-004/012
* Event semantics — CORE-003
* in-memory MVP persistence boundary — CORE-005/015
* public Runtime/API error boundary — CORE-018
* domain ownership — CORE-019
* documentation precedence — CORE-020

## Rule

If implementation encounters a behavior not covered by `CORE-001` through `CORE-020`, first determine whether it is:

1. a Framework-specific rule,
2. an implementation detail,
3. a future infrastructure concern, or
4. a genuinely new cross-framework architecture requirement.

Only the fourth category should reopen Core architecture.
