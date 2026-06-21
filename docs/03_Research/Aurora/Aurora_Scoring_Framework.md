# Aurora Scoring Framework

Version: 0.1

Status: Draft

Last Updated: 2026-06-21

Depends On:

* Aurora_Research.md
* Aurora_Operating_Model.md
* Aurora_Regime_Framework.md

---

# Purpose

This document defines how Aurora calculates market climate scores.

Aurora converts multiple market indicators into a standardized score between 0 and 100.

The objective is consistency rather than prediction.

---

# Scoring Philosophy

## Simplicity First

Aurora v1 prioritizes robustness over complexity.

Indicators should be:

* Observable
* Repeatable
* Explainable

---

## Consistency Over Precision

Aurora does not seek perfect market timing.

Aurora seeks stable interpretation of market conditions.

---

# Score Structure

Aurora Score consists of four components.

| Component  | Weight |
| ---------- | ------ |
| Trend      | 30     |
| Liquidity  | 30     |
| Credit     | 20     |
| Volatility | 20     |

Total:

100

---

# Trend Score

Purpose:

Measure market direction.

Candidate Inputs:

* SPY Trend
* QQQ Trend
* Market Breadth

Scoring Range:

0–100

Initial Method:

Simple Binary Scoring

Example:

SPY > 200DMA

= Positive

SPY < 200DMA

= Negative

Status:

Research Draft

---

# Liquidity Score

Purpose:

Measure availability of financial liquidity.

Candidate Inputs:

* Federal Reserve Balance Sheet
* M2 Growth
* Financial Conditions Index

Scoring Range:

0–100

Status:

Research Draft

---

# Credit Score

Purpose:

Measure risk appetite.

Candidate Inputs:

* HYG Trend
* Credit Spread Trend
* Corporate Bond Relative Strength

Scoring Range:

0–100

Status:

Research Draft

---

# Volatility Score

Purpose:

Measure market stress.

Candidate Inputs:

* VIX
* MOVE Index

Scoring Range:

0–100

Important:

Higher score indicates healthier conditions.

Lower volatility generally increases score.

---

# Component Bands

All components use the same scale.

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

# Aurora Score Formula

Aurora Score

=

Trend × 0.30

*

Liquidity × 0.30

*

Credit × 0.20

*

Volatility × 0.20

Output:

0–100

---

# State Momentum Score

Purpose:

Measure change in conditions.

Aurora evaluates score direction separately from score level.

---

## Improving

Aurora Score rising.

---

## Stable

Aurora Score unchanged.

---

## Deteriorating

Aurora Score falling.

---

# Regime Mapping

Aurora Score ≥ 70

Risk On

---

Aurora Score 50–69

Neutral

---

Aurora Score < 50

Risk Off

---

# Cross Asset Confirmation

Cross Asset indicators do not contribute directly to Aurora Score.

They provide environmental confirmation only.

Examples:

* Dollar
* Gold
* Oil
* Bitcoin

---

# Future Enhancements

Potential future additions:

* Dynamic Weights
* Global Liquidity Composite
* Stablecoin Liquidity Metrics
* On-Chain Risk Metrics
* Yield Curve Factors

Status:

Research Only

Not Approved

---

# Open Questions

RQ-201

Should Trend remain the largest component?

Status:

Open

---

RQ-202

How should Liquidity be measured?

Status:

Open

---

RQ-203

How should Credit be measured?

Status:

Open

---

RQ-204

How should Volatility be measured?

Status:

Open

---

RQ-205

What lookback period should State Momentum use?

Status:

Open

---

# Related Documents

* Aurora_Research.md
* Aurora_Operating_Model.md
* Aurora_Regime_Framework.md
