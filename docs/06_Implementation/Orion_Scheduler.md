# Orion Scheduler

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Orion_Runtime.md
* Orion_Engine.md
* Orion_Event_Model.md

---

# Purpose

Defines how Orion schedules and executes framework pipelines.

The scheduler coordinates execution timing while ensuring framework independence and deterministic execution order.

---

# Design Principles

The scheduler is responsible for:

* Triggering framework execution
* Managing execution order
* Preventing conflicting runs
* Recording execution history

The scheduler does not perform investment analysis.

---

# Scheduling Modes

Orion supports three execution modes.

## Manual

Execution initiated by the user.

Example:

```text
orion run
```

---

## Scheduled

Execution initiated automatically according to configured schedules.

Examples:

* Daily
* Weekly
* Monthly

---

## Event-Driven

Execution initiated by specific system events.

Examples:

* Market Close
* New Data Available
* Configuration Updated

---

# Default Schedule

Aurora

Frequency:

Daily

Purpose:

Monitor market conditions.

---

Moon

Frequency:

Monthly

Purpose:

Generate tactical allocation recommendations.

---

Supernova

Frequency:

Monthly

Purpose:

Review approved companies and watchlists.

---

Phoenix

Frequency:

Weekly

Purpose:

Review digital asset leadership.

---

# Execution Order

Default execution sequence:

```text
Aurora
      │
      ▼
Moon
      │
      ▼
Supernova
      │
      ▼
Phoenix
```

The execution order may be modified through configuration if required.

---

# Scheduler Workflow

```text
Scheduler Start
        │
Load Configuration
        │
Determine Scheduled Jobs
        │
Execute Framework
        │
Monitor Execution
        │
Record Events
        │
Update Runtime State
        │
Scheduler Complete
```

---

# Failure Handling

If a framework execution fails:

* Log the error
* Publish an execution event
* Preserve previous results
* Continue remaining scheduled jobs when possible

---

# Event Integration

The scheduler publishes:

* SchedulerStarted
* FrameworkStarted
* FrameworkCompleted
* FrameworkFailed
* SchedulerCompleted

Events follow:

Orion_Event_Model.md

---

# Runtime Integration

The scheduler operates within:

Orion_Runtime

---

# Configuration

Scheduling behavior is configured through:

config/system.yaml

Examples:

* Execution frequency
* Enabled frameworks
* Retry policy
* Parallel execution

---

# Future Enhancements

Potential additions:

* Dependency-aware scheduling
* Distributed execution
* Priority queues
* Retry strategies

Status:

Research Only

---

# Related Documents

* Orion_Runtime.md
* Orion_Engine.md
* Orion_Event_Model.md
* Orion_Service_Model.md