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

* Bull ??Bear Watch
* Bear ??Bull Watch

Aurora must report both:

1. Current Regime
2. Regime Direction

Status: Approved

Date: 2026-06-21

---

## D-021 ??Phoenix Scope and Core Digital Asset Separation

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

Approved

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

??
Market Context

??
Investor Interpretation

??
Moon / Supernova / Phoenix

??
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

### D-023 Terminology Reconciliation Note

D-023 is retained as the historical decision establishing Aurora as monitoring and Moon/Supernova/Phoenix as portfolio-oriented domains. Its historical terms ?�Monitoring Layer??and ?�Portfolio Engine??are superseded for Core architecture terminology by D-025 and the CORE-001 baseline: Aurora/Moon/Orbit/Supernova/Phoenix are **Frameworks**, and an **Engine** is a calculation/analysis module inside a Framework. The canonical application execution boundary is **Orion Runtime**.

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

### Decision

Moon shall use the following canonical portfolio domain model.

```text
StrategyResult
      ??ConsensusAllocation
      ??PortfolioTarget
      ??RebalancePlan
      ??ExecutionOrder
```

Current portfolio state is represented independently:

```text
PortfolioSnapshot
      ??Current Holdings
```

A `RebalancePlan` is derived from:

```text
PortfolioTarget + PortfolioSnapshot
      ??RebalancePlan
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
      ??Total Return Measurement
      ??ADM Strategy Calculation
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

# D.1?�D.2 Decision Review & Decision Lifecycle

## Context

Orion??Decision Review ?�역?�서 Analysis, Evidence Snapshot, Recommendation, User Decision, Review Record, Note �?관�?Relation)??lifecycle�?provenance�?명확???�의?�다.

?�심 목적?� ?�음�?같다.

* Analysis?� Recommendation??lifecycle??분리?�다.
* Recommendation�?User Decision??lifecycle??분리?�다.
* Review가 Recommendation ?�는 Decision??직접 ?�정?��? ?�도�??�다.
* 기존 ?�단???�정??경우 기존 기록??변경하지 ?�고 ?�로??기록???�성?�다.
* 모든 중요???�단�?변경의 provenance�?추적 가?�하�??�다.
* ?�재 ?�태�?mutable pointer??별도 status field???�존?��? ?�고 lifecycle�?lineage?�서 결정?????�도�??�다.

---

## D.1 ??Decision Review Framework

### 1. Architecture Boundary

Orion???�단 ?�름?� ?�음�?같이 분리?�다.

```text
Analysis
   ??Evidence Snapshot
   ??Recommendation
   ??User Decision

Review Record
   ?��? Recommendation / Decision???�향??주는 trigger?� 결과�?기록
```

Actual Trading?� Orion???��? ?�역?�다.

```text
Analysis
??Recommendation
??User Decision
??Actual Trading (Outside Orion)
```

Orion?� ?�제 주문 ?�행 ?��????�행 결과�?User Decision??lifecycle??반영?��? ?�는??

### 2. Recommendation Immutability

Recommendation?� Immutable?�다.

Recommendation???�용??변경되?�야 ?�는 경우 기존 Recommendation???�정?��? ?�는??

```text
R1 = Superseded
R2 = Active
```

R2??R1??`Supersedes`?�다.

Recommendation???�성?�면 ?�로??User Decision?� `Pending`?�로 ?�작?�다.

### 3. Evidence Snapshot

Recommendation ?�성 ???�용??Evidence Snapshot?� 고정?�다.

Analysis가 ?�후 변경되?�라???�시 Recommendation???�떤 evidence�?기반?�로 만들?�졌?��? ?�현?????�어???�다.

Provenance:

```text
Analysis Version
      ??Evidence Snapshot
      ??Recommendation
      ??User Decision
```

### 4. Review Trigger

Review???�음 ??종류??trigger�?발생?????�다.

* Regular Review
* Material Change

Change Detection�?Material Change ?�단?� 별개??개념?�다.

Review??변경이 감�??�었?�는 ?�실�?그것??Recommendation 변경을 ?�구?�는지 ?��?�?분리?�서 ?�단?�다.

### 5. Review Result

Review Result???�음 ??가지�?구분?�다.

* `No Change`
* `Reconsideration Required`
* `Recommendation Change Required`

`No Change`??명시?�인 Review Record�??�긴??

Review Record ?�체가 Recommendation??직접 변경하지 ?�는??

### 6. Reconsideration

`Reconsideration Required`??경우 Recommendation?� ?��??�다.

기존 Active User Decision?� `Superseded`가 ?�고 ?�로??Pending User Decision???�성?�다.

```text
Recommendation R1
    ??Decision D1 = Superseded
