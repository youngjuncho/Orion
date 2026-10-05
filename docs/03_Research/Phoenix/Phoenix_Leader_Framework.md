# Phoenix Leader Framework

Version: 0.1

Status: Draft

Last Updated: 2026-10-05

Depends On:

* Phoenix_Research.md
* Phoenix_Category_Framework.md
* Phoenix_Operating_Model.md

---

# Purpose

This document defines how Phoenix evaluates category leaders, challengers, and replacement risk.

Phoenix seeks to identify leadership transitions within digital asset ecosystems.

---

# Core Principle

Price is not leadership.

Leadership is determined by ecosystem strength.

---

# Evaluation Model

Each category is evaluated using four dimensions:

1. Adoption
2. Ecosystem
3. Economics
4. Momentum

---

# Leader Score

Leader Score is the primary ranking metric.

Maximum Score:

100

---

# Dimension 1

Adoption

Weight:

25%

Measures:

* Active users
* Transaction activity
* Network utilization

Score Range:

0-25

---

# Dimension 2

Ecosystem

Weight:

25%

Measures:

* Developer activity
* Number of applications
* Ecosystem growth

Score Range:

0-25

---

# Dimension 3

Economics

Weight:

25%

Measures:

* Revenue generation
* Fee generation
* Economic sustainability

Score Range:

0-25

---

# Dimension 4

Momentum

Weight:

25%

Measures:

* Relative market strength
* Capital inflows
* Narrative strength

Score Range:

0-25

---

# Leader Classification

## Gold

Leader Score

80+

Current category leader.

---

## Silver

Leader Score

65-79

Primary challenger.

---

## Bronze

Leader Score

50-64

Emerging contender.

---

## Watchlist

Leader Score

Below 50

Research only.

---

# Challenger Model

Each category maintains:

One Primary Challenger

Selection Rule:

Highest ranked non-leader asset.

---

Example

Smart Contract Platforms

Gold

SOL

Score:

85

---

Silver

SUI

Score:

73

---

Bronze

APT

Score:

58

---

# Leadership Trend

Tracks movement over time.

States:

Improving

Stable

Weakening

---

Improving

Leader Score increasing.

---

Stable

Leader Score unchanged.

---

Weakening

Leader Score declining.

---

# Replacement Risk and Leadership State

Replacement Risk is derived from the score gap between the current Leader and Primary Challenger.

Score Gap:

Leader Score - Challenger Score

The canonical mapping is:

| Score Gap | Replacement Risk | Leadership State | Action |
|---|---|---|---|
| 20+ | Low | Dominant | Hold |
| 10-19 | Medium | Stable | Monitor |
| 0-9 | High | Competitive | Review |
| Challenger exceeds Leader | Critical | Transition | Review Required |

`Disrupted` is not a separate score-gap band. It is the terminal leadership state used when the Promotion Rule has been satisfied and the challenger is formally confirmed as the new leader.

For a Disrupted state:

- Replacement Risk remains Critical until the new leader is formally recorded.
- Action: Rebalance Candidate.

No production-facing Phoenix document may introduce a second risk/state vocabulary or a conflicting numeric mapping.

---

# Replacement Risk Calculation

Initial Orion Standard

Replacement Risk is based on:

Leader Score

minus

Challenger Score

The score-gap mapping above is authoritative.

The worked examples in Phoenix_Scoring_Framework.md and Phoenix_Operating_Model.md must use the same mapping.

---

# Promotion Rule

A challenger may become leader when:

1. Challenger Score exceeds Leader Score

AND

2. Challenger remains ahead for two consecutive reviews

---

Action:

Leadership Review

---

# Demotion Rule

Current leader loses leadership status when:

Promotion Rule is satisfied.

---

Action:

Rebalance Candidate

---

# Review Frequency

Leader Review

Monthly

---

Category Review

Quarterly

---

Framework Review

Annually

---

# Governance

Leadership changes require:

* Review validation
* Decision log entry

before implementation.

---

# Open Issues

OI-601

Final metric definitions.

Status:

Open

---

OI-602

Data source selection.

Status:

Open

---

OI-603

Category-specific weighting.

Status:

Open

---

OI-604

Replacement Risk methodology.

Status:

Closed

Resolution:

Resolved by D-035. Phoenix now uses one canonical score-gap, Replacement Risk, and Leadership State mapping across production-facing documentation.

---

# Next Document

Phoenix_Scoring_Framework.md

Purpose:

Define scoring methodology and score aggregation rules.
