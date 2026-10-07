# Implementation Roadmap

Version: 2.0

Status: Active

Last Updated: 2026-10-07

## Purpose

Defines the current software implementation sequence after the Core Architecture Review.

## Architecture Status

Core architecture is **closed** by `CORE-001` through `CORE-020`. Remaining work in Core is implementation and validation, not another architecture redesign.

## Workstream A — Core Runtime

Status: Implementation Pending

1. Public Orion Runtime entry point — Partial: `RuntimeSession.execute_frameworks()` now provides the initial orchestration boundary
2. Full runtime lifecycle orchestration — Pending: Decision/State/Event pipeline remains
3. Framework execution isolation — Partial: explicit executor boundary and failure transition are implemented
4. FrameworkResult collection/validation — Implemented for the initial orchestration boundary
5. Decision resolution boundary — implemented in RuntimeSession
6. State Transition + StateStore commit — implemented in RuntimeSession
7. Domain/Lifecycle Event creation — implemented: execution-correlated EventStore append boundary; state-transition events are created only after successful StateStore commit
8. RuntimeResult construction — partial: OrionResult now returns the execution EventStore view

## Workstream B — Data Pipeline

Status: Contract Closed / Implementation Pending

1. Source adapters
2. Raw-to-normalized transformation
3. Validation and freshness checks
4. Canonical MarketDataSet production
5. Runtime data handoff integration

## Workstream C — Moon Vertical Slice

Status: Partial

Already established:

* StrategyResult
* consensus allocation
* execution mapping
* PortfolioTarget

Next:

* PortfolioSnapshot
* RebalancePlan
* Runtime integration
* CLI end-to-end execution

## Workstream D — Frameworks

Implement only after each Framework's governing specification is sufficiently complete.

* Aurora — methodology first, then implementation
* Supernova — framework governance first, then engine integration
* Phoenix — category/leader/scoring governance first, then engine integration

## Workstream E — Presentation / API

* CLI full Runtime integration — Pending: command handlers still expose legacy framework-specific commands
* Dashboard Runtime integration — Partial: Dashboard consumes only `OrionResult.dashboard_data`; framework-engine dependency is explicitly prohibited and regression-tested
* API implementation when required

## Workstream F — Future Infrastructure

Not current Core blockers:

* durable State/Event persistence
* replay/event-sourcing capabilities
* production storage technology
* retention infrastructure
* distributed runtime

## Implementation Rules

* Documentation/approved contract precedes new business behavior.
* Do not invent investment methodology.
* Do not activate unresolved strategies.
* Do not move investment logic into CLI, Dashboard, or Data layer.
* Do not create generic abstractions without a concrete responsibility.
* Do not reopen Core architecture for normal implementation gaps.
