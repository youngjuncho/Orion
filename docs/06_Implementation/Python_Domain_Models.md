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
| Framework | Framework |
| Strategy | Strategy |
| StrategyResult | StrategyResult |
| Portfolio | Portfolio |
| Allocation | Allocation |
| Score | Score |
| State | State |
| Review | Review |
| Decision | Decision |
| DashboardCard | DashboardCard |

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

Represents the aggregated portfolio allocation.

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