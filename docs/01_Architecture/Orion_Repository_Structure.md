# Orion Repository Structure

Version: 1.0

Status: Draft

Last Updated: 2026-07-26

Depends On:

* Orion_Operating_Architecture.md
* Orion_Technical_Architecture.md
* Orion_Domain_Model.md

---

# Purpose

This document defines the repository structure of Orion OS.

The objective is to ensure consistent implementation and maintainability.

---

# Repository Layout

```text
orion/
  docs/
  src/
  tests/
  config/
  data/
  logs/
  scripts/
  requirements.txt
  README.md
```

---

# Source Layout

```text
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
```

---

# src/orion/core

Shared functionality.

Examples:

* Configuration
* Logging
* Scoring
* Data Models
* Utilities

---

# src/data

Responsibilities:

* Collection
* Normalization
* Validation
* Storage

No investment logic permitted.

---

# src/orion/frameworks/moon

ETF portfolio engine.

Responsibilities:

* Strategy execution
* Consensus allocation
* Rebalancing calculations

---

# src/orion/frameworks/aurora

Monitoring engine.

Responsibilities:

* Indicator evaluation
* Regime classification
* Risk monitoring

---

# src/orion/frameworks/supernova

Equity portfolio engine.

Responsibilities:

* Theme evaluation
* Company scoring
* Replacement risk

---

# src/orion/frameworks/phoenix

Digital asset portfolio engine.

Responsibilities:

* Category evaluation
* Leader selection
* Challenger monitoring

---

# src/orion/dashboard

Responsibilities:

* Dashboard rendering
* Summary generation
* Visualization

Dashboard is presentation-only.

---

# src/orion/cli

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
