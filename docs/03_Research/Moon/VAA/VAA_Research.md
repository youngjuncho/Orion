# VAA Research Specification

Version: 1.1

Status: Research ? core G12 method specified; empirical validation remains open

Author:

Wouter Keller

Publication:

Vigilant Asset Allocation

Last Updated:

2026-10-18

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

# Momentum Measurement ? Source-Verified G12 Rule

The Keller and Keuning (2017) VAA paper defines the fast 13612W momentum
filter from total-return-adjusted monthly prices. For price series `P`, the
score is:

`M = 12 ¡¿ (P(t)/P(t?1) ? 1) + 4 ¡¿ (P(t)/P(t?3) ? 1) + 2 ¡¿ (P(t)/P(t?6) ? 1) + (P(t)/P(t?12) ? 1)`

The same score is used for relative ranking and for classifying an offensive
asset as bad when its score is non-positive (`M <= 0`). Thirteen month-end
observations are therefore required. The score is a weighted sum of the four
period returns, not a normalized average; dividing by a positive constant would
not change ranking or the sign test, but Orion records the source formula as
written for reproducibility.

For VAA-G12, the source specifies 12 offensive assets, defensive universe
`SHY`, `IEF`, `LQD`, `T=2` and breadth threshold `B=4`. The original linear
cash fraction is `CF = min(1, b/B)`, where `b` is the number of offensive
assets with non-positive momentum. The Easy Trading (ET) variant rounds the
cash allocation to whole position units of size `1/T`, producing defensive
fractions of 0%, 50% or 100% for G12.

Evidence: Keller, W. J. and Keuning, J. W. (2017), *Breadth Momentum and
Vigilant Asset Allocation (VAA): Winning More by Losing Less*, SSRN 3002624
(https://ssrn.com/abstract=3002624). Source-aligned public implementations
provide corroboration, not a substitute for the paper. Orion must retain the
citation and distinguish paper rules from local engineering choices.

Status: Formula and G12 parameter definitions source-verified. Independent
backtest replication and live-data validation remain open.

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

# Research Questions and Decisions

## RQ-401 ? Final Offensive Universe Definition

Status: Resolved for the VAA-G12 source-method baseline; change requires a
recorded Orion decision.

Decision: `SPY, IWM, QQQ, VGK, EWJ, VWO, VNQ, GSG, GLD, TLT, HYG, LQD`.

Evidence: Keller and Keuning (2017), VAA-G12 universe definition. This is the
signal universe, not an execution-ETF mapping.

## RQ-402 ? Final Defensive Universe Definition

Status: Resolved for the VAA-G12 source-method baseline; execution mapping is
not implied.

Decision: `SHY, IEF, LQD`.

Evidence: Keller and Keuning (2017), VAA-G12 default cash/defensive universe.
`LQD` also appears in the offensive universe in the source definition.

## RQ-403 ? Exact Momentum Formula

Status: Resolved for the source-method baseline; implementation parity is
covered by code tests, while independent numerical replication remains open.

Decision: `13612W = 12¡¿R1 + 4¡¿R3 + 2¡¿R6 + R12`, where `Rk = P(t)/P(t?k) ? 1`,
using total-return-adjusted monthly prices. The same score drives ranking and
the non-positive momentum test.

## RQ-404 ? Breadth Threshold Definition

Status: Resolved for the VAA-G12 source-method baseline.

Decision: `b` is the number of the 12 offensive assets with `13612W <= 0`;
`B=4`. The original linear cash fraction is `min(1, b/B)`. The Easy Trading
variant rounds defensive allocation to whole `1/T` units; with `T=2`, G12
allocations are 0%, 50%, and 100% defensive.

## RQ-405 ? Number of Selected Assets

Status: Resolved for the VAA-G12 + Easy Trading candidate; empirical replication
and Orion approval remain open.

Decision: `T=2`. Fully offensive: two highest-ranked offensive assets at 50%
each. Partial defense: the highest-ranked offensive asset and the highest-
ranked defensive asset at 50% each. Fully defensive: the highest-ranked
defensive asset at 100%.

## RQ-406 ? Source Method or Alternative Implementation

Status: Resolved as a terminology/method selection; production approval remains
open.

Decision: Use Keller and Keuning's VAA-G12 as the source baseline and identify
the whole-position rounding variant as **Easy Trading (ET)**. ¡°Easy Investing¡±
was an incorrect label in the earlier research question and is not treated as a
separate methodology without a specific source. Orion-specific data validation,
execution mapping and governance remain local implementation concerns.

# Research Conclusion

The source-method baseline for VAA-G12 is now specified: G12 offensive and
defensive universes, 13612W momentum, `B=4`, `T=2`, and Easy Trading whole-
position rounding. The decisions above close the method-definition questions;
they do not certify historical performance, approve execution mappings, or
activate VAA in Moon.

Principle: Original First; Customization Later. Any departure from the source
baseline must be described as an Orion modification, justified, tested, and
recorded in the Decision Log.

# Next Document

VAA_Orion.md

Purpose:

Define Orion-specific implementation details while preserving the original methodology.