# Orion Repository Structure

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

Depends On:

* Orion_Operating_Architecture.md
* Orion_Technical_Architecture.md
* Orion_Data_Model.md

---

# Purpose

This document defines the repository structure of Orion OS.

The objective is to ensure consistent implementation and maintainability.

---

# Repository Layout

```text
orion/

├── docs/
├── src/
├── tests/
├── config/
├── data/
├── logs/
├── scripts/
├── requirements.txt
└── README.md
```

---

# Source Layout

```text
src/

├── core/
├── data/
├── moon/
├── aurora/
├── supernova/
├── phoenix/
├── dashboard/
└── cli/
```

---

# Core

Shared functionality.

Examples:

* Configuration
* Logging
* Scoring
* Data Models
* Utilities

---

# Data

Responsibilities:

* Collection
* Normalization
* Validation
* Storage

No investment logic permitted.

---

# Moon

ETF portfolio engine.

Responsibilities:

* Strategy execution
* Consensus allocation
* Rebalancing calculations

---

# Aurora

Monitoring engine.

Responsibilities:

* Indicator evaluation
* Regime classification
* Risk monitoring

---

# Supernova

Equity portfolio engine.

Responsibilities:

* Theme evaluation
* Company scoring
* Replacement risk

---

# Phoenix

Digital asset portfolio engine.

Responsibilities:

* Category evaluation
* Leader selection
* Challenger monitoring

---

# Dashboard

Responsibilities:

* Dashboard rendering
* Summary generation
* Visualization

---

# CLI

Responsibilities:

* Command routing
* Reporting
* Operational workflows

---

# Tests

Mirror source structure whenever possible.

---

# Future Extensions

Potential additions:

* api/
* database/
* ai/
* notifications/

---

# Next Document

Orion_Data_Pipeline.md
