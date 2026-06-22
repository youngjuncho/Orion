# Orion Glossary

Version: 1.0

Status: Approved

Last Updated: 2026-06-22

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

---

# Architecture Terms

## Orion OS

The complete personal investment operating system.

Orion consists of:

* Aurora
* Moon
* Supernova
* Phoenix

---

## Framework

A major investment domain within Orion.

Examples:

* Aurora
* Moon
* Supernova
* Phoenix

---

## Engine

A calculation or analysis component within a framework.

Examples:

* Aurora Trend Engine
* Aurora Liquidity Engine
* Moon Scoring Engine

---

## Strategy

A rules-based investment methodology.

Examples:

* ADM
* BAA
* BDA
* HAA
* VAA

---

## Dashboard

A user-facing visualization layer.

Dashboards present framework outputs.

---

# Operating Architecture Terms

## Monitoring Layer

A framework that provides market context but does not directly manage portfolios.

Current Monitoring Layer:

* Aurora

---

## Portfolio Engine

A framework that manages a specific asset class portfolio.

Current Portfolio Engines:

* Moon
* Supernova
* Phoenix

---

## Portfolio

A collection of investable assets managed under a framework.

Examples:

* Moon ETF Portfolio
* Supernova Equity Portfolio
* Phoenix Digital Asset Portfolio

---

# Aurora Terms

## Regime

The current market environment.

Examples:

* Risk-On
* Risk-Off
* Neutral

---

## Transition

The directional movement of a regime.

Examples:

* Improving
* Stable
* Deteriorating

---

## Indicator

A measurable input used by Aurora.

Examples:

* Credit Spread
* Yield Curve
* VIX

---

## Core Indicator

An indicator used directly in regime determination.

---

## Cross Asset Indicator

An indicator used for contextual analysis.

Examples:

* Gold
* Oil
* Bitcoin
* Dollar Index

---

# Moon Terms

## Dynamic Asset Allocation

An allocation methodology that changes portfolio weights based on market conditions.

---

## Consensus Allocation

The aggregation of multiple strategy outputs into a single portfolio allocation.

---

## Signal Asset

The asset used for strategy calculations.

Example:

SPY

---

## Execution Asset

The asset actually purchased.

Example:

SPYM

---

## Rebalance

The process of adjusting portfolio allocations.

Moon default frequency:

Monthly

---

# Supernova Terms

## 5D Framework

The megatrend model used by Supernova.

Components:

* Decoupling
* Deglobalization
* Demographics
* Decarbonization
* Digital Transformation

---

## Theme

A long-term structural trend.

Themes originate from the 5D Framework.

---

## Watchlist

A curated list of approved and candidate companies.

---

## Approved Company

A company eligible for portfolio inclusion.

---

## Candidate Company

A company under evaluation for future approval.

---

## Replacement Risk

The probability that an approved company loses leadership status.

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

The strongest project within a category.

Leaders are eligible for portfolio inclusion.

---

## Challenger

The strongest competitor to the current leader.

Challengers are monitored but not held.

---

## Watchlist Asset

A project being monitored for future leadership potential.

---

## Leadership Transition

A change in category leadership.

Example:

SOL → SUI

---

## Replacement Risk

The probability that a challenger replaces the current leader.

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

Active and authorized for production use.

---

## Candidate

Under evaluation and not yet approved.

---

## Retired

No longer actively used.

---

## Superseded

Replaced by a newer decision or framework.

---

## Decision Log

The authoritative record of major Orion decisions.

Location:

docs/05_Decisions/Decision_Log.md

---

# Future Terms

Additional terms may be added as Orion evolves.

All terminology changes should be reflected in:

* Orion_Glossary.md
* Decision_Log.md

---

# Next Document

None

This document serves as a shared reference for all Orion frameworks.
