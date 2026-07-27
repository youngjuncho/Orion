# HAA Orion Implementation Specification

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* HAA_Research.md
* docs/02_Investment_Framework/Moon/Moon_Current_Production.md
* docs/02_Investment_Framework/Moon/Moon_Object_Model.md
* docs/06_Implementation/Moon_Interface.md

---

# Purpose

This document defines the Orion-specific implementation of the HAA strategy.

While HAA_Research.md preserves the original Keller methodology, this document specifies how HAA is implemented within Orion OS.

The implementation follows the standard Moon Strategy interface and produces a StrategyResult consumed by the Moon Consensus Allocation engine.

---

# Implementation Principles

## Original First

The original HAA methodology remains the reference implementation.

---

## Practical Execution

The Orion implementation prioritizes:

* Simplicity
* ETF availability
* Monthly execution
* Research reproducibility

---

# Orion HAA Universe

## Canary Universe

Purpose:

Evaluate overall market health before allocating capital.

Current Status:

Pending validation against the original methodology.

---

## Offensive Universe

Purpose:

Primary growth allocation during favorable market conditions.

Candidate Assets:

* SPY
* QQQ
* IWM
* EFA
* EEM
* VNQ
* DBC

Status:

Pending Final Approval

---

## Defensive Universe

Purpose:

Capital preservation during deteriorating market conditions.

Candidate Assets:

* BIL
* IEF
* TLT
* LQD

Status:

Pending Final Approval

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

HAA implements the standard Moon Strategy interface.

Input:

* Market Data
* Strategy Configuration

Output:

* StrategyResult

The StrategyResult is consumed by the Moon Consensus Allocation engine.

Reference:

docs/06_Implementation/Moon_Interface.md

---

# Canary Evaluation

Purpose:

Determine whether the market environment supports offensive positioning.

Methodology:

Pending validation.

Related Research Question:

RQ-301

---

# Momentum Calculation

Purpose:

Rank candidate assets.

Current Status:

Pending validation against the original methodology.

Related Research Question:

RQ-302

---

# Asset Selection

Purpose:

Generate a StrategyResult containing the selected offensive or defensive assets.

The StrategyResult is passed to the Moon Consensus Allocation engine.

---

If Canary Conditions are Healthy:

Select the highest-ranked assets from the Offensive Universe.

---

If Canary Conditions are Deteriorating:

Select assets from the Defensive Universe.

---

Number of Selected Assets:

Pending validation.

Status:

Open

Related Research Question:

RQ-305

---

# Signal Universe

Signal generation uses the original research ETF universe whenever possible.

Examples:

* SPY
* QQQ
* EEM
* DBC
* BIL

Signal integrity has priority over execution convenience.

---

# Execution Universe

Execution assets follow:

docs/02_Investment_Framework/Moon/Moon_Execution_Mapping.md

Examples:

* SPY → SPYM
* QQQ → QQQM
* IWM → VTWO
* EEM → VWO
* DBC → BCI
* BIL → SGOV

---

# State Model

## Risk On

Condition:

Healthy Canary Signals

Output:

State:
Risk On

Universe:
Offensive

---

## Risk Off

Condition:

Negative Canary Signals

Output:

State:
Risk Off

Universe:
Defensive

---

# Moon Dashboard Output

Example

Strategy:
HAA

Selected Assets:

SPY

QQQ

DBC

State:
Risk On

Canary Status:
Healthy

Rebalance Date:
2026-06-30

Next Action:
Hold

---

# CLI Output

Command

orion moon haa

Example

HAA

State:
Risk On

Canary:
Healthy

Selected Assets:

SPY

QQQ

DBC

Next Rebalance:

2026-06-30

---

# Dashboard Score

HAA contributes to the Moon Dashboard.

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
* Canary Status
* Momentum Values

---

# Known Open Issues

OI-301

Final Canary Universe.

Status:

Open

---

OI-302

Final Momentum Formula.

Status:

Open

---

OI-303

Final Asset Universe Validation.

Status:

Open

---

OI-304

Validation against the Easy Investing implementation.

Status:

Open

Related Research Question:

RQ-306

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