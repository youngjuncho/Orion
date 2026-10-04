# Orion Implementation Review

## 1. Purpose

This document reviews the current Orion implementation state during the transition from documentation to implementation.

The purpose of this review is not to redesign Orion.

It is to determine:

* what has already been decided,
* what is sufficiently specified for implementation,
* what is genuinely unresolved,
* what currently blocks implementation,
* what can proceed independently,
* and what should be deferred.

The review exists as a temporary control point for the current implementation stage.

Permanent decisions and project knowledge must be promoted to the appropriate documents under `docs/`.

---

# 2. Executive Assessment

## 2.1 Overall conclusion

Orion is **not going in the wrong architectural direction**.

The current implementation broadly follows the intended separation between:

```text
CLI
  ↓
Dashboard / Framework Entry Points
  ↓
Frameworks
  ↓
Core Models / Services
```

The architectural boundary established by D-023 remains valid:

```text
                     Orion
                       │
         ┌─────────────┴─────────────┐
         │                           │
      Aurora                   Portfolio Engines
  Monitoring Layer          ┌────────┼────────┐
                            Moon  Supernova  Phoenix
```

Aurora is the Monitoring Layer.

Moon, Supernova, and Phoenix are independent Portfolio Engines.

Dashboard remains presentation-only.

These boundaries should not be changed merely to simplify implementation.

---

## 2.2 What the first implementation pass demonstrated

The first implementation pass exposed an important fact:

> The primary problem is no longer missing Python scaffolding.

The implementation has reached the boundary of what the current documentation specifies in sufficient detail.

When Codex encounters an undefined rule, it should therefore stop rather than invent investment behavior.

This is expected behavior.

The correct response is:

```text
Implementation
      ↓
Specification boundary discovered
      ↓
Review
      ↓
Decision / Specification
      ↓
Permanent documentation
      ↓
Implementation resumes
```

Not:

```text
Implementation
      ↓
Guess
      ↓
Patch
      ↓
More code
```

---

# 3. Current Implementation Baseline

The current repository contains the main application areas required by the architecture:

```text
src/
├── data/
└── orion/
    ├── cli/
    ├── core/
    ├── dashboard/
    ├── frameworks/
    │   ├── aurora/
    │   ├── moon/
    │   ├── phoenix/
    │   └── supernova/
    └── services/
```

The implementation has already established:

* core models,
* configuration loading and validation,
* CLI routing,
* framework scaffolds,
* dashboard presentation layer,
* initial framework models and report entry points.

The supplied repository snapshot was executable and its current test suite passed.

However:

> Passing tests are not evidence that the investment methodologies are complete.

The current tests primarily validate contracts, models, validation, routing, state transitions, and currently implemented calculation components.

They do not establish that the complete investment pipelines are implemented.

---

# 4. Architecture Status

## 4.1 Preserve

The following architectural decisions are considered established and should not be reopened merely because implementation is inconvenient.

### Aurora

Aurora is the Monitoring Layer.

It provides:

* Market Regime
* Risk State
* Transition Risk
* Market Context / Commentary

Aurora does not directly manage portfolios.

Aurora does not generate buy/sell instructions.

### Moon

Moon is the ETF Portfolio Engine.

### Supernova

Supernova is the Equity Portfolio Engine.

### Phoenix

Phoenix is the Digital Asset Portfolio Engine.

### Dashboard

Dashboard is a presentation layer.

It consumes framework outputs.

It does not own:

* investment logic,
* scoring logic,
* allocation logic,
* regime logic.

---

# 5. Architecture Documentation Drift

## 5.1 Python package structure

The current source tree has already evolved substantially.

The implementation currently uses:

```text
src/orion/
```

with framework packages beneath it.

The previous proposed deeper hierarchy containing:

```text
runtime/
domain/
infrastructure/
config/
utils/
```

is not currently implemented.

### Review decision

Do not perform another large package migration at this stage.

Instead:

1. Treat the current package structure as the V1 implementation baseline.
2. Update package-structure documentation to match reality.
3. Explicitly document the role of `src/data/`.
4. Treat deeper separation as future refactoring unless implementation requires it.

