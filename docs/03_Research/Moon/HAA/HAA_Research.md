# HAA Research Specification

Version: 1.0

Status: Research

Author:

Wouter Keller

Publication:

Hybrid Asset Allocation

Last Updated:

2026-06-20

---

# Overview

HAA (Hybrid Asset Allocation) is a tactical asset allocation framework developed by Wouter Keller.

The strategy combines:

1. Relative Momentum
2. Absolute Momentum
3. Canary Assets
4. Dual Momentum Concepts

to provide a balance between growth and risk management.

HAA extends the ideas introduced in BAA by incorporating additional momentum and allocation mechanisms.

---

# Source Material

Primary Source:

Hybrid Asset Allocation

Author:

Wouter Keller

Supporting Concepts:

* Dual Momentum
* Bold Asset Allocation
* Relative Momentum
* Absolute Momentum

---

# Research Objective

Determine whether capital should be allocated to:

* Offensive Assets
* Defensive Assets

based on market health and momentum conditions.

---

# Core Concepts

## Relative Momentum

Ranks assets by strength.

Question:

Which assets are strongest?

---

## Absolute Momentum

Evaluates whether risky assets should be owned.

Question:

Are market conditions favorable?

---

## Canary Assets

Provide an early warning system.

Question:

Is the environment healthy enough for offensive positioning?

---

## Hybrid Allocation

Combines multiple momentum concepts to improve risk-adjusted returns.

Question:

How should capital be allocated across asset classes?

---

# Original Framework

HAA consists of three layers.

## Canary Universe

Used to determine market health.

Status:

Research In Progress

---

## Offensive Universe

Used during favorable market conditions.

Typical assets include:

* US Equity
* International Equity
* Emerging Markets
* REITs
* Commodities

---

## Defensive Universe

Used during deteriorating market conditions.

Typical assets include:

* Treasury Bonds
* Short-Term Treasuries
* Cash Equivalents

---

# Decision Process

Step 1

Evaluate Canary Assets.

---

Step 2

Determine market regime.

---

Step 3

Select top-ranked assets from the appropriate universe.

---

Step 4

Allocate capital according to the selected assets.

---

# Momentum Measurement

Common implementations use:

* 1 Month
* 3 Month
* 6 Month
* 12 Month

lookback periods.

Exact methodology requires validation.

---

# Evaluation Frequency

Monthly

---

# Rebalancing Frequency

Monthly

---

# Expected Benefits

Historical research suggests HAA may provide:

* Strong risk-adjusted returns
* Lower drawdowns
* Improved crisis protection
* Faster risk adaptation

---

# Known Limitations

## Model Complexity

HAA is more complex than ADM and BAA.

---

## Implementation Variability

Results may differ depending on:

* Asset universe
* Canary construction
* Momentum formula

---

## Research Dependency

Accurate implementation requires validation against the original methodology.

---

# Research Questions

RQ-301

Final Canary Universe Definition.

Status:

Open

---

RQ-302

Exact Momentum Formula.

Status:

Open

---

RQ-303

Final Offensive Universe.

Status:

Open

---

RQ-304

Final Defensive Universe.

Status:

Open

---

RQ-305

Number of Selected Assets.

Status:

Open

---

RQ-306

Does Orion follow the original paper or Easy Investing implementation?

Status:

Open

---

# Research Conclusion

HAA is approved for further implementation research.

The original methodology must be fully documented before Orion-specific modifications are introduced.

Principle:

Original First

Customization Later

---

# Next Document

HAA_Orion.md

Purpose:

Define Orion-specific implementation details while preserving the original methodology.
