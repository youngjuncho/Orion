# Orion Decision Queue

## 1. Purpose

This document contains only the decisions that must be resolved to allow Orion implementation to proceed correctly.

It is not a permanent decision log.

When a decision is made, it must be promoted to the appropriate document under:

```text
docs/05_Decisions/
```

and all affected Framework / Research / Implementation documents must be updated.

When a decision is made, it must be promoted to the appropriate permanent record under:

```text
docs/05_Decisions/
```

The permanent record is the Decision Log and, where required, a dedicated decision document.

All affected Framework / Research / Implementation documents must then be updated.

> **Review identifies decisions. `05_Decisions` preserves decisions.**

The Decision Queue is a working queue, not the authoritative historical record.

Once a decision has been promoted and its affected documentation has been reconciled, the corresponding queue item may be marked `DECIDED`.

---

# 2. Decision Status

Each item uses one of the following statuses:

| Status          | Meaning                                                                  |
| --------------- | ------------------------------------------------------------------------ |
| `OPEN`          | A genuine decision is still required                                     |
| `PROPOSED`      | A preferred option has been identified but not yet approved              |
| `DECIDED`       | Decision has been made and must be promoted to permanent documentation   |
| `SPEC_REQUIRED` | Direction is known, but implementation-level specification is incomplete |
| `DEFERRED`      | Valid issue, but not required for the current milestone                  |
| `BLOCKED`       | Prevents the current implementation slice from proceeding                |

---

# 3. Decision Priority

## Current implementation priority

```text
P0 — Must resolve before Moon MVP
P1 — Must resolve before the affected Framework is implemented
P2 — Important, but does not block current implementation
```

The immediate implementation target is:

```text
Moon
  ↓
one complete strategy
  ↓
end-to-end vertical slice
```

Therefore decisions unrelated to the Moon MVP must not unnecessarily block current implementation.

---

# 4. P0 — Moon Portfolio Contract

## ID

`DQ-MOON-001`

## Status

`DECIDED`

## Priority

`P0`

## Problem

The existing documentation uses `Portfolio` inconsistently.

Different documents currently imply that `Portfolio` may contain:

* allocation,
* current holdings,
* target holdings,
* rebalance date,
* execution orders.

The Python implementation does not represent all of these concepts in one object.

The implementation therefore needs a canonical domain model before additional portfolio behavior is implemented.

## Required decision

Adopt the conceptual separation:

```text
StrategyResult
    ↓
ConsensusAllocation
    ↓
PortfolioTarget
    ↓
RebalancePlan
    ↓
ExecutionOrder
```

and independently:

```text
PortfolioSnapshot
    ↓
Current Holdings
```

Then:

```text
PortfolioTarget + PortfolioSnapshot
            ↓
       RebalancePlan
```

## Proposed V1 interpretation

### StrategyResult

One strategy's output.

```text
Strategy
Signal
Allocation
Score / supporting information
```

### ConsensusAllocation

Aggregated allocation resulting from multiple strategies.

It represents the strategy-level consensus.

### PortfolioTarget

The desired allocation using actual execution assets.

### PortfolioSnapshot

The actual current portfolio holdings.

### RebalancePlan

The changes required to move:

```text
PortfolioSnapshot
        ↓
PortfolioTarget
```

### ExecutionOrder

A concrete trade instruction.

This should remain outside the current MVP unless actual order execution is explicitly in scope.

## Decision required

Approve the above separation as the canonical V1 domain model.

## Consequence

The existing `Portfolio` object should not be expanded indefinitely to contain all portfolio concepts.

---

# 5. P0 — ADM Defensive Asset

## ID

`DQ-ADM-001`

## Status

`DECIDED`

## Priority

`P0`

## Decision

ADM에서는 Monitoring / Signal Asset과 Execution Asset을 분리한다.

- Monitoring / Signal Asset: 전략 계산과 상태 판단에 사용하는 대표 자산
- Execution Asset: 실제 Portfolio Output에 사용하는 자산
- 두 자산 간의 관계는 명시적인 Execution Mapping으로 관리한다.

현재 승인된 매핑:

| Monitoring / Signal Asset | Execution Asset |
|---|---|
| BIL | SGOV |
| SHY | SCHO |

따라서 Codex는 Signal Asset을 임의로 Execution Asset으로 변경해서는 안 되며, 실제 Output Asset은 명시된 Mapping을 사용해야 한다.