The project should not enter another architecture-driven migration before the investment engines are working.

---

# 6. `src/data` Boundary

The current implementation uses:

```text
src/data/
```

for shared data contracts.

For V1, this boundary should remain explicit.

`src/data/` may contain:

* observation contracts,
* market-data batch contracts,
* validation contracts,
* normalized data contracts.

It must not contain:

* investment logic,
* framework logic,
* scoring logic,
* portfolio decisions.

The current data layer should remain contract-oriented until the corresponding data service is deliberately implemented.

---

# 7. Framework Implementation Status

## 7.1 Aurora

### Implemented

* report model,
* indicator model,
* regime model,
* engine scaffold,
* report entry point.

### Not yet implemented

* final scoring,
* regime calculation,
* state momentum,
* transition-risk calculation.

### Classification

```text
SPEC
```

Aurora should not receive invented scoring logic.

Before implementation of business behavior, the following must be explicitly specified:

```text
indicator definitions
component scoring
Aurora score
regime thresholds
state momentum
transition risk
```

---

## 7.2 Moon

Moon is currently the most important implementation target.

### Implemented

* strategy model,
* allocation model,
* portfolio model,
* engine scaffold,
* report entry point,
* currently implemented ADM calculation components.

### Not yet complete

* PortfolioSnapshot and RebalancePlan construction (post-MVP),
* ADM defensive-asset choice and market-observation rules,
* ADM execution mappings,
* complete end-to-end CLI execution.

### Classification

```text
DECISION + SPEC + IMPLEMENT
```

Moon is therefore neither "not started" nor "implementation-ready".

It is the first Framework where implementation has exposed concrete specification boundaries.

---

# 8. Moon as the Current Implementation Frontier

The immediate target should be a single end-to-end Moon vertical slice.

The intended flow is:

```text
Market Data
    ↓
ADM
    ↓
StrategyResult
    ↓
Consensus
    ↓
Execution Mapping
    ↓
Portfolio Target
    ↓
Moon State
    ↓
Moon Report
    ↓
CLI
```

Do not implement all five Moon strategies simultaneously.

First make one complete strategy work end-to-end.

The implementation is considered meaningful only when the entire flow works without business-logic placeholders.

---

# 9. Moon Decisions and Specifications

The following areas require explicit attention before the corresponding implementation can be considered complete.

## 9.1 Portfolio contracts

Decision D-027 establishes the canonical Moon portfolio flow:

```text
Portfolio
ConsensusAllocation
PortfolioTarget
PortfolioSnapshot
RebalancePlan
```

`PortfolioTarget` construction and validation are implemented. Snapshot and
rebalance construction are outside the current MVP boundary. The canonical
decision should not be redefined in multiple documents.

---

## 9.2 ADM methodology

The following ADM decisions remain open:

```text
ADM OI-001
Market observation date / freshness / missing-data rules
```

OI-002 and OI-003 were resolved by D-028: use adjusted-price total return,
with dividend adjustment handled by the normalized data layer. Remaining
market-data rules must be resolved from the authoritative Orion contract.

The coding agent must not infer missing methodology from common investment practice.

In particular, calculations involving:

* price history,
* defensive selection,

must follow the approved Orion methodology.

---

## 9.3 Execution Mapping

The distinction between:

```text
Signal / Research Asset
```

and:

```text
Execution Asset
```

must be preserved.

The mapping must be explicit.

An unmapped execution asset should result in an explicit failure rather than silent substitution.

---

# 10. Moon Operational Configuration

Configuration represents:

```text
Operational State
```

not:

```text
Research Notebook
```

Only implementation-ready and operationally approved strategies should be treated as active runtime configuration.

Configuration must not imply that an unfinished strategy is executable.

Therefore the operational Moon configuration must be made truthful before the Moon MVP is considered complete.

---

# 11. Supernova

## Current implementation

Implemented:

* report model,
* theme model,
* candidate-company model,
* approved-company model,
* engine scaffold,
* report entry point.