Decision D2 = Pending
```

### 7. Recommendation Change

`Recommendation Change Required`??경우 기존 Recommendation??Superseded 처리?�고 ?�로??Recommendation???�성?�다.

기존 Recommendation???�재 Active/Pending Decision??Superseded 처리?�다.

??Recommendation?�는 ?�로??Pending Decision???�성?�다.

기존 Decision history�??�로??Recommendation?�로 복사?��? ?�는??

Recommendation �?lineage??`Supersedes` 관계로 ?�결?�다.

---

# D.2 ??Decision Lifecycle & Relation Model

## 1. User Decision Lifecycle

User Decision??lifecycle?� ?�음 ??가지??

```text
Pending
Active
Superseded
```

`Rejected`??lifecycle???�니??Outcome?�다.

?�라??

```text
Status = Active
Outcome = Rejected
```

가 가?�하??

Outcome?� ?�음 ??가지�??�한?�다.

* `Accepted`
* `Rejected`

Conditional Acceptance??별도 lifecycle???�니??

```text
Outcome = Accepted
Conditions = <condition>
```

?�로 ?�현?�다.

조건???�는 Accepted Decision?� `Conditions = null`?�다.

Rejected Decision?�도 Conditions�??????�다.

## 2. Decision Immutability

User Decision?� Immutable?�다.

?�음 ?�항??변경되�??�로??Decision???�성?�다.

* Outcome 변�?* Conditions???��? 변�?* Recommendation 변경에 ?�른 ?�로???�단
* Reconsideration???�른 ?�로???�단

기존 Decision?� `Superseded`�??�긴??

?�순??wording-only clarification?� Decision??변경하지 ?�고 별도??Note/Clarification?�로 기록?�다.

## 3. Decision Supersession

??Decision??기존 Decision???�체하??경우:

```text
New Decision
   ?��? Supersedes Decision
   ?��? triggered_by_review (?�당?�는 경우)
```

기존 Decision??`Superseded Reason`???�수�?기록?�다.

Recommendation 변�??�문??Decision??Superseded?�는 경우:

```text
Superseded Reason = Recommendation Superseded
superseded_by_recommendation_id = R2
```

Superseded??Decision??Outcome�?Conditions??변경하지 ?�는??

## 4. Current Decision

Current Decision?� 별도??`current_decision_id` pointer�??�?�하지 ?�는??

Lifecycle??기반?�로 결정?�다.

Recommendation ?�나???�??

* Active Decision?� 최�? 1�?* Pending Decision?� 최�? 1�?
�??�용?�다.

Reconsideration ??기존 Active Decision??먼�? Supersede?�고 ?�로??Pending Decision???�성?�다.

?�라???�일 Recommendation ?�래?�서 `Active + Pending` Decision???�시???��??��? ?�는??

Pending Decision??존재?�는 ?�태?�서 추�? Review가 발생?�면 ?�로??Pending Decision??만들지 ?�고 기존 Pending Decision???��??�며 Review Record�?추�??�다.

?? Recommendation ?�체가 변경되�?기존 Pending Decision??Superseded?�고 ?�로??Recommendation???�로??Pending Decision???�성?�다.

## 5. Recommendation?�Decision Relationship

Recommendation�?User Decision?� 1:N 관계다.

?�나??Recommendation?�는 ?�러 historical Decision??존재?????��?�??�재 ?�효??Decision?� lifecycle 규칙???�라 결정?�다.

??Recommendation?� ?�전 Decision history�?복사?��? ?�는??

---

# Review / Decision Interaction

Review?� User Decision?� ?�립 객체??

Review Record???�단??trigger?�고 근거�??�기지�?Recommendation?�나 Decision??직접 ?�정?��? ?�는??

```text
Review Record
   ?��? No Change
   ?��? Reconsideration Required
   ?��? Recommendation Change Required
```

??Decision??Review ?�문???�성??경우 `triggered_by_review`�??�당 Review Record�?참조?�다.

`No Change` Review?�서??기존 Active Decision??그�?�??��??�다.

---

# Note / Clarification

Note/Clarification?� Decision 변경을 ?�?�하지 ?�는??

Note??Immutable?�며 ?�음 ?�보�?가진다.

* `created_at`
* `created_by`
* `note_type`
* `content`
* `target_type`
* `target_id`

`created_by`???�재 ?�계?�서 ?�음?�로 ?�한?�다.

* `User`
* `System`

Note Type 초기 집합:

* `Clarification`
* `Correction`
* `Context`
* `Observation`
* `Other`

`Other`�??�택?�면 `Other Type Description`???�수�??�다.

Note???�음 주요 객체??attach?????�다.

* Analysis
* Evidence Snapshot
* Recommendation
* User Decision
* Review Record

Note???�른 Note?�도 ?�결?????�다.

초기 Relation Type:

* `Supersedes`
* `Related To`

`Related To`??undirected relation?�다.

`Supersedes`??directed relation?�다.

Self-reference??금�??�다.

`Supersedes` cycle?� 금�??�다.

중복 Relation??금�??�다.

---

# Supersedes Relation

`Supersedes` 관�??�체??provenance???��?�?취급?�다.

?�반?�으�?source??`created_at`?� target보다 ?�후?�야 ?�다.

?? migration/import?�서??temporal validation exception???�용?�다.

Exception?� ?�음 ?�보�?가진다.

* `exception_type`
* `exception_description`

`exception_type = Other`??경우 ?�세 ?�명???�수�??�다.

Exception 기록 ?�체??Immutable?�다.

?�못 ?�성??`Supersedes` 관계는 직접 ??��?�거??취소?��? ?�는??

별도??`Invalidates Supersedes` 관계�? ?�성?�여 ?�당 Supersedes 관계�? 무효?�한??

---

# Invalidates Supersedes

?�못??`Supersedes` 관계는 ?�음 구조�??�정?�다.

```text
Supersedes Relation
       ??Invalidates Supersedes
