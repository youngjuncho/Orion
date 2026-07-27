# Supernova Pipeline

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Supernova_Engine.md
* Orion_Runtime.md

---

# Purpose

Defines the execution pipeline for the Supernova framework.

The pipeline describes how research data flows through the Supernova Engine to produce portfolio recommendations.

---

# Pipeline Overview

```text
Market Data
      │
      ▼
Company Universe
      │
      ▼
Theme Evaluation
      │
      ▼
Company Scoring
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

Load Universe

Inputs:

* Approved companies
* Candidate companies

Output:

Company Repository

---

## Stage 2

Evaluate Themes

Tasks:

* Map companies to themes
* Update theme strength
* Detect structural changes

Output:

Theme Evaluation

---

## Stage 3

Score Companies

Tasks:

* Calculate quality metrics
* Calculate growth metrics
* Normalize scores

Output:

Company Scores

---

## Stage 4

Assign States

Tasks:

* Evaluate thresholds
* Update company states
* Detect transitions

Output:

Company States

---

## Stage 5

Update Watchlists

Tasks:

* Add candidates
* Remove obsolete entries
* Promote approved companies

Output:

Updated Watchlists

---

## Stage 6

Generate Reviews

Tasks:

* Schedule reviews
* Produce review records
* Publish events

Output:

Review Records

---

## Stage 7

Publish Results

Outputs include:

* Dashboard cards
* Reports
* Orion services
* Historical records

---

# Runtime Integration

The pipeline is executed by:

Orion_Runtime

Execution may be:

* Manual
* Scheduled

---

# Error Handling

Pipeline failures should:

* Preserve previous results
* Log all errors
* Generate pipeline events

---

# Event Flow

Typical events:

```text
UniverseLoaded

↓

ThemeEvaluated

↓

CompanyScored

↓

StateUpdated

↓

WatchlistUpdated

↓

ReviewGenerated

↓

PipelineCompleted
```

---

# Related Documents

* Supernova_Engine.md
* Orion_Runtime.md
* Orion_Event_Model.md
* Orion_Service_Model.md