# Orion Implementation Status Report

Version: 2.2

Status: Current Baseline

Last Updated: 2026-10-10

## Executive Status

* Core architecture closure is declared by the 2026-10-07 baseline; per-ID evidence and numbering remain under traceability audit.
* Core Runtime orchestration and canonical data handoff exist as in-memory MVP boundaries. Runtime failure residual-effect semantics remain under D-052.
* Framework implementation is partial. ADM is inactive; its signal-to-execution mapping is open under D-051. Portfolio cash valuation/target semantics are open under D-053.
* Data contracts, source-agnostic normalization, structural validation, provider-neutral adaptation, and policy-explicit ADM utilities exist. Production collection and an end-to-end Framework consumer path are not implemented.

## Current Status

| Area | Status | Notes |
|---|---|---|
| Configuration loader | Implemented | typed validation and required-file checks |
| Core domain models | Partial | shared contracts exist; account aggregation and end-to-end portfolio state projection remain |
| RuntimeSession / RuntimeContext | Implemented with known failure gap | executor failures stop the run; post-loop event-recording failure can leave session status `Running` (D-052) |
| StateStore / EventStore | Implemented | in-memory stores; transition-event failure may follow state commit (D-052) |
| Public Orion Runtime | MVP implemented | framework orchestration and optional Decision -> State Transition -> State Commit -> Event lifecycle |
| Durable State/Event storage | Future | outside current MVP |
| Moon | Partial | common target, valuation, rebalance, and explicit sizing-input operations exist; ADM mapping and Runtime rebalance integration remain |
| Aurora | Incomplete | methodology and scoring are not finalized |
| Supernova / Phoenix | Partial | governance and report scaffolding exist; placeholder output is not an authoritative registry |
| Data contracts | Implemented | `MarketDataPoint` / `MarketDataSet` structural contracts |
| Data normalization | Implemented utility | deterministic source-agnostic normalization; not production collection or source-specific validation |
| Provider-neutral adapter | Implemented utility | wraps supplied batches; no live provider, retries, cache, or fallback policy |
| Runtime data handoff | Implemented boundary | data reaches `RuntimeContext`; current report and Moon adapters do not consume it to produce strategy results |
| CLI routing | Implemented | unsupported/scaffold commands still need explicit unavailable behavior and failure exit codes |
| Dashboard | Partial | read-only boundary exists; Runtime presentation integration remains partial |
| Public API | Partial | error boundary is specified; standardized client-facing mapping and endpoints remain |

## Moon Status

The proposal flow for supplied StrategyResults is implemented:

```text
StrategyResult -> ConsensusAllocation -> Execution Mapping -> PortfolioTarget
```

Common-domain operations include PortfolioState/Snapshot records,
caller-supplied valuation, current-allocation projection, deterministic
weight-based `RebalancePlan` construction, and `ExecutionOrder` materialization
from explicit sizing inputs. Account aggregation, authoritative current-state
projection, and Runtime rebalance integration remain pending. Cash inclusion,
target/residual treatment, valuation currency, and FX responsibility remain
unresolved under D-053.

ADM activation remains blocked by D-051 because the current execution mapper
does not accept VTI, VEU, or SGOV as signal keys. `active_strategies` is empty.

## Data Status

```text
Raw source batch -> normalization utility -> MarketDataSet -> RuntimeContext
```

These are available boundaries, not an integrated production pipeline. Runtime
can accept a canonical dataset, but current adapters do not consume it through
ADM to produce a `PortfolioTarget`. Source collection, source-specific
validation/freshness policy, and fallback behavior remain open.

## Test Baseline

Test counts in dated integration notes below are historical snapshots. This
report makes no claim about the current test-suite count; obtain it from a
canonical test run when verification is requested.

## Architecture vs Implementation

Do not interpret incomplete implementation as a new architecture requirement.
The reported `CORE-001` through `CORE-020` baseline is under per-ID provenance
and numbering audit.

## Historical Integration Records

The dated entries below preserve the status and test counts at the time they
were written. They do not override the current status table above.
## 2026-10-07 Runtime Integration Step 2

Runtime now implements the Decision Candidate → Accepted Decision → State Transition → StateStore commit boundary. Acceptance and transition policies remain explicit callables; no Framework directly mutates StateStore. Multiple accepted transitions from one execution are committed as one authoritative `OrionStateSnapshot`. Domain Event creation and EventStore persistence remain the next Runtime workstream.

## 2026-10-08 Runtime Integration Step 7

End-to-end integration verification now covers the Public OrionRuntime with report-capable Framework Adapters and a canonical Decision → StateStore → Domain Event slice. The Step 7 state was intentionally partial at that time. Step 18 subsequently closed the public single-call lifecycle gap; the current Runtime status is recorded in the Step 18 and Governance sections below.


## 2026-10-08 Runtime Integration Step 15

Supernova and Phoenix are integrated at the Framework Runtime boundary through report adapters. Their existing satellite semantics remain Framework-owned; they are not forced into the Common Portfolio Domain and do not generate PortfolioTarget decisions merely because they execute inside the Runtime.

## 2026-10-08 Runtime Integration Step 16

A full five-Framework Runtime matrix now verifies one Public `OrionRuntime.run()` execution across Aurora, Moon, Orbit, Supernova, and Phoenix in registry order. Failure isolation is verified at the failing Framework boundary: later Frameworks are not executed and no partial successful `OrionResult` is returned.

## 2026-10-08 Runtime Integration Step 17 — CORE-012 Lifecycle Audit

The implemented lifecycle was audited against CORE-012 without introducing new architecture. Current status is: Initialize **Implemented**; Configuration **Implemented**; Data **Implemented** at the canonical handoff boundary; State Restore **Partial** (in-memory restore only); Context **Implemented**; Framework Execution **Implemented**; Result Validation **Implemented**; Decision Resolution **Partial** (Session-level API only); State Transition **Partial** (Session-level API only); State Commit **Partial** (Session-level API only); Event Creation **Partial** (Session-level API only); Persistence **Partial** (MVP in-memory stores; durable persistence remains future); Presentation **Implemented**; Completion **Implemented**.

The Step 17 audit recorded the pre-Step 18 gap. Step 18 subsequently connected the existing Decision → State Transition → State Commit → Event pipeline into the public single-call lifecycle without changing Core architecture.

## 2026-10-08 Runtime Integration Step 18 — Public Canonical Lifecycle

The Public `OrionRuntime.run()` supports one canonical single-call lifecycle from
FrameworkResult through Decision Resolution, State Transition, StateStore commit,
and optional correlated Domain Event creation. The framework-only public path
remains backward compatible when lifecycle handlers are omitted.

Step 18 baseline validation: **174 tests passed**. The remaining Runtime partials
are limited to in-memory State Restore and durable Persistence, which remain
outside the MVP boundary defined by D-030.

## 2026-10-08 Runtime Governance — Default Auto-Approval

D-050 establishes Auto-Approval as the default Runtime Decision Acceptance Policy.
The public `OrionRuntime.run()` may therefore omit the acceptance handler during
the canonical lifecycle; the Runtime materializes each `DecisionCandidate` as the
existing `AcceptedDecision` contract. An explicit acceptance handler remains
supported for rejection or conditional acceptance. Framework boundaries and the
State Transition → StateStore → Domain Event lifecycle are unchanged.

Governance validation: **176 tests passed**. Two tests were added to verify the
Auto-Approval contract and public Runtime defaulting behavior.
