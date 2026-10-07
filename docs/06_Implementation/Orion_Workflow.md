# Orion Workflow

Version: 1.0

Status: Draft

Last Updated: 2026-07-28

Depends On:

* Orion_Runtime.md
* Orion_Scheduler.md
* Orion_Engine.md

---

# Purpose

Defines the end-to-end execution workflow of Orion OS.

The workflow describes how Orion coordinates framework execution from startup to result publication.

---

# Design Principles

Orion executes independent investment frameworks through a common orchestration layer.

Each framework is responsible for its own analysis, while Orion coordinates execution, state management, and reporting.

---

# Execution Overview

```text
User / Scheduler
        │
        ▼
Orion Runtime
        │
        ▼
Orion Scheduler
        │
        ▼
Orion Engine
        │
 ┌──────┼───────────────┐
 │      │       │       │
 ▼      ▼       ▼       ▼
Aurora Moon Orbit Supernova Phoenix
 │      │       │       │
 ▼      ▼       ▼       ▼
Pipelines
 │
 ▼
State Updates
 │
 ▼
Events
 │
 ▼
Services
 │
 ▼
Dashboards / Reports
```

---

# Execution Workflow

## Step 1

Start Runtime

The Orion Runtime initializes the execution environment.

Tasks:

* Load configuration
* Initialize services
* Restore runtime state

---

## Step 2

Run Scheduler

The Orion Scheduler determines which frameworks should execute.

Scheduling may be:

* Manual
* Scheduled
* Event-Driven

---

## Step 3

Execute Framework Engines

The Orion Engine invokes each enabled framework in the configured execution order.

Default order:

1. Aurora
2. Moon
3. Supernova
4. Phoenix

---

## Step 4

Run Framework Pipelines

Each framework executes its internal pipeline.

Typical pipeline stages include:

* Load data
* Evaluate entities
* Calculate scores
* Assign states
* Generate events
* Publish results

---

## Step 5

Update System State

Framework outputs are written to the shared Orion State Model.

This ensures consistent state across:

* Dashboards
* Reports
* Services

---

## Step 6

Publish Events

Frameworks publish lifecycle events.

Examples:

* StateUpdated
* ScoreCalculated
* ReviewGenerated
* PipelineCompleted

---

## Step 7

Refresh Services

Orion Services consume updated framework outputs.

Examples:

* Dashboard Service
* Reporting Service
* CLI Service

---

## Step 8

Complete Execution

The runtime records execution history and returns to an idle state.

---

# Framework Responsibilities

Aurora

* Evaluate market conditions
* Classify market regimes
* Produce environmental context

---

Moon

* Execute tactical allocation strategies
* Aggregate strategy outputs
* Produce portfolio allocations

---

Supernova

* Evaluate companies
* Score investment candidates
* Maintain long-term watchlists

---

Phoenix

* Evaluate digital asset ecosystems
* Identify category leaders
* Monitor leadership transitions

---

# State Flow

```text
Framework
      │
      ▼
Score
      │
      ▼
State
      │
      ▼
Event
      │
      ▼
Service
      │
      ▼
Dashboard
```

---

# Error Handling

Framework failures should:

* Preserve previous valid state
* Publish failure events
* Log diagnostic information
* Continue execution when possible

---

# Related Documents

* Orion_Runtime.md
* Orion_Scheduler.md
* Orion_Engine.md
* Orion_State_Model.md
* Orion_Event_Model.md
* Orion_Service_Model.md