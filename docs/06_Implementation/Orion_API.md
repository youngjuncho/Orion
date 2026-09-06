# Orion API Specification

Version: 1.0

Status: Draft

Last Updated: 2026-07-28

Depends On:

* Orion_Runtime.md
* Orion_Service_Model.md
* Orion_State_Model.md
* Orion_Event_Model.md
* Orion_Engine.md

---

# Purpose

This document defines the public application programming interface (API) of Orion OS.

The Orion API provides a stable contract between the core engine and external consumers, including:

* CLI
* Dashboard
* Scheduled Jobs
* Future REST API
* Future Web UI

The API exposes Orion functionality without exposing internal implementation details.

---

# Current Implementation Boundary

`orion.core.api_models` currently provides typed result contracts for
framework results, health reports, and complete Orion results. The public
operations listed below are not yet wired to a runtime coordinator, and the
API does not yet expose a standardized client-facing exception hierarchy.
Until that contract is approved, internal configuration, framework, and
storage exceptions remain outside the public API surface.

---

# Design Principles

## Stable Interface

Consumers should depend on public APIs rather than internal engine implementations.

---

## Framework Independence

Each framework exposes a consistent execution interface.

---

## Stateless Execution

API methods should produce results from the current runtime state without retaining execution-specific state.

Persistent state is managed separately by the Runtime layer.

---

## Strong Typing

Every public API should return a well-defined domain object.

---

# Orion API

The Orion Engine exposes the following primary operations.

```text
run()

run_framework()

get_state()

get_events()

get_services()

report()

dashboard()

health()

shutdown()
```

---

# run()

Purpose:

Execute the complete Orion runtime.

Returns:

OrionResult

Execution Flow:

```text
Runtime

↓

Aurora

↓

Moon

↓

Supernova

↓

Phoenix

↓

Aggregation

↓

OrionResult
```

---

# run_framework()

Purpose:

Execute a single framework independently.

Parameters:

* Framework Name

Supported Frameworks:

* Aurora
* Moon
* Supernova
* Phoenix

Returns:

FrameworkResult

---

# get_state()

Purpose:

Return the current Orion state model.

Returns:

StateModel

Examples:

* Current Regime
* Active Strategies
* Framework Status
* Portfolio Status

---

# get_events()

Purpose:

Return recent runtime events.

Returns:

Event Collection

Examples:

* Rebalance Completed
* Review Finished
* Configuration Reloaded

---

# get_services()

Purpose:

Return registered services.

Returns:

Service Registry

---

# report()

Purpose:

Generate a standardized Orion report.

Supported Formats:

* Console
* Markdown
* JSON

Returns:

Report

---

# dashboard()

Purpose:

Return dashboard-ready data.

Returns:

DashboardModel

Consumers:

* Orion Dashboard
* Moon Dashboard
* Aurora Dashboard

---

# health()

Purpose:

Return runtime health information.

Checks:

* Configuration
* Data Availability
* Service Status
* Framework Status

Returns:

HealthReport

---

# shutdown()

Purpose:

Gracefully terminate Orion runtime.

Responsibilities:

* Flush Logs
* Save State
* Close Services

---

# Result Objects

## OrionResult

Contains:

* Runtime Summary
* Framework Results
* State Snapshot
* Generated Events

---

## FrameworkResult

Contains:

* Framework Name
* Execution Status
* State
* Score
* Generated Events

---

## HealthReport

Contains:

* Overall Status
* Failed Components
* Warning Messages

---

# Error Handling

Public APIs should never expose internal exceptions.

Errors should be converted into standardized error responses.

Example:

```text
ConfigurationError

↓

APIError

↓

Client
```

---

# API Consumers

Current Consumers:

* CLI
* Dashboard

Future Consumers:

* REST API
* Web UI
* Mobile Application

---

# Relationship With Other Documents

The Orion API is implemented by:

* Orion_Engine.md

The Orion API consumes:

* Orion_Runtime.md
* Orion_Service_Model.md
* Orion_State_Model.md
* Orion_Event_Model.md

The CLI specification is defined in:

* Orion_CLI_Spec.md

The Dashboard specification is defined in:

* Orion_Dashboard_Spec.md

---

# Future Extensions

Potential future additions:

* Plugin API
* Remote Execution API
* Event Subscription API
* Streaming Dashboard API

Status:

Research Only

Not Approved
