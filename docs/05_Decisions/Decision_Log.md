# Orion Decision Log

This document records all material architectural, investment, governance, and operational decisions made within Orion OS.

## Decision Status Definitions

Approved

Decision is active and governs Orion.

Draft

Decision is under evaluation.

Superseded

Decision has been replaced by one or more newer decisions.

Retired

Decision is no longer used and has no active replacement.

---

## D-001

### Decision

Moon does not create proprietary investment strategies.

### Rationale

Moon is designed to implement academically researched or publicly validated investment strategies rather than inventing new methodologies.

### Status

Approved

### Date

2026-06-14

---

## D-002

### Decision

Moon is used for actual portfolio rebalancing.

### Rationale

Moon serves as the tactical asset allocation engine of Orion and directly supports investment decisions.

### Details

Rebalancing Frequency:

* Monthly

### Status

Approved

### Date

2026-06-14

---

## D-003

### Decision

Supernova is a long-term equity portfolio based on the 5D Megatrend Framework.

### Details

5D Themes:

* Decoupling
* Deglobalization
* Demographics
* Decarbonization
* Digital Transformation

### Status

Approved

### Date

2026-06-14

---

## D-004

### Decision

Supernova follows a monthly accumulation model.

### Details

Holdings are intended for long-term ownership.

Replacement occurs only when the approved company list changes.

### Status

Approved

### Date

2026-06-14

---

## D-005

### Decision

Phoenix is a digital asset observation and investment framework focused on category leaders outside BTC, ETH, and SOL.

### Initial Watchlist

* TAO
* LINK
* AAVE
* SUI
* RENDER
* WLD
* ONDO

### Status

Superseded

### Superseded By

* D-021 Phoenix Scope and Core Asset Separation
* D-022 Phoenix Portfolio Construction Methodology

### Date

2026-06-14

---

## D-006

### Decision

Rename DAA to BDA.

### Rationale

The strategy operates exclusively within a bond ETF universe and does not represent a generic Dynamic Asset Allocation framework.

The new name improves clarity and reduces ambiguity within Orion documentation.

### Impact

All future references should gradually migrate from DAA to BDA.

### Status

Approved

### Date

2026-06-20

---

## D-007

### Decision

Supernova operates as a long-term Dollar Cost Averaging (DCA) framework.

### Rationale

Short-term market conditions are not considered a reliable basis for timing purchases within long-term megatrend investments.

### Details

Investment Frequency:

* Monthly

Purchases continue regardless of market volatility.

### Status

Approved

### Date

2026-06-20

---

## D-008

### Decision

Moon uses Equal Strategy Weighting.

### Rationale

No single strategy is assumed to be consistently superior.

Equal weighting reduces model risk and prevents discretionary strategy selection.

### Details

All active Moon strategies receive equal portfolio weight.

### Status

Approved

### Date

2026-06-20

---

## D-009

### Decision

Moon allows overlapping asset exposure.

### Rationale

When multiple independent strategies select the same asset, the overlap is interpreted as a stronger consensus signal.

### Details

Asset duplication is not removed.

Repeated selections increase final portfolio weight.

### Status

Approved

### Date

2026-06-20

---

## D-010

### Decision

Moon aggregates strategy outputs through Consensus Allocation.

### Rationale

Final portfolio weights should reflect agreement across independent strategies rather than arbitrary optimization.

### Details

Strategy outputs are combined and normalized to produce final portfolio allocations.

### Status

Approved

### Date

2026-06-20

---

## D-011

### Decision

Aurora is an observational framework and does not generate investment recommendations.

### Rationale

Aurora exists to provide market context rather than act as an investment allocation engine.

This separation preserves the independence of Moon, Supernova, and Phoenix.

### Status

Approved

### Date

2026-06-20

---

## D-012

### Decision

Moon separates signal assets from execution assets.

### Rationale

Academic research and published strategies are defined using
specific benchmark ETFs.

To preserve methodological integrity, signal generation shall
use the original asset universe whenever possible.

Execution may use lower-cost equivalent ETFs.

### Example

Signal Asset:
SPY

Execution Asset:
SPYM

Signal Asset:
BIL

Execution Asset:
SGOV

### Status

Approved

### Date

2026-06-20

---

## D-013

Moon execution ETF mappings shall be reviewed annually.

Review criteria include:

- Expense ratio
- Liquidity
- Assets under management
- Tracking quality
- Tax efficiency

### Date

2026-06-20

---

## D-014

Moon strategies are documented in two layers:

1. Research Specification
2. Orion Implementation Specification

Research documents preserve original methodology.

Implementation documents define Orion-specific execution details.

Status: Approved

Date: 2026-06-21

---

## D-015

Moon Governance Framework is established as the governing document for all Moon strategies.

All future strategy additions, removals, methodology changes, and implementation changes must comply with Moon_Governance.md.

Status: Approved

Date: 2026-06-21

---

## D-016

Moon uses Strategy Consensus Allocation as the portfolio aggregation methodology.

Final portfolio weights are derived from the combined output of approved strategies.

Moon does not apply discretionary weighting between strategies.

Status: Approved

Date: 2026-06-21

---

## D-017

Aurora shall monitor not only current market regime but also regime transition dynamics.

Aurora outputs must include:

* Current State
* State Momentum

Examples:

* Improving
* Stable
* Deteriorating

Purpose:

Detect potential market regime changes before full regime confirmation.

Status: Approved

Date: 2026-06-21

---

## D-018

Aurora shall distinguish between Core Indicators and Cross Asset Indicators.

Core Indicators determine the primary market regime.

Cross Asset Indicators provide additional environmental context.

Examples:

Core:
* Trend
* Liquidity
* Volatility
* Credit

Cross Asset:
* Dollar
* Gold
* Oil
* Bitcoin

