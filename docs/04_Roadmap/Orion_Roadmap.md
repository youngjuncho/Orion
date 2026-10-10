# Orion Roadmap

Version: 2.0

Status: Active

Last Updated: 2026-10-10

## Vision

Build a Personal Investment Operating System that enables the investor to understand asset-allocation status, market climate, megatrend status, and digital-asset status within one minute.

## Roadmap Model

The previous phase-only roadmap is superseded because implementation maturity now differs materially by workstream. Current planning uses workstreams and explicit architecture/implementation status.

### A. Architecture & Contract

**Architecture baseline: declared closed; traceability audit open**

* The 2026-10-07 baseline reports CORE-001 through CORE-020; individual ID-to-evidence mapping is under audit.
* Canonical domain ownership, Runtime lifecycle, State/Event/Decision/Error contracts, and data handoff are recorded in the architecture baseline.
* Do not infer an individual decision record from the ordinal position of a topic in the baseline.

### B. Core Runtime

**Architecture: established / Implementation: MVP implemented**

* RuntimeSession, RuntimeContext, and ServiceRegistry -> implemented
* StateStore and EventStore -> in-memory implementations
* Public OrionRuntime.run() -> implemented
* Decision -> State Transition -> coordinated State/Event commit -> implemented as an in-memory MVP under D-052
* OrionResult construction -> implemented

### C. Data Pipeline

**Contract: Established / Implementation: Partial**

* Canonical observation and MarketDataSet contracts -> implemented
* Source-agnostic normalization and structural validation -> implemented
* Direct/provider MarketDataSet Runtime handoff -> implemented
* Source collection, source-specific semantic validation, freshness policy, and fallback behavior -> pending

### D. Framework Implementation

#### Moon

**Architecture: established / Implementation: Partial**

Established:

* StrategyResult
* ConsensusAllocation
* Common PortfolioTarget production

Remaining:

* Account aggregation and authoritative PortfolioState projection
* Runtime handoff and end-to-end Moon rebalance integration
* ADM activation remains separate; identity mappings are implemented under D-051 and `active_strategies` remains empty

#### Aurora

**Framework specification/implementation: PENDING**

Indicator definitions, scoring methodology, regime thresholds, and transition-risk rules must be finalized before production calculation logic is implemented.

#### Supernova

**Framework governance/specification: separately governed**

Core does not redefine Supernova methodology. Core tracks implementation readiness only.

#### Phoenix

**Framework governance/specification: separately governed**

Category/Leader/Scoring governance is Framework-owned. Core tracks implementation readiness only.

### E. Presentation & External Interface

CLI:

* Command routing is implemented.
* Runtime-backed report commands are partial; full integration remains pending.

Dashboard:

* Read-only presentation boundary is implemented.
* Runtime-integrated view is partial.

API:

* Public Runtime/API error contract is specified; standardized client-facing exception mapping remains pending.
* Concrete endpoint and serialization implementation are future work.

## Status Principle

```text
DECIDED
  ↓
IMPLEMENTATION READY
  ↓
IMPLEMENTED
  ↓
VALIDATED
  ↓
ACTIVE
```

Configuration cannot create approval. A strategy or framework becomes executable only when its governing specification and activation state permit execution.

## Next Implementation Direction

D-051 and D-052 are approved and implemented. Complete the Core decision-evidence traceability audit, then continue with production data policies, authoritative portfolio-state projection, Moon rebalance Runtime integration, and remaining CLI/Dashboard/API work.

This roadmap does not redefine investment methodology or framework governance.
