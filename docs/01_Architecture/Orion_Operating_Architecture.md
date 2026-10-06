# Orion Operating Architecture

Version: 1.0

Status: Approved

Last Updated: 2026-09-06

Depends On:

* Vision_Summary.md
* Orion_Technical_Architecture.md

---

# Purpose

This document defines the operational architecture of Orion OS.

While the Technical Architecture describes how Orion is implemented, the Operating Architecture describes how Orion organizes investment decisions and portfolio management.

---

# Core Principle

Orion is a Personal Investment Operating System.

Its purpose is not to predict markets.

Its purpose is to provide structured decision support across multiple asset classes.

---

# Architecture Overview

Orion consists of:

* One Monitoring / Market Environment Framework
* Four Portfolio Investment Frameworks

```text
                    Orion OS

                         │

          ┌──────────────┴──────────────┐
          │                             │

          ▼                             ▼

      Aurora                 Investment Frameworks

(Market Monitoring)                   │

                      ┌───────┬───────┬──────────┬─────────┐
                      │       │       │          │
                      ▼       ▼       ▼          ▼
                    Moon    Orbit  Supernova  Phoenix
                      │       │       │          │
                      ▼       ▼       ▼          ▼
                    Dynamic  Static  Equity     Digital
                     AA       AA    Satellite   Asset
```

---

# Monitoring Layer

## Aurora

Purpose:

Market Climate Monitoring

Aurora monitors:

* Liquidity
* Growth
* Inflation
* Credit
* Risk Appetite
* Trend Strength

Aurora does not manage portfolios.

Aurora does not generate buy or sell orders.

Aurora provides market context.

---

## Core Question

What is the current market environment?

---

## Outputs

* Aurora Score
* Market Regime
* Risk State
* Transition Risk
* Market Commentary

---

# Investment Frameworks

Each portfolio-producing Investment Framework manages its own Portfolio according to its own methodology.
Each framework operates independently. Engine is an implementation/runtime term, not an investment-level category.

---

## Moon

Purpose:

Dynamic Asset Allocation Framework

Asset Class:

Dynamic Asset Allocation Portfolio

---

### Core Question

What should be owned now?

---

### Outputs

* ETF Selection
* Asset Allocation
* Rebalance Signals
* Portfolio State

---

### Characteristics

* Tactical
* Trend Following
* Dynamic Asset Allocation

---

## Orbit

Purpose:

Static Asset Allocation Framework

Core Question

What is the target allocation for the static portfolio?

Characteristics

* Strategic
* Static target allocation
* Periodic rebalancing

Orbit is independent of Moon. Any Moon → Orbit asset movement is a Portfolio Transfer operation and does not represent a decision dependency.

---

## Supernova

Purpose:

Long-Term Equity Engine

Asset Class:

Individual Equities

---

### Core Question

Which companies are most likely to dominate the future?

---

### Outputs

* Approved Companies
* Watchlist
* Company Scores
* Theme Exposure

---

### Characteristics

* Long-Term Ownership
* Megatrend Focused
* Quality Compounders

---

## Phoenix

Purpose:

Digital Asset Leadership Engine

Asset Class:

Digital Assets

---

### Core Question

Which digital asset ecosystems are becoming leaders?

---

### Outputs

* Category Leaders
* Challengers
* Replacement Risk
* Leadership Trend

---

### Characteristics

* Category-Based
* Leadership Focused
* Replacement Driven

---

# Common Portfolio Domain

Portfolio management is modeled independently from the investment methodology.

```text
PortfolioTarget + PortfolioState
             ↓
       RebalancePlan
             ↓
       ExecutionOrder
```

A Transfer is a separate Portfolio Operation and is not a Rebalance.

```text
Source Portfolio → Transfer → Destination Portfolio
```

Portfolio State is derived from actual Position and Cash state. An overall portfolio view, when needed, is a derived aggregate view rather than a canonical source of truth.

---

# Portfolio Mapping

## Dynamic Asset Allocation Portfolio

Managed By:

Moon

Examples:

* Moon Production Portfolio
* ADM
* BAA
* HAA
* VAA
* BDA

---

## Equity Portfolio

Managed By:

Supernova

Examples:

* NVIDIA
* Microsoft
* ASML
* Eli Lilly

---

## Digital Asset Portfolio

Managed By:

Phoenix

Examples:

* SOL
* LINK
* TAO
* ONDO

Core assets:

* BTC
* ETH

remain outside Phoenix governance.

Reference:

D-021

---

# Relationship Between Engines

The engines are independent.

A change in one engine does not require changes in another engine.

Examples:

* Aurora Risk-Off does not automatically trigger Moon rebalancing.
* Aurora Risk-On does not automatically trigger Supernova purchases.
* Phoenix leader changes do not affect Moon allocation.

Each engine maintains independent governance.

---

# Role Of Aurora

Aurora serves as Orion's monitoring and interpretation layer.

Aurora provides context for investment decisions.

Aurora does not control the other Investment Frameworks.

Aurora informs.

Each Investment Framework decides within its own governance.

---

# Decision Flow

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

# Governance

Changes to:

* Engine responsibilities
* Asset ownership
* Portfolio boundaries
* Monitoring responsibilities

must be recorded in:

Decision_Log.md

before implementation.

---

# Future Architecture

Potential future modules:

* AI Commentary Engine
* Risk Engine
* Portfolio Analytics Engine
* Tax Optimization Engine

Status:

Research

---

# Relationship With Technical Architecture

Technical Architecture

Defines implementation structure.

Operating Architecture

Defines investment decision structure.

Both documents are required.

---

# Next Document

Orion_Glossary.md

Purpose:

Define shared terminology used across Orion OS.
