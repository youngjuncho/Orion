# VAA Research Specification

Version: 1.0

Status: Research

Author:

Wouter Keller

Publication:

Vigilant Asset Allocation

Last Updated:

2026-06-20

---

# Overview

VAA (Vigilant Asset Allocation) is a tactical asset allocation framework developed by Wouter Keller.

The strategy combines:

1. Relative Momentum
2. Absolute Momentum
3. Breadth-Based Risk Detection

to dynamically allocate capital between offensive and defensive assets.

The primary objective is to remain invested during favorable market environments while rapidly reducing risk exposure during deteriorating conditions.

---

# Source Material

Primary Source:

Vigilant Asset Allocation

Author:

Wouter Keller

Supporting Concepts:

* Relative Momentum
* Absolute Momentum
* Breadth Momentum
* Risk Management

---

# Research Objective

Determine whether capital should be allocated to:

* Offensive Assets
* Defensive Assets

based on market breadth and momentum conditions.

---

# Core Concepts

## Relative Momentum

Ranks candidate assets.

Question:

Which assets are strongest?

---

## Absolute Momentum

Evaluates whether risky assets should be owned.

Question:

Are market conditions sufficiently healthy?

---

## Breadth Evaluation

Measures how many offensive assets exhibit negative momentum.

Question:

How widespread is market weakness?

---

## Vigilance

Risk allocation changes as market weakness expands.

The strategy becomes progressively more defensive as negative momentum increases.

---

# Original Framework

VAA consists of two universes.

## Offensive Universe

Used when market conditions are favorable.

Typical assets include:

* US Equity
* International Equity
* Emerging Markets
* Real Estate
* Commodities

---

## Defensive Universe

Used when market conditions deteriorate.

Typical assets include:

* Treasury Bonds
* Intermediate Treasuries
* Cash Equivalents

---

# Decision Process

Step 1

Calculate momentum for all offensive assets.

---

Step 2

Count the number of offensive assets with negative momentum.

---

Step 3

Determine defensive allocation percentage.

---

Step 4

Allocate remaining capital to top-ranked offensive assets.

---

# Momentum Measurement

Common implementations use weighted momentum calculations.

Exact methodology requires validation.

Status:

Research In Progress

---

# Evaluation Frequency

Monthly

---

# Rebalancing Frequency

Monthly

---

# Expected Benefits

Historical research suggests VAA may provide:

* Strong risk-adjusted returns
* Reduced drawdowns
* Faster response to market deterioration
* Improved downside protection

---

# Known Limitations

## Model Sensitivity

Results depend heavily on momentum calculation methodology.

---

## Asset Universe Dependency

Different universes may produce different outcomes.

---

## Implementation Variability

Public implementations may differ from the original paper.

---

# Research Questions

RQ-401

Final Offensive Universe Definition.

Status:

Open

---

RQ-402

Final Defensive Universe Definition.

Status:

Open

---

RQ-403

Exact Momentum Formula.

Status:

Open

---

RQ-404

Breadth Threshold Definition.

Status:

Open

---

RQ-405

Number of Selected Assets.

Status:

Open

---

RQ-406

Does Orion follow the original paper or Easy Investing implementation?

Status:

Open

---

# Research Conclusion

VAA is approved for further implementation research.

The original methodology must be fully documented before Orion-specific modifications are introduced.

Principle:

Original First

Customization Later

---

# Next Document

VAA_Orion.md

Purpose:

Define Orion-specific implementation details while preserving the original methodology.