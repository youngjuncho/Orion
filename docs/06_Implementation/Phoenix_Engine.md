# Phoenix Engine

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Phoenix_Operating_Model.md
* Orion_State_Model.md
* Orion_Event_Model.md

---

# Purpose

Defines the execution engine for the Phoenix framework.

The Phoenix Engine evaluates digital asset categories, projects, and ecosystem leadership to produce long-term digital asset portfolio recommendations.

Unlike Moon, Phoenix focuses on structural leadership within digital asset ecosystems rather than tactical market timing.

---

# Responsibilities

The Phoenix Engine is responsible for:

* Loading category definitions
* Loading candidate projects
* Evaluating ecosystem leadership
* Calculating project scores
* Updating project states
* Managing watchlists
* Producing review records

---

# Inputs

The engine consumes:

* Category definitions
* Candidate universe
* Market data
* On-chain metrics
* Review records
* Configuration

---

# Outputs

The engine produces:

* Project scores
* Project states
* Category summaries
* Review recommendations
* Dashboard data

---

# Core Components

## Category Loader

Loads:

* Category definitions
* Approved leaders
* Challengers

---

## Leadership Engine

Evaluates:

* Category leadership
* Competitive position
* Ecosystem strength

---

## Scoring Engine

Calculates normalized project scores.

Score Range:

0–100

---

## State Engine

Assigns project states.

Examples:

* Leader
* Challenger
* Watchlist
* Review
* Replaced

---

## Review Engine

Determines whether a project requires:

* Monthly Review
* Quarterly Review
* Event-Driven Review

---

# Engine Lifecycle

```text
Load Categories
        │
Load Projects
        │
Evaluate Leadership
        │
Score Projects
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

State transitions follow:

Orion_State_Model.md

The engine never updates project states without validation.

---

# Event Generation

The engine publishes events including:

* ProjectReviewed
* LeaderChanged
* ChallengerPromoted
* CategoryUpdated
* WatchlistChanged

Events follow:

Orion_Event_Model.md

---

# Dashboard Integration

Provides data for:

* Phoenix Dashboard
* Orion Dashboard

---

# Related Documents

* Phoenix_Operating_Model.md
* Orion_State_Model.md
* Orion_Event_Model.md
* Orion_Service_Model.md