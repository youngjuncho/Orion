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
      orbit/
      phoenix/
      supernova/
    services/
  data/
```

---

# src/orion/core

Shared functionality.

The core layer is the intended home for the common Portfolio Domain. The domain contract includes Portfolio, PortfolioTarget, PortfolioState, RebalancePlan, ExecutionOrder, Transfer, Asset, Position, Account, and Cash. Framework-specific concepts remain inside their respective framework packages.

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

Dynamic asset allocation framework implementation.

Responsibilities:

* Strategy execution
* Consensus allocation
* Rebalancing calculations

---

# src/orion/frameworks/orbit

Static asset allocation framework implementation.

Responsibilities:

* Maintain strategic target allocation
* Produce rebalance inputs
* Represent Orbit-specific configuration and state

Orbit implementation is a planned extension; this directory is not yet required to exist in the current runtime.

---

# src/orion/frameworks/aurora

Monitoring framework implementation.

Responsibilities:

* Indicator evaluation
* Regime classification
* Risk monitoring

---

# src/orion/frameworks/supernova

Equity satellite framework implementation.

Responsibilities:

* Theme evaluation
* Company scoring
* Replacement risk

---

# src/orion/frameworks/phoenix

Digital asset satellite framework implementation.

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
