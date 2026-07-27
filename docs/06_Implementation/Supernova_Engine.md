# Supernova Engine

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

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
* Financial metrics
* Review records
* Configuration

---

# Outputs

The engine produces:

* Company scores
* Company states
* Theme summaries
* Review recommendations
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

Calculates normalized company scores.

Score Range:

0–100

---

## State Engine

Assigns company states.

Examples:

* Leader
* Watch
* Review
* Replacement Candidate

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
Score Companies
      │
Assign States
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