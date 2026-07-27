# BAA Orion Implementation Specification

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* BAA_Research.md
* Moon_Current_Production.md
* Moon_Object_Model.md

---

# Purpose

This document defines the Orion implementation of the Bold Asset Allocation (BAA) strategy.

While BAA_Research.md preserves the original Wouter Keller methodology, this document specifies how BAA is implemented as a Moon Strategy within Orion OS.

The document focuses on implementation behavior rather than investment research.

---

# Role Within Moon

BAA is an independent Moon strategy.

Its responsibility is to:

* Load market data
* Evaluate Canary conditions
* Rank candidate assets
* Select target assets
* Produce a StrategyResult

BAA does not:

* Aggregate portfolio allocations
* Execute trades
* Apply execution asset mappings

Those responsibilities belong to the Moon Engine.

---

# Strategy Lifecycle

```text
Load Market Data

↓

Evaluate Canary Conditions

↓

Calculate Momentum

↓

Rank Candidate Assets

↓

Select Target Assets

↓

Generate StrategyResult
```

---

# Investment Universe

## Canary Universe

Purpose

Detect deterioration in market conditions before allocating capital.

Status

Research In Progress

Final universe pending validation against the original methodology.

---

## Offensive Universe

Purpose

Primary growth allocation during Risk On conditions.

Candidate Assets

* SPY
* QQQ
* IWM
* EFA
* EEM
* VNQ
* DBC

Status

Pending Final Approval

---

## Defensive Universe

Purpose

Capital preservation during Risk Off conditions.

Candidate Assets

* BIL
* IEF
* TLT
* LQD

Status

Pending Final Approval

---

# Data Source

Primary Source

Yahoo Finance

Reasons

* Free
* Reliable
* Python ecosystem support

Backup Sources

* Stooq
* Alpha Vantage
* Polygon

Status

Future Review

---

# Evaluation Schedule

Evaluation Frequency

Monthly

Evaluation Date

Last Trading Day

Execution Date

Next Trading Day

---

# Signal Calculation

BAA evaluates:

1. Canary Conditions
2. Relative Momentum Ranking

Status

Pending validation against the original methodology.

Related Research Questions

* RQ-101
* RQ-102

---

# Selection Rules

If Canary Conditions are healthy:

* Rank the Offensive Universe
* Select the highest-ranked assets

If Canary Conditions deteriorate:

* Select assets from the Defensive Universe

Number of selected assets

Pending validation.

Related Research Question

RQ-105

---

# Signal Universe

Signal generation uses the original research ETF universe whenever possible.

Examples

* SPY
* QQQ
* EEM
* DBC
* BIL

Signal integrity has priority over execution convenience.

---

# Execution Universe

Execution assets follow:

Moon_Execution_Mapping.md

Examples

* SPY → SPYM
* QQQ → QQQM
* EEM → VWO
* DBC → BCI
* BIL → SGOV

Execution mapping is performed by the Moon Engine after StrategyResult generation.

---

# Strategy Output

BAA produces a StrategyResult object.

Required Fields

* Strategy Name
* Signal Date
* Selected Assets
* Target Weights
* Metadata

Example

```text
Strategy: BAA

Signal Date:
2026-06-30

Selected Assets:

SPY
QQQ

Weights:

50%
50%

State:
Risk On
```

---

# State Model

BAA exposes an operational state.

## Risk On

Condition

Healthy Canary Conditions

Universe

Offensive

---

## Risk Off

Condition

Negative Canary Conditions

Universe

Defensive

The state is informational only.

Portfolio construction remains the responsibility of the Moon Engine.

---

# Integration With Moon

The Moon Engine executes the following workflow.

```text
BAA

↓

StrategyResult

↓

Consensus Allocation

↓

Execution Mapping

↓

Portfolio
```

BAA is independent of all other Moon strategies.

Portfolio aggregation is performed only by the Moon Engine.

---

# Dashboard Output

Moon Dashboard displays:

* Current State
* Canary Status
* Selected Assets
* Target Weights
* Next Rebalance Date

Dashboard presentation is separate from strategy logic.

---

# CLI Output

Command

```text
orion moon baa
```

Example

```text
Strategy: BAA

State: Risk On

Canary: Healthy

Selected Assets:

SPY
QQQ

Next Rebalance:

2026-06-30
```

---

# Rebalancing Policy

Frequency

Monthly

Forced Rebalance

Not Allowed

Manual Override

Not Allowed

---

# Logging Requirements

Each execution stores:

* Signal Date
* Selected Assets
* Previous Assets
* Canary Status
* Momentum Values
* Strategy Version

---

# Known Open Issues

OI-101

Final Canary Universe

Status

Open

---

OI-102

Final Momentum Formula

Status

Open

---

OI-103

Number of Selected Assets

Status

Open

---

OI-104

Validation against Easy Investing implementation

Status

Open

Related Research Question

RQ-106

---

# Related Documents

* BAA_Research.md
* Moon_Current_Production.md
* Moon_Object_Model.md
* Moon_Interface.md