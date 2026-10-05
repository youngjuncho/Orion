# Phoenix Scoring Framework

Version: 0.1

Status: Draft

Last Updated: 2026-10-05

Depends On:

* Phoenix_Leader_Framework.md

---

# Purpose

This document defines how Phoenix assigns scores to digital asset projects.

Scores are used to determine:

* Category Leaders
* Challengers
* Leadership Trends
* Replacement Risk

---

# Scoring Philosophy

The objective is not false precision.

Phoenix scoring is judgment-assisted-by-metrics rather than a fully formula-driven quantitative model.

A repeatable scoring process is preferred over a complex model. Raw metrics inform the assessment but do not mechanically determine the score unless a separate metric-to-score rule has been explicitly approved.

Each 0-10 scoring dimension uses qualitative anchors. Reviewers must retain the principal evidence supporting the assigned score.

---

# Score Structure

Total Score:

100

---

Adoption

25

---

Ecosystem

25

---

Economics

25

---

Momentum

25

---

# Adoption

Measures real-world usage.

Maximum:

25

---

## User Activity

0-10

Qualitative Score Anchors:

* 0-2: Very Weak
* 3-4: Weak
* 5-6: Moderate
* 7-8: Strong
* 9-10: Exceptional

Examples:

* Active addresses
* Daily users
* Transaction count

---

## Network Utilization

0-10

Qualitative Score Anchors:

* 0-2: Very Weak
* 3-4: Weak
* 5-6: Moderate
* 7-8: Strong
* 9-10: Exceptional

Examples:

* Transaction volume
* Network demand
* Utilization growth

---

## Adoption Trend

0-5

Examples:

* User growth
* Usage acceleration

---

Maximum:

25

---

# Ecosystem

Measures ecosystem strength.

Maximum:

25

---

## Developer Activity

0-10

Qualitative Score Anchors:

* 0-2: Very Weak
* 3-4: Weak
* 5-6: Moderate
* 7-8: Strong
* 9-10: Exceptional

Examples:

* Active developers
* Github activity
* Contributor growth

---

## Application Ecosystem

0-10

Qualitative Score Anchors:

* 0-2: Very Weak
* 3-4: Weak
* 5-6: Moderate
* 7-8: Strong
* 9-10: Exceptional

Examples:

* Number of applications
* Ecosystem diversity
* Ecosystem growth

---

## Strategic Position

0-5

Examples:

* Industry relevance
* Ecosystem importance

---

Maximum:

25

---

# Economics

Measures economic sustainability.

Maximum:

25

---

## Revenue Generation

0-10

Qualitative Score Anchors:

* 0-2: Very Weak
* 3-4: Weak
* 5-6: Moderate
* 7-8: Strong
* 9-10: Exceptional

Examples:

* Protocol revenue
* Fee generation

---

## Economic Efficiency

0-10

Qualitative Score Anchors:

* 0-2: Very Weak
* 3-4: Weak
* 5-6: Moderate
* 7-8: Strong
* 9-10: Exceptional

Examples:

* Revenue growth
* Sustainability

---

## Treasury Strength

0-5

Examples:

* Financial resources
* Runway

---

Maximum:

25

---

# Momentum

Measures market leadership.

Maximum:

25

---

## Relative Strength

0-10

Qualitative Score Anchors:

* 0-2: Very Weak
* 3-4: Weak
* 5-6: Moderate
* 7-8: Strong
* 9-10: Exceptional

Examples:

* Relative performance
* Capital inflows

---

## Narrative Strength

0-10

Qualitative Score Anchors:

* 0-2: Very Weak
* 3-4: Weak
* 5-6: Moderate
* 7-8: Strong
* 9-10: Exceptional

Examples:

* Market attention
* Institutional interest
* Sector relevance

---

## Momentum Trend

0-5

Examples:

* Improving
* Stable
* Weakening

---

Maximum:

25

---

# Score Interpretation

## Gold

80-100

Category Leader

---

## Silver

65-79

Primary Challenger

---

## Bronze

50-64

Emerging Candidate

---

## Watchlist

Below 50

Research Only

---

# Leadership Trend

Monthly score comparison.

---

Improving

Score increase:

5+

---

Stable

Score change:

-4 to +4

---

Weakening

Score decrease:

5+

---

# Replacement Risk

Calculated using the canonical score-gap mapping defined in Phoenix_Leader_Framework.md.

| Score Gap | Replacement Risk | Leadership State |
|---|---|---|
| 20+ | Low | Dominant |
| 10-19 | Medium | Stable |
| 0-9 | High | Competitive |
| Challenger exceeds Leader | Critical | Transition |

When the Promotion Rule is satisfied, the leadership state becomes Disrupted until the replacement is formally recorded.

The worked example below must follow this mapping.

---

# Review Record

Each reviewed score should record:

* Score
* Evidence
* Assessment
* Review Date

The principal evidence should be sufficient for another reviewer to understand why the score was assigned.

# Monthly Review Process

For each category:

1. Score Leader
2. Score Challenger
3. Calculate Score Gap
4. Calculate Replacement Risk
5. Update Leadership Trend
6. Record Results

---

# Example

Category:

Smart Contract Platforms

---

Leader

SOL

Score:

84

---

Challenger

SUI

Score:

78

---

Gap:

6

---

Replacement Risk:

High

---

State:

Competitive

---

Action:

Review

---

# Governance

Score changes must be documented.

Leadership changes require:

* Review validation
* Decision log entry

before implementation.

---

# Open Issues

OI-701

Automated scoring sources.

Status:

Open

Note:

Automation is not required for v1. Raw metrics remain supporting evidence unless an explicit metric-to-score rule is approved.

---

OI-702

Category-specific adjustments.

Status:

Open

---

OI-703

Historical score database.

Status:

Open

---

# Next Document

Phoenix_Dashboard_Spec.md

Purpose:

Define dashboard structure, reporting format, leadership monitoring, and replacement risk visualization.
