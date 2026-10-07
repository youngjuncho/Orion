# Python Package Structure

Version: 2.0

Status: Approved V1 Baseline

Last Updated: 2026-10-07

Depends On:

* Orion_Domain_Model.md
* Orion_Runtime.md
* Orion_Service_Model.md

---

# Purpose

This document describes the Python package layout currently implemented by
Orion. It separates the actual V1 scaffolding from packages reserved for
future evolution.

---

# Current Package Layout

```text
src/
  orion/
    __init__.py
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
    __init__.py
    contracts.py
```

The current implementation uses `src/orion/core` for shared contracts and
runtime-oriented in-memory infrastructure. Framework-specific investment
logic belongs under `src/orion/frameworks/<framework>`. The `src/data`
package contains normalized data contracts only and must not contain
investment logic.

The current data contracts are `MarketDataPoint` for one typed observation
and `MarketDataSet` for a duplicate-free batch with an `as_of` value. They
validate scalar value and metadata types and preserve immutable snapshots.
They do not define source adapters, freshness, missing-observation policy, or
market-data persistence.

---

# Current Responsibilities

| Package | Responsibility | Current status |
|---|---|---|
| `orion.core` | Configuration, domain contracts, runtime context, state/event stores, registries, API result contracts | Implemented scaffolding |
| `orion.frameworks.aurora` | Aurora models, engine and report entry point | Scaffold; scoring not finalized |
| `orion.frameworks.moon` | Moon models, ADM selection, consensus and execution mapping | Partial implementation |
| `orion.frameworks.supernova` | Supernova models, engine and report entry point | Scaffold; scoring not finalized |
| `orion.frameworks.phoenix` | Phoenix models, engine and report entry point | Scaffold; leadership rules not finalized |
| `orion.dashboard` | Read-only presentation models and renderer | Implemented presentation boundary |
| `orion.cli` | Command routing and report commands | Implemented routing |
| `orion.services` | In-memory service registry | Implemented registry only |
| `data` | Normalized observations and batches | Contracts only |

---

# Dependency Direction

```text
CLI / Dashboard
       |
       v
Orion Runtime / API Contracts
       |
       v
Framework Engines
       |
       v
Core Domain Contracts and Data Contracts
```

Framework packages must not depend directly on one another. Dashboard code
consumes framework or runtime results and does not calculate signals, scores,
states, allocations, or regimes.

---

# Future Package Evolution

The following packages are design targets, not requirements of the current
scaffolding:

```text
src/orion/
  runtime/
  domain/
  infrastructure/
  config/
  utils/
```

They may be introduced when the Runtime, persistence, source adapters, and
domain boundaries are specified well enough to justify the migration. The
current source tree must not be treated as incomplete merely because these
future packages do not yet exist.

---

# Testing Layout

Tests mirror the implemented package layout:

```text
tests/
  data/
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
```

---

# Related Documents

* Orion_Domain_Model.md
* Orion_Runtime.md
* Orion_Engine.md
* Orion_Service_Model.md
