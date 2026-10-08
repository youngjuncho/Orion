# Implementation Roadmap

Version: 2.1

Status: Active

Last Updated: 2026-10-08

## Purpose

Defines the current software implementation sequence after the Core Architecture Review.

## Architecture Status

Core architecture is **closed** by `CORE-001` through `CORE-020`. Remaining work in Core is implementation and validation, not another architecture redesign.

## Workstream A — Core Runtime

Status: MVP Complete — canonical Runtime lifecycle implemented; durable persistence remains deferred

1. Public Orion Runtime entry point — Implemented: `OrionRuntime.run()` is the public application boundary and delegates to `RuntimeSession`
2. Full runtime lifecycle orchestration — Implemented for the MVP: public `OrionRuntime.run()` supports the canonical Decision → State Transition → State Commit → Event lifecycle; durable production persistence remains deferred
3. Framework execution isolation — Implemented: explicit executor boundary and failure transition are implemented and validated
4. FrameworkResult collection/validation — Implemented for the initial orchestration boundary
5. Decision resolution boundary — implemented in RuntimeSession
6. State Transition + StateStore commit — implemented in RuntimeSession
7. Domain/Lifecycle Event creation — implemented: execution-correlated EventStore append boundary; state-transition events are created only after successful StateStore commit
8. RuntimeResult construction — Implemented for the current execution boundary: OrionResult returns FrameworkResults, StateStore snapshot, EventStore view, and dashboard data

## Workstream B — Data Pipeline

Status: Contract Closed / Implementation Pending

1. Source adapters
2. Raw-to-normalized transformation
3. Validation and freshness checks
4. Canonical MarketDataSet production
5. Runtime data handoff integration

## Workstream C — Moon Vertical Slice

Status: Partial — Runtime vertical slice established through PortfolioTarget proposal

Already established:

* StrategyResult
* consensus allocation
* execution mapping
* PortfolioTarget
* Moon Runtime adapter exposing PortfolioTarget as DecisionCandidate
* Public Runtime integration test for the Moon proposal boundary

Next:

* PortfolioSnapshot — existing common contract validated
* RebalancePlan — implemented as deterministic target/current-weight delta operation
* Runtime integration — pending explicit PortfolioState/current-weight handoff
* ExecutionOrder — canonical materialization boundary implemented with explicit sizing inputs; quantity policy remains external
* CLI end-to-end execution

## Workstream D — Frameworks

Implement only after each Framework's governing specification is sufficiently complete.

* Aurora — methodology first, then implementation
* Supernova — framework governance first, then engine integration
* Phoenix — category/leader/scoring governance first, then engine integration

## Workstream E — Presentation / API

* CLI full Runtime integration — Partial: report commands use the Public OrionRuntime; legacy framework-specific commands remain
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

### Runtime Integration Update — Step 6

- Framework Adapter boundary: Implemented for report-capable Aurora, Moon, Supernova, and Phoenix engines.
- CLI Runtime integration: Implemented for their `report` commands.
- Orbit adapter: Deferred until explicit Portfolio/Target execution inputs are supplied; no synthetic identifiers are introduced.
- Existing framework domain APIs remain unchanged.

### Runtime Integration Update — Step 7

- Added end-to-end integration tests covering the Public OrionRuntime → Framework Adapter → FrameworkResult boundary across Aurora, Moon, Supernova, and Phoenix.
- Added a canonical Decision → StateStore → Domain Event integration slice test.
- Current verification baseline: 150 tests passing.
- The public `OrionRuntime.run()` intentionally remains a FrameworkResult execution boundary; full production Decision/State/Event orchestration in one public call is not marked complete until explicit production decision-resolution inputs and data handoff are integrated.

## Runtime Integration Update — Step 18/19

- Public `OrionRuntime.run()` now supports the canonical Decision → State Transition → State Commit → Event lifecycle.
- Runtime Decision Acceptance Governance defaults to Auto-Approval while preserving an explicit acceptance-handler boundary for rejection or conditional acceptance.
- Framework-only `run()` remains backward compatible.
- Durable persistence, replay, broker execution, and investment methodology remain outside the MVP scope.
- Verification baseline: 176 tests passing.

## Runtime Integration Update — Step 8

- Added the `MarketDataProvider` runtime-facing contract for canonical data handoff.
- `OrionRuntime.run()` now accepts either a validated `MarketDataSet` or a provider returning one.
- The Runtime rejects simultaneous direct and provider data inputs.
- Frameworks continue to receive only canonical `MarketDataSet` through `RuntimeContext`.
- Source adapters, raw-to-normalized transformation, validation/freshness policy, and production storage remain pending.
- Verification baseline: 153 tests passing.

### Runtime Integration Update — Step 9

- Added `MoonPortfolioAdapter` to expose the existing `StrategyResult → ConsensusAllocation → PortfolioTarget` lifecycle through the canonical Runtime `FrameworkResult → DecisionCandidate` boundary.
- Added a Moon vertical-slice integration test covering Runtime → Moon Engine → PortfolioTarget proposal.
- Fixed a deterministic Decimal normalization issue in Moon execution-asset mapping so valid consensus weights satisfy the Common `PortfolioTarget` exact-total contract.
- RebalancePlan and ExecutionOrder remain outside this slice because current-state weights and executable quantities are not supplied by the existing Moon Runtime input contract.
- Verification baseline: 155 tests passing.


### Runtime Integration Update — Step 10

- Added the canonical `build_rebalance_plan()` operation from current allocations to `RebalancePlan`.
- Rebalance planning remains weight-based and deterministic; zero-delta assets are omitted.
- Concrete `ExecutionOrder` quantity generation remains pending because portfolio valuation and/or price inputs are not yet part of the current Runtime handoff.
- No synthetic valuation, price, or order quantity was introduced.

### Runtime Integration Update — Step 11

- Added the common `PortfolioValuation` contract for authoritative portfolio valuation inputs.
- Added `value_portfolio_state()` using caller-supplied normalized prices; no price discovery or FX conversion is performed in the portfolio layer.
- Added `current_allocations_from_valuation()` with explicit cash included in total portfolio value.
- Added `build_rebalance_plan_from_state()` to connect `PortfolioState` + valuation inputs to the canonical `RebalancePlan`.
- Added `ExecutionSizingInput` as the explicit boundary for already-resolved executable quantities and order identities.
- Added `build_execution_orders()` to materialize canonical `ExecutionOrder` objects without calculating prices, quantities, fees, lot sizes, or broker constraints.
- Quantity-sizing policy remains external and is not invented by the common Portfolio Domain.
- Verification baseline: 162 tests passing.

### Runtime Integration Update — Step 13

- Validated that `ExecutionOrder` materialization is the terminal output of the current Moon execution-domain slice.
- Added regression coverage confirming materialization preserves `status="planned"` and does not represent broker execution or fill.
- Reconfirmed D-027 boundary: broker submission, fills, settlement, ledger mutation, and actual holding updates remain outside the current Moon MVP.
- Verification baseline: 163 tests passing.
