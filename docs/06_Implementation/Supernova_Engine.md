# Supernova Engine

Version: 1.1

Status: Draft

Last Updated: 2026-10-05

Depends On:

* Supernova_Operating_Model.md
* Orion_State_Model.md
* Orion_Event_Model.md

---

# Purpose

Defines the execution engine for the Supernova framework.

The Supernova Engine evaluates companies, themes, and watchlists to produce long-term equity investment recommendations.

Unlike Moon, Supernova focuses on structural trends rather than tactical allocation.

---

# Responsibilities

The Supernova Engine is responsible for:

* Loading approved companies
* Loading candidate companies
* Evaluating investment themes
* Calculating company scores
* Updating company states
* Managing watchlists
* Producing review records

---

# Inputs

The engine consumes:

* Company universe
* Theme definitions
* Evidence-backed company score reviews
* Review records
* Configuration

Company scoring input follows the approved evidence contract:

```text
Company Research Record
    ↓
Dimension Review
    ├── Score
    ├── Evidence
    ├── Assessment
    └── Source Provenance
    ↓
Company Score
```

Raw metrics may inform an assessment but do not mechanically determine a score unless a separate governance rule is approved.

---

# Outputs

The engine produces:

* Company scores
* Company states
* Theme summaries
* Review recommendations
* Governance review records
* Dashboard data

---

# Core Components

## Universe Loader

Loads:

* Approved companies
* Candidate companies

---

## Theme Engine

Evaluates:

* Theme alignment
* Structural relevance
* Long-term outlook

---

## Scoring Engine

Consumes evidence-backed dimension reviews and produces a normalized company score.

Score Range:

0–100

The Company Score is a governance assessment, not a purchase-timing signal.

## Governance Boundary

Company Score does not automatically assign Portfolio State, Leadership Role, or Replacement Risk. Those outcomes are documented through a Governance Decision.

The engine may validate the shape of a governance result, but it does not invent governance thresholds or approve a transition. Governance decisions must retain: Company Score, Portfolio State, Leadership Role, Replacement Risk, Primary Risk Driver, Action, Rationale, Evidence Summary, Review Date, and Approver.

Score-to-state mappings are intentionally not encoded as automatic thresholds in v1.

---

## State Engine

Maintains two separate dimensions:

Portfolio State:

* Approved
* Watchlist
* Review Required
* Retired

Leadership Role:

* Leader
* Challenger
* Candidate

A score may support a transition but does not automatically perform it.

---

## Review Engine

Determines whether a company requires:

* Monthly Review
* Quarterly Review
* Annual Review

---

# Engine Lifecycle

```text
Load Universe
      │
Evaluate Themes
      │
Collect / Validate Evidence
      │
Assess Dimensions
      │
Score Companies
      │
Governance Review
      │
Update States
      │
Update Watchlists
      │
Generate Reviews
      │
Publish Results
```

---

# State Management

State transitions are handled by:

Orion_State_Model.md

The engine never changes state directly without validation.

---

# Event Generation

The engine publishes events including:

* CompanyReviewed
* CompanyPromoted
* CompanyDemoted
* ThemeUpdated
* WatchlistChanged

Events follow:

Orion_Event_Model.md

---

# Dashboard Integration

Provides data for:

* Supernova Dashboard
* Orion Dashboard

---

# Related Documents

* Supernova_Operating_Model.md
* Orion_State_Model.md
* Orion_Event_Model.md
* Orion_Service_Model.md