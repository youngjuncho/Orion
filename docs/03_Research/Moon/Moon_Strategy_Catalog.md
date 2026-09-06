# Moon Strategy Catalog

Version: 1.1

Status: Active

Last Updated: 2026-07-27

Depends On:

* Moon_Object_Model.md
* Moon_Current_Production.md

---

# Purpose

This document catalogs all tactical asset allocation strategies registered by
Moon. Registration does not imply that a strategy is approved for execution.

It defines the research status, implementation status, and operational role of each strategy within Orion OS.

Moon implements academically researched investment methodologies using a standardized execution framework.

---

# Strategy Architecture

All Moon strategies implement the common Moon Strategy Interface defined in:

docs/02_Investment_Framework/Moon/Moon_Object_Model.md

Each strategy must provide:

- Strategy metadata
- Signal generation
- Asset selection
- Allocation output

Individual strategy documents define only their strategy-specific rules.

---

# Strategy Status

| Strategy | Research | Orion Spec | Coding | Status |
|----------|----------|------------|---------|--------|
| ADM | Draft with OI-001..003 open | Partial | Partial signal selection only | Registered; inactive |
| BAA | Open issues OI-101..104 | Draft | Not Started | Registered; inactive |
| VAA | Open issues OI-401..405 | Draft | Not Started | Registered; inactive |
| HAA | Open issues OI-301..304 | Draft | Not Started | Registered; inactive |
| BDA | Open issues OI-201..203 | Draft | Not Started | Registered; inactive |

The operational execution allowlist is maintained separately in
`config/moon.yaml` as `active_strategies`. It is empty until a strategy's
research and Orion implementation specification are ready and its execution
mappings are approved.

---

# Priority Order

Current implementation priority:

1. ADM
2. BAA
3. VAA
4. HAA
5. BDA

This order reflects implementation priority only.

It does not imply portfolio weighting or investment preference.

---

# Strategy Summary

## ADM

Full Name:

Absolute Dual Momentum

Author:

Gary Antonacci

Purpose:

Select the strongest equity market while avoiding major drawdowns through relative and absolute momentum.

Characteristics:

- Relative Momentum
- Absolute Momentum
- Monthly Rebalancing
- Single Asset Selection

Output:

One selected asset.

---

## BAA

Full Name:

Bold Asset Allocation

Author:

Wouter Keller

Purpose:

Allocate between offensive and defensive universes using Canary assets.

Characteristics:

- Canary Filter
- Offensive / Defensive Allocation
- Momentum Ranking
- Multiple Asset Selection

Output:

Multiple selected assets.

---

## VAA

Full Name:

Vigilant Asset Allocation

Author:

Wouter Keller

Purpose:

Adjust risk exposure according to market breadth deterioration.

Characteristics:

- Breadth Evaluation
- Progressive Defense
- Momentum Ranking

Output:

Multiple selected assets.

---

## HAA

Full Name:

Hybrid Asset Allocation

Author:

Wouter Keller

Purpose:

Combine momentum ranking with Canary-based market evaluation.

Characteristics:

- Hybrid Allocation
- Canary Filter
- Momentum Ranking

Output:

Multiple selected assets.

---

## BDA

Full Name:

Bond Dynamic Allocation

Purpose:

Allocate among bond asset classes using momentum-based selection.

Characteristics:

- Bond Rotation
- Duration Management
- Defensive Focus

Output:

One selected asset.

Status:

Research Validation Required.

---

# Common Strategy Interface

Every Moon strategy implements the standardized interface.

Each strategy produces a StrategyResult object containing:

- Strategy Name
- Evaluation Date
- State
- Selected Assets
- Target Weights
- Supporting Metrics

Moon aggregates all StrategyResult objects into a Consensus Allocation.

---

# Implementation Principle

Moon separates signal generation from execution.

Signal generation uses the original research universe whenever possible.

Execution assets may differ according to:

Moon_Execution_Mapping.md

Principle:

Signal Integrity Has Priority Over Execution Convenience.

---

# Consensus Allocation

Each strategy contributes equally to the final Moon portfolio unless explicitly changed by governance.

Final portfolio allocation is calculated using StrategyResult objects.

Reference:

Moon_Current_Production.md

Moon_Object_Model.md

---

# Future Expansion

Potential future additions:

- GTAA
- KDAA
- Accelerating Dual Momentum
- Trend Following Models

Status:

Research Only

Not Approved

---

# Related Documents

* Moon_Object_Model.md
* Moon_Current_Production.md
* Moon_Execution_Mapping.md
* Orion_IPS.md
* ADM_Orion.md
* BAA_Orion.md
* VAA_Orion.md
* HAA_Orion.md
* BDA_Orion.md
* Decision_Log.md