```

`Invalidates Supersedes`???�정 `Supersedes Relation ID`�?직접 참조?�다.

?�재 ?�효?��? 별도??status field가 ?�니??lineage?�서 ?�출?�다.

`Invalidates Supersedes` 관�??�체??Immutable?�다.

`Invalidates Supersedes` ?�체�??�시 invalidate?�는 recursive 구조???�용?��? ?�는??

?�???�못??invalidation?� 별도??Correction?�로 ?�정?�다.

---

# Correction

Correction?� ?�정 `Invalidates Supersedes` 관계�? ?�정?�기 ?�한 Immutable 기록?�다.

?�수 ?�보:

* `target_relation_id`
* `correction_type`
* `description`
* `created_at`
* `created_by`

`created_by`???�재 ?�계?�서 ?�음?�로 ?�한?�다.

* `User`
* `System`

?�재 Correction Type?� 최소 모델�??�음 ?�나�??�의?�다.

* `Restore Validity`

�?

```text
Invalidates Supersedes
       ??Correction
       ??Restore Validity
```

Correction?� ?�일??Invalidates Supersedes 관계에 ?�???�러 �?존재?????�다.

Correction?� 기존 Correction???�정?�거????��?��? ?�는??

?�재 ?�태�?결정???�는 가??최근 Correction???�용?�다.

?�렬 규칙:

1. `created_at`
2. ?�일 timestamp??경우 `Correction ID`

`Correction ID` ?�체???�번?�나 ?�간???��?�?갖�? ?�는?? ?�순 identifier?�며 timestamp tie-breaker로만 ?�용?�다.

---

# Current Relation Validity

?�재 관계의 ?�효?��? ?�?�된 mutable status가 ?�니??lineage?�서 deterministic?�게 계산?�다.

개념?�으�?

```text
Supersedes
   ??Invalidates Supersedes
   ??Latest Correction
```

`Restore Validity` Correction??존재?�면 ?�당 `Invalidates Supersedes`???�력???�거??것으�?간주?�고 ?�래 `Supersedes` 관계�? ?�시 ?�효?�진??

?�라??Current State??별도??mutable state field가 ?�니??relation lineage??계산 결과??

---

# Core Invariants

?�음 규칙?� D.1?�D.2?�서 ?�정???�심 invariant??

1. Recommendation?� Immutable?�다.
2. User Decision?� Immutable?�다.
3. Review Record??Recommendation/Decision??직접 ?�정?��? ?�는??
4. Analysis 변�??�체??Recommendation 변경을 ?��??��? ?�는??
5. Recommendation 변경이 ?�요??경우 ?�로??Recommendation???�성?�다.
6. Decision 변경이 ?�요??경우 ?�로??Decision???�성?�다.
7. 기존 기록?� ??��?��? ?�고 Superseded lineage�??��??�다.
8. Recommendation ?�나?�는 최�? ?�나??Active Decision??존재?�다.
9. Recommendation ?�나?�는 최�? ?�나??Pending Decision??존재?�다.
10. Recommendation reconsideration ??Active + Pending Decision???�시???��??��? ?�는??
11. Actual Trading execution state??Orion??Decision lifecycle???�함?��? ?�는??
12. Current state??가?�한 경우 mutable pointer/status가 ?�니??lifecycle�?lineage?�서 ?�출?�다.
13. 모든 중요??변경�? provenance�??��??�다.
14. Supersedes lineage??cycle??가�????�다.
15. Invalidates �?Correction??Immutable provenance�??��??�다.

---

# Decision Traceability

?�번 D.1?�D.2 ?�계 결정?� Review Session??개별 결정 번호�??�해 추적?�다.

Review Session 결정 번호??permanent Decision ID가 ?�니??
Permanent architectural record??�?Decision Log??기록??D-xxx Decision�??�당 결정 블록?�다.

?�재 ?�인??Review Session 결정 범위:

* D.1-54 ~ D.1-67: Review / Recommendation / Decision lifecycle �?provenance
* D.2-01 ~ D.2-10: Review / Decision 기본 lifecycle
* D.2-11 ~ D.2-46: Decision lifecycle, Outcome, Conditions, Actual Trading boundary
* D.2-47 ~ D.2-80: Note, Relation, Supersedes, Invalidates 구조
* D.2-81: Invalidates Supersedes / Correction lifecycle 관??결정
* D.2-84 ~ D.2-100: Invalidates Supersedes Correction �?deterministic validity

D.2-82 �?D.2-83?� ?�재 Decision Review 기록?�서 ?�문 결정 ?�용??복구?��? 못했?��?�?�?Log?�서???��?�?추정?��? ?�는??

?�당 결정???�제�?존재?�고 구현 ?�는 문서 ?�합?�에 ?�향??주는 것으�??�인??경우, ?�래 Review 기록??복구????별도�?보완?�다.

개별 Review Session 결정�?�?Decision Log??permanent record ?�이??불일치�? 발견??경우, 추정?�로 ?�정?��? ?�고 provenance�??�인?????�정?�다.

---

# Consequences

??결정?�로 Orion??Decision Review 모델?� ?�음 ?�성??갖는??

* Append-only history
* Immutable Recommendation
* Immutable User Decision
* Explicit Review Record
* Explicit provenance
* Recommendation?�Decision lineage
* Supersedes lineage
* Invalidates lineage
* Correction lineage
* Deterministic current-state derivation

?�후 구현?�서????규칙???�의�??�순?�하거나 mutable status/pointer�??�체하지 ?�는??

구현??불�??�한 변경이 ?�요??경우 ?�로??Decision Record�??�성?�여 �?결정과의 관계�? 명시?�다.

---

---

## D-031 ??Phoenix Production Category Set

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

## D-032 ??Phoenix Multi-Category Membership and Unique-Asset Portfolio Construction

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

* DePIN ??Leader
* AI Infrastructure ??Challenger

Portfolio:

RENDER ??one position maximum

### Rationale

Category leadership and portfolio identity are separate concepts. Multi-category membership preserves analytical fidelity without creating duplicate portfolio positions.

---

## D-033 ??Phoenix Judgment-Assisted-by-Metrics Scoring Model

Date:

2026-10-05

Status:

Approved

Category:

Phoenix

### Decision

Phoenix scoring shall remain a judgment-assisted-by-metrics model rather than a fully formula-driven quantitative model.

Each 0??0 scoring dimension shall use qualitative anchors. Reviewers shall retain the principal evidence supporting each assigned score.

Raw metrics may inform the assessment but shall not mechanically determine the score unless a separate metric-to-score rule is explicitly approved.

### Minimum Review Record

Each reviewed score should record:

* Score
* Evidence
* Assessment
* Review Date

### Rationale

The existing 0??0 ranges are useful for structured comparison, but the current framework does not define sufficiently reproducible metric-to-score formulas. Requiring full automation at this stage would create false precision and unnecessary implementation scope.

---

## D-034 ??Phoenix Approved Leaders Registry

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

* Smart Contract Platforms ??SOL
* Oracle Networks ??LINK
* Real World Assets ??ONDO
* AI Infrastructure ??TAO
* Data Availability ??TIA

Only Approved leaders are eligible for formal Phoenix portfolio construction under D-022.

Configuration membership alone does not constitute approval evidence.

---

## D-035 ??Phoenix Canonical Replacement Risk and Leadership State Mapping

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
Score Gap = Leader Score ??Challenger Score
```

