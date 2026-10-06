# Orion Domain Model

Version: 1.0

Status: Draft

Last Updated: 2026-07-28

Depends On:

* Orion_Domain_Model.md
* Orion_State_Model.md
* Orion_Event_Model.md
* Orion_Service_Model.md

---

# Purpose

Defines the implementation-level domain model for Orion OS.

This document bridges the logical architecture and the software implementation by defining the core domain objects used throughout the system.

All framework implementations should follow this model whenever practical.

---

# Design Principles

The Orion domain model is:

* Framework-independent
* State-driven
* Event-oriented
* Strongly typed
* Immutable where practical

Business logic belongs in Engines and Services.

Domain objects should primarily represent data.

---

# Core Domain Hierarchy

The Orion domain model distinguishes framework structure from portfolio
decision and execution concepts.

The general framework relationship is:

```text
Framework
    │
    ├── Engine
    │      │
    │      ▼
    │    Entity
    │      │
    │      ├── Score
    │      │
    │      └── State
    │
    └── Strategy
```

For any portfolio-producing framework, the common portfolio lifecycle is:

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

Current portfolio state is represented by `PortfolioState`. Historical captures are represented by `PortfolioSnapshot`.

```text
Account
├── Position → Asset
└── Cash
      ↓
PortfolioState
```

A rebalance plan is derived from the desired portfolio target and the
current portfolio state:

```text
PortfolioTarget + PortfolioState
            ↓
       RebalancePlan
```

`ExecutionOrder` represents a concrete trade instruction. Actual trade
execution is outside the current Moon MVP scope.

---

# Framework

Represents one investment framework.

Examples:

* Aurora
* Moon
* Supernova
* Phoenix

Fields:

* id
* name
* version
* status
* description

---

# Engine

Represents an execution engine.

Fields:

* id
* framework
* version
* enabled

Responsibilities:

* Execute analysis
* Produce results
* Publish events

---

# Entity

Represents any evaluated object.

Examples:

* Strategy
* Indicator
* Company
* Digital Asset
* Theme
* Category

Common Fields:

* id
* name
* framework
* status
* metadata

---

# Score

Represents a normalized evaluation.

Fields:

* value
* band
* calculated_at

Range:

0–100

Score Bands:

* Exceptional
* Strong
* Healthy
* Stable
* Neutral
* Weak
* Danger
* Critical

---

# State

Represents the current condition of an entity.

Fields:

* name
* previous_state
* changed_at

Examples:

Aurora

* Risk On
* Neutral
* Risk Off

Moon

* Risk On
* Risk Off
* Defensive

Supernova

* Leader
* Watch
* Review

Phoenix

* Leader
* Challenger
* Watchlist

---

# Strategy

Moon-specific entity.

Fields:

* name
* version
* status
* configuration

A registered strategy is not necessarily an active strategy.

Only explicitly activated strategies may participate in production execution.

---

# StrategyResult

Represents the output produced by one strategy execution.

Fields:

* strategy_name
* signal_date
* selected_assets
* weights
* score
* state

A StrategyResult represents the result of one strategy independently.
It does not represent the final Moon portfolio.

---

# ConsensusAllocation

Represents the allocation produced by aggregating multiple StrategyResults.

It represents strategy-level consensus before execution-asset translation.

Fields:

* allocations
* source_strategies
* calculated_at

ConsensusAllocation does not represent current holdings and does not
represent an execution order.

---

# PortfolioTarget

Represents the desired portfolio allocation using actual execution assets.

It is the target state that the portfolio should reach after applying
execution mapping.

Fields:

* allocations
* rebalance_date
* status

PortfolioTarget represents a desired state, not current holdings.

---

# Portfolio

Represents a logical investment unit managed by an Investment Framework.
Portfolio is distinct from Account.

# Account

Represents a custody/accounting boundary containing Positions and Cash.

# Asset

Represents the canonical identity/reference of an investable instrument.

# Position

Represents an actual holding of an Asset within an Account. Position is the canonical source for actual quantity and market value.

# Cash

Represents an Account-level cash balance.

# PortfolioState

Represents the current state of a Portfolio derived from underlying Position and Cash state.

Fields may include:

* current allocation
* portfolio value
* status
* valuation timestamp