## Consequence

ADM 구현에서는 다음 구조를 따른다.

```text
Monitoring / Signal Asset
        ↓
Strategy Calculation
        ↓
Selected Asset
        ↓
Execution Mapping
        ↓
Execution Asset

---

# 6. P0 — ADM Total Return Methodology

## ID

`DQ-ADM-002`

## Status

`DECIDED`

## Priority

`P0`

## Decision

ADM의 Trailing 12-Month Total Return은 Adjusted Price를 이용하여 계산한다.

```text
TR_12M =
    AdjustedPrice[t]
    /
    AdjustedPrice[t-12M]
    - 1

Orion은 ADM 내부에서 배당금을 별도로 재구성하거나 합산하지 않는다.

Adjusted Price는 배당 및 기타 조정사항을 반영한 Total Return Proxy로 취급하며,
ADM은 Data Layer에서 제공되는 정규화된 Adjusted Price를 입력으로 사용한다.

따라서:

Market Data Source
        ↓
Normalized Adjusted Price
        ↓
ADM
        ↓
12M Total Return
        ↓
Momentum / Signal
Consequence

ADM의 투자 로직과 배당 데이터 처리 로직을 분리한다.

배당 처리 방식은 Data Layer의 Adjusted Price normalization 책임이며,
adm.py에서 직접 dividend calculation을 수행하지 않는다.

DQ-ADM-003 — Dividend Adjustment는 본 결정으로 함께 해결한다.

---

# 7. P0 — ADM Dividend Handling

## ID

`DQ-ADM-003`

## Status

`DECIDED`

## Priority

`P0`

Decision:
DQ-ADM-002의 Adjusted Price 방식을 채택함에 따라
ADM에서는 배당금을 별도로 계산하지 않는다.
배당 효과는 Data Layer가 제공하는 Adjusted Price에 반영된 것으로 취급한다.
---

# 8. P0 — ADM Execution Mapping

## ID

`DQ-ADM-004`

## Status

`DECIDED`

## Priority

`P0`

Execution Mapping은 명시적으로 관리한다. 현재 승인된 mapping은 사용한다. 동시에 동일 Category 내의 Execution Candidate를 주기적으로 검토하여 더 적합한 ETF가 발견되면 mapping을 갱신할 수 있다.

---

# 9. P0 — Moon Strategy Activation

## ID

`DQ-MOON-002`

## Status

`DECIDED`

## Priority

`P0`

## Decision

V1의 operational execution allowlist에는 실제로 구현되고 검증된 전략만
포함한다. 이는 D-026의 `strategies` registry와 `active_strategies`
allowlist 분리를 따른다.

`strategies`는 알려진 strategy specification의 registry이므로 Research /
Development 전략도 포함할 수 있다. 등록만으로 실행 가능해지는 것은 아니다.

현재 Moon MVP의 첫 번째 End-to-End Vertical Slice는 ADM으로 진행한다.

ADM vertical slice가 검증되고 활성화 승인을 받기 전까지 현재 실행 allowlist는
비어 있다. 현재 설정은:

```yaml
strategies:
  - ADM
  - BAA
  - BDA
  - HAA
  - VAA
active_strategies: []
```

이다. ADM vertical slice 검증과 승인 후 `active_strategies`에 ADM만
추가한다.

BAA, BDA, HAA, VAA는 Research / Development 상태로 유지하며 현재 Moon MVP의
Operational Execution에는 참여시키지 않는다.

전략이 구현되고 검증된 이후 별도의 승인 절차를 거쳐 Operational Configuration에 추가한다.

## Rule

Configuration에 등록되어 있다는 사실만으로 해당 전략을 Executable로 간주하지 않는다.

```text
Configured
    ≠
Executable
```

현재 V1에서는:

```text
Implementation-ready
        ↓
Validated
        ↓
Operationally Active
```

인 전략만 실행한다.

## Consequence

Moon MVP는 모든 전략을 동시에 구현하지 않는다.

```text
Moon
  ↓
ADM
  ↓
End-to-End Vertical Slice
  ↓
Validation
```

을 먼저 완료한다.

다른 전략은 현재 구현 범위에서 제외하되 Research / Development 대상으로 유지한다.

---

# 10. P1 — Canonical Domain Model Mapping

## ID

`DQ-DOMAIN-001`

## Status

`OPEN`

## Priority

`P1`

## Problem