Status: Approved

Date: 2026-06-21

---

## D-019

Aurora shall manage indicators using an indicator lifecycle.

States:

* Candidate
* Approved
* Retired

Only Approved indicators may be used in production scoring.

All status changes must be recorded in Aurora documentation and the Decision Log.

Status: Approved

Date: 2026-06-21

---

## D-020

Aurora shall monitor regime transitions separately from regime classification.

Transition monitoring is considered a primary objective of Aurora.

Examples:

* Bull → Bear Watch
* Bear → Bull Watch

Aurora must report both:

1. Current Regime
2. Regime Direction

Status: Approved

Date: 2026-06-21

---

## D-021 — Phoenix Scope and Core Digital Asset Separation

Date:

2026-06-21

Status:

Approved

### Decision

Bitcoin (BTC) and Ethereum (ETH) are excluded from Phoenix.

BTC and ETH are treated as Core Digital Assets and are managed independently from Phoenix.

Phoenix focuses exclusively on altcoin category leaders and leadership transitions.

### Core Digital Asset Allocation

Default allocation:

* BTC 60%
* ETH 40%

Accumulation method:

* Periodic purchases
* No tactical rebalancing
* Long-term holding

### Phoenix Scope

Phoenix manages:

* Smart Contract Leaders
* Oracle Leaders
* AI Infrastructure Leaders
* RWA Leaders
* Other approved category leaders

Phoenix does not manage:

* BTC
* ETH

### Rebalancing Principle

Price changes alone shall not trigger portfolio rebalancing.

Phoenix responds to:

* Leadership changes
* Category leader replacement
* Replacement risk events

### Rationale

BTC and ETH currently represent foundational digital asset infrastructure.

Phoenix exists to identify emerging category leaders and potential future winners rather than manage established core digital assets.

Separating Core Digital Assets from Phoenix simplifies portfolio construction and preserves Phoenix's focus on leadership monitoring.

### Impact

Core Digital Assets

* BTC
* ETH

Phoenix Portfolio

* Altcoin category leaders only

Status:

Effective immediately.

---

## D-022

Date:

2026-06-22

Status:

Approved

Category:

Phoenix

---

## Title

Phoenix Portfolio Construction Methodology

---

## Context

Phoenix identifies digital asset leaders at the category level.

The framework evaluates:

* Categories
* Leaders
* Challengers
* Replacement Risk

A portfolio construction methodology is required.

Key questions:

* Should challengers be included?
* How many assets should be held?
* How should weights be assigned?

---

## Decision

Phoenix shall invest only in approved category leaders.

Challengers and watchlist assets are used exclusively for monitoring and replacement evaluation.

They are not eligible for portfolio inclusion.

Portfolio weights are assigned equally across all approved leaders.

---

## Example

Approved Leaders:

* SOL
* LINK
* TAO
* ONDO
* TIA

Result:

* SOL 20%
* LINK 20%
* TAO 20%
* ONDO 20%
* TIA 20%

---

## Leadership Change

If a challenger becomes the new approved leader:

Example:

Before

* SOL

After

* SUI

The portfolio shall rebalance during the next review cycle.

---

## Exclusions

Phoenix does not manage:

* BTC
* ETH

These assets are managed separately under D-021.

---

## Rationale

Leader-only construction aligns with the purpose of Phoenix.

Phoenix exists to identify and own category leaders.

It does not attempt to predict future leaders before leadership has been established.

This approach:

* Simplifies operations
* Reduces turnover
* Improves explainability
* Maintains consistency with the framework philosophy

---

## Consequences

Benefits

* Simple implementation
* Clear governance
* Lower operational complexity

Risks

* Leadership transitions may be captured later
* Challenger upside may be missed

These risks are accepted.

---

## Review Trigger

This decision should be reconsidered if:

* Phoenix exceeds 10 portfolio assets
* Leadership turnover becomes frequent
* Historical testing demonstrates superior challenger participation

---

## Related Documents

Phoenix_Operating_Model.md

Phoenix_Leader_Framework.md

Phoenix_Scoring_Framework.md

Phoenix_Category_Framework.md

---

## Status

Approved

---

## D-023

Date:

2026-06-22

Title:

Orion Operating Architecture Established

Status:

Superseded by D-042

---

### Context

As Orion evolved, the distinction between monitoring functions and portfolio management functions became increasingly important.

Initial architecture discussions treated Aurora, Moon, Supernova, and Phoenix as equivalent engines.

However, further analysis showed that Aurora serves a fundamentally different purpose.

---

### Decision

Orion shall be organized into:

* One Monitoring Layer
* Three Portfolio Engines

Architecture:

Aurora

↓

Market Context

↓

Investor Interpretation

↓

Moon / Supernova / Phoenix

↓

Portfolio Actions

---

Aurora is designated as Orion's Monitoring Layer.

Aurora provides:

* Market Regime
* Risk State
* Transition Risk
* Market Commentary

Aurora does not directly manage portfolios.

Aurora does not generate buy or sell instructions.

---

Moon is designated as the ETF Portfolio Engine.

Supernova is designated as the Equity Portfolio Engine.

Phoenix is designated as the Digital Asset Portfolio Engine.

Each portfolio engine remains independently governed.

---

### Consequences

Benefits:

* Clear separation of monitoring and execution responsibilities
* Simplified mental model
* Improved modularity
* Better alignment with actual portfolio structure

Risks:

* Portfolio engines may interpret Aurora differently
* Some overlap may remain during future framework evolution

---

### Reference Documents

* Orion_Operating_Architecture.md
* Orion_Technical_Architecture.md

---

## D-024

Orion shall maintain a centralized glossary.

The glossary defines standard terminology used across all Orion documentation.

Examples:

* OS
* Framework
* Engine
* Dashboard
* Strategy
* Signal
* State
* Regime

The glossary serves as the authoritative terminology reference for Orion OS.

Status: Approved

Date: 2026-06-21

---

## D-025

Orion shall use the following architecture terminology.

OS:
The complete Orion investment operating system.

Framework:
A major investment domain within Orion.

Engine:
A calculation or analysis module inside a framework.

Strategy:
A rules-based investment methodology within a framework.

Examples:

Moon = Framework

ADM = Strategy

Aurora Trend = Engine

Orion = OS

Status: Approved

Date: 2026-06-21

---

## D-026

### Decision

Moon configuration shall distinguish registered strategies from active
strategies.

### Details

`strategies` is the registry of known strategy specifications.
`active_strategies` is the explicit execution allowlist and must be a subset
of the registered strategies. A strategy with unresolved research or
implementation issues remains registered but inactive.

The initial operational allowlist is empty until an approved strategy is
explicitly activated.

### Rationale

Registration must not imply production readiness. This prevents draft
investment methodology from entering execution merely because a strategy is
listed in configuration.

### Status

Approved

### Date

2026-09-06

---

## D-027

### Status

Superseded in scope by D-042 and D-043. The Moon-specific StrategyResult and ConsensusAllocation concepts remain valid; the common PortfolioTarget / PortfolioState / RebalancePlan / ExecutionOrder concepts are now part of the common Orion Portfolio Domain.

### Decision

Moon shall use the following canonical portfolio domain model.

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

Current portfolio state is represented independently:

```text
PortfolioSnapshot
      ↓
Current Holdings
```

A `RebalancePlan` is derived from:

```text
PortfolioTarget + PortfolioSnapshot
      ↓
RebalancePlan
```

### Details

`StrategyResult` represents the output of an individual strategy, including its signal, allocation, and supporting information.

`ConsensusAllocation` represents the allocation resulting from the aggregation of multiple strategy results.

`PortfolioTarget` represents the desired portfolio allocation using the actual execution assets.

`PortfolioSnapshot` represents the actual current portfolio holdings.

`RebalancePlan` represents the changes required to move the current portfolio represented by `PortfolioSnapshot` toward the desired allocation represented by `PortfolioTarget`.

`ExecutionOrder` represents a concrete trade instruction.

These concepts shall remain distinct and shall not be collapsed into a single `Portfolio` object.

### Scope

`ExecutionOrder` is part of the canonical domain model but actual order execution is outside the current Moon MVP unless explicitly brought into scope by a future decision.

### Rationale

The term `Portfolio` has previously been used to represent multiple distinct concepts, including allocation, current holdings, target holdings, rebalancing, and execution.

Separating these concepts provides a stable domain model for Moon implementation and prevents the `Portfolio` object from accumulating unrelated responsibilities.

### Status

Approved

### Date

2026-09-06

---

## D-028

### Decision

ADM shall use adjusted-price-based total return measurement for strategy calculation.

Dividend distributions shall be incorporated through the adjusted price series and shall not be calculated separately within the ADM strategy logic.

### Details

ADM return calculation shall use the adjusted price provided by the data layer.

The conceptual calculation is:

```text
Adjusted Price
      ↓
Total Return Measurement
      ↓
ADM Strategy Calculation
```

ADM shall not independently calculate dividend distributions from raw dividend data as part of its core strategy calculation.

The responsibility for producing the appropriate adjusted-price series belongs to the data layer.

Raw close prices and adjusted prices therefore have distinct purposes:

* Raw Close: represents the unadjusted market price.
* Adjusted Price: provides the price series used for ADM total-return measurement.

### Rationale

ADM evaluates asset performance on a total-return basis.

Using the adjusted price series allows dividend distributions to be incorporated consistently into the return calculation without introducing a separate dividend calculation inside the strategy implementation.

This keeps the strategy logic focused on investment methodology while data adjustment remains a responsibility of the data layer.

### Scope

This decision defines the return measurement methodology used by ADM.

It does not define the broader data-provider selection, data-quality policy, or historical data validation process.

### Status

Approved

### Date

2026-09-06

---

## D-030

### Decision

Moon MVP shall use in-memory persistence only.

Historical state persistence and event replay are outside the current Moon MVP scope.

The current in-memory `EventStore` and `StateStore` contracts shall remain
the runtime persistence boundary for the MVP.

Future persistent storage shall be introduced behind these domain/runtime
contracts without coupling the domain model to a specific storage technology.

### Details

The following are explicitly outside the current MVP scope:

* Persistent historical state storage
* Event replay
* Selection of a specific database or storage engine
* Definition of a production retention policy

The following remain within the current MVP implementation scope:

* In-memory `EventStore`
* In-memory `StateStore`
* Runtime state handling
* Execution history within the current runtime boundary

A future persistence implementation may define storage technology,
retention policy, and replay behavior through a separate decision.

### Rationale

The current Orion implementation is focused on validating the runtime
architecture and portfolio execution flow.

Introducing a specific persistent storage technology before the runtime
contracts are stabilized would unnecessarily couple implementation details
to the current architecture.

Keeping persistence behind the existing contracts allows the MVP to proceed
while preserving a clear migration path to persistent storage.

### Scope

This decision defines the persistence boundary for the current Moon MVP.

It does not select a database, storage engine, retention policy, or future
event-replay architecture.

### Status

Approved

### Date

2026-09-07

---

# D.1–D.2 Decision Review & Decision Lifecycle

## Context

Orion의 Decision Review 영역에서 Analysis, Evidence Snapshot, Recommendation, User Decision, Review Record, Note 및 관계(Relation)의 lifecycle과 provenance를 명확히 정의한다.

핵심 목적은 다음과 같다.

