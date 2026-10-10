# Phoenix Pipeline

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

> **Current implementation boundary:** This is a design draft. Phoenix governance and its authoritative registry are not integrated into the Runtime. Do not present hard-coded scaffold data as current approved leaders or scores. Framework results and proposed events return through Runtime contracts; Phoenix does not publish directly to Dashboard, EventStore, or durable history.

Depends On:

* Phoenix_Engine.md
* Orion_Runtime.md

---

# Purpose

Defines the execution pipeline for the Phoenix framework.

The pipeline describes how research data flows through the Phoenix Engine to evaluate digital asset ecosystems and produce portfolio recommendations.

---

# Pipeline Overview

```text
Market Data
      │
      ▼
Category Definitions
      │
      ▼
Project Universe
      │
      ▼
Leadership Evaluation
      │
      ▼
Project Scoring
      │
      ▼
State Assignment
      │
      ▼
Watchlist Update
      │
      ▼
Review Generation
      │
      ▼
Dashboard Output
```

---

# Pipeline Stages

## Stage 1

Load Categories

Inputs:

* Category definitions
* Approved leaders
* Challengers

Output:

Category Repository

---

## Stage 2

Load Project Universe

Tasks:

* Load approved projects
* Load candidate projects
* Validate metadata

Output:

Project Repository

---

## Stage 3

Evaluate Leadership

Tasks:

* Compare projects within categories
* Detect leadership changes
* Evaluate ecosystem strength

Output:

Leadership Evaluation

---

## Stage 4

Score Projects

Tasks:

* Calculate ecosystem metrics
* Calculate project quality
* Normalize scores

Output:

Project Scores

---

## Stage 5

Assign States

Tasks:

* Evaluate thresholds
* Update project states
* Detect leadership transitions

Output:

Project States

---

## Stage 6

Update Watchlists

Tasks:

* Add promising candidates
* Remove obsolete projects
* Promote new leaders

Output:

Updated Watchlists

---

## Stage 7

Generate Reviews

Tasks:

* Schedule reviews
* Produce review records
* Return proposed event records in the Framework result for Runtime handling

Output:

Review Records

---

## Stage 8

Return a canonical Framework result through the Orion Runtime adapter. Runtime
owns presentation handoff and event storage. This draft does not authorize
direct publishing or durable history storage.

---

# Runtime Integration

The public Orion Runtime invokes a Framework adapter. Full Phoenix governance
registry integration remains unimplemented.

Execution may be:

* Manual
* Scheduled

---

# Error Handling

This draft does not define partial-result or retry behavior. The public Runtime
stops on Framework failure and does not return a partial successful
`OrionResult`.

---

# Event Flow

Typical events:

```text
CategoriesLoaded

↓

ProjectsLoaded

↓

LeadershipEvaluated

↓

ProjectsScored

↓

StatesUpdated

↓

WatchlistsUpdated

↓

ReviewsGenerated

↓

PipelineCompleted
```

---

# Related Documents

* Phoenix_Engine.md
* Orion_Runtime.md
* Orion_Event_Model.md
* Orion_Service_Model.md
