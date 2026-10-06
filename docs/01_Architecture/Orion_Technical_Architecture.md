# Orion Technical Architecture

## Purpose

This document defines the technical architecture of Orion OS.

Orion is designed as a modular Personal Investment Operating System consisting of independently testable frameworks that can operate through CLI and Web interfaces.

---

# System Overview

Orion OS consists of five Investment Frameworks. Aurora is a Monitoring / Market Environment Framework; Moon, Orbit, Supernova, and Phoenix are independently governed Investment Frameworks that manage portfolios.

```text
Orion OS

  Monitoring Framework
    Aurora

  Investment Frameworks
    Aurora      (Monitoring / Market Environment)
    Moon        (Dynamic Asset Allocation)
    Orbit       (Static Asset Allocation)
    Supernova   (Equity Satellite)
    Phoenix     (Digital Asset Satellite)
```

Aurora provides market context.

Moon, Supernova, and Phoenix provide portfolio intelligence.

Each framework is independently executable and independently testable.

Reference:

* D-023
* Orion_Operating_Architecture.md

---

# Design Principles

## Modular

Each framework and dashboard must be isolated from the others.

A failure in one module must not affect the operation of another module.

---

## Reproducible

All calculations must be deterministic.

Given the same inputs, Orion should produce the same outputs.

---

## Research Driven

Investment logic must originate from:

* Academic research
* Published methodologies
* Verifiable investment frameworks

Investment logic belongs in framework modules and shared core modules, not in dashboard modules.

---

## State Driven

The system reports states.

The system does not generate price predictions.

---

# Logical Architecture

```text
Data Layer
  -> Framework Engines
  -> Framework Results / State
  -> Orion Runtime
  -> Dashboard Presentation
  -> CLI / Web UI
```

Aurora provides market context and does not control the other Investment Frameworks.
Moon, Orbit, Supernova, and Phoenix are independently governed Investment Frameworks.

The term Engine denotes an implementation/runtime component and is not an investment-level architectural category.

---

# Directory Structure

```text
orion/
  docs/
  src/
    orion/
      cli/
      core/
      dashboard/
      frameworks/
        aurora/
        moon/
        phoenix/
        supernova/
      services/
    data/
  tests/
  config/
  requirements.txt
```

---

# Core Components

## Core

Shared system utilities.

Responsibilities:

* Configuration
* Logging
* Scoring models
* State models
* Shared utilities

---

## Data Layer

Responsibilities:

* Data collection
* Data normalization
* Data validation

The Data Layer must not contain investment logic.

---

## Framework Layer

Responsibilities:

* Framework execution
* Signal generation
* State generation
* Portfolio or monitoring outputs

Framework logic belongs inside:

* `src/orion/frameworks/moon`
* `src/orion/frameworks/aurora`
* `src/orion/frameworks/supernova`
* `src/orion/frameworks/phoenix`

---

## Common Portfolio Domain

The common Portfolio Domain is shared by Moon, Orbit, Supernova, and Phoenix.
It is independent of any one investment methodology.

```text
Portfolio
戍式式 PortfolioTarget
戍式式 PortfolioState
戌式式 Operations
    戍式式 Rebalance
    戍式式 Execution
    戌式式 Transfer
```

Custody/accounting state is represented separately:

```text
Portfolio
    ⊿
Account
戍式式 Position ⊥ Asset
戌式式 Cash
```

Current Portfolio Value and Current Allocation are derived from Position and Cash.
PortfolioTarget is the canonical source for desired allocation.

# Dashboard Layer

Responsibilities:

* Dashboard rendering
* Visualization
* Summary display
* Navigation
* Consumption of framework outputs

The Dashboard Layer is presentation-only.

Investment logic must not live inside dashboard modules.

Dashboard code belongs inside:

* `src/orion/dashboard`

---

# Moon Architecture

## Purpose

Dynamic Asset Allocation Framework.

---

## Inputs

Market prices

ETF prices

Historical returns

---

## Outputs

```text
Current Asset

Momentum State

Risk State

Next Rebalance Date
```

---

## Planned Strategies

* ADM
* BAA
* BDA
* HAA
* VAA

Each strategy must be implemented as an independent module.

---

# Aurora Architecture

## Purpose

Monitoring Framework.

Aurora monitors market climate and provides context.

Aurora does not manage portfolios.

---

## Inputs

Macroeconomic indicators

Liquidity indicators

Market risk indicators

---

## Outputs

```text
Aurora Score

Market Regime

Risk State

Transition Risk
```

---

# Supernova Architecture

## Purpose

Equity Satellite Framework for 5D Megatrend companies.

---

## Inputs

Company universe

5D classifications

Fundamental data

Moat indicators

---

## Outputs

```text
Theme Health

Leader Status

Replacement Risk

Accumulation Status
```

---

# Phoenix Architecture

## Purpose

Digital Asset Satellite Framework.

---

## Inputs

Market data

On-chain data

Flow data

Category classifications

---

## Outputs

```text
Phoenix Score

Category Leader

Trend Strength

Replacement Risk
```

---

# Scoring Engine

Framework engines and shared core utilities should use a common scoring framework.

Dashboards display resulting scores but do not calculate investment logic.

Range:

0-100

Bands:

90-100 Exceptional

80-89 Strong

70-79 Healthy

60-69 Stable

50-59 Neutral

40-49 Weak

30-39 Danger

0-29 Critical

---

# Data Sources

## Initial Sources

Moon

* Yahoo Finance

Aurora

* FRED
* Yahoo Finance

Supernova

* Public market data

Phoenix

* CoinGecko
* CryptoQuant
* Exchange APIs

---

# User Interfaces

## CLI

Examples:

```bash
orion moon

orion aurora

orion supernova

orion phoenix

orion dashboard
```

---

## Web Dashboard

Technology:

Streamlit

Future:

FastAPI

React

---

# Development Roadmap

Phase 1

Moon

Objective:

Monthly rebalancing engine

---

Phase 2

Aurora

Objective:

Market climate monitoring framework

---

Phase 3

Supernova

Objective:

5D megatrend equity engine

---

Phase 4

Phoenix

Objective:

Digital Asset Satellite Framework

---

Phase 5

AI Commentary

Objective:

Automated market summaries

---

Phase 6

Web Dashboard

Objective:

Unified investment operating system