* Analysis와 Recommendation의 lifecycle을 분리한다.
* Recommendation과 User Decision의 lifecycle을 분리한다.
* Review가 Recommendation 또는 Decision을 직접 수정하지 않도록 한다.
* 기존 판단을 수정할 경우 기존 기록을 변경하지 않고 새로운 기록을 생성한다.
* 모든 중요한 판단과 변경의 provenance를 추적 가능하게 한다.
* 현재 상태를 mutable pointer나 별도 status field에 의존하지 않고 lifecycle과 lineage에서 결정할 수 있도록 한다.

---

## D.1 — Decision Review Framework

### 1. Architecture Boundary

Orion의 판단 흐름은 다음과 같이 분리한다.

```text
Analysis
   ↓
Evidence Snapshot
   ↓
Recommendation
   ↓
User Decision

Review Record
   └─ Recommendation / Decision에 영향을 주는 trigger와 결과를 기록
```

Actual Trading은 Orion의 외부 영역이다.

```text
Analysis
→ Recommendation
→ User Decision
→ Actual Trading (Outside Orion)
```

Orion은 실제 주문 실행 여부나 실행 결과를 User Decision의 lifecycle에 반영하지 않는다.

### 2. Recommendation Immutability

Recommendation은 Immutable하다.

Recommendation의 내용이 변경되어야 하는 경우 기존 Recommendation을 수정하지 않는다.

```text
R1 = Superseded
R2 = Active
```

R2는 R1을 `Supersedes`한다.

Recommendation이 생성되면 새로운 User Decision은 `Pending`으로 시작한다.

### 3. Evidence Snapshot

Recommendation 생성 시 사용한 Evidence Snapshot은 고정한다.

Analysis가 이후 변경되더라도 당시 Recommendation이 어떤 evidence를 기반으로 만들어졌는지 재현할 수 있어야 한다.

Provenance:

```text
Analysis Version
      ↓
Evidence Snapshot
      ↓
Recommendation
      ↓
User Decision
```

### 4. Review Trigger

Review는 다음 두 종류의 trigger로 발생할 수 있다.

* Regular Review
* Material Change

Change Detection과 Material Change 판단은 별개의 개념이다.

Review는 변경이 감지되었다는 사실과 그것이 Recommendation 변경을 요구하는지 여부를 분리해서 판단한다.

### 5. Review Result

Review Result는 다음 세 가지로 구분한다.

* `No Change`
* `Reconsideration Required`
* `Recommendation Change Required`

`No Change`도 명시적인 Review Record로 남긴다.

Review Record 자체가 Recommendation을 직접 변경하지 않는다.

### 6. Reconsideration

`Reconsideration Required`인 경우 Recommendation은 유지한다.

기존 Active User Decision은 `Superseded`가 되고 새로운 Pending User Decision을 생성한다.

```text
Recommendation R1
    ↓
Decision D1 = Superseded
Decision D2 = Pending
```

### 7. Recommendation Change

`Recommendation Change Required`인 경우 기존 Recommendation을 Superseded 처리하고 새로운 Recommendation을 생성한다.

기존 Recommendation의 현재 Active/Pending Decision도 Superseded 처리한다.

새 Recommendation에는 새로운 Pending Decision을 생성한다.

기존 Decision history를 새로운 Recommendation으로 복사하지 않는다.

Recommendation 간 lineage는 `Supersedes` 관계로 연결한다.

---

# D.2 — Decision Lifecycle & Relation Model

## 1. User Decision Lifecycle

User Decision의 lifecycle은 다음 세 가지다.

```text
Pending
Active
Superseded
```

`Rejected`는 lifecycle이 아니라 Outcome이다.

따라서:

```text
Status = Active
Outcome = Rejected
```

가 가능하다.

Outcome은 다음 두 가지로 제한한다.

* `Accepted`
* `Rejected`

Conditional Acceptance는 별도 lifecycle이 아니라:

```text
Outcome = Accepted
Conditions = <condition>
```

으로 표현한다.

조건이 없는 Accepted Decision은 `Conditions = null`이다.

Rejected Decision에도 Conditions를 둘 수 있다.

## 2. Decision Immutability

User Decision은 Immutable하다.

다음 사항이 변경되면 새로운 Decision을 생성한다.

* Outcome 변경
* Conditions의 의미 변경
* Recommendation 변경에 따른 새로운 판단
* Reconsideration에 따른 새로운 판단

기존 Decision은 `Superseded`로 남긴다.

단순한 wording-only clarification은 Decision을 변경하지 않고 별도의 Note/Clarification으로 기록한다.

## 3. Decision Supersession

새 Decision이 기존 Decision을 대체하는 경우:

```text
New Decision
   ├─ Supersedes Decision
   └─ triggered_by_review (해당하는 경우)
```

기존 Decision의 `Superseded Reason`을 필수로 기록한다.

Recommendation 변경 때문에 Decision이 Superseded되는 경우:

```text
Superseded Reason = Recommendation Superseded
superseded_by_recommendation_id = R2
```

Superseded된 Decision의 Outcome과 Conditions는 변경하지 않는다.

## 4. Current Decision

Current Decision은 별도의 `current_decision_id` pointer로 저장하지 않는다.

Lifecycle을 기반으로 결정한다.

Recommendation 하나에 대해:

* Active Decision은 최대 1개
* Pending Decision은 최대 1개

를 허용한다.

Reconsideration 시 기존 Active Decision을 먼저 Supersede하고 새로운 Pending Decision을 생성한다.

따라서 동일 Recommendation 아래에서 `Active + Pending` Decision을 동시에 유지하지 않는다.

Pending Decision이 존재하는 상태에서 추가 Review가 발생하면 새로운 Pending Decision을 만들지 않고 기존 Pending Decision을 유지하며 Review Record만 추가한다.

