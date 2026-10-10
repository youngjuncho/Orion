# Orion Implementation Review - Core Traceability Audit

Version: 2.0

Review Date: 2026-10-10

## Executive Decision

**Core Architecture closure claim: UNDER TRACEABILITY AUDIT**

The 2026-10-07 baseline reports `CORE-001` through `CORE-020` as closed, but
does not map each identifier to an individual decision/evidence record. Treat
that numbered set as a reported baseline until its provenance and numbering
are reconciled. This review does not invent missing decisions.

## Canonical Runtime

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
               Acceptance
                    ↓
          Accepted Decision
                    ↓
            State Transition
                    ↓
               StateStore
                    ↓
          Authoritative State
                    ↓
              Domain Event
                    ↓
               EventStore
                    ↓
              RuntimeResult
```

## Canonical Data Pipeline

```text
External Source → Raw → Normalization → Validation → Canonical MarketDataSet → Framework
```

## Canonical Portfolio Model

```text
StrategyResult → ConsensusAllocation → PortfolioTarget → RebalancePlan → ExecutionOrder → ExecutionResult
```

`PortfolioSnapshot` is independent current portfolio state and is an input to `RebalancePlan`.

## Architecture Topics Reported as Closed

The baseline lists the following topics as closed. Their per-ID decision evidence is still being reconciled:

* terminology and Framework hierarchy
* Runtime lifecycle
* Framework contract
* Decision contract
* State Transition contract
* Event semantics
* Error/failure contract
* Persistence boundaries
* Data handoff
* execution identity/correlation
* canonical domain ownership
* package baseline
* roadmap/status reconciliation

## Current Implementation Status (2026-10-10)

The source tree now implements more than the original closure review recorded.
The following status reflects the implemented boundaries, not production
readiness or a claim that downstream external systems are integrated.

Implemented MVP boundaries:

* Public `OrionRuntime.run()` and `RuntimeSession` framework orchestration.
* Optional Decision acceptance, State Transition, StateStore commit, and
  execution-correlated EventStore append lifecycle.
* `MarketDataSet` direct/provider handoff to framework `RuntimeContext`.
* Common `PortfolioState` / `PortfolioSnapshot` records, caller-supplied
  valuation, current allocation projection, deterministic `RebalancePlan`,
  and `ExecutionOrder` materialization from explicit sizing inputs.
* Moon proposal boundary through the common `PortfolioTarget` and
  `DecisionCandidate` contracts.

Still pending or deliberately outside the current boundary:

* A production data pipeline: source-specific adapters, collection,
  freshness policy, semantic validation, and fallback behavior.
* A portfolio state projection from one or more Accounts and a Runtime handoff
  of authoritative portfolio state/current weights into Moon rebalance planning.
* End-to-end Moon rebalance integration. The present portfolio operations are
  callable domain functions, not an execution lifecycle wired into Runtime.
* Order sizing policy, broker submission, fills, settlement, ledger updates,
  and resulting position/cash mutation.
* Framework methodology/governance that remains unresolved in Aurora,
  Supernova, and Phoenix specifications.
* Full CLI/Dashboard integration and a client-facing API error mapping.
* Durable State/Event persistence, replay, and production infrastructure.

The current public Runtime lifecycle is an in-memory MVP. Framework-only
execution remains supported. Auto-Approval is the current default acceptance
policy when callers opt into the decision lifecycle; it does not supply
portfolio execution or broker approval.

Future:

* durable State/Event storage
* replay/event sourcing capabilities
* production infrastructure choices

## Documentation Authority

1. Decision Log — approved historical decisions
2. Core Contract documents — Runtime/State/Event/Decision/Error/Persistence/Data semantics
3. Canonical Domain Model — object meaning and ownership
4. Framework Specification — framework methodology and governance
5. Operational Configuration — current approved operational settings
6. Python implementation — implementation of approved contracts
7. Tests — validation of approved contracts

If a conflict cannot be resolved by ownership and approved decisions, stop and create an explicit Open Question rather than guessing.

## Closure Rule

Do not reopen Core architecture for normal implementation gaps. A new Core decision is required only for a genuinely new cross-framework architectural requirement not covered by `CORE-001` through `CORE-020`.