Canonical mapping:

| Score Gap | Replacement Risk | Leadership State | Action |
|---|---|---|---|
| 20+ | Low | Dominant | Hold |
| 10??9 | Medium | Stable | Monitor |
| 0?? | High | Competitive | Review |
| Challenger exceeds Leader | Critical | Transition | Review Required |

`Disrupted` is a confirmed transition state used when the Promotion Rule has been satisfied and the challenger is formally confirmed as the new leader. It is not a separate score-gap band.

The worked examples in Phoenix documentation must use this mapping literally.

### Rationale

The previous documents contained incompatible risk/state vocabularies and an example that translated `Gap 6 ??High Risk` into `Transition` without a defined rule. This decision removes that ambiguity and makes the score-gap calculation, risk, state, and action deterministic.

## D-036 ??Supernova Multi-Theme Attribution and Theme Concentration

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

## D-037 ??Supernova Portfolio State and Leadership Role Separation

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
NVDA ??Approved + Leader
AMD  ??Watchlist + Challenger
```

### Rationale

Separating ownership state from leadership role prevents the existing lifecycle from incorrectly treating Approved Company and Leader as the same concept.

---

## D-038 ??Supernova Company Scoring and Evidence Contract

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova retains the existing five company-scoring dimensions and weights:

* Theme Exposure ??20%
* Competitive Moat ??25%
* Leadership Position ??25%
* Growth Quality ??15%
* Execution Quality ??15%

The scoring model is judgment-assisted by evidence rather than fully formula-driven. Each reviewed dimension shall retain Score, Evidence, Assessment, and Review Date. Qualitative anchors shall support score assignment. Raw metrics may inform an assessment but do not mechanically determine the score unless a separate rule is explicitly approved.

Company Score does not automatically determine Portfolio State or Leadership Role and is not a purchase-timing signal.

### Rationale

The existing dimensions and weights provide a stable v1 structure while avoiding false precision from unapproved metric-to-score formulas.

---

## D-039 ??Supernova Approved Company Capacity

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova v1 does not impose a hard maximum Approved Company count. The current five Approved Companies remain the current portfolio state and are not a hard cap. Any future maximum or target range must be established by an explicit governance decision before additional Approved Companies are admitted beyond the current governance intent.

### Rationale

The repository contains unresolved maximum-capacity issues, but no canonical approved numeric cap. An earlier proposed 10??5 range is not treated as an approved decision.

---

## D-040 ??Supernova Equal Weight Target and Smart DCA

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

## D-041 ??Supernova Replacement and Portfolio Transition Governance

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

## D-042 ??Supernova Candidate and Watchlist Lifecycle Governance

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

## D-043 ??Supernova Theme Health and Lifecycle Evaluation

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Theme Evaluation is a separate layer from Company Evaluation. Supernova may record a 0??00 Theme Health Score as an evidence-assisted governance input, together with Evidence, Assessment, State, Trend, and Review Date.

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

## D-044 ??Supernova Evidence, Assessment, and Review Traceability

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

## D-045 ??Supernova Company Score Aggregation Contract

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova Company Score is the weighted aggregation of the five approved company-scoring dimensions:

* Theme Exposure ??20%
* Competitive Moat ??25%
* Leadership Position ??25%
* Growth Quality ??15%
* Execution Quality ??15%

All five dimensions are required. Missing dimensions are not imputed and remaining dimensions are not reweighted. Duplicate or unsupported dimensions invalidate the Research Record for scoring. The resulting weighted score is rounded to the nearest integer using conventional half-up rounding.

Company Score remains a governance input and does not automatically assign Portfolio State, Leadership Role, Replacement Risk, or a trading action.

### Rationale

A deterministic aggregation rule makes the approved scoring framework reproducible while preserving the existing evidence-assisted judgment model at the dimension level. Requiring complete dimension coverage prevents partial evidence from silently changing the meaning of the score.


## D-046 ??Supernova Score-to-Governance Decision Boundary

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

## D-047 ??Supernova Replacement Risk Definition

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova Replacement Risk is an independent governance assessment of the
likelihood that an Approved Company may no longer deserve its portfolio position
and may require Replacement or Retirement at a future governance review. It is
not a short-term price, valuation, or market-volatility risk measure and is not
mechanically derived from Company Score.

Replacement Risk shall be assessed using four evidence-based axes:

* Leadership Threat
* Moat Deterioration
* Growth / Execution Deterioration
* Thesis Integrity

A challenger is not required for Replacement Risk to escalate. Conversely, a
stronger challenger does not automatically imply high Replacement Risk when the
Approved Company's leadership and thesis remain durable.

Risk levels remain qualitative:

* Very Low ??no material replacement evidence; leadership and thesis remain strong
* Low ??concerns exist but long-term leadership and thesis remain durable
* Medium ??material warning signals warrant focused monitoring or review
* High ??core leadership, moat, growth, execution, or thesis has materially weakened
* Critical ??structural leadership or thesis is substantially broken and Replace or
  Retire is a realistic governance outcome

Replacement Risk escalation is a review trigger, not an automatic trading rule.
Final action remains a separate Governance Decision.

### Rationale

This definition preserves the governance boundary established in D-046 while
making Replacement Risk operationally assessable. It also prevents Supernova from
becoming a copy of Phoenix's challenger-relative replacement model: Supernova must
be able to recognize replacement risk caused by deterioration of the Approved
Company itself, even without a clear challenger.

---

## D-048 ??Supernova Governance Review Reproducibility Contract

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

Supernova V1 defines reproducibility at the **governance-record level**, not as identical independent human numeric scoring. A complete review must preserve sufficient evidence, assessments, dimension scores, temporal cutoff, Replacement Risk assessment, action, and governance decision to allow another reviewer to reconstruct the reasoning path.

Company Score aggregation remains deterministic under D-045 once the five dimension scores are assigned. V1 does not introduce numeric calibration thresholds for assigning the individual 0??00 dimension scores.

The canonical governance action vocabulary from D-046 is authoritative: `Continue`, `Promote`, `Review`, `Replace`, and `Retire`. Descriptive phrases may be used in rationale but must not become alternative action types.

`Primary Risk Driver` identifies the most decision-relevant concern. `None material` is valid when no material concern is identified.

`Evidence As Of` records the temporal evidence cutoff considered by the review and is distinct from `Review Date`.

### Rationale

The five-company baseline demonstrated that Company Score can be reconstructed deterministically from recorded dimension scores and that Replacement Risk can be documented without a challenger. Requiring identical human scores would introduce false precision into an intentionally evidence-assisted framework. The appropriate V1 control is traceability, canonical terminology, and explicit governance decisions.

### Consequence

No additional Replacement Risk formula or numeric threshold is required for Supernova V1. Future calibration may be introduced only through an explicit governance decision if repeated reviews demonstrate unacceptable reviewer divergence.

---

## D-049 ??Supernova Five-Company Baseline Governance Approval

Date:

2026-10-05

Status:

Approved

Category:

Supernova

### Decision

YJ approved the 2026-10-05 Supernova governance baseline for the five current Approved Companies: NVDA, GOOGL, ISRG, PLTR, and CEG.

The approved baseline is:

* NVDA ??Company Score 97, Approved, Leader, Replacement Risk Low, Action Continue
* GOOGL ??Company Score 93, Approved, Leader, Replacement Risk Low, Action Continue
* ISRG ??Company Score 97, Approved, Leader, Replacement Risk Very Low, Action Continue
* PLTR ??Company Score 95, Approved, Leader, Replacement Risk Low, Action Continue
* CEG ??Company Score 91, Approved, Leader, Replacement Risk Low, Action Continue

This decision confirms the governance state for the review cycle. It is not an automatic trade instruction and does not override the existing Portfolio Transition process. Future changes require the normal Supernova governance review and decision process.

Approver: YJ

### Rationale

The five-company baseline was reviewed after completion of the Supernova governance contracts, including Company Score aggregation, Replacement Risk, score-to-governance boundaries, lifecycle governance, and reproducibility. YJ approved the resulting records without requiring further governance redesign.


---

## D-050 ??Runtime Default Decision Acceptance Policy

Date:

2026-10-08

Status:

Approved

Category:

Runtime Governance

### Decision

The Orion Runtime default Decision Acceptance Policy is **Auto-Approval**.

A Framework continues to produce only a `DecisionCandidate`. The Framework does
not accept its own candidate and does not directly create authoritative state.
When the public Runtime executes the canonical decision lifecycle without an
explicit acceptance handler, the Runtime applies the Auto-Approval policy and
materializes the candidate as the existing `AcceptedDecision` contract.

The canonical lifecycle remains:

```text
DecisionCandidate
    ??Acceptance Policy
    ??AcceptedDecision
    ??StateTransition
    ??StateStore
    ??Domain Event
    ??EventStore
    ??RuntimeResult