단, Recommendation 자체가 변경되면 기존 Pending Decision도 Superseded되고 새로운 Recommendation에 새로운 Pending Decision을 생성한다.

## 5. Recommendation–Decision Relationship

Recommendation과 User Decision은 1:N 관계다.

하나의 Recommendation에는 여러 historical Decision이 존재할 수 있지만 현재 유효한 Decision은 lifecycle 규칙에 따라 결정한다.

새 Recommendation은 이전 Decision history를 복사하지 않는다.

---

# Review / Decision Interaction

Review와 User Decision은 독립 객체다.

Review Record는 판단을 trigger하고 근거를 남기지만 Recommendation이나 Decision을 직접 수정하지 않는다.

```text
Review Record
   ├─ No Change
   ├─ Reconsideration Required
   └─ Recommendation Change Required
```

새 Decision이 Review 때문에 생성된 경우 `triggered_by_review`로 해당 Review Record를 참조한다.

`No Change` Review에서는 기존 Active Decision을 그대로 유지한다.

---

# Note / Clarification

Note/Clarification은 Decision 변경을 대신하지 않는다.

Note는 Immutable하며 다음 정보를 가진다.

* `created_at`
* `created_by`
* `note_type`
* `content`
* `target_type`
* `target_id`

`created_by`는 현재 단계에서 다음으로 제한한다.

* `User`
* `System`

Note Type 초기 집합:

* `Clarification`
* `Correction`
* `Context`
* `Observation`
* `Other`

`Other`를 선택하면 `Other Type Description`을 필수로 한다.

Note는 다음 주요 객체에 attach할 수 있다.

* Analysis
* Evidence Snapshot
* Recommendation
* User Decision
* Review Record

Note는 다른 Note에도 연결할 수 있다.

초기 Relation Type:

* `Supersedes`
* `Related To`

`Related To`는 undirected relation이다.

`Supersedes`는 directed relation이다.

Self-reference는 금지한다.

`Supersedes` cycle은 금지한다.

중복 Relation도 금지한다.

---

# Supersedes Relation

`Supersedes` 관계 자체도 provenance의 일부로 취급한다.

일반적으로 source의 `created_at`은 target보다 이후여야 한다.

단, migration/import에서는 temporal validation exception을 허용한다.

Exception은 다음 정보를 가진다.

* `exception_type`
* `exception_description`

`exception_type = Other`인 경우 상세 설명을 필수로 한다.

Exception 기록 자체도 Immutable하다.

잘못 생성된 `Supersedes` 관계는 직접 삭제하거나 취소하지 않는다.

별도의 `Invalidates Supersedes` 관계를 생성하여 해당 Supersedes 관계를 무효화한다.

---

# Invalidates Supersedes

잘못된 `Supersedes` 관계는 다음 구조로 정정한다.

```text
Supersedes Relation
       ↓
Invalidates Supersedes
```

`Invalidates Supersedes`는 특정 `Supersedes Relation ID`를 직접 참조한다.

현재 유효성은 별도의 status field가 아니라 lineage에서 도출한다.

`Invalidates Supersedes` 관계 자체는 Immutable하다.

`Invalidates Supersedes` 자체를 다시 invalidate하는 recursive 구조는 허용하지 않는다.

대신 잘못된 invalidation은 별도의 Correction으로 정정한다.

---

# Correction

Correction은 특정 `Invalidates Supersedes` 관계를 정정하기 위한 Immutable 기록이다.

필수 정보:

* `target_relation_id`
* `correction_type`
* `description`
* `created_at`
* `created_by`

`created_by`는 현재 단계에서 다음으로 제한한다.

* `User`
* `System`

현재 Correction Type은 최소 모델로 다음 하나만 정의한다.

* `Restore Validity`

즉:

```text
Invalidates Supersedes
       ↓
Correction
       ↓
Restore Validity
```

Correction은 동일한 Invalidates Supersedes 관계에 대해 여러 개 존재할 수 있다.

Correction은 기존 Correction을 수정하거나 삭제하지 않는다.

현재 상태를 결정할 때는 가장 최근 Correction을 사용한다.

정렬 규칙:

1. `created_at`
2. 동일 timestamp인 경우 `Correction ID`

`Correction ID` 자체는 순번이나 시간적 의미를 갖지 않는다. 단순 identifier이며 timestamp tie-breaker로만 사용한다.

---

# Current Relation Validity

현재 관계의 유효성은 저장된 mutable status가 아니라 lineage에서 deterministic하게 계산한다.

개념적으로:

```text
Supersedes
   ↓
Invalidates Supersedes
   ↓
Latest Correction
```

`Restore Validity` Correction이 존재하면 해당 `Invalidates Supersedes`의 효력이 제거된 것으로 간주하고 원래 `Supersedes` 관계가 다시 유효해진다.

따라서 Current State는 별도의 mutable state field가 아니라 relation lineage의 계산 결과다.

---

# Core Invariants

다음 규칙은 D.1–D.2에서 확정한 핵심 invariant다.

1. Recommendation은 Immutable하다.
2. User Decision은 Immutable하다.
3. Review Record는 Recommendation/Decision을 직접 수정하지 않는다.
4. Analysis 변경 자체는 Recommendation 변경을 의미하지 않는다.
5. Recommendation 변경이 필요한 경우 새로운 Recommendation을 생성한다.
6. Decision 변경이 필요한 경우 새로운 Decision을 생성한다.
7. 기존 기록은 삭제하지 않고 Superseded lineage를 유지한다.
8. Recommendation 하나에는 최대 하나의 Active Decision이 존재한다.
9. Recommendation 하나에는 최대 하나의 Pending Decision이 존재한다.
10. Recommendation reconsideration 시 Active + Pending Decision을 동시에 유지하지 않는다.
11. Actual Trading execution state는 Orion의 Decision lifecycle에 포함하지 않는다.
12. Current state는 가능한 경우 mutable pointer/status가 아니라 lifecycle과 lineage에서 도출한다.
13. 모든 중요한 변경은 provenance를 유지한다.
14. Supersedes lineage는 cycle을 가질 수 없다.
15. Invalidates 및 Correction도 Immutable provenance를 유지한다.

