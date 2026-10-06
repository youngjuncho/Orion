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
├── Orbit State
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
* Framework States
* Derived Overall Portfolio View (optional)
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

Represent the current state of one Portfolio managed by one portfolio-producing Investment Framework.

PortfolioState is not a consolidated cross-framework source of truth.

Fields may include:

* Current Allocation
* Portfolio Value
* Position references
* Cash exposure
* Valuation Timestamp
* Status

Current Allocation and Portfolio Value are derived from underlying Position and Cash state.

# Overall Portfolio View

An optional derived aggregate view across Moon, Orbit, Supernova, and Phoenix. It is not a canonical source of truth and must not replace individual PortfolioState objects.

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
