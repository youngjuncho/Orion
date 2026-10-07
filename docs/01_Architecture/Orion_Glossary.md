# Orion Glossary

Version: 1.1

Status: Approved

Last Updated: 2026-07-27

Depends On:

* Orion_Operating_Architecture.md
* Orion_Technical_Architecture.md

Reference:

* D-024
* D-025

---

# Purpose

This document defines the standard terminology used throughout Orion OS.

All Orion documentation should use these definitions consistently.

This glossary is the authoritative reference for terminology across all Orion frameworks.

---

# Architecture Terms

## Orion OS

The complete personal investment operating system.

Orion OS consists of four major investment frameworks:

* Aurora
* Moon
* Orbit
* Supernova
* Phoenix

---

## Framework

A major investment domain within Orion OS.

Each framework owns a distinct investment responsibility.

Current Frameworks:

* Aurora
* Moon
* Orbit
* Supernova
* Phoenix

---

## Engine

A calculation or analysis component within a framework.

Engines perform specific analytical tasks but do not define overall investment policy.

Examples:

* Aurora Trend Engine
* Aurora Liquidity Engine
* Moon Scoring Engine

---

## Strategy

A rules-based investment methodology executed within a framework.

Strategies generate investment signals according to predefined rules.

Examples:

* ADM
* BAA
* BDA
* HAA
* VAA

---

## Dashboard

A user-facing visualization layer.

Dashboards display framework outputs without changing investment decisions.

---

# Common Operating Terms

## State

The current operating condition of a framework or model.

A State describes the present condition only.

Examples:

Aurora

* Risk On
* Neutral
* Risk Off

Moon

* Risk On
* Risk Off

---

## Score

A normalized numerical assessment used to summarize current conditions.

Scores provide interpretation rather than prediction.

Typical Range:

0–100

Examples:

* Aurora Score
* Moon Strategy Score

---

## Portfolio

A collection of investable assets managed by a framework.

Examples:

* Moon ETF Portfolio
* Supernova Equity Portfolio
* Phoenix Digital Asset Portfolio

---

# Operating Architecture Terms

## Monitoring Framework

A framework that observes market conditions without directly managing portfolios.

Current Monitoring Framework:

* Aurora

---

## Portfolio Framework

A framework that manages investable assets according to predefined rules.

Current Portfolio Frameworks:

* Moon
* Supernova
* Phoenix

---

# Aurora Terms

## Regime

The current market environment determined by Aurora.

Examples:

* Risk On
* Neutral
* Risk Off

---

## State Momentum

The directional movement of the current regime.

Examples:

* Improving
* Stable
* Deteriorating

---

## Indicator

A measurable market input evaluated by Aurora.

Examples:

* Credit Spread
* Yield Curve
* VIX

---

## Core Indicator

An indicator that directly contributes to Aurora Score and Regime classification.

Examples:

* Trend
* Liquidity
* Credit
* Volatility

---

## Cross Asset Indicator

An indicator used for contextual confirmation.

Cross Asset Indicators do not directly affect Aurora Score.

Examples:

* Dollar Index
* Gold
* Oil
* Bitcoin

---

# Moon Terms

## Dynamic Asset Allocation

An investment methodology that adjusts portfolio allocation according to strategy signals.

---

## Consensus Allocation

The aggregation of multiple strategy outputs into a single portfolio allocation.

---

## Signal Asset

The reference asset used for research, signal generation, and backtesting.

Example:

SPY

---

## Execution Asset

The ETF used for real portfolio implementation.

Example:

SPYM

---

## Momentum State

The current momentum condition of a strategy.

Examples:

* Positive
* Negative

---

## Risk State

The current risk posture implied by a strategy.

Examples:

* Risk On
* Risk Off

---

## Rebalance

The process of adjusting portfolio holdings to match target allocations.

Moon default frequency:

Monthly

---

# Supernova Terms

## 5D Framework

The structural megatrend model used by Supernova.

Components:

* Decoupling
* Deglobalization
* Demographics
* Decarbonization
* Digital Transformation

---

## Theme

A long-term structural investment trend.

Themes originate from the 5D Framework.

---

## Watchlist

A curated list of approved and candidate companies.

---

## Approved Company

A company eligible for portfolio inclusion.

---

## Candidate Company

A company under evaluation.

---

# Phoenix Terms

## Category

A digital asset ecosystem grouping.

Examples:

* Smart Contract Platforms
* Oracle Networks
* AI Infrastructure
* Real World Assets

---

## Leader

The strongest approved project within a category.

---

## Challenger

The strongest competing project within a category.

---

## Watchlist Asset

A project monitored for future leadership potential.

---

## Leadership Transition

A change in category leadership.

Example:

SOL → SUI

---

## Core Digital Assets

Digital assets managed outside Phoenix.

Current Core Assets:

* BTC
* ETH

Reference:

D-021

---

# Governance Terms

## Approved

Authorized for production use.

---

## Candidate

Under evaluation.

---

## Retired

No longer actively used.

---

## Superseded

Replaced by a newer framework or decision.

---

## Decision Log

The authoritative record of major Orion decisions.

Location:

docs/05_Decisions/Decision_Log.md

---

# Future Terms

Additional terminology may be added as Orion OS evolves.

All terminology updates should be reflected in:

* Orion_Glossary.md
* Decision_Log.md

---

# Next Document

Moon_Current_Production.md