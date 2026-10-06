# Orion Event Model

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

The Orion Engine recognizes the following event categories.

| Category | Purpose |
|----------|---------|
| System | Engine lifecycle |
| Aurora | Market environment |
| Moon | Dynamic allocation framework |
| Orbit | Static allocation framework |
| Supernova | Equity research / satellite governance |
| Phoenix | Digital asset research / satellite governance |
| Portfolio | Common portfolio domain |
| Governance | Documentation and approval |

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

Represent changes within an individual Portfolio.

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
