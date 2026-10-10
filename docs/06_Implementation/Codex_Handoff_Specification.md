# Orion Codex Handoff Specification

**Baseline:** Step 19 — Runtime Default Decision Acceptance Policy (Auto-Approval)  
**Date:** 2026-10-08  
**Status:** Handoff candidate / architecture freeze

## 1. Purpose

This document is the implementation boundary for Codex work on the Orion Runtime.
Codex must implement only explicitly requested changes and must not redesign the
Core Runtime architecture, investment methodology, or Framework responsibilities.

## 2. Canonical Framework Architecture

Orion has five independent Frameworks:

- Aurora — Market / Environment Monitoring
- Moon — Dynamic Asset Allocation
- Orbit — Static Asset Allocation
- Supernova — Individual Equity Satellite
- Phoenix — Digital Asset Satellite

Moon and Orbit are equal, independent Portfolio / Asset Allocation Frameworks.
Neither Framework is a parent or sub-strategy of the other.

Supernova and Phoenix remain satellite Frameworks and are not forced into the
Common Portfolio Domain.

## 3. Canonical Runtime Lifecycle

```text
MarketData
  -> RuntimeContext
  -> Framework
  -> FrameworkResult
  -> DecisionCandidate
  -> Decision Acceptance Policy
  -> AcceptedDecision
  -> StateTransition
  -> StateStore
  -> Domain Event
  -> EventStore
  -> RuntimeResult / OrionResult
  -> Presentation
```

The Runtime is the orchestration authority.
Frameworks propose decisions; they do not accept decisions, commit state, or
publish events directly.

## 4. Decision Governance

### 4.1 Default policy

The default Runtime Decision Acceptance Policy is **Auto-Approval**.

For a `DecisionCandidate`, the default policy materializes the existing
`AcceptedDecision` contract. It does not create a new decision type.

The current default acceptance marker is:

```text
accepted_by = "orion-runtime:auto-approval"
```

### 4.2 Important distinction

Auto-Approval means automatic **governance acceptance of a Framework proposal**.
It does not mean:

- automatic investment methodology;
- automatic broker order submission;
- automatic fill or settlement;
- automatic transfer of money;
- bypassing StateStore commit rules.

### 4.3 Explicit acceptance remains supported

A caller may provide an explicit acceptance handler to reject or conditionally
accept candidates. Therefore the acceptance boundary must remain explicit even
though the default policy is Auto-Approval.

### 4.4 Framework boundary

A Framework must never construct an authoritative `AcceptedDecision` on behalf
of Runtime Governance or mutate Runtime state/event stores directly.

## 5. State and Event Contract

The following ordering is mandatory:

1. Candidate is produced.
2. Acceptance policy produces `AcceptedDecision` or rejection.
3. Accepted decision produces `StateTransition`.
4. Snapshot and transition events are constructed and staged.
5. Runtime validates the snapshot, transition/entity correlation, and complete
   event batch.
6. Runtime commits the snapshot and events together to their in-memory stores.
7. Runtime returns the resulting `OrionResult`.

No event may represent an uncommitted state transition.
No state commit may occur after a failed transition or failed validation.

## 6. Failure Isolation

- Framework registry order is authoritative for one Runtime execution.
- A Framework failure stops the current execution.
- A failed Framework must not produce a successful partial `OrionResult`.
- Acceptance, transition, snapshot, state commit, and event creation failures
  must propagate deterministically through the Runtime lifecycle.
- Any staging, validation, or store-commit failure leaves both stores unchanged
  and closes the active session as `Error`.
- One `OrionRuntime` instance accepts one public `run()` call.
- Runtime failure must not silently convert an error into acceptance.

## 7. Public Runtime Compatibility

Two intentional public paths exist and must not be collapsed without a new
architecture decision:

### Framework-only path

`OrionRuntime.run(executors)` remains available for framework execution and
report-oriented callers.

### Full lifecycle path

`OrionRuntime.run(...)` can execute the canonical decision/state/event lifecycle
when lifecycle handlers are supplied. If lifecycle mode is entered and no
explicit `accept` handler is supplied, the Runtime uses the default Auto-Approval
policy.

