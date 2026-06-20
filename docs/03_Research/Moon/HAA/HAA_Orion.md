# HAA Orion Implementation Specification

Version: 0.1

Status: Draft

Last Updated: 2026-06-20

Depends On:

* HAA_Research.md

---

# Purpose

This document defines the Orion-specific implementation of the HAA strategy.

While HAA_Research.md preserves the original research foundation, this document specifies how HAA is implemented within Orion OS.

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

Pending validation against original methodology.

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

# Evaluation Frequency

Monthly

---

# Evaluation Date

Last Trading Day

---

# Execution Date

Next Trading Day

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

Pending validation against original methodology.

Related Research Question:

RQ-302

---

# Asset Selection

If Canary Conditions are Healthy:

Select top-ranked assets from the Offensive Universe.

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

docs/02_Investment_Framework/Moon_Execution_Mapping.md

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

Current Assets:
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

State: Risk On

Canary: Healthy

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

Validation against Easy Investing implementation.

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