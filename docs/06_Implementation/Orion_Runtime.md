# 2026-10-07 Core Reconciliation Addendum

> **Current authority:** The canonical Runtime lifecycle is defined by `CORE-004` and `CORE-012`. Historical references to “Orion Engine” mean the application Runtime and should not be interpreted as a separate Core component.

Canonical lifecycle:

```text
Initialize → Configuration → Data → State Restore → Context
→ Framework Execution → Result Validation → Decision Resolution
→ State Transition → State Commit → Event Creation
→ Persistence → Presentation → Completion
```

`RuntimeSession` is one execution lifecycle boundary; `RuntimeContext` is the execution-scoped input bundle. `build_context()` is assembly only. A Framework executor failure stops the current execution; the public Runtime does not return a partial successful `OrionResult`. Framework-event recording is now inside the failure boundary and closes the session as `Error` if it fails. A transition-event failure can still occur after snapshot commit; remaining residual-side-effect and Runtime-reuse questions are tracked under Draft D-052.

---

> **Document status:** The original body below was marked Draft in July 2026 and is retained as context. Use this reconciliation addendum, later dated audit notes, and the current Runtime contracts where wording conflicts; do not treat every historical workflow step as implemented.

# Orion Runtime

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Orion_Engine.md
* Orion_Domain_Model.md
* Orion_Configuration_Schema.md
* Moon_Object_Model.md

---

# Purpose

This document defines the runtime environment of Orion OS.

The Orion Runtime represents the in-memory state of the system during execution.

It provides shared access to configuration, market data, framework instances, execution results, and system state.

The runtime exists only while the Orion Engine is executing.

---

# Design Principles

## Single Runtime Instance

Each Orion Engine execution creates one Orion Runtime instance.

The runtime is shared across all framework executions.

---

## Shared Context

Frameworks receive the runtime as a shared execution context.

Frameworks should not communicate directly with one another.

All shared information flows through the runtime.

The read-only `RuntimeContext` exposes configuration, normalized market data,
registered services, framework results, system state, and dashboard data.
Framework and service registries provide read-only snapshots when values are
passed into that context.
Frameworks may consume these values but must not mutate the shared context.

---

## Stateless Frameworks

Framework implementations should avoid maintaining internal persistent state.

Persistent system state is managed by the Orion Runtime.

---

# Runtime Architecture

```text
Orion Runtime

├── Configuration
├── Market Data
├── Framework Registry
├── Framework Results
├── System State
├── Portfolio
├── Dashboard Data
├── Logger
└── Execution Metadata
```

---

# Runtime Components

The current `RuntimeSession` owns the in-memory framework registry, service
registry, event store, and state store for one execution. These components are
temporary and are not durable persistence.

After frameworks are registered, `RuntimeSession.build_context()` creates the
read-only `RuntimeContext` consumed by framework code. The Runtime now also
provides `OrionRuntime.run()` as the public application entry point. It creates a
`RuntimeSession` and delegates canonical framework orchestration to it. The
underlying `RuntimeSession.execute_frameworks()` accepts explicit framework
executors, invokes them in registry order, validates the canonical
`FrameworkResult` contract, and assembles the public `OrionResult`.

The Runtime now also provides the Decision Resolution → State Transition →
StateStore commit boundary. Frameworks propose `DecisionCandidate` values only.
An explicit acceptance callback produces `AcceptedDecision` values; an explicit
transition callback produces `StateTransition` values; the resulting transitions
are committed as one authoritative `OrionStateSnapshot` for the execution. No
decision is accepted implicitly. After a successful state commit, an optional
Runtime event factory may create correlated Domain Events, which are then appended
to the execution-scoped `EventStore`. `RuntimeSession.record_events()` rejects
events whose `execution_id` does not match the current execution. EventStore is
append-only in-memory storage for the MVP; durable persistence remains a later
workstream. Framework code does not mutate StateStore, EventStore, or Dashboard
state directly.

## Configuration

Purpose:

Provide system-wide configuration.

Examples:

* Active Strategies
* Indicator Weights
* Rebalance Schedule
* Data Directories

Source:

Configuration files.

---

## Market Data

Purpose:

Provide normalized market data for all frameworks.

Examples:

* ETF Prices
* Equity Prices
* Index Data
* Economic Indicators

The runtime provides read-only access. Dashboard data is exposed through the official runtime result boundary; presentation code does not call Framework Engines directly.

---

## Framework Registry

Purpose:

Maintain active framework instances.

Current Frameworks:

* Aurora
* Moon
* Orbit
* Supernova
* Phoenix

Each framework is initialized once per execution.

---

## Framework Results

Purpose:

Store the output generated by each framework.

Examples:

Aurora

* Regime
* Score
* State Momentum

Moon

* Strategy Results
* Consensus Allocation

Supernova

* Approved Companies
* Watchlist

Phoenix

* Category Leaders
* Watchlist

---

## System State

Purpose:

Represent the current operational state of Orion.

Examples:

