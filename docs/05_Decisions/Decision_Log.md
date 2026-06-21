# Orion Decision Log

This document records all material architectural, investment, governance, and operational decisions made within Orion OS.

---

## D-001

### Decision

Moon does not create proprietary investment strategies.

### Rationale

Moon is designed to implement academically researched or publicly validated investment strategies rather than inventing new methodologies.

### Status

Approved

### Date

2026-06-14

---

## D-002

### Decision

Moon is used for actual portfolio rebalancing.

### Rationale

Moon serves as the tactical asset allocation engine of Orion and directly supports investment decisions.

### Details

Rebalancing Frequency:

* Monthly

### Status

Approved

### Date

2026-06-14

---

## D-003

### Decision

Supernova is a long-term equity portfolio based on the 5D Megatrend Framework.

### Details

5D Themes:

* Decoupling
* Deglobalization
* Demographics
* Decarbonization
* Digital Transformation

### Status

Approved

### Date

2026-06-14

---

## D-004

### Decision

Supernova follows a monthly accumulation model.

### Details

Holdings are intended for long-term ownership.

Replacement occurs only when the approved company list changes.

### Status

Approved

### Date

2026-06-14

---

## D-005

### Decision

Phoenix is a digital asset observation and investment framework focused on category leaders outside BTC, ETH, and SOL.

### Initial Watchlist

* TAO
* LINK
* AAVE
* SUI
* RENDER
* WLD
* ONDO

### Status

Draft

### Date

2026-06-14

---

## D-006

### Decision

Rename DAA to BDA.

### Rationale

The strategy operates exclusively within a bond ETF universe and does not represent a generic Dynamic Asset Allocation framework.

The new name improves clarity and reduces ambiguity within Orion documentation.

### Impact

All future references should gradually migrate from DAA to BDA.

### Status

Approved

### Date

2026-06-20

---

## D-007

### Decision

Supernova operates as a long-term Dollar Cost Averaging (DCA) framework.

### Rationale

Short-term market conditions are not considered a reliable basis for timing purchases within long-term megatrend investments.

### Details

Investment Frequency:

* Monthly

Purchases continue regardless of market volatility.

### Status

Approved

### Date

2026-06-20

---

## D-008

### Decision

Moon uses Equal Strategy Weighting.

### Rationale

No single strategy is assumed to be consistently superior.

Equal weighting reduces model risk and prevents discretionary strategy selection.

### Details

All active Moon strategies receive equal portfolio weight.

### Status

Approved

### Date

2026-06-20

---

## D-009

### Decision

Moon allows overlapping asset exposure.

### Rationale

When multiple independent strategies select the same asset, the overlap is interpreted as a stronger consensus signal.

### Details

Asset duplication is not removed.

Repeated selections increase final portfolio weight.

### Status

Approved

### Date

2026-06-20

---

## D-010

### Decision

Moon aggregates strategy outputs through Consensus Allocation.

### Rationale

Final portfolio weights should reflect agreement across independent strategies rather than arbitrary optimization.

### Details

Strategy outputs are combined and normalized to produce final portfolio allocations.

### Status

Approved

### Date

2026-06-20

---

## D-011

### Decision

Aurora is an observational framework and does not generate investment recommendations.

### Rationale

Aurora exists to provide market context rather than act as an investment allocation engine.

This separation preserves the independence of Moon, Supernova, and Phoenix.

### Status

Approved

### Date

2026-06-20

---

## D-012

### Decision

Moon separates signal assets from execution assets.

### Rationale

Academic research and published strategies are defined using
specific benchmark ETFs.

To preserve methodological integrity, signal generation shall
use the original asset universe whenever possible.

Execution may use lower-cost equivalent ETFs.

### Example

Signal Asset:
SPY

Execution Asset:
SPYM

Signal Asset:
BIL

Execution Asset:
SGOV

### Status

Approved

### Date

2026-06-20

---

## D-013

Moon execution ETF mappings shall be reviewed annually.

Review criteria include:

- Expense ratio
- Liquidity
- Assets under management
- Tracking quality
- Tax efficiency

### Date

2026-06-20

---

## D-014

Moon strategies are documented in two layers:

1. Research Specification
2. Orion Implementation Specification

Research documents preserve original methodology.

Implementation documents define Orion-specific execution details.

Status: Approved

Date: 2026-06-21

---

## D-015

Moon Governance Framework is established as the governing document for all Moon strategies.

All future strategy additions, removals, methodology changes, and implementation changes must comply with Moon_Governance.md.

Status: Approved

Date: 2026-06-21

---

## D-016

Moon uses Strategy Consensus Allocation as the portfolio aggregation methodology.

Final portfolio weights are derived from the combined output of approved strategies.

Moon does not apply discretionary weighting between strategies.

Status: Approved

Date: 2026-06-21

---

## D-017

Aurora shall monitor not only current market regime but also regime transition dynamics.

Aurora outputs must include:

* Current State
* State Momentum

Examples:

* Improving
* Stable
* Deteriorating

Purpose:

Detect potential market regime changes before full regime confirmation.

Status: Approved

Date: 2026-06-21

---

## D-018

Aurora shall distinguish between Core Indicators and Cross Asset Indicators.

Core Indicators determine the primary market regime.

Cross Asset Indicators provide additional environmental context.

Examples:

Core:
* Trend
* Liquidity
* Volatility
* Credit

Cross Asset:
* Dollar
* Gold
* Oil
* Bitcoin

Status: Approved

Date: 2026-06-21

---

## D-018

Orion shall use the following architecture terminology.

OS:
The complete Orion investment operating system.

Framework:
A major investment domain within Orion.

Engine:
A calculation or analysis module inside a framework.

Strategy:
A rules-based investment methodology within a framework.

Examples:

Moon = Framework

ADM = Strategy

Aurora Trend = Engine

Orion = OS

Status: Approved

Date: 2026-06-21

---

## D-019

Aurora shall manage indicators using an indicator lifecycle.

States:

* Candidate
* Approved
* Retired

Only Approved indicators may be used in production scoring.

All status changes must be recorded in Aurora documentation and the Decision Log.

Status: Approved

Date: 2026-06-21

---

## D-020

Aurora shall monitor regime transitions separately from regime classification.

Transition monitoring is considered a primary objective of Aurora.

Examples:

* Bull → Bear Watch
* Bear → Bull Watch

Aurora must report both:

1. Current Regime
2. Regime Direction

Status: Approved

Date: 2026-06-21

---