---

# Decision Traceability

이번 D.1–D.2 설계 결정은 Review Session의 개별 결정 번호를 통해 추적한다.

Review Session 결정 번호는 permanent Decision ID가 아니다.
Permanent architectural record는 본 Decision Log에 기록된 D-xxx Decision과 해당 결정 블록이다.

현재 확인된 Review Session 결정 범위:

* D.1-54 ~ D.1-67: Review / Recommendation / Decision lifecycle 및 provenance
* D.2-01 ~ D.2-10: Review / Decision 기본 lifecycle
* D.2-11 ~ D.2-46: Decision lifecycle, Outcome, Conditions, Actual Trading boundary
* D.2-47 ~ D.2-80: Note, Relation, Supersedes, Invalidates 구조
* D.2-81: Invalidates Supersedes / Correction lifecycle 관련 결정
* D.2-84 ~ D.2-100: Invalidates Supersedes Correction 및 deterministic validity

D.2-82 및 D.2-83은 현재 Decision Review 기록에서 원문 결정 내용을 복구하지 못했으므로 본 Log에서는 의미를 추정하지 않는다.

해당 결정이 실제로 존재하고 구현 또는 문서 정합성에 영향을 주는 것으로 확인될 경우, 원래 Review 기록을 복구한 후 별도로 보완한다.

개별 Review Session 결정과 본 Decision Log의 permanent record 사이에 불일치가 발견될 경우, 추정으로 수정하지 않고 provenance를 확인한 후 정정한다.

---

# Consequences

이 결정으로 Orion의 Decision Review 모델은 다음 특성을 갖는다.

* Append-only history
* Immutable Recommendation
* Immutable User Decision
* Explicit Review Record
* Explicit provenance
* Recommendation–Decision lineage
* Supersedes lineage
* Invalidates lineage
* Correction lineage
* Deterministic current-state derivation

향후 구현에서는 이 규칙을 임의로 단순화하거나 mutable status/pointer로 대체하지 않는다.

구현상 불가피한 변경이 필요한 경우 새로운 Decision Record를 생성하여 본 결정과의 관계를 명시한다.

---

---

## D-031 — Phoenix Production Category Set

Date:

2026-10-05

Status:

Approved

Category:

Phoenix

### Decision

Phoenix production portfolio construction shall use exactly five production-eligible categories:

* Smart Contract Platforms
* Oracle Networks
* Real World Assets
* AI Infrastructure
* Data Availability

Store of Value remains outside Phoenix under D-021.

The remaining documented categories are retained for research/reference purposes but are not production eligible unless separately approved.

### Rationale

The runtime configuration already operates on these five categories. Explicit production eligibility separates the operational portfolio universe from the broader research category framework.

### Consequences

Category `Status` and `Production Eligible` are separate dimensions.

Changes to the production category set require a new Decision Log entry before implementation.

---

## D-032 — Phoenix Multi-Category Membership and Unique-Asset Portfolio Construction

Date:

2026-10-05

Status:

Approved

Category:

Phoenix

### Decision

Phoenix permits an asset to belong to multiple categories.

Category roles are evaluated independently. The same asset may be a Leader in one category and a Challenger or Watchlist asset in another.

Portfolio construction operates on unique assets. The same asset may appear only once in the Phoenix portfolio even when it has roles in multiple categories.

### Example

RENDER

* DePIN → Leader
* AI Infrastructure → Challenger

Portfolio:

RENDER → one position maximum

### Rationale

Category leadership and portfolio identity are separate concepts. Multi-category membership preserves analytical fidelity without creating duplicate portfolio positions.

---

## D-033 — Phoenix Judgment-Assisted-by-Metrics Scoring Model

Date:

2026-10-05

Status:

Approved

Category:

Phoenix

### Decision

Phoenix scoring shall remain a judgment-assisted-by-metrics model rather than a fully formula-driven quantitative model.

Each 0–10 scoring dimension shall use qualitative anchors. Reviewers shall retain the principal evidence supporting each assigned score.

Raw metrics may inform the assessment but shall not mechanically determine the score unless a separate metric-to-score rule is explicitly approved.

### Minimum Review Record

Each reviewed score should record:

* Score
* Evidence
* Assessment
* Review Date

### Rationale

The existing 0–10 ranges are useful for structured comparison, but the current framework does not define sufficiently reproducible metric-to-score formulas. Requiring full automation at this stage would create false precision and unnecessary implementation scope.

---

## D-034 — Phoenix Approved Leaders Registry

Date:

2026-10-05

Status:

Approved

Category:

Phoenix

### Decision

Phoenix shall maintain `Phoenix_Approved_Leaders_v1.md` as the authoritative registry of current category leadership decisions.

The registry is separate from:

* Category definitions
* Leader-selection methodology
* Scoring methodology
* Runtime configuration

The current five configuration leaders are recorded as Provisional until explicit approval evidence is documented.

### Current Provisional Leaders

* Smart Contract Platforms → SOL
* Oracle Networks → LINK
* Real World Assets → ONDO
* AI Infrastructure → TAO
* Data Availability → TIA

Only Approved leaders are eligible for formal Phoenix portfolio construction under D-022.

Configuration membership alone does not constitute approval evidence.

---

## D-035 — Phoenix Canonical Replacement Risk and Leadership State Mapping