* Current Regime
* Current Portfolio Allocation
* Current Theme Leaders
* Current Digital Asset Leaders

The System State is updated after all framework execution is complete.

---

## Portfolio

Purpose:

Represent the consolidated investment portfolio.

Examples:

* ETF Allocation
* Equity Holdings
* Digital Asset Allocation

Portfolio construction is performed by individual frameworks.

The runtime stores the consolidated result.

---

## Dashboard Data

Purpose:

Provide normalized data for dashboard visualization.

The Dashboard consumes runtime data through the official `OrionResult.dashboard_data` boundary. It performs no investment calculations and does not call Framework Engines directly.

---

## Logger

Purpose:

Record execution activity.

Examples:

* Execution Start
* Execution End
* Framework Status
* Errors
* Warnings

---

## Execution Metadata

Purpose:

Record execution information.

Examples:

* Execution ID
* Start Time
* End Time
* Duration
* Orion Version

---

# Runtime Lifecycle

```text
Engine Start

↓

Create Runtime

↓

Load Configuration

↓

Load Market Data

↓

Initialize Frameworks

↓

Execute Frameworks

↓

Aggregate Results

↓

Update System State

↓

Generate Dashboard Data

↓

Persist Results

↓

Destroy Runtime
```

---

# Runtime Access Rules

Frameworks may:

* Read Configuration
* Read Market Data
* Read Previous System State
* Write Framework Results

Frameworks must not:

* Modify another framework's results
* Directly invoke another framework
* Modify shared configuration

---

# State Persistence

The runtime itself is temporary.

Persistent information is stored separately after execution.

Examples:

* Portfolio Snapshots
* Regime History
* Review Records
* Execution Logs

---

# Error Recovery

If a framework fails:

* Record the error
* Preserve completed framework results
* Continue independent framework execution when possible

Critical runtime failures terminate execution.

---

# Relationship With Orion Engine

The Orion Engine manages execution.

The Orion Runtime manages execution state.

Relationship:

```text
Orion Engine

↓

Orion Runtime

↓

Framework Execution

↓

Framework Results
```

---

# Future Enhancements

Potential future additions:

* Parallel Runtime Support
* Incremental State Updates
* Distributed Execution Context
* Plugin Runtime Registry
* Background Task Management

Status:

Research Only

Not Approved

---

# Related Documents

* Orion_Engine.md
* Orion_Domain_Model.md
* Orion_Configuration_Schema.md
* Moon_Object_Model.md
* Aurora_Interface.md
* Moon_Interface.md
* Supernova_Interface.md
* Phoenix_Interface.md

## Step 5 — Framework Adapter / CLI Boundary

The public `OrionRuntime` boundary now accepts canonical framework adapters. Existing framework engines are adapted without changing their domain APIs through `orion.core.framework_adapters`.

Report-capable framework CLI commands (`aurora report`, `moon report`, `supernova report`, `phoenix report`) invoke the public Runtime boundary through `orion.cli.runtime`. The CLI may format the original framework report after the adapter has executed, but it does not execute the engine directly from `orion.cli.main`.

Orbit does not receive a report adapter in this step because its current engine contract requires explicit Portfolio/Target identifiers and an effective date; inventing those values at the CLI boundary would violate the Common Portfolio Domain contract. Orbit remains a Runtime-capable framework once its execution inputs are supplied explicitly.

## Canonical Market Data Handoff — Runtime Integration Step 8

`OrionRuntime.run()` accepts either an already validated `MarketDataSet` or a
runtime-facing `MarketDataProvider` whose `load()` method returns one.

The Runtime does not collect, normalize, or freshness-score external data. The
provider boundary exists only to hand a canonical dataset into
`RuntimeContext.market_data` before Framework execution.

The two input forms are mutually exclusive. Source adapters, raw-to-normalized
transformation, validation/freshness policy, and production storage remain
outside the current Runtime implementation.

### Portfolio valuation handoff

The common portfolio layer now accepts an explicit `PortfolioValuation` boundary. Runtime callers may supply canonical, already-normalized prices to value a `PortfolioState`; the portfolio layer performs no price discovery or FX conversion. `current_allocations_from_valuation()` projects asset weights using total portfolio value, including explicit cash value in the denominator. This closes the current-state/valuation input needed for deterministic `RebalancePlan` construction without introducing synthetic prices or quantities.


### Execution-order sizing handoff — Runtime Integration Step 12

The common portfolio layer now exposes `ExecutionSizingInput` and `build_execution_orders()`. The boundary accepts already-resolved executable quantities and order identities and materializes canonical `ExecutionOrder` objects from a `RebalancePlan`. Quantity calculation, price selection, fees, lot sizes, fractional-share rules, and broker constraints remain outside the common Portfolio Domain.

### Execution boundary validation — Runtime Integration Step 13

The Runtime integration now treats canonical `ExecutionOrder` materialization as
the terminal output of the current Moon execution-domain slice. Materializing an
`ExecutionOrder` does not imply broker submission, fill, settlement, ledger update,
or mutation of actual holdings.