Not yet implemented:

* final company scoring,
* theme weighting,
* leadership determination,
* state thresholds,
* watchlist lifecycle,
* replacement rules,
* DCA behavior.

### Classification

```text
SPEC
```

The 5D framework exists conceptually, but the implementation-ready evaluation methodology is not yet sufficiently closed.

Do not invent company-scoring rules merely to complete the Python implementation.

---

# 12. Phoenix

## Current implementation

Implemented:

* report model,
* category model,
* candidate-asset model,
* leader model,
* challenger model,
* engine scaffold,
* report entry point.

Not yet implemented:

* final category methodology,
* leader metrics,
* challenger metrics,
* replacement-risk calculation,
* leadership-transition behavior,
* review-trigger implementation.

### Existing portfolio-construction decision

Phoenix invests only in approved category leaders.

Challengers and watchlist assets are used for monitoring and replacement evaluation.

They are not eligible for portfolio inclusion.

Approved leaders are equally weighted.

BTC and ETH are managed separately from Phoenix.

These are established decisions and should not be reopened during implementation unless the governing decision is explicitly reconsidered.

### Classification

```text
SPEC
```

The remaining work is primarily to close the evaluation methodology sufficiently for implementation.

---

# 13. Dashboard

The dashboard boundary is correct.

Current implementation provides:

* dashboard presentation models,
* read-only dashboard composition,
* textual rendering,
* CLI dashboard integration.

The dashboard must remain presentation-only.

The current direct construction of Framework engines is acceptable as a scaffold, but the target architecture is:

```text
CLI
  ↓
OrionEngine / Runtime
  ↓
Framework Results
  ↓
Orion State
  ↓
Dashboard View Model
  ↓
Dashboard
```

The dashboard should not become the orchestration layer.

### Classification

```text
IMPLEMENT LATER
```

Richer dashboard work should wait until framework outputs and data contracts are stable.

---

# 14. CLI

The CLI structure is already useful.

Implemented routing includes commands for:

* version,
* health,
* config,
* dashboard,
* data status/update,
* Moon,
* Aurora,
* Supernova,
* Phoenix.

However, many framework commands currently return placeholder responses.

The correct sequence is:

```text
Define command output contract
        ↓
Connect to real engine/service
        ↓
Test
        ↓
Mark implemented
```

Do not add commands simply because they appear in documentation.

The CLI should consume the application engine rather than become another location for business logic.

---

# 15. Runtime and API

The complete Runtime/API architecture should not be implemented before the first real end-to-end Framework execution exists.

The recommended sequence is:

```text
Moon end-to-end
      ↓
OrionEngine
      ↓
RuntimeSession
      ↓
Services
      ↓
Result
      ↓
State
      ↓
Events
```

Only after this is working should the complete Runtime/API layer be expanded.

The API documentation currently describes operations such as:

```text
run()
run_framework()
get_state()
get_events()
get_services()
report()
dashboard()
health()
shutdown()
```

but these should not be implemented merely to satisfy documentation.

First establish one real execution path.

Then expose API operations around that real engine.

---

# 16. Data Infrastructure

The data layer should be implemented after the ADM methodology and required data contracts are frozen.

Target:

```text
Yahoo Finance
    ↓
Raw Data
    ↓
Normalization
    ↓
Validation
    ↓
MarketDataSet
    ↓
ADM
```

The current `src/data` contract layer should remain contract-oriented until this stage.

---

# 17. What Actually Blocks Codex?

A problem is considered an implementation blocker only when the missing information prevents the next coherent implementation step.

The current review identifies the following primary blockers:

### Blocking

```text
1. Canonical Moon portfolio contracts
2. ADM unresolved methodology issues
3. ADM execution mappings
4. Truthful operational Moon configuration
```

These directly affect the Moon end-to-end MVP.

### Not currently blocking Moon

```text
1. Final Aurora scoring
2. Final Supernova scoring
3. Final Phoenix scoring
4. Rich dashboard rendering
5. Complete public API
6. Historical state persistence
7. Full data infrastructure
```

