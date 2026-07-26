# Aurora Scoring Framework

Version: 1.0

Status: Draft

Last Updated: 2026-07-26

Depends On:

* Aurora_Research.md
* Aurora_Operating_Model.md
* Aurora_Regime_Framework.md
* Orion_Glossary.md

---

# Purpose

This document defines how Aurora calculates market climate scores.

Aurora converts multiple market indicators into a standardized score between 0 and 100.

The objective is consistency rather than prediction.

Aurora does not attempt to forecast returns.

Aurora does not generate investment recommendations.

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

## State Over News

Aurora is designed to describe market state, not react to daily news flow.

---

# Definitions

## Score

A numeric representation of current market conditions on a 0–100 scale.

A score may represent either:

* a component condition, or
* the aggregate Aurora Score

---

## State

A qualitative description derived from score level or score direction.

Examples:

* Improving
* Stable
* Deteriorating

---

## Regime

A higher-level market posture derived from Aurora Score.

Examples:

* Risk On
* Neutral
* Risk Off

---

## Component

One of the four inputs used to build Aurora Score:

* Trend
* Liquidity
* Credit
* Volatility

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

# Score Bands

All scores use the same scale.

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

(Trend × 0.30)
+
(Liquidity × 0.30)
+
(Credit × 0.20)
+
(Volatility × 0.20)

Output:

0–100

---

# Component Specifications

## Trend Score

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

Approved trend indicators shall be converted to component sub-scores using the indicator rule defined in the corresponding research and operating documents.

The Trend Score is the arithmetic mean of approved trend sub-scores.

Example:

* SPY > 200DMA = Positive
* SPY < 200DMA = Negative

Status:

Research Draft

---

## Liquidity Score

Purpose:

Measure availability of financial liquidity.

Candidate Inputs:

* Federal Reserve Balance Sheet
* M2 Growth
* Financial Conditions Index

Scoring Range:

0–100

Initial Method:

Normalized Composite Scoring

Approved liquidity indicators shall be converted to 0–100 sub-scores using documented indicator-specific rules.

The Liquidity Score is the arithmetic mean of approved liquidity sub-scores.

Status:

Research Draft

---

## Credit Score

Purpose:

Measure risk appetite.

Candidate Inputs:

* HYG Trend
* Credit Spread Trend
* Corporate Bond Relative Strength

Scoring Range:

0–100

Initial Method:

Normalized Composite Scoring

Approved credit indicators shall be converted to 0–100 sub-scores using documented indicator-specific rules.

The Credit Score is the arithmetic mean of approved credit sub-scores.

Status:

Research Draft

---

## Volatility Score

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

Initial Method:

Inverse Scoring

Approved volatility indicators shall be converted so that lower stress produces higher scores.

The Volatility Score is the arithmetic mean of approved volatility sub-scores.

Status:

Research Draft

---

# State Momentum Score

Purpose:

Measure change in conditions.

Aurora evaluates score direction separately from score level.

This is a directional measure of the Aurora Score over time.

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

Cross Asset indicators may support interpretation of the current market regime, but they do not change the Aurora Score directly.

---

# Indicator Governance

Only Approved indicators may be used in production scoring.

Indicator lifecycle states are governed separately by Aurora documentation and the Decision Log.

Status transitions must be recorded when an indicator changes state.

Reference:

Aurora_Indicator_Catalog.md

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

## RQ-201

Should Trend remain the largest component?

Status:

Open

---

## RQ-202

How should Liquidity be measured?

Status:

Open

---

## RQ-203

How should Credit be measured?

Status:

Open

---

## RQ-204

How should Volatility be measured?

Status:

Open

---

## RQ-205

What lookback period should State Momentum use?

Status:

Open

---

# Change Control

All material changes to this document must be recorded in:

docs/05_Decisions/Decision_Log.md

Material changes include:

* Component weights
* Score bands
* Regime mapping
* Indicator definitions
* Scoring methodology
* Approved indicator lifecycle changes

---

# Related Documents

* Aurora_Research.md
* Aurora_Operating_Model.md
* Aurora_Regime_Framework.md
* Aurora_Indicator_Catalog.md
* Orion_Glossary.md
* Decision_Log.md