This boundary follows D-027: actual order execution remains outside the current
Moon MVP unless a future architecture decision explicitly brings it into scope.


# 2026-10-08 CORE-012 Runtime Lifecycle Audit (Pre-Step 18)

The Runtime implementation has been audited against the canonical CORE-012 lifecycle without changing the architecture or introducing new investment logic.

| Lifecycle stage | Current implementation status | Boundary |
|---|---|---|
| Initialize | Implemented | `RuntimeSession` creation |
| Configuration | Implemented | `OrionConfig` supplied to session/context |
| Data | Implemented | canonical `MarketDataSet` / provider handoff |
| State Restore | Partial | in-memory `StateStore` restore; durable restore is future |
| Context | Implemented | read-only `RuntimeContext` |
| Framework Execution | Implemented | registry-ordered Framework adapters |
| Result Validation | Implemented | `FrameworkResult` validation |
| Decision Resolution | Partial | `RuntimeSession.resolve_and_commit()` only |
| State Transition | Partial | canonical transition callback at Session boundary |
| State Commit | Partial | `StateStore` commit at Session boundary |
| Event Creation | Partial | correlated Domain Events at Session boundary |
| Persistence | Partial | in-memory MVP `StateStore` / `EventStore` |
| Presentation | Implemented | `OrionResult` / dashboard boundary |
| Completion | Implemented | session completion after framework execution |

The table above records the pre-Step 18 audit state. Step 18 subsequently closed the public single-call lifecycle gap without changing the Core architecture. The canonical Decision → State Transition → State Commit → Event path is now available through `OrionRuntime.run()` when lifecycle handlers are supplied (with Auto-Approval as the default acceptance policy).

This is an implementation gap, not a Core architecture gap. `CORE-001` through `CORE-020` remain closed. Durable persistence and replay remain outside the MVP boundary defined by D-030.

# Runtime Integration Step 15

Supernova and Phoenix are integrated through report adapters at the Framework boundary. Their satellite semantics remain Framework-owned and are not converted into Common Portfolio Domain decisions.

# Runtime Integration Step 16

The Public Runtime is validated against all five Frameworks: Aurora, Moon, Orbit, Supernova, and Phoenix. The registry order is authoritative for one Runtime execution, and Framework failure stops the current execution without returning a partial successful `OrionResult`.

# Runtime Integration Step 18

The Public `OrionRuntime.run()` can now execute the canonical Decision → State
Transition → State Commit → Event path in the same public lifecycle when explicit
Decision lifecycle handlers are supplied.

The public boundary accepts three required handlers for a decision lifecycle:

* `accept(DecisionCandidate) -> AcceptedDecision | None` (optional; defaults to the
  Runtime Auto-Approval policy)
* `transition(AcceptedDecision) -> StateTransition`
* `snapshot(tuple[StateTransition, ...]) -> OrionStateSnapshot`

An optional `event_factory(StateTransition) -> Event` creates correlated Domain
Events after the authoritative StateStore commit. The default Runtime acceptance
policy is Auto-Approval: each candidate is explicitly materialized as an
`AcceptedDecision` with `accepted_by = "orion-runtime:auto-approval"`. Frameworks
continue to propose `DecisionCandidate` values only and cannot self-accept. A
caller may provide an explicit acceptance handler when rejection or conditional
acceptance is required.

The existing framework-only `OrionRuntime.run()` path remains backward compatible
when no lifecycle handlers are supplied. This preserves report-only and framework
integration callers while making the full canonical lifecycle available through
one public call when an explicit decision policy is present.

The Runtime does not introduce investment methodology, broker execution, or
persistent storage in this step. Durable State/Event persistence remains outside
the MVP boundary defined by D-030.

## 2026-10-08 CORE-012 Step 18 Reconciliation

| Lifecycle stage | Status after Step 18 | Boundary |
|---|---|---|
| Initialize | Implemented | `OrionRuntime.create_session()` |
| Configuration | Implemented | `OrionConfig` |
| Data | Implemented | canonical `MarketDataSet` / provider |
| State Restore | Partial | in-memory `StateStore`; durable restore future |
| Context | Implemented | `RuntimeContext` |
| Framework Execution | Implemented | registry-ordered adapters |
| Result Validation | Implemented | `FrameworkResult` validation |
| Decision Resolution | Implemented | Public `run()` + default Auto-Approval or explicit acceptance handler |
| State Transition | Implemented | Public `run()` + explicit transition handler |
| State Commit | Implemented | `StateStore.publish()` |
| Event Creation | Implemented | optional event factory after commit |
| Persistence | Partial | in-memory MVP stores; durable persistence future |
| Presentation | Implemented | `OrionResult` / dashboard boundary |
| Completion | Implemented | Public lifecycle completes after decision path |

Step 18 closes the previous **public single-call lifecycle integration gap**
without changing the Core architecture or introducing an implicit investment
policy. The remaining partial lifecycle items are State Restore and durable
Persistence, both intentionally outside the current MVP scope.
