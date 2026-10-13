# VAA Orion Implementation Specification

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* VAA_Research.md
* docs/02_Investment_Framework/Moon/Moon_Current_Production.md
* docs/02_Investment_Framework/Moon/Moon_Object_Model.md
* docs/06_Implementation/Moon_Interface.md

---

# Purpose

This document defines the Orion-specific implementation of the VAA strategy.

While VAA_Research.md preserves the original Keller methodology, this document specifies how VAA is implemented within Orion OS.

The implementation follows the standard Moon Strategy interface and produces a StrategyResult consumed by the Moon Consensus Allocation engine.

---

# Implementation Principles

## Original First

The original VAA methodology remains the reference implementation.

---

## Practical Execution

The Orion implementation prioritizes:

* Simplicity
* ETF availability
* Monthly execution
* Research reproducibility

---

# Orion VAA Universe

## Offensive Universe

Purpose:

Primary growth allocation during favorable market conditions.

Candidate Assets:

* SPY
* EFA
* EEM
* AGG
* LQD
* VNQ
* DBC

Status:

Pending validation against the original methodology.

---

## Defensive Universe

Purpose:

Capital preservation during deteriorating market conditions.

Candidate Assets:

* SHY
* IEF
* LQD

Status:

Pending validation against the original methodology.

---

# Data Source

Primary Source

Yahoo Finance

Reason:

* Free
* Reliable
* Python ecosystem support

---

Backup Sources

* Stooq
* Alpha Vantage
* Polygon

Status:

Future Review

---

# Evaluation Schedule

## Evaluation Frequency

Monthly

---

## Evaluation Date

Last Trading Day

---

## Execution Date

Next Trading Day

---

# Strategy Interface

VAA implements the standard Moon Strategy interface.

Input:

* Market Data
* Strategy Configuration

Output:

* StrategyResult

The StrategyResult is consumed by the Moon Consensus Allocation engine.

Reference:

docs/06_Implementation/Moon_Interface.md

---

# Breadth Evaluation

Purpose:

Measure the number of offensive assets with negative momentum.

The defensive allocation increases as market weakness expands.

Current Status:

Pending validation.

Related Research Question:

RQ-404

---

# Momentum Calculation

Purpose:

Rank candidate assets.

Current Status:

Pending validation against the original methodology.

Related Research Question:

RQ-403

---

# Asset Selection

Purpose:

Generate a StrategyResult containing the selected offensive and/or defensive assets.

The StrategyResult is passed to the Moon Consensus Allocation engine.

---

If Breadth Conditions are Favorable:

Allocate to the highest-ranked offensive assets.

---

If Breadth Conditions are Deteriorating:

Allocate partially or fully to defensive assets.

---

Number of Selected Assets:

Pending validation.

Status:

Open

Related Research Question:

RQ-405

---

# Signal Universe

Signal generation uses the original research ETF universe whenever possible.

Examples:

* SPY
* EEM
* AGG
* VNQ
* DBC

Signal integrity has priority over execution convenience.

---

# Execution Universe

Execution assets follow:

docs/02_Investment_Framework/Moon/Moon_Execution_Mapping.md

Examples:

* SPY → SPYM
* EFA → VEA
* EEM → VWO
* AGG → BND
* LQD → VCIT
* VNQ → USRT
* DBC → BCI
* SHY → SCHO
* IEF → VGIT

---

# State Model

## Risk On

Condition:

Breadth conditions are favorable.

Output:

State:
Risk On

Universe:
Offensive

---

## Partial Defense

Condition:

Some offensive assets exhibit negative momentum.

Output:

State:
Partial Defense

Universe:
Mixed

---

## Defensive

Condition:

Broad market weakness detected.

Output:

State:
Defensive

Universe:
Defensive

---

# Moon Dashboard Output

Example

Strategy:
VAA

Selected Assets:

SPY

EEM

State:
Risk On

Breadth:
Healthy

Rebalance Date:
2026-06-30

Next Action:
Hold

---

# CLI Output

Command

orion moon vaa

Example

VAA

State:
Risk On

Breadth:
Healthy

Selected Assets:

SPY

EEM

Next Rebalance:

2026-06-30

---

# Dashboard Score

VAA contributes to the Moon Dashboard.

Score Calculation:

Not Yet Defined

Future Document:

Moon_Scoring_Framework.md

Status:

Pending

---

# Rebalancing Policy

Default Frequency

Monthly

---

Forced Rebalance

Not Allowed

---

Manual Override

Not Allowed

---

# Logging Requirements

Every rebalance event must store:

* Date
* StrategyResult
* Selected Assets
* Previous Assets
* Breadth Score
* Momentum Values

---

# Known Open Issues

OI-401

Final Offensive Universe.

Status:

Open

---

OI-402

Final Defensive Universe.

Status:

Open

---

OI-403

Final Momentum Formula.

Status:

Open

---

OI-404

Breadth Threshold Validation.

Status:

Open

---

OI-405

Validation against the Easy Investing implementation.

Status:

Open

Related Research Question:

RQ-406

---

# Approval Status

Research:
In Progress

Implementation:
Draft

Coding:
Not Started

---

# Related Documents

* Moon_Current_Production.md
* Moon_Object_Model.md
* Moon_Interface.md
* Moon_Execution_Mapping.md
* Moon_Scoring_Framework.md

---

# Variant Comparison Addendum (2026-10-13)

Status: Draft — Not Approved for Production

## Reference Variant Is Not Yet Selected

The current Orion offensive candidate list (SPY, EFA, EEM, AGG, LQD, VNQ, DBC) is a custom seven-asset list. It does not match the commonly documented G4 or G12 offensive universe. The defensive candidates (SHY, IEF, LQD) match the commonly documented defensive universe.

Do not infer the strategy variant from the current candidate list.

## Keep These Parameters Separate

- `breadth_threshold` (`B`): breadth parameter from the selected VAA variant.
- `top_offensive_count` (`T`): number of top-ranked offensive assets held when offensive allocation is nonzero.
- `cash_fraction` (`CF`): defensive allocation fraction computed using the selected variant's exact rule.

For the original-paper G12 parameterization commonly reported as T=2 and B=4, the Easy Trading rule is discretized: `CF = floor(b * T / B) / T`, where `b` counts offensive scores <= 0. This produces 0%, 50%, or 100% defensive allocation, not linear 0%, 25%, 50%, 75%, 100% allocation.

Some public implementations use a different G12 profile (for example TopO=5 or linear allocation). Treat these as custom variants unless their equivalence to the original paper is demonstrated. The Easy Investing implementation is not present in the repository ZIP and has not yet been verified.

## Signal and Execution Separation

The canonical signal universe determines momentum, ranking, and breadth. Execution mappings are applied only after the strategy result is produced. A mapping must not alter the signal universe or momentum calculation.

## Implementation Gate

Before coding, record:
1. Exact selected variant and source.
2. Offensive and defensive signal universes.
3. 13612W price series and formula.
4. Breadth comparison (`<= 0` or another explicitly justified rule).
5. `T`, `B`, and exact `CF` equation.
6. Missing data and insufficient history behavior.
7. Monthly signal date and execution timing.
8. Expected `StrategyResult` state, weights, and metadata for each allocation state.

Until these decisions are resolved, status remains Research In Progress / Coding Not Started.