The logical domain model, Python domain models, data model, and actual source tree are not yet completely aligned.

## Required mapping

Create one authoritative mapping table covering at least:

```text
Framework
Strategy
StrategyResult
Score
State
Review
Decision
Event
OrionStateSnapshot
Allocation
ConsensusAllocation
PortfolioTarget
PortfolioSnapshot
RebalancePlan
ExecutionOrder
DashboardCard
```

The table must identify:

```text
Domain Concept
    ↓
Canonical Documentation
    ↓
Python Model
    ↓
Status
```

---

# 11. P1 — Runtime Lifecycle Contract

## ID

`DQ-RUNTIME-001`

## Status

`OPEN`

## Priority

`P1`

## Problem

The broader Orion architecture describes Runtime responsibilities, but the complete lifecycle contract is not yet implemented.

The intended direction is:

```text
OrionEngine
    ↓
RuntimeSession
    ↓
Services
    ↓
Framework
    ↓
Result
    ↓
State
    ↓
Events
```

## Decision required

Before full Runtime implementation, define:

* initialization,
* execution,
* state ownership,
* event semantics,
* error handling,
* shutdown,
* repeated execution behavior.

## Current rule

Do not allow Runtime work to block the Moon vertical slice unless Moon implementation demonstrates a direct dependency.

---

# 12. P1 — Event Semantics

## ID

`DQ-RUNTIME-002`

## Status

`OPEN`

## Priority

`P1`

## Problem

Orion contains both:

```text
Domain Changes
```

and:

```text
Lifecycle Events
```

but their semantic distinction must be explicit.

## Required distinction

Examples:

```text
Domain Event
- regime changed
- allocation changed
- leadership changed
```

versus:

```text
Lifecycle Event
- framework started
- framework completed
- runtime initialized
- runtime shutdown
```

These must not be conflated.

---

# 13. P1 — Aurora Scoring

## ID

`DQ-AURORA-001`

## Status

`OPEN`

## Priority

`P1`

## Problem

Aurora has a valid conceptual architecture but its final scoring methodology is not implementation-ready.

The following remain to be closed:

```text
Indicator definitions
Component scoring
Aurora score
Regime thresholds
State momentum
Transition risk
```

The intended conceptual chain is:

```text
Indicator
    ↓
ComponentScore
    ↓
AuroraScore
    ↓
Regime
    ↓
RiskState
    ↓
TransitionRisk
```

## Decision

Do not ask Codex to invent these calculations.

The Aurora research and framework documents must first be consolidated into an approved implementation specification.

---

# 14. P1 — Supernova Company Evaluation

## ID

`DQ-SUPERNOVA-001`

## Status

`OPEN`

## Priority

`P1`

## Problem

Supernova has the 5D conceptual framework but does not yet have a sufficiently precise implementation methodology for:

```text
Company scoring
Theme weighting
State thresholds
Watchlist lifecycle
Replacement rules
DCA behavior
```

## Decision

The scoring and lifecycle methodology must be explicitly approved before implementation.

Codex must not invent company-selection criteria.

---

# 15. P1 — Phoenix Leadership Evaluation

## ID

`DQ-PHOENIX-001`

## Status

`OPEN`

## Priority

`P1`

## Problem

Phoenix has an established Leader / Challenger / Watchlist conceptual structure, but implementation-level rules remain incomplete.

Required:

```text
Category list
Leader metrics
Challenger metrics
Replacement risk
Leadership transition
Review trigger
```

## Existing governance that should be preserved

Phoenix portfolio inclusion is restricted to approved category leaders.

Challengers and watchlist assets are monitoring candidates rather than automatic portfolio holdings.

BTC and ETH remain outside the Phoenix portfolio-engine scope as Core Digital Assets.

These existing decisions should not be reopened merely because implementation is incomplete.

---

# 16. Decisions That Are NOT Current Blockers

The following should not block the current Moon MVP:

```text
Aurora final scoring
Supernova final scoring
Phoenix final scoring
Rich dashboard rendering
Complete public API
Historical state persistence
Full multi-framework Runtime
```

They become relevant when their implementation phase begins.

---

# 17. Decision Rules for Codex

Codex must follow these rules while this queue contains open items.

## Rule 1

Do not invent an investment decision.

## Rule 2

Do not infer a missing rule from common industry practice.

## Rule 3

Do not use a passing test as evidence that an undocumented investment rule has been approved.

## Rule 4

