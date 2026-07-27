# Orion Engine

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Orion_Runtime.md
* State_Model.md
* Event_Model.md
* Service_Model.md
* Moon_Engine.md
* Aurora_Engine.md

---

# Purpose

This document defines the top-level execution engine of Orion OS.

The Orion Engine coordinates framework execution, manages the runtime lifecycle, and provides a unified execution interface for the system.

Individual investment logic remains the responsibility of each framework.

---

# Responsibilities

The Orion Engine is responsible for:

* Initializing the runtime
* Loading configuration
* Starting framework engines
* Coordinating execution
* Managing state transitions
* Publishing events
* Handling shutdown procedures

The Orion Engine does not implement investment logic.

---

# System Architecture

```text
                 Orion Engine
                      │
        ┌─────────────┼─────────────┐
        │             │             │
    Runtime      Event Bus     State Manager
        │
        ├───────────┬───────────────┐
        │           │               │
Aurora Engine  Moon Engine  Supernova Engine  Phoenix Engine
```

---

# Startup Sequence

The Orion Engine starts the system in the following order.

1. Initialize Runtime
2. Load Configuration
3. Register Services
4. Restore Previous State
5. Start Framework Engines
6. Publish Startup Event

---

# Runtime Coordination

The Orion Engine provides the execution context shared by all framework engines.

Shared resources include:

* Configuration
* Data Services
* Logging
* Event Bus
* State Manager

---

# Execution Flow

Each execution cycle follows the same sequence.

```text
Runtime Tick

↓

Collect Market Data

↓

Aurora Engine

↓

Moon Engine

↓

Supernova Engine

↓

Phoenix Engine

↓

State Update

↓

Dashboard Update

↓

Persist State
```

Framework execution order may evolve in future releases.

---

# Engine Lifecycle

Every framework engine follows the same lifecycle.

```text
Initialize

↓

Load Data

↓

Execute

↓

Publish Events

↓

Update State

↓

Complete
```

---

# Event Coordination

The Orion Engine routes events through the Event Bus.

Typical events include:

* RuntimeStarted
* MarketDataUpdated
* FrameworkCompleted
* PortfolioUpdated
* RuntimeStopped

---

# Error Handling

Framework failures should be isolated whenever possible.

The Orion Engine should:

* Log failures
* Publish error events
* Preserve runtime stability
* Continue execution of unaffected frameworks

Critical failures may terminate the runtime.

---

# Configuration

The Orion Engine loads configuration from:

```text
config/

system.yaml
moon.yaml
aurora.yaml
supernova.yaml
phoenix.yaml
```

Configuration is managed through the Configuration Service.

---

# Dashboard Integration

The Orion Engine publishes normalized state information for dashboard consumers.

Examples:

* Orion Dashboard
* Moon Dashboard
* Aurora Dashboard

Dashboards consume published state and do not execute framework logic directly.

---

# CLI Integration

Example commands:

```text
orion run

orion moon run

orion aurora run

orion dashboard
```

The CLI invokes the Orion Engine, which coordinates all framework execution.

---

# Future Enhancements

Potential future additions:

* Parallel framework execution
* Distributed execution
* Scheduled automation
* Plugin architecture
* Cloud deployment

Status:

Research Only

Not Approved

---

# Related Documents

* Orion_Runtime.md
* State_Model.md
* Event_Model.md
* Service_Model.md
* Moon_Engine.md
* Aurora_Engine.md
* Supernova_Engine.md
* Phoenix_Engine.md