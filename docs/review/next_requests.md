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

### 2. D-052 — Runtime Failure / Commit Semantics (Implemented)

Approved and implemented: stage/validate framework events, snapshot, and transition events, then commit both stores together; failures leave stores unchanged and close the session as `Error`. Each `OrionRuntime` is single-run; snapshot execution ID/status and transition-to-candidate identity are validated.

The all-or-nothing guarantee applies to Orion-owned in-memory stores; it does not roll back external side effects from caller-supplied callbacks.

### 3. D-053 — Portfolio Cash Valuation / Target Semantics (Approved and Implemented)

Approved 2026-10-10. The valuation and rebalance APIs take the configured currency as `valuation_currency`, consume cash only from `PortfolioState.cash`, convert via explicit positive finite caller-supplied rates, and include the result in the current-weight denominator. Cash remains residual funding outside the fully invested target. Duplicate `(account_id, currency)` balances and missing foreign-currency rates are rejected. The portfolio layer performs no FX lookup.

### 4. D-054 — Default Acceptance of Rebalance Plan Proposals (Approved)

Approved 2026-10-10: retain D-050's candidate-type-agnostic Auto-Approval. A Moon `RebalancePlanProposal` is accepted by default independently from its linked target proposal when no custom acceptance handler is supplied. This does not submit or execute orders. A custom handler can still reject or conditionally accept either candidate.

### 5. D-055 — ADM Absolute-Momentum Signal Policy (Approved)

Approved 2026-10-10: SGOV is the comparison benchmark; the selected risk asset's trailing-12-month adjusted-price return must be strictly greater than SGOV's, with equality false. The comparison helper uses this D-055 policy by default. Provider/source semantics, calendar interpretation, freshness thresholds, and production governance provenance remain separate gates. Keep ADM inactive and signal assembly blocked until those gates are closed.

## Next Implementation Work (after the decisions)

### Core Runtime

Public framework orchestration and the optional in-memory decision/state/event lifecycle are implemented. D-052 failure semantics are approved and implemented; durable persistence and replay remain future scope.

### Data Pipeline

Canonical observation contracts, source-agnostic normalization, structural validation, direct/provider `MarketDataSet` Runtime handoff, and context-aware delivery to Moon strategy factories are implemented. Remaining work is production collection, source-specific semantic validation, freshness thresholds, source failure/fallback behavior, and approved ADM signal assembly policy.

### Moon

The common domain provides PortfolioState/Snapshot records, caller-supplied valuation, deterministic weight-based RebalancePlan construction, and ExecutionOrder materialization from explicit sizing inputs. D-053 cash valuation is implemented. The Moon adapter emits a separate RebalancePlanProposal linked to the target when the caller supplies current PortfolioState and valuation-price factories. Custom acceptance handlers can decide independently; D-050's default Auto-Approval accepts both candidate types. Account aggregation remains caller-owned. Keep ADM inactive until provider/source semantics, freshness, and production governance gates close and activation is separately approved. Execution sizing and broker lifecycle remain out of scope.

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
