# Moon Strategy Catalog

Version: 1.0

Status: Active

Last Updated: 2026-06-21

---

# Overview

Moon is the tactical asset allocation engine of Orion OS.

Moon implements academically researched and publicly validated investment strategies.

Moon does not create proprietary investment strategies.

Principle:

Original First

Customization Later

---

# Strategy Status

| Strategy | Research | Orion Spec | Coding      | Status |
| -------- | -------- | ---------- | ----------- | ------ |
| ADM      | Complete | Complete   | Not Started | Active |
| BAA      | Complete | Complete   | Not Started | Active |
| VAA      | Complete | Complete   | Not Started | Active |
| HAA      | Complete | Complete   | Not Started | Active |
| BDA      | Complete | Complete   | Not Started | Active |

---

# Priority Order

1. ADM
2. BAA
3. VAA
4. HAA
5. BDA

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

* Simple
* Transparent
* Monthly Rebalancing
* Equity Rotation

---

## BAA

Full Name:

Bold Asset Allocation

Author:

Wouter Keller

Purpose:

Allocate capital between offensive and defensive universes using canary assets.

Characteristics:

* Canary System
* Offensive / Defensive Allocation
* Momentum Ranking
* Monthly Rebalancing

---

## VAA

Full Name:

Vigilant Asset Allocation

Author:

Wouter Keller

Purpose:

Adjust portfolio risk based on market breadth deterioration.

Characteristics:

* Breadth-Based Risk Control
* Momentum Ranking
* Progressive Defense
* Monthly Rebalancing

---

## HAA

Full Name:

Hybrid Asset Allocation

Author:

Wouter Keller

Purpose:

Combine momentum and canary-based risk management into a hybrid tactical allocation framework.

Characteristics:

* Hybrid Allocation
* Momentum Ranking
* Risk Management Focus
* Monthly Rebalancing

---

## BDA

Full Name:

Bond Dynamic Allocation

Purpose:

Rotate among bond asset classes based on momentum and trend conditions.

Characteristics:

* Bond Rotation
* Duration Management
* Defensive Allocation
* Monthly Rebalancing

Status:

Research Validation Required

---

# Strategy Categories

## Equity Momentum

* ADM

---

## Multi-Asset Tactical Allocation

* BAA
* VAA
* HAA

---

## Bond Tactical Allocation

* BDA

---

# Implementation Principle

Signal generation uses the original research universe whenever possible.

Execution ETFs may differ from research ETFs.

Reference:

Moon_Execution_Mapping.md

Principle:

Signal Integrity Has Priority Over Execution Convenience

---

# Current Production Candidate

ADM

Reason:

* Simplest implementation
* Strong academic foundation
* Easy validation
* Clear signal structure

---

# Future Expansion

Potential future additions:

* GTAA
* KDAA
* Accelerating Dual Momentum
* Trend Following Models

Status:

Research Only

Not Approved

---

# Related Documents

* Orion_IPS.md
* Moon_Execution_Mapping.md
* Decision_Log.md
* ADM_Research.md
* ADM_Orion.md
* BAA_Research.md
* BAA_Orion.md
* VAA_Research.md
* VAA_Orion.md
* HAA_Research.md
* HAA_Orion.md
* BDA_Research.md
* BDA_Orion.md
