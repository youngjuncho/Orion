# Orion Decision Log

This document records all material architectural, investment, governance, and operational decisions made within Orion OS.

## Decision Status Definitions

Approved

Decision is active and governs Orion.

Draft

Decision is under evaluation.

Superseded

Decision has been replaced by one or more newer decisions.

Retired

Decision is no longer used and has no active replacement.

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

Superseded

### Superseded By

* D-021 Phoenix Scope and Core Asset Separation
* D-022 Phoenix Portfolio Construction Methodology

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

## D-021 — Phoenix Scope and Core Digital Asset Separation

Date:

2026-06-21

Status:

Approved

### Decision

Bitcoin (BTC) and Ethereum (ETH) are excluded from Phoenix.

BTC and ETH are treated as Core Digital Assets and are managed independently from Phoenix.

Phoenix focuses exclusively on altcoin category leaders and leadership transitions.

### Core Digital Asset Allocation

Default allocation:

* BTC 60%
* ETH 40%

Accumulation method:

* Periodic purchases
* No tactical rebalancing
* Long-term holding

### Phoenix Scope

Phoenix manages:

* Smart Contract Leaders
* Oracle Leaders
* AI Infrastructure Leaders
* RWA Leaders
* Other approved category leaders

Phoenix does not manage:

* BTC
* ETH

### Rebalancing Principle

Price changes alone shall not trigger portfolio rebalancing.

Phoenix responds to:

* Leadership changes
* Category leader replacement
* Replacement risk events

### Rationale

BTC and ETH currently represent foundational digital asset infrastructure.

Phoenix exists to identify emerging category leaders and potential future winners rather than manage established core digital assets.

Separating Core Digital Assets from Phoenix simplifies portfolio construction and preserves Phoenix's focus on leadership monitoring.

### Impact

Core Digital Assets

* BTC
* ETH

Phoenix Portfolio

* Altcoin category leaders only

Status:

Effective immediately.

---

## D-022

Date:

2026-06-22

Status:

Approved

Category:

Phoenix

---

## Title

Phoenix Portfolio Construction Methodology

---

## Context

Phoenix identifies digital asset leaders at the category level.

The framework evaluates:

* Categories
* Leaders
* Challengers
* Replacement Risk

A portfolio construction methodology is required.

Key questions:

* Should challengers be included?
* How many assets should be held?
* How should weights be assigned?

---

## Decision

Phoenix shall invest only in approved category leaders.

Challengers and watchlist assets are used exclusively for monitoring and replacement evaluation.

They are not eligible for portfolio inclusion.

Portfolio weights are assigned equally across all approved leaders.

---

## Example

Approved Leaders:

* SOL
* LINK
* TAO
* ONDO
* TIA

Result:

* SOL 20%
* LINK 20%
* TAO 20%
* ONDO 20%
* TIA 20%

---

## Leadership Change

If a challenger becomes the new approved leader:

Example:

Before

* SOL

After

* SUI

The portfolio shall rebalance during the next review cycle.

---

## Exclusions

Phoenix does not manage:

* BTC
* ETH

These assets are managed separately under D-021.

---

## Rationale

Leader-only construction aligns with the purpose of Phoenix.

Phoenix exists to identify and own category leaders.

It does not attempt to predict future leaders before leadership has been established.

This approach:

* Simplifies operations
* Reduces turnover
* Improves explainability
* Maintains consistency with the framework philosophy

---

## Consequences

Benefits

* Simple implementation
* Clear governance
* Lower operational complexity

Risks

* Leadership transitions may be captured later
* Challenger upside may be missed

These risks are accepted.

---

## Review Trigger

This decision should be reconsidered if:

* Phoenix exceeds 10 portfolio assets
* Leadership turnover becomes frequent
* Historical testing demonstrates superior challenger participation

---

## Related Documents

Phoenix_Operating_Model.md

Phoenix_Leader_Framework.md

Phoenix_Scoring_Framework.md

Phoenix_Category_Framework.md

---

## Status

Approved

---

## D-023

Date:

2026-06-22

Title:

Orion Operating Architecture Established

Status:

Approved

---

### Context

As Orion evolved, the distinction between monitoring functions and portfolio management functions became increasingly important.

Initial architecture discussions treated Aurora, Moon, Supernova, and Phoenix as equivalent engines.

However, further analysis showed that Aurora serves a fundamentally different purpose.

---

### Decision

Orion shall be organized into:

* One Monitoring Layer
* Three Portfolio Engines

Architecture:

Aurora

↓

Market Context

↓

Investor Interpretation

↓

Moon / Supernova / Phoenix

↓

Portfolio Actions

---

Aurora is designated as Orion's Monitoring Layer.

Aurora provides:

* Market Regime
* Risk State
* Transition Risk
* Market Commentary

Aurora does not directly manage portfolios.

Aurora does not generate buy or sell instructions.

---

Moon is designated as the ETF Portfolio Engine.

Supernova is designated as the Equity Portfolio Engine.

Phoenix is designated as the Digital Asset Portfolio Engine.

Each portfolio engine remains independently governed.

---

### Consequences

Benefits:

* Clear separation of monitoring and execution responsibilities
* Simplified mental model
* Improved modularity
* Better alignment with actual portfolio structure

Risks:

* Portfolio engines may interpret Aurora differently
* Some overlap may remain during future framework evolution

---

### Reference Documents

* Orion_Operating_Architecture.md
* Orion_Technical_Architecture.md

---

## D-024

Orion shall maintain a centralized glossary.

The glossary defines standard terminology used across all Orion documentation.

Examples:

* OS
* Framework
* Engine
* Dashboard
* Strategy
* Signal
* State
* Regime

The glossary serves as the authoritative terminology reference for Orion OS.

Status: Approved

Date: 2026-06-21

---

## D-025

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


---