Date:

2026-10-05

Status:

Approved

Category:

Phoenix

### Decision

Phoenix shall use one canonical Replacement Risk and Leadership State mapping across all production-facing documentation.

Replacement Risk is derived from:

```text
Score Gap = Leader Score − Challenger Score
```

Canonical mapping:

| Score Gap | Replacement Risk | Leadership State | Action |
|---|---|---|---|
| 20+ | Low | Dominant | Hold |
| 10–19 | Medium | Stable | Monitor |
| 0–9 | High | Competitive | Review |
| Challenger exceeds Leader | Critical | Transition | Review Required |

`Disrupted` is a confirmed transition state used when the Promotion Rule has been satisfied and the challenger is formally confirmed as the new leader. It is not a separate score-gap band.

The worked examples in Phoenix documentation must use this mapping literally.

### Rationale

The previous documents contained incompatible risk/state vocabularies and an example that translated `Gap 6 → High Risk` into `Transition` without a defined rule. This decision removes that ambiguity and makes the score-gap calculation, risk, state, and action deterministic.

## D-036 — Supernova Multi-Theme Attribution and Theme Concentration

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova permits a company to have meaningful exposure to multiple 5D themes. Each theme relationship is evaluated independently. A multi-theme company does not receive an automatic score bonus and does not require a single primary theme.

Theme exposure and portfolio theme concentration are separate governance questions. Supernova v1 does not impose a hard theme-concentration limit. Theme concentration shall be monitored and may be addressed by a future governance decision.

### Rationale

Multi-theme attribution preserves the structural nature of the 5D framework without conflating categorization with portfolio concentration.

---

## D-037 — Supernova Portfolio State and Leadership Role Separation

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova uses two independent governance dimensions.

Portfolio State:

* Approved
* Watchlist
* Review Required
* Retired

Leadership Role:

* Leader
* Challenger
* Candidate

Only Approved companies are eligible for accumulation. Leadership Role does not imply portfolio eligibility.

Example:

```text
NVDA → Approved + Leader
AMD  → Watchlist + Challenger
```

### Rationale

Separating ownership state from leadership role prevents the existing lifecycle from incorrectly treating Approved Company and Leader as the same concept.

---

## D-038 — Supernova Company Scoring and Evidence Contract

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova retains the existing five company-scoring dimensions and weights:

* Theme Exposure — 20%
* Competitive Moat — 25%
* Leadership Position — 25%
* Growth Quality — 15%
* Execution Quality — 15%

The scoring model is judgment-assisted by evidence rather than fully formula-driven. Each reviewed dimension shall retain Score, Evidence, Assessment, and Review Date. Qualitative anchors shall support score assignment. Raw metrics may inform an assessment but do not mechanically determine the score unless a separate rule is explicitly approved.

Company Score does not automatically determine Portfolio State or Leadership Role and is not a purchase-timing signal.

### Rationale

The existing dimensions and weights provide a stable v1 structure while avoiding false precision from unapproved metric-to-score formulas.

---

## D-039 — Supernova Approved Company Capacity

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova v1 does not impose a hard maximum Approved Company count. The current five Approved Companies remain the current portfolio state and are not a hard cap. Any future maximum or target range must be established by an explicit governance decision before additional Approved Companies are admitted beyond the current governance intent.

### Rationale

The repository contains unresolved maximum-capacity issues, but no canonical approved numeric cap. An earlier proposed 10–15 range is not treated as an approved decision.

---

## D-040 — Supernova Equal Weight Target and Smart DCA

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

The target portfolio weight for each Approved Company is equal weight:

```text
Target Weight = 1 / N
```

Monthly DCA capital shall be allocated preferentially toward underweight Approved Companies to move the portfolio toward target equal weights. Existing holdings are not sold solely to correct market-driven drift.

Conceptually:

```text
Deficit_i = max(Target Weight_i - Current Weight_i, 0)
DCA Allocation_i
= Deficit_i / Sum(Deficit) × Monthly DCA
```

Company Score does not determine DCA allocation or purchase timing.

### Rationale

Equal Weight defines the target state; Smart DCA defines the contribution method. This separates portfolio construction from research scoring and reduces unnecessary selling.

---

## D-041 — Supernova Replacement and Portfolio Transition Governance

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Replacement follows three separate stages:

1. Research / Detection
2. Governance Decision
3. Portfolio Transition

A challenger becoming stronger is a review trigger, not an automatic trade trigger. Score alone cannot automatically replace an Approved Company. Normal replacement occurs at the next regular review cycle after governance approval. Emergency Review may be used for clear structural thesis failure.

Replacement and Retirement are distinct:

* Replacement: Approved Company A is replaced by Approved Company B.
* Retirement / Exit: Approved Company A is removed without requiring a replacement.

Price movement alone does not trigger replacement.

### Rationale

Separating detection, governance, and execution prevents research signals from becoming unintended automatic trades.

---

## D-042 — Supernova Candidate and Watchlist Lifecycle Governance

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Candidate and Watchlist are research/portfolio-state stages. Promotion and removal use explicit eligibility criteria and documented evidence; company scores inform decisions but do not automatically trigger state transitions.

Minimum Approved eligibility includes:

* Clear relationship to at least one approved 5D theme
* Theme remains structurally valid
* Competitive position is sufficient
* Long-term growth thesis is credible
* No core thesis disproof
* Rational portfolio-level reason for inclusion relative to the current Approved Universe
* Evidence recorded
* Governance approval

Short-term price movement alone does not trigger promotion or removal.

### Rationale

A relative governance decision is more appropriate than an arbitrary numeric threshold for long-horizon thematic equities.

---

