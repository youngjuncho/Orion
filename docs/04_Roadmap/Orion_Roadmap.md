# Orion Roadmap

Version: 2.0

Status: Active

Last Updated: 2026-10-07

## Vision

Build a Personal Investment Operating System that enables the investor to understand asset-allocation status, market climate, megatrend status, and digital-asset status within one minute.

## Roadmap Model

The previous phase-only roadmap is superseded because implementation maturity now differs materially by workstream. Current planning uses workstreams and explicit architecture/implementation status.

### A. Architecture & Contract

**Architecture: CLOSED**

* CORE-001 through CORE-020 established
* Canonical domain ownership established
* Runtime lifecycle established
* State/Event/Decision/Error contracts established
* Data handoff established
* Package baseline reconciled
* Core architectural blockers: 0

Remaining: documentation reconciliation/maintenance only.

### B. Core Runtime

**Architecture: CLOSED / Implementation: PENDING**

* RuntimeSession ? implemented
* RuntimeContext ? implemented
* ServiceRegistry ? implemented
* StateStore ? in-memory implementation
* EventStore ? in-memory implementation
* Public Runtime orchestration ? pending
* Full Decision ¡æ State Transition ¡æ Event pipeline integration ? pending
* RuntimeResult integration ? pending

### C. Data Pipeline

**Contract: CLOSED / Implementation: PENDING**

```text
Source ¡æ Raw ¡æ Normalize ¡æ Validate ¡æ Canonical MarketDataSet
```

Remaining:

* source adapters
* normalization implementation
* freshness validation
* missing-data/source-failure handling
* production data integration

### D. Framework Implementation

#### Moon

**Architecture: mostly CLOSED / Implementation: PARTIAL**

Established:

* StrategyResult
* consensus allocation
* execution mapping
* PortfolioTarget

Remaining:

* PortfolioSnapshot
* RebalancePlan
* end-to-end Runtime integration
* data pipeline integration

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

* architecture ? CLOSED
* routing ? IMPLEMENTED
* full Runtime-backed framework execution ? pending

Dashboard:

* presentation-only boundary ? CLOSED
* Runtime-integrated view ? pending

API:

* public Runtime/API error contract ? CLOSED
* concrete endpoint/serialization implementation ? pending/future

## Status Principle

```text
DECIDED
  ¡é
IMPLEMENTATION READY
  ¡é
IMPLEMENTED
  ¡é
VALIDATED
  ¡é
ACTIVE
```

Configuration cannot create approval. A strategy or framework becomes executable only when its governing specification and activation state permit execution.

## Next Implementation Direction

```text
Core Runtime implementation
        ¡é
Canonical Data pipeline
        ¡é
Moon end-to-end vertical slice
        ¡é
Framework-specific implementation
        ¡é
CLI / Dashboard integration
        ¡é
API / durable persistence as required
```

This roadmap does not redefine investment methodology or framework governance.
