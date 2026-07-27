# Orion Engine

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Orion_Operating_Architecture.md
* Orion_Data_Model.md
* Orion_Configuration_Model.md
* Moon_Object_Model.md
* Aurora_Interface.md
* Moon_Interface.md
* Supernova_Interface.md
* Phoenix_Interface.md

---

# Purpose

This document defines the execution engine of Orion OS.

The Orion Engine is responsible for coordinating all framework execution, managing shared state, and producing a unified system output.

Individual frameworks remain responsible for their own domain logic.

The Orion Engine is responsible for orchestration.

---

# Design Principles

## Separation of Responsibilities

Frameworks perform calculations.

The Orion Engine manages execution.

---

## Deterministic Execution

Given identical inputs and configuration, Orion Engine should always produce identical outputs.

---

## Framework Independence

Each framework operates independently through a standardized interface.

Frameworks should not directly invoke one another.

---

# Responsibilities

The Orion Engine is responsible for:

* Loading configuration
* Initializing framework objects
* Coordinating execution order
* Managing shared state
* Persisting execution results
* Producing dashboard data
* Producing CLI output
* Recording execution logs

The Orion Engine is not responsible for:

* Investment decisions
* Strategy calculations
* Indicator calculations
* Security selection

These responsibilities belong to the individual frameworks.

---

# Engine Lifecycle

Each execution follows the same lifecycle.

```text
Initialize

↓

Load Configuration

↓

Load Market Data

↓

Execute Frameworks

↓

Aggregate Results

↓

Persist State

↓

Generate Outputs

↓

Shutdown
```

---

# Execution Order

The default execution sequence is:

```text
Aurora

↓

Moon

↓

Supernova

↓

Phoenix
```

Aurora executes first because it evaluates the market environment.

Moon executes independently using its own strategy logic.

Supernova and Phoenix execute independently of Moon.

Execution order does not imply dependency unless explicitly defined.

---

# Framework Interfaces

Every framework implements a common execution interface.

Required methods:

```python
initialize()

load_data()

run()

get_result()

shutdown()
```

Framework-specific calculations remain internal.

---

# Shared Objects

Frameworks exchange only standardized objects.

Examples:

* FrameworkResult
* Score
* State
* Allocation
* Portfolio
* ReviewRecord

Shared object definitions are maintained in:

* Orion_Data_Model.md
* Moon_Object_Model.md

---

# Engine Result

Each execution produces a single Engine Result.

Minimum fields:

* Execution Time
* Framework Results
* Dashboard Data
* Portfolio Allocations
* System Status

---

# State Management

The Orion Engine maintains the latest system state.

Examples:

* Current Aurora Regime
* Current Moon Allocation
* Current Supernova Watchlist
* Current Phoenix Leaders

Historical state management may be added in future versions.

---

# Error Handling

Framework failures should be isolated whenever possible.

If a framework fails:

* Record the error
* Preserve previous successful state if applicable
* Continue executing remaining independent frameworks when safe

Critical initialization failures terminate execution.

---

# Logging

Each execution records:

* Start Time
* End Time
* Framework Status
* Execution Duration
* Errors
* Warnings

Logs should support debugging and auditability.

---

# Scheduling

Default production schedule:

* Monthly portfolio evaluation
* Daily market monitoring
* Manual execution supported

Scheduling configuration is defined externally.

---

# Dashboard Integration

The Orion Dashboard consumes Engine Results only.

The Dashboard performs no investment calculations.

Its responsibility is visualization.

---

# CLI Integration

Example:

```text
orion run
```

Execution Flow:

```text
CLI

↓

Orion Engine

↓

Framework Execution

↓

Results
```

Framework-specific commands remain available.

Examples:

```text
orion aurora

orion moon

orion supernova

orion phoenix
```

---

# Future Enhancements

Potential future additions:

* Parallel framework execution
* Incremental updates
* Event-driven execution
* Distributed processing
* Background scheduling

Status:

Research Only

Not Approved

---

# Related Documents

* Orion_Operating_Architecture.md
* Orion_Data_Model.md
* Orion_Configuration_Model.md
* Moon_Object_Model.md
* Aurora_Interface.md
* Moon_Interface.md
* Supernova_Interface.md
* Phoenix_Interface.md