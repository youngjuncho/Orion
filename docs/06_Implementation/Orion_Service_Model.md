# Orion Service Model

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Orion_Engine.md
* Orion_Runtime.md
* Orion_State_Model.md
* Orion_Event_Model.md
* Orion_Configuration_Schema.md

---

# Purpose

This document defines the shared service layer of Orion OS.

Services provide reusable infrastructure capabilities shared across all frameworks.

Business logic remains within individual frameworks.

Services provide supporting functionality only.

---

# Implementation Status

The current implementation is intentionally limited to a single execution
and in-memory contracts. The service names below describe target boundaries;
they do not imply that a corresponding production service exists.

| Service | Current status |
|---|---|
| Configuration | Implemented through the strict core configuration loader |
| Logging | Implemented through core logging utilities |
| Service Registry | Implemented in-memory for one execution, with read-only snapshots for runtime context |
| Event | Event contract and in-memory EventStore exist; coordinated service not implemented |
| State / Persistence | In-memory StateStore exists; durable persistence is not implemented |
| Market Data | Data contracts exist; collection and normalization service not implemented |
| Dashboard / Reporting | Dashboard renderer and framework report entry points exist; coordinated services not implemented |

Runtime coordination, durable persistence, external publishing, and scheduler
integration remain specified-but-not-implemented work.

---

# Design Principles

## Separation of Concerns

Frameworks perform investment analysis.

Services provide infrastructure.

The Orion Engine coordinates execution.

---

## Shared Infrastructure

Common functionality should be implemented once and reused across the system.

Frameworks should not duplicate infrastructure code.

---

## Stateless Services

Services should avoid maintaining business state.

Persistent state is managed by the Orion Runtime and State Model.

---

# Service Architecture

```text
Orion Engine

↓

Runtime

↓

Services

├── Configuration Service
├── Market Data Service
├── Persistence Service
├── Logging Service
├── Dashboard Service
├── Reporting Service
└── Event Service

↓

Frameworks
```

---

# Configuration Service

Purpose:

Load and validate Orion configuration.

Responsibilities:

* Load configuration files
* Validate schemas
* Provide configuration access
* Support environment overrides

Examples:

* moon.yaml
* aurora.yaml
* phoenix.yaml

---

# Market Data Service

Purpose:

Provide normalized market data.

Responsibilities:

* Download market data
* Normalize symbols
* Cache datasets
* Validate completeness

Supported Data:

* ETFs
* Stocks
* Indices
* Economic Indicators

Future support:

* Cryptocurrency
* On-chain metrics

---

# Persistence Service

Purpose:

Persist Orion outputs.

Responsibilities:

* Save State
* Save Events
* Save Portfolio Snapshots
* Save Reports

Examples:

* JSON
* SQLite
* PostgreSQL

---

# Logging Service

Purpose:

Provide centralized logging.

Responsibilities:

* Execution Logs
* Framework Logs
* Error Logs
* Audit Logs

Logging should be standardized across all frameworks.

---

# Dashboard Service

Purpose:

Prepare dashboard data.

Responsibilities:

* Aggregate framework outputs
* Build dashboard cards
* Normalize presentation data

The Dashboard Service prepares data only.

Visualization is handled by the Dashboard.

---

# Reporting Service

Purpose:

Generate reports.

Examples:

* Monthly Summary
* Portfolio Report
* Aurora Report
* Strategy Report

Reports consume State and Event data.

---

# Event Service

Purpose:

Manage Orion events.

Responsibilities:

* Collect Events
* Validate Events
* Store Events
* Publish Events

Future versions may support external event subscriptions.

---

# Service Lifecycle

```text
Initialize

↓

Load Configuration

↓

Load Data

↓

Execute Frameworks

↓

Persist Results

↓

Generate Reports

↓

Shutdown
```

---

# Service Access

Frameworks may access services through the Orion Runtime.

Example:

```text
Runtime

↓

Configuration Service

Market Data Service

Logging Service
```

Frameworks should not instantiate services directly.

---

# Dependency Rules

Allowed:

```text
Framework

↓

Service
```

Not Allowed:

```text
Service

↓

Framework
```

Services remain independent of investment logic.

---

# Future Enhancements

Potential future services:

* Notification Service
* Scheduler Service
* Plugin Manager
* Authentication Service
* Machine Learning Service
* Backtesting Service

Status:

Research Only

Not Approved

---

# Related Documents

* Orion_Engine.md
* Orion_Runtime.md
* Orion_State_Model.md
* Orion_Event_Model.md
* Orion_Configuration_Schema.md
* Orion_Domain_Model.md
