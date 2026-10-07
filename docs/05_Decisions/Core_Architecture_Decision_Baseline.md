# Core Architecture Decision Baseline

Version: 1.0

Status: Approved / Closed

Date: 2026-10-07

## Purpose

This file provides a single navigation point for the closed Core Architecture baseline. The detailed historical decisions remain in `Decision_Log.md`.

## Decision Set

`CORE-001` through `CORE-020` establish the following canonical contracts:

1. Terminology / Engine hierarchy
2. Source of Truth vs Derived values
3. Event Contract
4. Runtime Lifecycle
5. Persistence and Source-of-Truth boundaries
6. Framework ↔ Core interface
7. Decision Contract
8. State Transition Contract
9. Error and Failure Contract
10. Observability and Audit
11. Canonical Domain Model and Ownership
12. Canonical Runtime Execution Sequence
13. Configuration / Registry / RuntimeContext
14. Data Contract and Runtime Data Handoff
15. StateStore / EventStore / Repository boundary
16. Result Contract
17. Runtime Execution Identity / Correlation
18. Public Runtime / API Error Contract
19. Canonical Domain ↔ Ownership Mapping
20. Documentation Authority and Contract Precedence

## Closure Status

**Core Architecture: CLOSED**

**Core architectural blockers: 0**

Remaining work is implementation, validation, Framework-specific specification, or future infrastructure.

## Canonical Flow

```text
Configuration + Validated Data + Authoritative State
                    ↓
              RuntimeContext
                    ↓
                Framework
                    ↓
             FrameworkResult
                    ↓
          Decision Candidate
                    ↓
          Accepted Decision
                    ↓
            State Transition
                    ↓
               StateStore
                    ↓
          Authoritative State + Domain Event
                    ↓
              EventStore
                    ↓
              RuntimeResult
```

## Important Boundaries

* Aurora, Moon, Orbit, Supernova, and Phoenix are Frameworks.
* Engine is a calculation/analysis module inside a Framework.
* Frameworks cannot directly mutate StateStore/EventStore or update Dashboard state.
* Calculation results do not automatically become authoritative State.
* Domain Events are immutable historical facts and are emitted after successful State commit.
* Event Sourcing is not adopted.
* Frameworks consume canonical `MarketDataSet` rather than raw provider-specific data.
* `src/data` is a shared data-contract package, not an investment Framework.

## Reopening Rule

Do not reopen this baseline for implementation details already covered by the existing contracts. A new Core decision is warranted only when a genuinely new cross-framework architectural requirement appears.
