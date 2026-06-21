# VAA Orion Implementation Specification

Version: 0.1

Status: Draft

Last Updated: 2026-06-21

Depends On:

* VAA_Research.md

---

# Purpose

This document defines the Orion-specific implementation of the VAA strategy.

While VAA_Research.md preserves the original research foundation, this document specifies how VAA is implemented within Orion OS.

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

Pending validation against original methodology.

---

## Defensive Universe

Purpose:

Capital preservation during deteriorating market conditions.

Candidate Assets:

* SHY
* IEF
* LQD

Status:

Pending validation against original methodology.

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

Pending validation against original methodology.

Related Research Question:

RQ-403

---

# Asset Selection

If Breadth Conditions are Favorable:

Allocate to top-ranked offensive assets.

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

docs/02_Investment_Framework/Moon_Execution_Mapping.md

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

Current Assets:
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

State: Risk On

Breadth: Healthy

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

Validation against Easy Investing implementation.

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