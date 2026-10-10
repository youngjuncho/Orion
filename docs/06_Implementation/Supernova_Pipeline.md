# Supernova Pipeline

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

> **Current implementation boundary:** This is a design draft. D-049 records a five-company governance baseline, but the authoritative registry snapshot contract explicitly has no Runtime integration or strategy-activation mechanism. A report must not present hard-coded scaffold data as the current approved registry. Framework results and proposed events return through Runtime contracts; Supernova does not publish directly to Dashboard, EventStore, or durable history.

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

Collect and Assess Evidence

Tasks:

* Collect evidence for each company-scoring dimension
* Validate evidence provenance
* Record an evidence-based assessment
* Preserve review date and source references

Output:

Evidence-backed Dimension Reviews

---

## Stage 4

Score Companies

Tasks:

* Apply the approved qualitative anchors
* Require all five scoring dimensions
* Calculate the weighted Company Score using the approved 20/25/25/15/15 weights
* Do not impute missing dimensions or reweight partial records
* Preserve the underlying Evidence and Assessment records

Output:

Company Scores

---

## Stage 5

Governance Review and State Assignment

Tasks:

* Review Company Score and supporting evidence
* Evaluate Portfolio State and Leadership Role separately
* Detect governance-required transitions

Output:

Governance Review Results

---

## Stage 6

Update Watchlists and Generate Reviews

Tasks:

* Update candidates and watchlists after governance review
* Schedule reviews
* Produce review records
* Return proposed event records in the Framework result for Runtime handling

Output:

Updated Watchlists and Review Records

---

## Stage 7

Return a canonical Framework result through the Orion Runtime adapter. Runtime
owns presentation handoff and event storage. This draft does not authorize
direct publishing or durable history storage.

---

# Runtime Integration

The public Orion Runtime invokes a Framework adapter. Full Supernova governance
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
UniverseLoaded

↓

ThemeEvaluated

↓

EvidenceCollected

↓

CompanyScored

↓

GovernanceReviewed

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
