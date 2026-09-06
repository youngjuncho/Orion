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

```text
Framework
    │
    ▼
Engine
    │
    ▼
Entity
    │
    ▼
Score
    │
    ▼
State
    │
    ▼
Event
```

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

---

# StrategyResult

Output produced by a strategy execution.

Fields:

* strategy_name
* signal_date
* selected_assets
* weights
* score
* state

---

# Portfolio

Represents a framework allocation.

Fields:

* framework
* allocations
* rebalance_date
* status

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
