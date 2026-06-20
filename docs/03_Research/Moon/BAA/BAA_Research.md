# BAA Research Specification

Version: 1.0

Status: Research

Author:

Wouter Keller

Publication:

Bold Asset Allocation

Last Updated:

2026-06-20

---

# Overview

BAA (Bold Asset Allocation) is a tactical asset allocation framework developed by Wouter Keller.

The strategy combines:

1. Relative Momentum
2. Absolute Momentum
3. Canary Assets

to improve risk-adjusted returns and provide earlier detection of deteriorating market conditions.

BAA extends traditional dual momentum approaches by introducing a market health indicator layer.

---

# Source Material

Primary Source:

Bold Asset Allocation

Author:

Wouter Keller

Publication Year:

2022

Supporting Concepts:

* Relative Momentum
* Absolute Momentum
* Canary Momentum
* Dual Momentum

---

# Research Objective

Determine whether capital should be allocated to:

* Offensive Assets
* Defensive Assets

based on market conditions identified through Canary Assets.

---

# Core Concepts

## Relative Momentum

Relative momentum ranks assets within a candidate universe.

The strongest assets are selected.

Question:

Which assets are currently strongest?

---

## Absolute Momentum

Absolute momentum evaluates whether selected assets exhibit positive trend characteristics.

Question:

Should risky assets be owned at all?

---

## Canary Assets

Canary Assets serve as an early warning system.

The purpose is to identify deteriorating market conditions before major risk assets experience significant declines.

Question:

Is the market environment healthy enough to own offensive assets?

---

# Original Framework

BAA consists of three universes.

## Canary Universe

Used for market health evaluation.

Original candidates include:

* Emerging Markets
* Commodities
* Bonds
* International Assets

Exact implementation varies by version.

---

## Offensive Universe

Used during Risk-On conditions.

Examples:

* US Equity
* International Equity
* Emerging Markets
* REITs
* Commodities

---

## Defensive Universe

Used during Risk-Off conditions.

Examples:

* Treasury Bonds
* Short-Term Treasuries
* Cash Equivalents

---

# Decision Process

Step 1

Evaluate Canary Universe.

---

Step 2

Count negative momentum Canary Assets.

---

Step 3

Determine risk regime.

Risk-On

or

Risk-Off

---

Step 4

Select highest-ranked assets from the appropriate universe.

---

# Momentum Measurement

Original Methodology:

Multi-period momentum ranking.

Common implementation:

Weighted momentum using:

* 1 Month
* 3 Month
* 6 Month
* 12 Month

lookback periods.

---

# Portfolio States

## State A

Risk On

Condition:

Healthy Canary Signals

Action:

Allocate to Offensive Assets

---

## State B

Risk Off

Condition:

Deteriorating Canary Signals

Action:

Allocate to Defensive Assets

---

# Expected Benefits

Historical research suggests BAA may provide:

* Faster risk reduction
* Lower drawdowns
* Improved crisis protection
* Strong long-term risk-adjusted returns

---

# Known Limitations

## Model Complexity

BAA is more complex than ADM.

---

## Universe Sensitivity

Results depend heavily on:

* Asset selection
* Canary construction
* Momentum methodology

---

## Implementation Variability

Multiple public implementations exist.

Results may differ across:

* Books
* Whitepapers
* Websites
* Third-party implementations

---

# Research Questions

RQ-101

Final Canary Universe Definition

Status:

Open

---

RQ-102

Exact Momentum Formula

Status:

Open

---

RQ-103

Final Offensive Universe

Status:

Open

---

RQ-104

Final Defensive Universe

Status:

Open

---

RQ-105

Number of Assets Selected

Status:

Open

---

RQ-106

Does Orion follow the original paper or Easy Investing implementation?

Status:

Open

---

# Research Conclusion

BAA is approved for further implementation research.

The original methodology must be fully documented before Orion-specific modifications are introduced.

Principle:

Original First

Customization Later

---

# Next Document

BAA_Orion.md

Purpose:

Define Orion-specific implementation details while preserving the original BAA methodology.