# Aurora Regime Framework

Version: 0.1

Status: Draft

Last Updated: 2026-06-21

Depends On:

* Aurora_Research.md
* Aurora_Operating_Model.md

---

# Purpose

This document defines how Aurora converts market observations into market regime classifications.

Aurora evaluates market conditions through a structured scoring framework.

The objective is to classify:

* Market Regime
* State Momentum

using observable indicators.

---

# Aurora Regime Model

Aurora evaluates:

```text
Trend
Liquidity
Volatility
Credit
```

These four components form the Core Layer.

---

# Core Layer Weights

Initial Orion Framework

| Component  | Weight |
| ---------- | ------ |
| Trend      | 30%    |
| Liquidity  | 30%    |
| Credit     | 20%    |
| Volatility | 20%    |

Status:

Research Draft

Pending Validation

---

# Component Scoring

Each component produces a score:

```text
0 – 100
```

Interpretation:

90–100 Exceptional

80–89 Strong

70–79 Healthy

60–69 Stable

50–59 Neutral

40–49 Weak

30–39 Danger

0–29 Critical

---

# Trend Score

Purpose:

Measure market direction.

Candidate Indicators:

* SPY vs 200-Day MA
* QQQ vs 200-Day MA
* Market Breadth

Output:

0 – 100

---

# Liquidity Score

Purpose:

Measure financial system liquidity.

Candidate Indicators:

* Fed Balance Sheet
* M2 Growth
* Financial Conditions Index

Output:

0 – 100

---

# Credit Score

Purpose:

Measure risk appetite.

Candidate Indicators:

* HYG
* Credit Spreads
* Corporate Bond Strength

Output:

0 – 100

---

# Volatility Score

Purpose:

Measure market stress.

Candidate Indicators:

* VIX
* MOVE Index

Output:

0 – 100

Higher score means healthier conditions.

---

# Aurora Score

Formula

# Aurora Score

Trend × 0.30
+
Liquidity × 0.30
+
Credit × 0.20
+
Volatility × 0.20

Output:

0 – 100

---

# Regime Classification

## Risk On

Score:

70+

Characteristics:

* Positive Trend
* Healthy Liquidity
* Healthy Credit

Interpretation:

Supportive environment for risk assets.

---

## Neutral

Score:

50 – 69

Characteristics:

* Mixed Signals
* Transition Risk

Interpretation:

Environment lacks strong confirmation.

---

## Risk Off

Score:

Below 50

Characteristics:

* Weak Trend
* Weak Credit
* Elevated Stress

Interpretation:

Defensive conditions dominate.

---

# State Momentum Model

Aurora evaluates score direction separately from regime.

Purpose:

Detect potential regime changes.

---

# Improving

Condition:

Aurora Score increasing over time.

Examples:

* Liquidity improving
* Credit improving
* Volatility declining

Interpretation:

Conditions becoming healthier.

---

# Stable

Condition:

Aurora Score relatively unchanged.

Interpretation:

No significant directional shift.

---

# Deteriorating

Condition:

Aurora Score declining over time.

Examples:

* Credit weakening
* Liquidity contracting
* Volatility rising

Interpretation:

Conditions becoming weaker.

---

# Transition Signals

Aurora should monitor transition risk.

---

## Bull To Bear Warning

Condition:

Current Regime:

Risk On

State Momentum:

Deteriorating

Interpretation:

Early warning of weakening conditions.

---

## Bear To Bull Warning

Condition:

Current Regime:

Risk Off

State Momentum:

Improving

Interpretation:

Potential recovery environment developing.

---

# Cross Asset Confirmation

Cross Asset indicators provide context.

They do not determine the regime directly.

---

## Dollar

Interpretation:

Liquidity Conditions

---

## Gold

Interpretation:

Defensive Demand

---

## Oil

Interpretation:

Growth / Inflation Conditions

---

## Bitcoin

Interpretation:

Risk Appetite

---

# Example Output

Aurora Score:

82

Regime:

Risk On

State Momentum:

Improving

Cross Asset:

Dollar:
Weak

Gold:
Neutral

Oil:
Strong

Bitcoin:
Strong

Interpretation:

Supportive environment with improving conditions.

---

# Open Questions

RQ-101

Final Trend Indicators

Status:

Open

---

RQ-102

Final Liquidity Indicators

Status:

Open

---

RQ-103

Final Credit Indicators

Status:

Open

---

RQ-104

Final Volatility Indicators

Status:

Open

---

RQ-105

State Momentum Lookback Methodology

Status:

Open

---

# Related Documents

* Aurora_Research.md
* Aurora_Operating_Model.md
* Aurora_Scoring_Framework.md
