# 2026-10-07 Core Reconciliation Addendum

> **Current authority:** `CORE-002`, `CORE-008`, and `CORE-015` supersede older generalized “framework results become State” wording in this document.

Current rules:

* State = current authoritative domain facts.
* `OrionStateSnapshot` = immutable materialized representation of State at a point in time.
* A calculation result does not automatically become State.
* Authoritative State changes only through an explicit State Transition from an Accepted Decision or approved domain operation.
* StateStore is the authoritative current-state commit boundary.
* Transition events are staged before commit and recorded only together with a successful State commit.

---

> **Document status:** The original body below was marked Draft in July 2026 and is retained as historical context. The reconciliation rules above and current Core contracts take precedence where older state-construction language conflicts; a Draft label is not implementation approval.

# Orion State Model

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Orion_Runtime.md
* Orion_Domain_Model.md
* Orion_Engine.md
* Orion_Glossary.md

---

# Purpose

This document defines the system-wide state model of Orion OS.

A State represents the current condition of an entity at a specific point in time.

The Orion State Model provides a standardized representation of framework outputs for dashboards, reports, CLI commands, and future APIs.

---

# Design Principles

## State Over Prediction

Orion evaluates the current state of the investment environment.

It does not predict future outcomes.

---

## Standardized Representation

Every framework exposes its results through standardized State objects.

Framework-specific calculations remain internal.

---

## Immutable Snapshot

Each execution produces a complete snapshot of the current system state.

Historical comparisons are performed by comparing snapshots.

---

# State Hierarchy

```text
Orion State

├── Aurora State
├── Moon State
├── Supernova State
└── Phoenix State
```

---

# Orion State

The Orion State represents the complete operational status of Orion OS.

Fields:

* Timestamp
* Execution ID
* Orion Version
* Framework States
* Portfolio State
* System Status

---

# Aurora State

Purpose:

Represent the current market environment.

Fields:

* Regime
* Aurora Score
* State Momentum
* Component Scores
* Cross Asset Summary

Example:

```text
Regime:
Risk On

Score:
82

Momentum:
Improving
```

---

# Moon State

Purpose:

Represent the current tactical allocation.

Fields:

* Active Strategies
* Strategy Results
* Consensus Allocation
* Current Portfolio
* Next Rebalance Date

Example:

```text
Strategies:
ADM
BAA
VAA

Allocation:

SPYM 45%

QQQM 20%

VGIT 15%

SGOV 20%
```

---

# Supernova State

Purpose:

Represent the current equity framework.

Fields:

* Approved Companies
* Watchlist
* Theme Summary
* Review Status

Example:

```text
Approved:
12 Companies

Watchlist:
18 Companies
```

---

# Phoenix State

Purpose:

Represent the current digital asset framework.

Fields:

* Category Leaders
* Challengers
* Watchlist
* Category Summary

Example:

```text
AI Infrastructure

Leader:
TAO

Challenger:
FET
```

---

# Portfolio State

Purpose:

Represent the consolidated portfolio managed by Orion.

Fields:

* ETF Allocation
* Equity Holdings
* Digital Asset Holdings
* Cash Allocation

Portfolio State aggregates outputs from all portfolio frameworks.

---

# System Status

Purpose:

Represent operational health.

Possible Values:

* Initializing
* Running
* Completed
* Warning
* Error

---

# State Lifecycle

```text
Framework Execution

↓

Framework Results

↓

State Construction

↓

Dashboard

CLI

Reports

Future API
```

---

# State Update Rules

A new State Snapshot is created after every successful engine execution.

Previous snapshots remain unchanged.

State updates are atomic.

---

# Historical State

Future versions may maintain historical state snapshots.

Potential use cases:

* Regime History
* Portfolio History
* Leadership Changes
* Allocation Changes

Status:

Research Only

---

# Dashboard Integration

The Orion Dashboard consumes State objects only.

No investment calculations occur within the Dashboard.

---

# CLI Integration

Example:

```text
orion state
```

Possible Output:

```text
Aurora

Risk On

Moon

SPYM 45%

QQQM 20%

VGIT 15%

SGOV 20%

System

Completed
```

---

# Relationship With Runtime

The Orion Runtime stores temporary execution data.

The Orion State represents the finalized system output.

Relationship:

```text
Orion Runtime

↓

Framework Results

↓

Orion State

↓

Dashboard / CLI / Reports
```

---

# Future Enhancements

Potential future additions:

* Historical State Repository
* State Comparison Engine
* Change Detection
* Alert Generation
* State Diff Visualization

Status:

Research Only

Not Approved

---

# Related Documents

* Orion_Runtime.md
* Orion_Engine.md
* Orion_Domain_Model.md
* Orion_Glossary.md
* Orion_Dashboard_Spec.md
