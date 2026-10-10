# 2026-10-07 Core Reconciliation Addendum

> **Current authority:** `CORE-003` supersedes the historical event ordering/categories below where they conflict.

Two event categories are canonical:

* **Domain Event** — immutable historical fact / confirmed domain change.
* **Lifecycle Event** — Runtime/Framework execution lifecycle fact.

The canonical event identity contract is:

```text
event_id
event_type
event_category
occurred_at
execution_id
entity_type
entity_id
payload
```

`execution_id` is mandatory and provides correlation from one Runtime execution
through Framework results, accepted decisions, state transitions, and emitted
events. Legacy fields such as `source_framework`, state transition labels,
severity, descriptions, and review/decision references may be retained as
extension metadata but do not replace the canonical identity fields.

Examples of derived calculations that are not Events by default: ScoreCalculated, MetricCalculated, DashboardRendered, PortfolioWeightCalculated.

For state-changing operations:

```text
Accepted Decision → State Transition → successful State Commit → Domain Event
```

EventStore is append-only historical storage; Event Sourcing is not adopted.

---

## Runtime Event Correlation

`RuntimeSession.record_events()` is the MVP EventStore boundary. It accepts only
canonical `Event` instances whose `execution_id` matches the current
`ExecutionMetadata.execution_id`, rejects duplicate event identifiers, and appends
them to the execution-scoped in-memory EventStore.

For state-changing operations, `resolve_and_commit()` publishes the authoritative
`OrionStateSnapshot` first and then invokes its optional event factory. This keeps
the runtime ordering aligned with the canonical contract:

```text
Accepted Decision → State Transition → successful State Commit → Domain Event
```

The current implementation does not add durable persistence or Event Sourcing.

# Orion Event Model

> **Document status:** The original body below was marked Draft in July 2026 and is retained as historical context. The reconciliation addendum and current Core Event contract take precedence where older event ordering, publication, or storage language conflicts. A Framework does not publish directly to EventStore.

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Orion_Engine.md
* Orion_Runtime.md
* Orion_State_Model.md
* Orion_Domain_Model.md

---

# Purpose

This document defines the event model of Orion OS.

An Event represents a meaningful change that occurs during system execution.

Events provide the foundation for state updates, logging, notifications, automation, and future integrations.

---

# Design Principles

## State Changes Produce Events

Events are generated when the system detects meaningful changes.

Routine calculations that do not change system state should not generate events.

---

## Immutable Event Records

Once recorded, an Event must not be modified.

Historical analysis is performed by reviewing the event history.

---

## Framework Independence

Each framework may generate events independently.

The Orion Engine collects and processes all framework events.

---

# Event Lifecycle

```text
Framework Execution

↓

Event Generation

↓

Event Collection

↓

State Update

↓

Persistence

↓

Dashboard / CLI / Reports

↓

Future Notification Services
```

---

# Event Categories

The canonical event categories are defined by the Core event contract and are
independent of the Framework that produced the event. Framework identity, when
needed, is carried by `source_framework` or payload metadata.

| Category | Purpose |
|----------|---------|
| Domain Event | Immutable historical fact or confirmed domain change |
| Lifecycle Event | Runtime / Framework execution lifecycle fact |

Framework-specific event types such as Aurora, Moon, Supernova, Phoenix,
Portfolio, or Governance events are expressed through `event_type`,
`source_framework`, `entity_type`, and `payload`; they are not separate
canonical event categories.

---

# System Events

Purpose:

Represent Orion Engine lifecycle events.

Examples:

* Engine Started
* Engine Completed
* Engine Failed
* Configuration Loaded
* Runtime Initialized

---

# Aurora Events

Purpose:

Represent changes in market conditions.

Examples:

* Regime Changed
* State Momentum Changed
* Aurora Score Updated
* Indicator Threshold Crossed

Example:

```text
Previous Regime

Neutral

↓

Current Regime

Risk On
```

---

# Moon Events

Purpose:

Represent tactical allocation changes.

Examples:

* Strategy Signal Changed
* Consensus Allocation Updated
* Portfolio Rebalanced
* Strategy Activated
* Strategy Retired

Example:

```text
ADM

VTI

↓

VEU
```

---

# Supernova Events

Purpose:

Represent changes in equity research.

Examples:

* Company Approved
* Company Retired
* Theme Updated
* Watchlist Changed

---

# Phoenix Events

Purpose:

Represent changes in digital asset research.

Examples:

* Category Leader Changed
* Challenger Updated
* Watchlist Updated
* Category Created
* Category Retired

---

# Portfolio Events

Purpose:

Represent consolidated portfolio changes.

Examples:

* Allocation Updated
* Holding Added
* Holding Removed
* Cash Allocation Changed

---

# Governance Events

Purpose:

Represent controlled changes to Orion documentation and configuration.

Examples:

* Framework Updated
* Configuration Changed
* Decision Approved
* Strategy Added
* Strategy Removed

---

# Event Structure

Every Event contains the following fields.

Required Fields:

* Event ID
* Timestamp
* Category
* Event Type
* Source Framework
* Entity
* Previous State
* Current State
* Severity

Optional Fields:

* Description
* Metadata
* Related Decision
* Related Review

---

# Event Severity

Possible values:

* Information
* Notice
* Warning
* Critical

Severity indicates operational importance.

---

# Event Processing

The Orion Engine processes events after framework execution.

Processing sequence:

```text
Collect Events

↓

Validate

↓

Persist

↓

Update State

↓

Refresh Dashboard

↓

Generate Reports
```

---

# Event Persistence

Events should be stored as an append-only history.

Historical events enable:

* Audit trails
* State comparisons
* Portfolio history
* Regime history
* Leadership history

---

# Dashboard Integration

Dashboards may display recent events.

Examples:

* Latest Regime Change
* Latest Portfolio Rebalance
* Latest Approved Company
* Latest Category Leader

The Dashboard consumes Event records only.

It does not generate events.

---

# CLI Integration

Example:

```text
orion events
```

Example Output:

```text
2026-07-27

Aurora

Regime Changed

Neutral

↓

Risk On

Moon

Portfolio Rebalanced

SPYM

↓

QQQM
```

---

# Relationship With State Model

Events explain why the current State exists.

Relationship:

```text
Framework Execution

↓

Events

↓

State Update

↓

Dashboard / CLI
```

---

# Future Enhancements

Potential future additions:

* Event Filtering
* Event Subscription
* Notification Service
* Email Alerts
* Webhook Integration
* Event Replay

Status:

Research Only

Not Approved

---

# Related Documents

* Orion_Engine.md
* Orion_Runtime.md
* Orion_State_Model.md
* Orion_Domain_Model.md
* Orion_Dashboard_Spec.md
* Decision_Log.md
