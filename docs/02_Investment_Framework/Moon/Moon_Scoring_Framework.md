# Moon Scoring Framework

Version: 0.1

Status: Draft

Last Updated: 2026-06-21

---

# Purpose

This document defines how Moon generates strategy health scores.

The objective is not to predict returns.

The objective is to measure the current quality of strategy signals.

---

# Scoring Philosophy

Moon evaluates:

* Signal Strength
* Signal Breadth
* Asset Participation
* Risk State

Moon does not evaluate:

* Future returns
* Price targets
* Forecasts

---

# Score Range

0 – 100

---

# Score Bands

90 – 100

Exceptional

---

80 – 89

Strong

---

70 – 79

Healthy

---

60 – 69

Stable

---

50 – 59

Neutral

---

40 – 49

Weak

---

30 – 39

Danger

---

0 – 29

Critical

---

# Candidate Inputs

## Momentum Strength

Measures the magnitude of positive momentum.

Weight:

Pending

---

## Breadth

Measures participation across selected assets.

Weight:

Pending

---

## Risk State

Measures current defensive posture.

Weight:

Pending

---

## Signal Stability

Measures turnover frequency.

Weight:

Pending

---

# Example Interpretation

Score: 92

Meaning:

Strong momentum

Broad participation

Low defensive allocation

---

Score: 55

Meaning:

Mixed signals

Neutral conditions

---

Score: 25

Meaning:

Defensive posture

Weak participation

Elevated risk

---

# Future Research

Potential future scoring inputs:

* Relative Momentum Rank
* Absolute Momentum Rank
* Canary Health
* Breadth Deterioration
* Defensive Allocation Ratio

Status:

Research Only

---

# Related Documents

* Orion_Technical_Architecture.md
* Moon_Current_Production.md
* Moon_Governance.md
