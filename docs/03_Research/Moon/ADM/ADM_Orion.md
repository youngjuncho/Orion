# ADM Orion Implementation Specification

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* ADM_Research.md
* Moon_Current_Production.md
* Moon_Object_Model.md

---

# Purpose

This document defines the Orion implementation of the Accelerating Dual Momentum (ADM) strategy.

While ADM_Research.md preserves the original Gary Antonacci methodology, this document specifies how ADM is implemented as a Moon Strategy within Orion OS.

The document focuses on implementation behavior rather than investment research.

---

# Role Within Moon

ADM is an independent Moon strategy.

Its responsibility is to:

* Load market data
* Evaluate momentum signals
* Select target assets
* Produce a StrategyResult

ADM does not:

* Aggregate portfolio allocations
* Execute trades
* Apply execution asset mappings

Those responsibilities belong to the Moon Engine.

---

# Strategy Lifecycle

```text
Load Market Data

↓

Calculate Relative Momentum

↓

Calculate Absolute Momentum

↓

Select Target Asset

↓

Generate StrategyResult
```

---

# Investment Universe

## Risk Assets

### US Equity

Ticker:

VTI

Description:

US Total Stock Market

---

### International Equity

Ticker:

VEU

Description:

FTSE All-World ex-US

---

## Defensive Asset

Primary Candidate

Ticker:

SGOV

Description:

0–3 Month US Treasury ETF

Backup Candidates

* BIL
* SHY

Status:

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

Status:

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

ADM evaluates:

1. Relative Momentum
2. Absolute Momentum

Initial Orion Standard

Trailing 12-Month Total Return

Formula

AdjustedPrice[t] / AdjustedPrice[t-12M] − 1

Adjusted Price is supplied by the normalized data layer and is treated as a
total-return proxy. ADM does not reconstruct or separately add distributions.
The observation selection, freshness, and missing-data rules remain subject
to the market-data contract.

Status

Pending Validation

---

# Selection Rules

The strategy selects exactly one asset.

Selection priority:

1. Highest Relative Momentum
2. Absolute Momentum confirmation
3. Defensive Asset if momentum is negative

The selected asset receives 100% allocation within ADM.

---

# Strategy Output

ADM produces a StrategyResult object.

Required Fields

* Strategy Name
* Signal Date
* Selected Assets
* Target Weights
* Metadata

Example

```text
Strategy: ADM

Signal Date:
2026-06-30

Selected Asset:
VTI

Weight:
100%

State:
Risk On
```

---

# State Model

ADM exposes a simplified operational state.

## Risk On

Selected Asset

* VTI
* VEU

---

## Risk Off

Selected Asset

* SGOV

The state is informational only.

Portfolio construction remains the responsibility of the Moon Engine.

---

# Integration With Moon

The Moon Engine executes the following workflow.

```text
ADM

↓

StrategyResult

↓

Consensus Allocation

↓

Execution Mapping

↓

Portfolio
```

ADM is unaware of other Moon strategies.

ADM never performs portfolio aggregation.

---

# Dashboard Output

Moon Dashboard displays:

* Current State
* Selected Asset
* Relative Momentum
* Absolute Momentum
* Next Rebalance Date

Dashboard presentation is separate from strategy logic.

---

# CLI Output

Command

```text
orion moon adm
```

Example

```text
Strategy: ADM

State: Risk On

Selected Asset: VTI

Next Rebalance: 2026-06-30
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
* Selected Asset
* Previous Asset
* Relative Momentum
* Absolute Momentum
* Strategy Version

---

# Future Enhancements

Potential Orion Variants

* ADM-US
* ADM-Global
* ADM-Leveraged
* ADM-Rotation

Status

Research Only

Not Approved

---

# Known Open Issues

OI-001

Final defensive asset selection

Candidates

* SGOV
* BIL
* SHY

Status

Open

---

OI-002

Total return calculation methodology

Status

Resolved by D-028. Use adjusted-price total return as specified above.

---

OI-003

Dividend adjustment methodology

Status

Resolved by D-028. Dividend adjustments are handled by the data layer's
adjusted-price normalization; ADM does not calculate dividends separately.

---

# Related Documents

* ADM_Research.md
* Moon_Current_Production.md
* Moon_Object_Model.md
* Moon_Interface.md