# PortfolioSnapshot

Represents a historical, time-stamped capture of PortfolioState. It does not compete with PortfolioState as a canonical source of truth.

---

# RebalancePlan

Represents the changes required to move from the current portfolio state
to the desired portfolio target.

It is derived from:

```text
PortfolioTarget + PortfolioState
            ↓
       RebalancePlan
```

Fields:

* source_state
* target
* changes
* created_at
* status

A RebalancePlan describes required changes but does not itself execute trades.

---

# ExecutionOrder

Represents a concrete trade instruction derived from a RebalancePlan.

Fields and execution semantics are implementation concerns.

Actual order execution is outside the current Moon MVP scope.

---

# Transfer

Represents movement of an asset/value between Portfolios or Accounts. Transfer is distinct from Rebalance.

# Allocation

Represents a normalized portfolio allocation.

Fields:

* asset
* weight
* source

Allocation may be used as a component of StrategyResult,
ConsensusAllocation, or PortfolioTarget depending on context.

Example:

SPYM

Weight:

35%

Source:

Moon

---

# Indicator

Aurora-specific entity.

Fields:

* name
* category
* value
* score
* timestamp

---

# Company

Supernova-specific entity.

Fields:

* ticker
* name
* theme
* score
* state

---

# Digital Asset

Phoenix-specific entity.

Fields:

* symbol
* category
* score
* state

---

# Theme

Represents a long-term structural investment theme.

Fields:

* name
* score
* state
* trend

---

# Category

Represents a digital asset ecosystem.

Fields:

* name
* score
* leader
* state

---

# Review

Represents a scheduled evaluation.

Fields:

* framework
* entity
* review_type
* scheduled_date
* completed_date
* outcome

---

# Event

Represents a domain event.

Fields:

* id
* event_type
* timestamp
* framework
* entity
* payload

Examples:

* ScoreCalculated
* StateUpdated
* ReviewCompleted
* PipelineCompleted

---

# Configuration Reference

Configuration values should not be embedded in domain objects.

Runtime configuration is provided through:

* system.yaml
* moon.yaml
* aurora.yaml
* supernova.yaml
* phoenix.yaml

---

# Indicator

Aurora-specific entity.

Fields:

* name
* category
* value
* score
* timestamp

---

# Company

Supernova-specific entity.

Fields:

* ticker
* name
* theme
* score
* state

---

# Digital Asset

Phoenix-specific entity.

Fields:

* symbol
* category
* score
* state

---

# Theme

Represents a long-term structural investment theme.

Fields:

* name
* score
* state
* trend

---

# Category

Represents a digital asset ecosystem.

Fields:

* name
* score
* leader
* state

---

# Transfer

Represents movement of an asset/value between Portfolios or Accounts. Transfer is distinct from Rebalance.

# Allocation

Represents a normalized portfolio allocation.

Fields:

* asset
* weight
* source

Example:

SPYM

Weight:

35%

Source:

Moon

---

# Review

Represents a scheduled evaluation.

Fields:

* framework
* entity
* review_type
* scheduled_date
* completed_date
* outcome

---

# Event

Represents a domain event.

Fields:

* id
* event_type
* timestamp
* framework
* entity
* payload

Examples:

* ScoreCalculated
* StateUpdated
* ReviewCompleted
* PipelineCompleted

---

# Configuration Reference

Configuration values should not be embedded in domain objects.

Runtime configuration is provided through:

* system.yaml
* moon.yaml
* aurora.yaml
* supernova.yaml
* phoenix.yaml

---

# Relationships

```text
Framework
    │
    ├── Engine
    │      │
    │      ▼
    │    Entity
    │      │
    │      ▼
    │    Score
    │      │
    │      ▼
    │    State
    │
    ▼
Service
    │
    ▼
Event
```

---

# Mapping to Implementation

This document serves as the reference for:

* Python dataclasses
* Pydantic models
* Database schemas
* API contracts
* Dashboard models

Field names should remain consistent across all implementation layers whenever practical.

---

# Related Documents

* Orion_Domain_Model.md
* Orion_State_Model.md
* Orion_Event_Model.md
* Orion_Service_Model.md
* Orion_Runtime.md
