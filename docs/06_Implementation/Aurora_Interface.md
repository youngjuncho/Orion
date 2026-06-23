# Aurora Interface Specification

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

---

# Purpose

Defines the operational interface for Aurora.

---

# Responsibilities

Aurora is responsible for:

* Market monitoring
* Regime classification
* Transition monitoring
* Risk assessment

Aurora does not manage portfolios.

---

# Inputs

Market Data

Economic Data

Indicator Data

---

# Core Objects

Indicator

IndicatorGroup

Regime

RiskState

---

# Indicator Interface

Required Fields

Name

Category

Value

Score

State

---

# Regime Interface

Required Fields

Regime

Score

Direction

Confidence

---

# Output Schema

Aurora Score

Current Regime

Regime Direction

Risk State

---

# Dashboard Consumers

Aurora Dashboard

Orion Dashboard

---

# CLI Consumers

orion aurora report

orion aurora regime

orion aurora indicators
