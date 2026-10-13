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

---

# Variant Comparison Addendum ? Primary-Source Parameter Clarification

Last Updated: 2026-10-13

Status: Research Clarification ? Variant Not Yet Approved

## Reference VAA-G4

Commonly documented G4 profile:
- Offensive universe: SPY, EFA, EEM, AGG
- Defensive universe: LQD, IEF, SHY
- Top offensive holdings: T = 1
- Breadth threshold: B = 1

With B = 1, any offensive momentum score <= 0 results in a full defensive allocation.

## Reference VAA-G12

The original-paper parameterization is reported as:
- Offensive universe: SPY, IWM, QQQ, VGK, EWJ, VWO, VNQ, GSG, GLD, TLT, HYG, LQD
- Defensive universe: SHY, IEF, LQD
- Top offensive holdings: T = 2
- Breadth threshold: B = 4

The important distinction is that the original paper's Easy Trading approach discretizes the cash fraction into increments determined by T. A commonly reported formula is:

CF = floor(b ¡¿ T / B) / T

where b is the number of offensive assets whose 13612W score is <= 0. The defensive allocation is CF; the offensive allocation is 1 - CF.

For G12 (T=2, B=4), this yields:
- b = 0 or 1: CF = 0%
- b = 2 or 3: CF = 50%
- b >= 4: CF = 100%

This is not the same as the simplified linear formula CF = min(1, b/B), which would produce 25% and 75% defensive allocations for b=1 and b=3. Do not substitute the linear formula for the discretized original-paper rule without explicitly approving a variant change.

Some modern public implementations label a profile VAA-G12 while using TopO=5 and/or linear partial-defensive allocation. Those should be treated as implementation variants, not assumed equivalent to the original-paper T=2 configuration. The exact implementation referred to as ¡°Easy Investing¡± is not included in the current repository ZIP and therefore has not been independently verified.

## Momentum Formula

For month-end adjusted price P(t):
- R1 = P(t)/P(t-1) - 1
- R3 = P(t)/P(t-3) - 1
- R6 = P(t)/P(t-6) - 1
- R12 = P(t)/P(t-12) - 1
- 13612W = 12R1 + 4R3 + 2R6 + R12

Use the same score for ranking and the <= 0 breadth classification. The precise price field (adjusted close versus another total-return series), missing-data policy, and signal-to-execution timing must be specified before coding.

## Orion Difference Register

Orion's current candidate offensive list is SPY, EFA, EEM, AGG, LQD, VNQ, DBC. It is neither the canonical G4 universe nor the canonical G12 universe. The defensive candidates SHY, IEF, LQD align with the commonly documented defensive universe.

The current execution substitutions (SPY¡æSPYM, EFA¡æVEA, EEM¡æVWO, AGG¡æBND, LQD¡æVCIT, VNQ¡æUSRT, DBC¡æBCI, SHY¡æSCHO, IEF¡æVGIT) must remain execution-only and must not alter the signal calculations.

## Decisions Still Open

1. Choose original-paper G4, original-paper G12 (T=2, B=4), or a separately named custom variant.
2. Confirm exact momentum price series and missing-history behavior.
3. Confirm signal month-end and execution convention.
4. Retrieve and compare the actual Easy Investing implementation before claiming parity.
5. Define how the StrategyResult represents 0%, 50%, and 100% defensive allocations and how weights are assigned to selected assets.

No production VAA code should be written until these decisions are recorded and approved.

## References

- Keller & Keuning (2017), *Breadth Momentum and Vigilant Asset Allocation (VAA): Winning More by Losing Less*: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3002624
- Public implementation reference: https://github.com/penny-vault/vigilant-asset-allocation
- Public VAA-G12 summary: https://github.com/stockviz/blog/blob/master/vigilant-asset-allocation/VAA_Paper_Summary.md
