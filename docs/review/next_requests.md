# Review Follow-up Requests

Version: 2.0

Date: 2026-10-07

## Core Architecture

No further Core architecture decision is currently requested. `CORE-001` through `CORE-020` are closed.

## Next Implementation Work

### 1. Core Runtime

Implement the already-defined lifecycle:

```text
Configuration
→ Data
→ State Restore
→ RuntimeContext
→ Framework Execution
→ Result Validation
→ Decision Resolution
→ State Transition
→ State Commit
→ Event Creation
→ RuntimeResult
```

Do not redesign the contract while implementing it.

### 2. Data Pipeline

Implement:

* source adapter boundary
* normalization
* validation
* freshness checks
* canonical `MarketDataSet`

### 3. Moon

Continue from the approved portfolio model:

```text
PortfolioTarget + PortfolioSnapshot
        ↓
RebalancePlan
```

Then integrate the result with the Runtime.

### 4. Framework-Specific Work

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