Transition and snapshot handlers remain required for lifecycle execution.

## 8. MVP Scope

The MVP supports:

- in-memory `StateStore`;
- in-memory `EventStore`;
- Runtime lifecycle orchestration;
- Framework execution and validation;
- DecisionCandidate / AcceptedDecision / StateTransition contracts;
- Auto-Approval as default acceptance policy;
- explicit alternative acceptance policy;
- coordinated StateStore/EventStore commit after event staging and validation;
- five-Framework integration.

## 9. Explicitly Deferred Scope

Codex must **not** implement the following unless a new explicit decision is
provided:

- durable StateStore persistence;
- durable EventStore persistence;
- event replay / Event Sourcing;
- production retention policy;
- broker integration;
- order execution, fill, settlement, or reconciliation;
- new investment methodology;
- Framework-specific trading logic;
- automatic portfolio rebalancing logic;
- architecture redesign unrelated to the requested task.

D-030 remains authoritative for durable persistence/replay scope.

## 10. Architecture Invariants

Codex must preserve all of the following:

1. Runtime owns orchestration.
2. Frameworks do not own orchestration.
3. Frameworks do not mutate `StateStore` or `EventStore` directly.
4. Moon and Orbit remain independent Frameworks.
5. Common Portfolio Domain remains limited to the applicable portfolio
   architecture; Supernova/Phoenix are not forcibly converted into it.
6. `DecisionCandidate` is non-authoritative.
7. `AcceptedDecision` is explicit and authoritative for the acceptance boundary.
8. Auto-Approval is a Runtime Governance policy, not investment methodology.
9. Transition events are staged before commit and recorded only with the
   corresponding successful StateStore commit.
10. Durable persistence/replay remains deferred.
11. Existing backward-compatible framework-only Runtime behavior is preserved.

## 11. Allowed Change Principle

Codex should use the smallest implementation change that satisfies the explicit
request.

Do not rename or restructure existing Core contracts merely for stylistic
improvement. Do not introduce abstractions unless they are required by an
explicit acceptance criterion.

## 12. Required Validation

Every Codex implementation must provide:

- full test-suite execution;
- no regression of existing tests;
- tests for every changed contract or lifecycle behavior;
- verification that Framework failure does not yield a successful partial result;
- verification that event-factory, validation, and store-append failures leave
  both stores unchanged;
- verification that one Runtime instance rejects a second public run;
- verification that snapshot execution identity and transition-to-candidate
  identity are enforced;
- verification that default acceptance is Auto-Approval when lifecycle mode is
  entered without an explicit acceptance handler;
- verification that explicit acceptance handlers still support rejection;
- verification that Framework-only `run()` remains backward compatible.

## 13. Current Baseline

The historical Step 19 baseline was validated with:

```text
176 passed
```

The D-052 Runtime atomicity update was subsequently validated against the full
repository test suite on 2026-10-10.

This test count is a baseline reference, not a permanent requirement that the
suite remain exactly 176 tests after legitimate Codex changes. Any changed test
count must be explainable by the requested work.

## 14. Files / Areas Requiring Particular Protection

Codex must treat the following as protected architectural areas unless the task
explicitly names them:

- `src/orion/core/runtime_engine.py`
- `src/orion/core/runtime_session.py`
- `src/orion/core/decision.py`
- `src/orion/core/state_store.py`
- `src/orion/core/event_store.py`
- `src/orion/core/events.py`
- Framework registry and Framework adapter boundaries
- Core Architecture Decision documents
- D-030 persistence boundary

A change to these areas is allowed only when directly required by the handoff
request and must preserve the invariants in this document.

## 15. Completion Criteria for Codex Handoff

The handoff is complete when:

- this specification is frozen;
- Step 19 is synchronized to Git;
- the full test suite passes;
- no unresolved architecture blocker exists;
- deferred scope is explicitly preserved;
- Codex receives this document together with the Step 19 baseline.