```

Auto-Approval is a Runtime Governance acceptance policy. It is not investment
methodology, broker execution, order submission, fill, settlement, or a guarantee
that an external action occurs.

An explicit acceptance handler remains supported and takes precedence when a
caller requires rejection or conditional acceptance. `AcceptedDecision` remains
the authoritative acceptance representation.

The default is candidate-type agnostic. It also accepts a Moon
`RebalancePlanProposal` unless the caller supplies an acceptance handler that
rejects or conditionally accepts it. This acceptance does not submit or execute
orders.

### Rationale

The acceptance boundary is already part of the Core Runtime architecture. The
current MVP requires an acceptance handler even though Orion's intended operating
mode is automated. Making Auto-Approval the default removes unnecessary orchestration
friction while preserving the existing governance boundary and future ability to
introduce explicit review, rejection, or conditional acceptance.

### Consequence

No new Decision type or Framework responsibility is introduced. State transition,
StateStore commit, Domain Event creation, EventStore publication, failure isolation,
and the D-030 in-memory MVP boundary remain unchanged. Durable persistence, replay,
and external execution remain outside scope.

---

## D-051 ??ADM Signal-to-Execution Mapping

Date:

2026-10-10

Status:

Approved

Category:

Moon Strategy / Execution Mapping

### Issue Resolved

Before this decision, `ADM_Orion.md` specified VTI and VEU as risk assets and
SGOV as the defensive asset candidate, but neither the documented mapping nor
`ExecutionMapper` accepted these as signal inputs. Consequently, ADM output
could not be converted to the common `PortfolioTarget` through that mapping.

The current `config/moon.yaml` sets `active_strategies: []`; the mapping gap was
a gate before ADM activation, not a failure in an active production run.

### Research (2026-10-10)

Vanguard's published expense ratios are 0.03% for VTI, 0.04% for VEU, and
0.05% for VXUS (figures shown as of 2026-02-27 for VEU and VXUS; VTI's product
listing is current as of 2026-08-28). VXUS therefore is not cheaper than VEU
by expense ratio. VEU tracks the FTSE All-World ex-US Index; VXUS tracks the
FTSE Global All Cap ex US Index, which includes small-cap exposure and is not
an identical index substitution. A lower share price, if that is what
"cheaper" refers to, does not mean a lower fund expense ratio or equivalent
exposure.

Sources: [Vanguard VTI product listing](https://investor.vanguard.com/investment-products/list/all?assetclass=equity&filters=open&managementstyle=index&strategy=total_market_etfs), [Vanguard VEU product page](https://advisors.vanguard.com/investments/products/veu/vanguard-ftse-all-world-ex-us-etf), and [Vanguard VXUS product page](https://advisors.vanguard.com/investments/products/vxus/vanguard-total-international-stock-etf).

### Decision

ADM signal assets are also the execution assets for this mapping contract:

* VTI -> VTI
* VEU -> VEU
* SGOV -> SGOV

The existing BIL -> SGOV mapping remains in place for strategies that emit
BIL as their signal asset. Thus both BIL and ADM's direct SGOV signal resolve to
the SGOV execution asset.

This preserves ADM's specified instruments. No VEU -> VXUS substitution is
approved. This decision resolves the signal-to-execution mapping only; it does
not activate ADM, authorize a live trade, or approve any broker integration.
The existing `active_strategies: []` configuration remains unchanged.

### Implementation and Verification

The mapping contract and `ExecutionMapper` now explicitly identity-map VTI,
VEU, and SGOV. Runtime integration coverage exercises ADM selecting each of
these assets through `PortfolioTarget` construction. The focused Moon model
and runtime integration suites passed (24 tests, Python 3.12.13) on
2026-10-10. ADM remains inactive in configuration; this decision does not
enable strategy activation or live execution.

---

## D-052 ??Runtime Failure and Commit Semantics

Date:

2026-10-10

Status:

Approved

Category:

Runtime Governance

### Decision

The owner approved the following MVP semantics on 2026-10-10:

1. **All-or-nothing Orion-owned in-memory effects.** Stage Framework events,
   accepted transitions, the snapshot, and transition events; validate the
   complete write set; then publish state and events together. Any failed
   validation or coordinated store commit leaves both stores unchanged and
   closes an active session as `Error`.
   This guarantee does not roll back side effects performed externally by
   caller-supplied callbacks.
2. **One public run per `OrionRuntime` instance.** A second `run()` call is
   rejected. A separate execution uses a new Runtime with a new execution ID
   and fresh stores.
3. **Commit validation.** The snapshot execution ID must match the current
   execution and its status must be `Running`. Each transition's decision ID
   and entity type/ID must match its accepted candidate. All event execution IDs
   and duplicate IDs are validated before publishing anything. Previous-state
   continuity remains outside this MVP until authoritative entity-state
   projection is defined.

The decision changes event creation to pre-commit staging. Events are not
recorded unless the corresponding coordinated store commit succeeds.

### Implementation and Verification

Implemented with tests covering event-factory and store-append failures,
snapshot and entity correlation checks, and Runtime single-use. The full
repository test suite passed on 2026-10-10; Runtime, Event Model, State Model,
Handoff, roadmap, and status documentation now reflect the approved semantics.

---

## D-053 ??Portfolio Cash Valuation and Target Semantics

Date:

2026-10-10

Status:

Draft

Category:

Portfolio Domain / Moon

### Issue Under Review

Cash is modeled as an Account-level `CashBalance`, separate from Position.
At proposal time, `value_portfolio_state()` ignored `PortfolioState.cash` and
accepted a separate `cash_value` input. D-053 below resolves that gap.
`PortfolioTarget` allocations must sum
to 1 and have no explicit cash sleeve. Consequently, the contract does not say
whether cash is included in the valuation denominator, represented in target
weights, or treated as residual execution funding.

Balances may also use different currencies. Summing them without an approved
valuation-currency and FX-conversion boundary would not produce a meaningful
portfolio value.

### Decision Required

The owner must define:

* whether portfolio cash is included in total valuation and current asset
  weights;
* whether cash is an explicit target sleeve or remains outside the target as
  residual funding;
* which component supplies authoritative cash amounts and how duplicate
  account balances are aggregated;
* the valuation currency and the approved FX conversion boundary for
  multi-currency cash.

### D-053 ??Portfolio Cash Valuation and Target Semantics

Status: **Approved**
Decision date: 2026-10-10

1. Use `system.currency` as the valuation currency (currently KRW).
2. Treat `PortfolioState.cash` as the authoritative cash input. Reject
   duplicate `(account_id, currency)` balances rather than risk double-counting.
   Convert non-valuation currencies using
   caller-supplied, positive finite rates expressed as valuation-currency units
   per one unit of source currency. The portfolio layer performs no FX lookup.
3. Include converted cash in `PortfolioValuation.total_value` and therefore in
   the denominator used for current non-cash asset weights. `PortfolioTarget`
   remains fully invested with no cash allocation; cash stays as residual
   funding whose effect is reflected in the lower current asset weights.
4. Remove the separate `cash_value` argument so callers cannot silently omit
   the state cash balances. Missing FX for a non-valuation currency is an error.

The caller supplies `system.currency` as `valuation_currency`; asset prices
must already use that currency. FX rate source, timestamp/freshness policy,
and aggregation rules beyond duplicate-key rejection remain
caller/data-governance concerns.

### Implementation Evidence

The valuation and rebalance APIs consume `PortfolioState.cash`, convert with
explicit caller-supplied FX rates, and reject missing/invalid rates and
duplicate account/currency balances. Focused tests cover state cash valuation
and rebalance weights.

---

## D-054 — Default Acceptance of Rebalance Plan Proposals

Status: **Approved**
Date: 2026-10-10

Moon now emits a `RebalancePlanProposal` as a separate Runtime candidate. D-050
defines candidate-type-agnostic Auto-Approval as the default, so the plan is
automatically accepted in lifecycle runs without an explicit acceptance
handler. Acceptance is not order execution, but it records a plan as accepted
Runtime state when the caller's transition handler commits it.

The owner confirmed retaining D-050 as-is: Auto-Approve target and plan
proposals independently. Callers can still supply an acceptance handler to
reject or conditionally accept either candidate. Auto-Approval records
acceptance only; it does not submit or execute orders.

---

## D-055 — ADM Absolute-Momentum Signal Policy

Status: **Approved**
Date: 2026-10-10

The current ADM research describes absolute momentum relative to a cash or
defensive return, while `ADM_Orion.md` lists SGOV as the primary defensive
candidate and BIL/SHY as backups pending final approval. D-051 resolves the
signal-to-execution mapping for SGOV; it does not approve SGOV as the absolute-
momentum comparison benchmark. D-028 approves adjusted-price-based total-return
measurement, but the research marks the measurement standard pending
validation.

The owner approved SGOV as the absolute-momentum comparison benchmark and
approved a strict comparison: the selected risk asset is positive only when
its trailing-12-month return is greater than SGOV's trailing-12-month return.
Equal returns are false (Risk Off). Apply the same return horizon and
adjusted-price-based total-return convention to both instruments.

The approved comparison is implemented as the default `D-055` policy for
`compare_adm_absolute_momentum_returns()`. Provider choice, adjusted-price
source semantics, calendar interpretation, freshness limits, and production
governance provenance remain separate data-contract gates. ADM remains
inactive; this decision alone does not authorize signal assembly or activation.

---

## D-056 — ADM Provider-Independent Data Handling Defaults

Status: **Approved — engineering defaults only; provider contract remains open**
Date: 2026-10-10

The owner accepted the recommended provider-independent defaults for the ADM
data calculation boundary. For an explicitly supplied evaluation target and
12-month trailing target, select the latest eligible observation on or before
each target; never select a future observation. Use the same requested field,
target dates, and selection rule for VTI, VEU, and the SGOV comparison input.
If any required symbol, field, or endpoint is missing, invalid, stale under an
explicit caller policy, or conflicting, the calculation must fail closed and
must not fill, interpolate, or return a success-shaped partial result.

These defaults make selection deterministic and prevent look-ahead and silent
data substitution. They do not define how target dates are generated, approve
an exchange calendar or timezone, set a numeric freshness limit, resolve
provider-specific conflicts or revisions, or establish the permitted use or
adjustment semantics of any provider's price series. Those matters remain open
under PCD-01 through PCD-12. In particular, D-056 does not approve Yahoo
Finance or any other provider and does not authorize live collection, signal
assembly, or ADM activation.

The engineering boundary must retain enough selected-observation identity and
source metadata to explain a result. Durable snapshot storage and provider
revision precedence are not specified by this decision.

---

## D-057 — Alpha Vantage Monthly Adjusted Data Integration

Status: **Approved — private individual research scope; signal activation remains gated**
Date: 2026-10-10

The owner directed that the provider and integration be decided. Select Alpha
Vantage's `TIME_SERIES_MONTHLY_ADJUSTED` endpoint for VTI, VEU, and SGOV as
Orion's first concrete ADM source. The documented monthly series represents
the last trading day of each month and provides adjusted close plus dividend
information; Alpha Vantage states its adjusted pricing accounts for splits
and cash-dividend events. The strategy evaluates monthly, so this endpoint is
preferred over the premium daily-adjusted endpoint for the first integration.

The supported use is limited to private, individual investment research by the
user under Alpha Vantage's published terms and applicable account entitlement.
No redistribution, third-party display, organizational use, or commercial
service is authorized by this decision. If the actual use falls outside the
private individual scope, obtain written provider approval before fetching
data. The provider's documented adjustment method is accepted as the adapter
mapping for D-028's adjusted-price proxy, but historical revision behavior,
instrument coverage, and empirical parity remain subject to validation.

Implement a read-only provider adapter that loads all three instruments into
the canonical `MarketDataSet`, preserves provider/date/field/retrieval
provenance, enforces complete-batch validation, and fails closed on errors.
Read the API key only from `ORION_ALPHA_VANTAGE_API_KEY`; make three monthly
requests per load, sequentially, with a 15-second per-request timeout and no
retry, fallback, cache, or persistence. API errors or insufficient history
must reject the whole batch. The adapter does not calculate `ADMSignalInput`,
activate ADM, or imply a numeric freshness policy. Live execution remains
disabled until the open freshness and end-to-end governance gates are closed.
The provider currently documents a standard allowance of 25 API requests per
day; one full load uses three. Repeated manual runs remain subject to that
provider limit.

---

## D-058 — ADM Monthly Targets and Freshness Proposal

Status: **Proposed — freshness threshold requires owner approval**
Date: 2026-10-10

Recommend deriving the current endpoint as the last calendar day of the month
before the dataset's `as_of` month, which excludes a potentially incomplete
monthly bar. Derive the trailing endpoint as the last calendar day of the same
month in the prior year; this aligns monthly bars across leap years. The
provider's observation label remains the last trading day of each month, and
D-056's prior-observation-on-or-before selector remains in force. This target
rule is implemented by `derive_adm_monthly_target_dates()` as an explicit
engineering utility; its output does not itself authorize signal assembly.

Recommend a maximum calendar-age of seven days for each selected current and
trailing observation across VTI, VEU, and SGOV. This accommodates a month-end
falling on a weekend/holiday and short publication delay, while rejecting a
fallback to the previous monthly bar if the latest completed month is absent.
Apply one common limit to all required observations and fail closed if any
exceeds it. Keep the threshold caller-supplied until approved; do not silently
apply seven days to production calculations.

The proposal does not specify the next-trading-day execution date, session
timezone, publication-time SLA, provider revision handling, or ADM activation.
