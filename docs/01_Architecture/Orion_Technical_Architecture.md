# 2026-10-07 Core Reconciliation Addendum

> **Current authority:** The canonical application execution boundary is **Orion Runtime**. The historical ※Portfolio Engine§ wording below is superseded by `CORE-001` and `CORE-019`: Moon, Orbit, Supernova, and Phoenix are Portfolio / Investment Frameworks; their Engines are framework-internal.

Current package baseline:

```text
src/
戍式式 data/
戌式式 orion/
    戍式式 cli/
    戍式式 core/
    戍式式 dashboard/
    戍式式 frameworks/
    弛   戍式式 aurora/
    弛   戍式式 moon/
    弛   戍式式 phoenix/
    弛   戌式式 supernova/
    戌式式 services/
```

Current Core rule: Frameworks consume canonical `MarketDataSet` through `RuntimeContext`, return `FrameworkResult`, and do not directly mutate StateStore/EventStore or Dashboard state.

---

# Orion Technical Architecture

## Purpose

This document defines the technical architecture of Orion OS.

Orion is designed as a modular Personal Investment Operating System consisting of independently testable frameworks that can operate through CLI and Web interfaces.

---

# System Overview

Orion OS consists of five independently governed Frameworks. Aurora is the
market/environment monitoring Framework; Moon, Orbit, Supernova, and Phoenix
are portfolio/investment Frameworks. Framework Engines are implementation
modules inside their respective Frameworks.

```text
Orion OS

  Frameworks
    Aurora
    Moon
    Orbit
    Supernova
    Phoenix
```

Aurora provides market context. Moon and Orbit provide portfolio allocation
logic, while Supernova and Phoenix provide satellite investment intelligence.

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

Aurora is the Monitoring Framework. It provides market context and does not
control the other Frameworks. Moon, Orbit, Supernova, and Phoenix are
independently governed Frameworks; their Engines are framework-internal
calculation/analysis modules.

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
        orbit/
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

## Dashboard Layer

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

ETF Portfolio Engine.

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

Equity Portfolio Engine for 5D Megatrend companies.

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

Digital Asset Portfolio Engine.

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

Digital asset portfolio engine

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