## D-043 — Supernova Theme Health and Lifecycle Evaluation

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Theme Evaluation is a separate layer from Company Evaluation. Supernova may record a 0–100 Theme Health Score as an evidence-assisted governance input, together with Evidence, Assessment, State, Trend, and Review Date.

Theme State remains qualitative:

* Emerging
* Developing
* Established
* Mature
* Declining

Theme scores are not portfolio allocation weights and are not purchase-timing signals. Theme Score is not mechanically combined with Company Score. State transitions require documented evidence and governance review rather than automatic numeric thresholds.

Supernova v1 does not allocate portfolio capital directly by Theme.

### Rationale

Theme Health evaluates the structural investment environment, while Company Score evaluates company quality. Keeping these layers separate preserves the 5D framework without creating an unnecessary composite score.

---

## D-044 — Supernova Evidence, Assessment, and Review Traceability

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova research evaluations shall preserve Evidence, Assessment, Score where applicable, and Review Date as separate but linked records. Evidence provenance should be retained where practical, with primary company filings and official disclosures preferred for material claims and reliable secondary or analytical sources used as supplements.

Historical assessments shall remain traceable across review cycles.

### Rationale

Traceable evidence prevents scores from becoming unexplained numbers and allows future reviews to distinguish changed facts from changed judgment.

---


---

## D-045 — Supernova Company Score Aggregation Contract

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova Company Score is the weighted aggregation of the five approved company-scoring dimensions:

* Theme Exposure — 20%
* Competitive Moat — 25%
* Leadership Position — 25%
* Growth Quality — 15%
* Execution Quality — 15%

All five dimensions are required. Missing dimensions are not imputed and remaining dimensions are not reweighted. Duplicate or unsupported dimensions invalidate the Research Record for scoring. The resulting weighted score is rounded to the nearest integer using conventional half-up rounding.

Company Score remains a governance input and does not automatically assign Portfolio State, Leadership Role, Replacement Risk, or a trading action.

### Rationale

A deterministic aggregation rule makes the approved scoring framework reproducible while preserving the existing evidence-assisted judgment model at the dimension level. Requiring complete dimension coverage prevents partial evidence from silently changing the meaning of the score.


## D-046 — Supernova Score-to-Governance Decision Boundary

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Company Score, Leadership Role, Portfolio State, and Replacement Risk remain separate governance dimensions. Company Score is evidence for governance review but does not automatically determine any of the other dimensions.

Governance outcomes shall be recorded explicitly through a Governance Decision containing:

* Company Score
* Portfolio State
* Leadership Role
* Replacement Risk
* Action
* Rationale
* Evidence Summary
* Review Date
* Approver

Approved actions are limited to the governed decision set: Continue, Promote, Review, Replace, or Retire. Numeric score thresholds for these actions or states are not defined in v1.

Replace applies only to an Approved company undergoing a documented replacement decision. Retire applies when an Approved company is removed without requiring a replacement.

### Rationale

This preserves the distinction between deterministic score aggregation and qualitative investment governance. It prevents a high or low score from becoming an unintended trading or lifecycle signal.


---

## D-042 — Orion Investment Framework and Common Portfolio Domain Architecture

### Status

Approved

### Decision

The previous "one Monitoring Framework + three Portfolio Engines" model is superseded. Orion shall use five Investment Frameworks:

* Aurora — Monitoring / Market Environment Framework
* Moon — Dynamic Asset Allocation Framework
* Orbit — Static Asset Allocation Framework
* Supernova — Equity Satellite Framework
* Phoenix — Digital Asset Satellite Framework

Moon, Orbit, Supernova, and Phoenix are equal-level, independently governed Investment Frameworks. Engine is an implementation/runtime concept and is not an investment-level category.

### Common Portfolio Domain

PortfolioTarget, PortfolioState, RebalancePlan, ExecutionOrder, and Transfer are common Orion Portfolio Domain concepts. Moon-specific StrategyResult and ConsensusAllocation remain framework-specific.

### Scope

Orion manages the investment Frameworks and Portfolios for Moon, Orbit, Supernova, and Phoenix. Planet KRW, Planet USD, Deep AN/PN/DC, and Asteroid are outside Orion's managed Portfolio scope because they do not require Orion framework-level monitoring or decision support.

### Portfolio / Account Boundary

Portfolio is a logical investment-management unit. Account is a custody/accounting boundary. A Portfolio may be implemented through one or more Accounts. Position is the canonical actual holding of an Asset within an Account. Cash is an Account-level balance.

Portfolio Value and Current Allocation are derived from Position and Cash. PortfolioTarget is the canonical source for desired allocation. PortfolioState is the canonical current Portfolio state; PortfolioSnapshot is a historical capture of that state.

Transfer is distinct from Rebalance. Moon → Orbit asset movement is an operational Transfer and does not create an architectural dependency between Moon and Orbit.

### Consequences

* The Portfolio Domain is reusable across all four portfolio-producing frameworks.
* Orion does not need to model every real-world account or asset held by YJ.
* Overall Portfolio View, when needed, is derived and is not a canonical source of truth.
* Existing Moon-specific portfolio concepts are promoted only where they are framework-independent.

### References

* Orion_Technical_Architecture.md
* Orion_Operating_Architecture.md
* Orion_Data_Model.md
* Orion_Domain_Model.md
* Orion_State_Model.md

---

## D-043 — Portfolio State and Custody Truth Boundary

### Status

Approved

### Decision

Asset is reference/master data. Position is the canonical actual holding state. Cash is an Account-level balance. Portfolio Value and Current Allocation are derived valuation outputs. PortfolioTarget is desired state, while PortfolioState is current Portfolio state. PortfolioSnapshot is a historical capture.

### Rationale

This separation prevents target allocation, actual holdings, valuation, custody state, and execution instructions from being collapsed into one Portfolio object.

---
