# Python Domain Models

Version: 1.0

Status: Draft

Last Updated: 2026-07-28

Depends On:

* Orion_Domain_Model.md
* Orion_Runtime.md
* Orion_Service_Model.md

---

# Purpose

Defines how the logical Orion Domain Model is represented as Python domain classes.

This document serves as the bridge between the architecture documentation and the Python implementation.

Logical entities described in Orion_Domain_Model.md should map directly to Python classes whenever possible.

---

# Design Principles

The domain layer should:

* Represent business concepts only
* Remain independent of infrastructure
* Avoid framework coupling
* Support serialization
* Support future persistence
* Be testable in isolation

---

# Model Mapping

| Domain Model | Python Class |
|--------------|--------------|
| Framework | No standalone class yet; framework registry names are used |
| Strategy | `orion.frameworks.moon.models.Strategy` |
| StrategyResult | `orion.frameworks.moon.models.StrategyResult` |
| Portfolio | `orion.frameworks.moon.models.Portfolio` (minimal scaffold) |
| PortfolioTarget | `orion.frameworks.moon.models.PortfolioTarget` |
| Allocation | `orion.frameworks.moon.models.Allocation` |
| Score | `orion.core.models.Score` |
| State | `orion.core.models.State` |
| Review | No standalone class yet; `ReviewRecord` is a logical contract |
| Decision | `orion.core.models.DecisionRecord` |
| Event | `orion.core.events.Event` |
| OrionStateSnapshot | `orion.core.state.OrionStateSnapshot` |
| DashboardCard | `orion.core.models.DashboardCard` |

The table is intentionally explicit about concepts that are not implemented
yet. A logical entity must not be presented as a Python class until its
fields, lifecycle, and validation rules are approved.

`PortfolioTarget` is implemented separately with execution-asset allocations,
rebalance date, and caller-supplied status. The status is an opaque non-empty
label because the implementation documents do not define an allowed status
vocabulary.

## Data Contracts

| Contract | Python Class | Boundary |
|---|---|---|
| Normalized observation | `data.contracts.MarketDataPoint` | Typed scalar value and string metadata; immutable metadata snapshot |
| Observation batch | `data.contracts.MarketDataSet` | Unique observation identities, `as_of` label, immutable observation tuple |

These contracts do not determine source-specific fields, observation
freshness, missing-data behavior, or collection/normalization services.

---

# Framework

Represents one Orion investment framework.

Fields:

* id
* name
* version
* status
* description

---

# Strategy

Represents a strategy within Moon.

Fields:

* name
* version
* status

Methods:

* calculate()
* validate()

---

# StrategyResult

Represents the output of a strategy execution.

Fields:

* strategy_name
* signal_date
* selected_assets
* weights
* state
* score

---

# Portfolio

Represents the current minimal Moon portfolio scaffold. The separate target,
snapshot, rebalance-plan, and execution-order contracts remain specified but
not implemented; see `Moon_Object_Model.md`.

Fields:

* allocations
* rebalance_date
* total_weight

Methods:

* normalize()
* validate()

---

# Allocation

Represents a single asset allocation.

Fields:

* asset
* weight

---

# Score

Represents a normalized score.

Fields:

* value
* band
* description

---

# State

Represents the current state of an entity.

Fields:

* name
* description
* updated_at

Examples:

Moon

* Risk On
* Risk Off

Aurora

* Bull
* Neutral
* Bear

---

# Review

Represents a periodic review.

Fields:

* framework
* entity
* review_type
* outcome
* notes
* review_date

---

# Decision

Represents an architectural or investment decision.

Fields:

* decision_id
* title
* status
* category
* description
* created_at

---

# DashboardCard

Represents a dashboard component.

Fields:

* title
* state
* score
* trend
* updated_at

---

# Relationships

Framework

↓

Strategy

↓

StrategyResult

↓

Portfolio

↓

DashboardCard

---

# Serialization

Domain models should support:

* JSON
* YAML
* Future database persistence

---

# Validation

Every domain model should validate:

* Required fields
* Data types
* Business rules

Validation should occur before persistence or pipeline execution.

---

# Future Extensions

Potential additions:

* Historical snapshots
* Event references
* Audit metadata
* Version tracking

---

# Related Documents

* Orion_Domain_Model.md
* Orion_Runtime.md
* Orion_Service_Model.md
* Python_Package_Structure.md