These remain important, but they should not be allowed to block the first Moon vertical slice unless a new dependency is demonstrated.

---

# 18. What Codex Can Continue Doing

While a decision is unresolved, Codex should continue independent implementation where the specification is sufficient.

Examples:

```text
- contract cleanup
- test improvements
- command wiring where output contracts are known
- documentation reconciliation
- non-business-logic refactoring
- validation
- deterministic model construction
```

Codex should stop only at the actual specification boundary.

---

# 19. What Codex Must Not Do

Codex must not:

* invent investment methodology,
* infer missing thresholds,
* silently choose between conflicting documents,
* make tests define undocumented business policy,
* introduce investment logic into Dashboard,
* introduce investment logic into the data layer,
* duplicate business logic in CLI,
* perform another large package migration merely to match an older document,
* mark a scaffold as implemented because a Python class exists.

If a genuine investment-policy rule is missing:

```text
STOP
↓
Record the exact unresolved rule
↓
Return the blocker
```

A placeholder is preferable to invented investment behavior.

---

# 20. Implementation-Ready Definition

A Framework or feature is implementation-ready only when all relevant items below are defined:

```text
[ ] Purpose
[ ] Inputs
[ ] Outputs
[ ] Data types
[ ] Calculation rules
[ ] Thresholds
[ ] State transitions
[ ] Error behavior
[ ] Configuration ownership
[ ] Review cadence
[ ] Governance status
[ ] Deterministic example
```

If a required item is missing:

```text
DO NOT IMPLEMENT BUSINESS LOGIC
```

---

# 21. Definition of Done

A feature is not complete merely because its Python class exists.

The expected chain is:

```text
Documentation
      ↓
Approved Contract
      ↓
Implementation
      ↓
Unit Tests
      ↓
Integration Test
      ↓
CLI/API Consumer
      ↓
Status Report
```

These layers must remain aligned.

---

# 22. Recommended Implementation Order

The current recommended order is:

```text
1. Reconcile documentation with current package structure
        ↓
2. Establish canonical domain-model mapping
        ↓
3. Stabilize Moon contracts
        ↓
4. Resolve ADM methodology blockers
        ↓
5. Resolve ADM execution mappings
        ↓
6. Make Moon configuration truthful
        ↓
7. Complete one Moon/ADM end-to-end vertical slice
        ↓
8. Build required data infrastructure
        ↓
9. Establish Orion Runtime
        ↓
10. Expand to Aurora
        ↓
11. Expand to Supernova
        ↓
12. Expand to Phoenix
```

This order deliberately avoids broad implementation across all Frameworks before the first complete portfolio-engine pipeline is proven.

---

# 23. Review Exit Criteria

This implementation review may be considered closed for the current stage when:

```text
[ ] Current package structure is documented accurately
[ ] Domain model has one canonical mapping
[x] Moon portfolio contracts are resolved
[ ] ADM OI-001 is resolved
[x] ADM OI-002 is resolved
[x] ADM OI-003 is resolved
[ ] ADM execution mappings are approved
[ ] Moon operational configuration is truthful
[ ] One Moon/ADM vertical slice is implementation-ready
[x] Relevant tests are defined
[ ] Implementation roadmap reflects actual state
```

At that point, implementation should resume.

The next target is **not another broad documentation expansion**.

The next target is:

```text
Moon end-to-end MVP
```

---

# 24. Final Assessment

The first implementation pass should be considered successful.

It has established the initial executable structure and, more importantly, exposed the boundary between:

```text
What Orion has already decided
```

and:

```text
What Orion has not yet decided or specified sufficiently
```

The project should therefore not respond to the current situation by writing more placeholder code.

Instead:

```text
DECIDE
    ↓
SPECIFY
    ↓
IMPLEMENT
    ↓
TEST
    ↓
REPORT
    ↓
REVIEW
```

The purpose of the current `review/` directory is to control this transition.

Once the relevant decisions and specifications have been promoted to the permanent documentation, the temporary review material can be closed or replaced by the next development-stage review.
