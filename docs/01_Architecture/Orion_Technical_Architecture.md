# Orion Technical Architecture

## Purpose

This document defines the technical architecture of Orion OS.

Orion is designed as a modular Personal Investment Operating System consisting of independent analytical engines that can operate through CLI and Web interfaces.

---

# System Overview

Orion OS consists of four primary engines.

```text
Orion

├── Moon
├── Aurora
├── Supernova
└── Phoenix
```

Each engine is independently executable and independently testable.

---

# Design Principles

## Modular

Each dashboard must be isolated from the others.

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

---

## State Driven

The system reports states.

The system does not generate price predictions.

---

# Logical Architecture

```text
Data Layer
     ↓
Research Engine
     ↓
Scoring Engine
     ↓
Dashboard Engine
     ↓
CLI / Web UI
```

---

# Directory Structure

```text
orion/

├── docs/
│
├── src/
│   ├── core/
│   ├── data/
│   ├── dashboards/
│   ├── cli/
│   └── tests/
│
├── config/
│
├── data/
│
└── requirements.txt
```

---

# Core Components

## Core

Shared system utilities.

Responsibilities:

* Configuration
* Logging
* Scoring
* State models

---

## Data Layer

Responsibilities:

* Data collection
* Data normalization
* Data validation

The Data Layer must not contain investment logic.

---

## Dashboard Layer

Responsibilities:

* Strategy execution
* Signal generation
* State generation

---

# Moon Architecture

## Purpose

Dynamic asset allocation engine.

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

Market climate engine.

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
```

---

# Supernova Architecture

## Purpose

5D Megatrend monitoring engine.

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

Digital asset ecosystem engine.

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

All dashboards should use a common scoring framework.

Range:

0–100

Bands:

90–100 Exceptional

80–89 Strong

70–79 Healthy

60–69 Stable

50–59 Neutral

40–49 Weak

30–39 Danger

0–29 Critical

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

Market climate engine

---

Phase 3

Supernova

Objective:

5D megatrend engine

---

Phase 4

Phoenix

Objective:

Digital asset ecosystem engine

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

```
```

