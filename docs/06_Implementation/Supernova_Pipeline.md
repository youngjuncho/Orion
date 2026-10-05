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
* Publish events

Output:

Updated Watchlists and Review Records

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