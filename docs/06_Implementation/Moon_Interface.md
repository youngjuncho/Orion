# Moon Interface Specification

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

---

# Purpose

Defines the operational interface for Moon.

---

# Responsibilities

Moon is responsible for:

* Strategy execution
* Signal generation
* Consensus allocation
* Rebalance recommendations

---

# Inputs

Market Data

ETF Prices

Strategy Configuration

---

# Core Objects

Strategy

StrategyResult

Allocation

Portfolio

---

# Strategy Interface

Required Fields:

Name

Version

Status

---

Required Methods

load_data()

calculate_signal()

generate_result()

---

# Strategy Result

Required Fields

Strategy Name

Signal Date

Selected Assets

Weights

---

# Consensus Allocation

Input:

Multiple Strategy Results

Output:

Normalized Portfolio Allocation

---

# Output Schema

Portfolio Allocation

Current Holdings

Next Rebalance Date

Strategy Summary

---

# Dashboard Consumers

Moon Dashboard

Orion Dashboard

---

# CLI Consumers

orion moon run

orion moon report

orion moon allocation