Do not silently choose between conflicting documents.

## Rule 5

If an open decision blocks the current implementation slice:

```text
STOP
```

and report:

```text
Decision ID
Exact unresolved question
Why implementation depends on it
Possible options
Current recommended option, if documented
```

## Rule 6

If an open decision does not block the current implementation slice:

```text
CONTINUE INDEPENDENT WORK
```

---

# 18. Decision Promotion Rule

When an item is decided:

```text
OPEN
  ↓
Human Decision
  ↓
Permanent Decision Record
  ↓
05_Decisions/Decision_Log.md
  ↓
Affected Research / Framework / Implementation docs
  ↓
Decision Queue = DECIDED
```

The Decision Log is the authoritative historical record of material Orion decisions.

A dedicated decision document may be created when the decision requires substantial supporting specification, but it does not replace the permanent Decision Log entry.

The Decision Queue is not the permanent record.

A queue item must not be considered fully promoted merely because a preferred option was identified. The human decision must first be confirmed.

For decisions made during a structured Decision Review session:

```text
Review Decision
  ↓
Confirmed by User
  ↓
Recorded in Decision Log
  ↓
Affected documents reconciled
  ↓
Queue item = DECIDED
```

Review-session identifiers such as `D.1-54` or `D.2-100` are traceability identifiers within the review process. They are not substitutes for the permanent Decision Log record.

---

# 19. Current Priority Order

The recommended order is:

```text
P0-1  Canonical Moon Portfolio Contract
        ↓
P0-2  ADM Defensive Asset
        ↓
P0-3  ADM Total Return Methodology
        ↓
P0-4  ADM Dividend Handling
        ↓
P0-5  ADM Execution Mapping
        ↓
P0-6  Moon Strategy Activation
        ↓
      ADM End-to-End MVP
        ↓
P1    Runtime / Data / Other Framework Decisions
```

Where possible, documentation reconciliation may proceed in parallel with these decisions.

---

# 20. Current Decision Boundary

The current implementation boundary should be understood as:

```text
Already decided
        ↓
Canonical documentation
        ↓
Implementation-ready specification
        ↓
Codex
        ↓
Code
```

The coding agent must never cross the boundary:

```text
Unresolved investment policy
```

by making an implicit decision.

---

# 21. Exit Criteria

This Decision Queue can be considered cleared for the current Moon MVP decision scope when all decisions required for the immediate implementation slice have either:

1. been resolved and promoted to the permanent Decision Log, or
2. been explicitly deferred because they do not block the current implementation slice.

Current status:

```text
[x] DQ-MOON-001 portfolio contract resolved (D-027)

[x] DQ-MOON-002 strategy activation semantics resolved (D-026)

[x] DQ-ADM-002 total-return methodology resolved (D-028)

[x] DQ-ADM-003 dividend handling resolved (D-028)

[ ] DQ-ADM-001 defensive asset / execution mapping requires documentation reconciliation

[ ] DQ-ADM-004 concrete execution mappings require documentation reconciliation

[ ] ADM market-observation timing, freshness, and missing-data contract specified

[ ] DQ-DOMAIN-001 canonical domain model mapping

[ ] DQ-RUNTIME-001 runtime lifecycle contract

[ ] DQ-RUNTIME-002 event semantics

[ ] DQ-AURORA-001 Aurora scoring

[ ] DQ-SUPERNOVA-001 Supernova company evaluation

[ ] DQ-PHOENIX-001 Phoenix leadership evaluation
```

The unchecked items above do not all block the current Moon MVP.

The immediate implementation boundary remains:

```text
Permanent Decisions
        ↓
Implementation-ready specification
        ↓
Moon / ADM vertical slice
        ↓
Validation
        ↓
Codex implementation
```

Decision Review work outside the current implementation boundary must not be treated as a Moon MVP blocker unless a direct dependency is demonstrated.

D.1–D.2 Decision Review and Decision Lifecycle rules are considered resolved and are now preserved in `05_Decisions/Decision_Log.md`.

Their implementation impact should be handled when the corresponding Decision Review domain is implemented. They do not by themselves block the current Moon MVP.

---

# 22. Principle

The purpose of this queue is not to eliminate every unknown in Orion.

It is to eliminate the unknowns that prevent the **next correct implementation step**.

Therefore:

> **Resolve only what the current implementation requires, preserve what is already decided, and explicitly defer what belongs to a later stage.**
