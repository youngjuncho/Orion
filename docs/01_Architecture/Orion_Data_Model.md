# 2026-10-07 Core Reconciliation Addendum

> **Current authority:** The Core Architecture baseline is `CORE-001` through `CORE-020`. Where the historical sections below use `Engine`, `Portfolio`, `State`, or `Event` semantics that differ from the current baseline, this addendum and the canonical documents listed here take precedence.
>
> Canonical references: `docs/05_Decisions/Core_Architecture_Decision_Baseline.md`, `Orion_Operating_Architecture.md`, `Orion_Technical_Architecture.md`, and `Orion_Domain_Model.md`.

Current canonical portfolio model:

```text
StrategyResult → ConsensusAllocation → PortfolioTarget → RebalancePlan → ExecutionOrder → ExecutionResult

PortfolioSnapshot = independent current portfolio state
RebalancePlan = derived from PortfolioTarget + PortfolioSnapshot
```

State is authoritative current domain state; `OrionStateSnapshot` is an immutable representation. Calculation results do not automatically become State.

---

# Orion Data Model

Version: 1.1

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Orion_Operating_Architecture.md
* Orion_Technical_Architecture.md
* Orion_Glossary.md
* Moon_Object_Model.md

---

# Purpose

This document defines the core logical data model used throughout Orion OS.

The objective is to provide a consistent object model across all Orion frameworks.

The logical data model serves as the bridge between research documentation and software implementation.

---

# Design Principles

Orion is state-driven.

Frameworks evaluate observable entities.

Entities produce normalized results.

Dashboards consume standardized outputs.

The system does not generate forecasts.

---

# Core Object Hierarchy

```text
Orion

└── Framework
      ├── Engine
      │     ├── Input
      │     ├── Result
      │     └── Score
      │
      └── Dashboard
```

---

# Framework

A major investment domain.

Examples:

- Aurora
- Moon
- Supernova
- Phoenix

---

## Framework Fields

- Name
- Version
- Status
- Description
- Last Updated

---

# Engine

An Engine performs calculations within a Framework.

Examples:

- Aurora Trend Engine
- Moon Strategy Engine
- Phoenix Scoring Engine

---

## Engine Fields

- Name
- Version
- Status

---

# Score

Represents a normalized evaluation.

Range:

0–100

---

## Score Bands

90–100

Exceptional

---

80–89

Strong

---

70–79

Healthy

---

60–69

Stable

---

50–59

Neutral

---

40–49

Weak

---

30–39

Danger

---

0–29

Critical

---

# State

Represents the current condition of an entity.

State values are framework-specific.

Examples:

Aurora

- Risk On
- Neutral
- Risk Off

Moon

- Risk On
- Risk Off
- Defensive
- Partial Defense

Supernova

- Approved
- Watch
- Review

Phoenix

- Leader
- Challenger
- Watchlist

---

# Moon Data Model

Moon follows the object model defined in:

Moon_Object_Model.md

---

## Strategy

Represents one tactical allocation methodology.

Fields:

- Name
- Version
- Status

Methods:

- load_data()
- calculate_signal()
- generate_result()

---

## StrategyResult

Represents the output of one strategy evaluation.

Fields:

- Strategy Name
- Evaluation Date
- State
- Selected Assets
- Target Weights
- Metrics

---

## Allocation

Represents normalized portfolio weights.

Fields:

- Asset
- Weight

---

## Portfolio

Represents the aggregated Moon portfolio.

Fields:

- Holdings
- Allocation
- Rebalance Date

---

# Aurora Data Model

Aurora evaluates market conditions.

---

## Indicator

Fields:

- Name
- Category
- Value
- Score
- State

---

## Component Score

Fields:

- Trend
- Liquidity
- Credit
- Volatility

---

## Regime

Fields:

- Score
- Regime
- State Momentum

---

# Supernova Data Model

---

## Theme

Fields:

- Name
- Score
- State

---

## Company

Fields:

- Ticker
- Name
- Theme
- Status
- Score

---

# Phoenix Data Model

---

## Category

Fields:

- Name
- Score
- State

---

## Asset

Fields:

- Ticker
- Category
- Status
- Score

---

## Leadership

Fields:

- Leader
- Challenger
- Replacement Risk

---

# Dashboard Model

All dashboards consume standardized objects.

---

## Dashboard Card

Fields:

- Entity Name
- Score
- State
- Last Updated

---

# Review Model

Every framework supports periodic reviews.

---

## Review Record

Fields:

- Date
- Framework
- Entity
- Review Type
- Outcome
- Notes

---

# Decision Model

Material architectural changes require governance.

---

## Decision Record

Fields:

- Decision ID
- Date
- Category
- Status
- Title
- Description

Reference:

Decision_Log.md

---

# Relationship With Implementation

Python classes should map directly to this logical data model whenever practical.

Logical model changes should be documented before implementation.

---

# Related Documents

* Moon_Object_Model.md
* Orion_Glossary.md
* Orion_Technical_Architecture.md
* Orion_Operating_Architecture.md
* Decision_Log.md