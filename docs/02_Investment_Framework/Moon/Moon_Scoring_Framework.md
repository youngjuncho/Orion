# Moon Scoring Framework

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Moon_Object_Model.md
* Moon_Current_Production.md

---

# Purpose

This document defines how Moon evaluates the health of strategy outputs.

Moon Scoring measures the quality and consistency of current strategy signals.

The objective is consistency rather than prediction.

Moon does not forecast future returns.

---

# Scoring Philosophy

## Consistency Over Prediction

Moon evaluates the current state of strategy outputs using observable data.

Scores should be:

- Observable
- Repeatable
- Explainable

---

## Strategy-Centric Evaluation

Moon evaluates the quality of strategy signals rather than market forecasts.

Each strategy produces its own evaluation before participating in the Consensus Allocation.

---

# Moon Score Structure

Moon Score consists of four components.

| Component | Weight |
|-----------|-------:|
| Signal Strength | 30% |
| Breadth | 25% |
| Risk State | 25% |
| Signal Stability | 20% |

Total:

100%

---

# Signal Strength

Purpose:

Measure the strength of selected strategy signals.

Candidate Inputs:

- Relative Momentum
- Absolute Momentum
- Composite Momentum Score

Output:

0–100

Status:

Research Draft

---

# Breadth

Purpose:

Measure participation across the selected asset universe.

Candidate Inputs:

- Number of Positive Assets
- Participation Ratio
- Breadth Score

Output:

0–100

Status:

Research Draft

---

# Risk State

Purpose:

Measure the defensive posture of the strategy.

Candidate Inputs:

- Defensive Allocation Ratio
- Cash Allocation
- Bond Allocation

Output:

0–100

Higher scores indicate healthier offensive positioning.

Status:

Research Draft

---

# Signal Stability

Purpose:

Measure the consistency of strategy outputs over time.

Candidate Inputs:

- Turnover Frequency
- Signal Persistence
- Rebalance Stability

Output:

0–100

Higher scores indicate more stable signals.

Status:

Research Draft

---

# Component Bands

All components use the same interpretation scale.

90–100

Exceptional

---

80–89

Strong

---

70–79

Healthy

---

60–69

Stable

---

50–59

Neutral

---

40–49

Weak

---

30–39

Danger

---

0–29

Critical

---

# Moon Score Formula

Moon Score

=

(Signal Strength × 0.30)

+

(Breadth × 0.25)

+

(Risk State × 0.25)

+

(Signal Stability × 0.20)

Output:

0–100

---

# Strategy Score

Each Moon strategy may produce an individual Strategy Score.

Examples:

- ADM Score
- BAA Score
- VAA Score
- HAA Score
- BDA Score

Strategy Scores provide diagnostic information and do not directly determine portfolio allocation.

---

# Consensus Score

Moon may calculate an overall Consensus Score from all active Strategy Results.

Purpose:

Measure the overall health of the tactical allocation system.

Status:

Future Enhancement

---

# Dashboard Presentation

Moon Dashboard may display:

- Overall Moon Score
- Strategy Scores
- Selected Assets
- Current State
- Consensus Allocation

Moon Score is informational and does not replace strategy outputs.

---

# Future Enhancements

Potential future additions:

- Dynamic Component Weights
- Strategy Confidence Score
- Consensus Confidence Score
- Historical Score Trends
- Strategy Agreement Index

Status:

Research Only

Not Approved

---

# Open Questions

RQ-301

How should Signal Strength be standardized?

Status:

Open

---

RQ-302

How should Breadth be measured consistently across strategies?

Status:

Open

---

RQ-303

How should Risk State be quantified?

Status:

Open

---

RQ-304

How should Signal Stability be measured?

Status:

Open

---

RQ-305

Should Strategy Scores influence Dashboard ranking only, or future allocation decisions?

Status:

Open

---

# Related Documents

* Moon_Object_Model.md
* Moon_Current_Production.md
* Moon_Interface.md
* Orion_Glossary.md