# Orion Dashboard Specification

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

Depends On:

* Aurora_Dashboard_Spec.md
* Moon_Current_Production.md
* Supernova_Dashboard_Spec.md
* Phoenix_Dashboard_Spec.md

---

# Purpose

This document defines the top-level dashboard of Orion OS.

---

# Dashboard Hierarchy

```text
Orion Dashboard

├── Portfolio Summary
├── Aurora Summary
├── Moon Summary
├── Supernova Summary
└── Phoenix Summary
```

---

# Portfolio Summary

Displays:

* Total Portfolio Value
* Portfolio Allocation
* Portfolio Change
* Last Update

---

# Aurora Summary

Displays:

* Market Regime
* Risk State
* Regime Direction
* Aurora Score

---

# Moon Summary

Displays:

* Active Strategies
* Consensus Allocation
* Current Holdings
* Next Rebalance Date

---

# Supernova Summary

Displays:

* Approved Companies
* Theme Health
* Leadership Status
* Replacement Risk

---

# Phoenix Summary

Displays:

* Categories
* Current Leaders
* Challenger Status
* Replacement Risk

---

# Navigation

Dashboard should allow navigation to:

* Aurora
* Moon
* Supernova
* Phoenix

Detailed dashboards remain independent.

---

# Initial Technology

Version 1:

Streamlit

---

# Future Technology

Potential migration:

* FastAPI
* React
* Mobile Dashboard

---

# Refresh Frequency

Dashboard refreshes when underlying framework data updates.

---

# Design Principle

Aurora provides context.

Moon, Supernova, and Phoenix provide portfolio intelligence.

Dashboard aggregates outputs but does not generate investment decisions.

---

# Relationship With Architecture

Dashboard is a presentation layer.

Investment logic must remain within framework engines.

---

# Next Document

Orion_Roadmap.md
