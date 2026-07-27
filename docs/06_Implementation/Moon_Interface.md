# Moon Interface Specification

Version: 1.1

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Moon_Current_Production.md
* Moon_Execution_Mapping.md

---

# Purpose

This document defines the operational interface for Moon.

It specifies the common contract that all Moon strategies must implement.

The objective is to ensure consistent strategy execution, portfolio aggregation, and portfolio construction.

---

# Responsibilities

Moon is responsible for:

* Strategy execution
* Signal generation
* Strategy result generation
* Consensus allocation
* Execution asset translation
* Portfolio construction
* Rebalance recommendation

---

# Inputs

Moon consumes the following inputs:

* Market Data
* ETF Prices
* Strategy Configuration

---

# Core Objects

Moon uses the following core objects:

* Strategy
* StrategyResult
* ConsensusAllocation
* PortfolioAllocation

---

# Strategy Interface

Every Moon strategy must implement the following interface.

---

## Required Fields

Name

Version

Status

---

## Required Methods

load_data()

calculate_signal()

generate_result()

---

# Strategy Result

A StrategyResult represents the output of a single strategy.

---

## Required Fields

Strategy Name

Signal Date

Selected Assets

Asset Weights

Signal State

---

Example

Strategy:

ADM

Signal Date:

2026-06-30

Selected Assets:

* SPY

Asset Weights:

* SPY = 100%

Signal State:

Risk On

---

# Consensus Allocation

Moon combines multiple Strategy Results into a unified allocation.

Input:

Multiple Strategy Results

Output:

Consensus Allocation

Rules:

* Equal Strategy Weighting
* Equal Asset Weighting within each Strategy
* Automatic aggregation of overlapping assets

---

# Execution Mapping

Consensus Allocation is generated using Signal Assets.

Before portfolio construction, Signal Assets are translated into Execution Assets.

Translation rules are defined in:

Moon_Execution_Mapping.md

Signal Assets remain the canonical reference for research and validation.

---

# Portfolio Allocation

Portfolio Allocation represents the final target portfolio after execution mapping.

Required Fields:

Execution Assets

Target Weights

Signal Date

Next Rebalance Date

---

# Output Schema

Moon produces the following outputs:

* Strategy Results
* Consensus Allocation
* Portfolio Allocation
* Current Holdings
* Next Rebalance Date
* Strategy Summary

---

# Dashboard Consumers

The following dashboards consume Moon outputs:

* Moon Dashboard
* Orion Dashboard

---

# CLI Consumers

Moon provides the following CLI commands:

orion moon run

orion moon report

orion moon allocation

---

# Related Documents

* Moon_Current_Production.md
* Moon_Execution_Mapping.md
* Moon_Scoring_Framework.md
* ADM_Orion.md
* Orion_Glossary.md