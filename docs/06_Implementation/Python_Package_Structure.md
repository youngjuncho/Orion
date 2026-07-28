# Python Package Structure

Version: 1.0

Status: Draft

Last Updated: 2026-07-28

Depends On:

* Orion_Domain_Model.md
* Orion_Runtime.md
* Orion_Service_Model.md

---

# Purpose

Defines the standard Python package structure for Orion OS.

The package structure mirrors the Orion architecture to ensure consistency between documentation and implementation.

---

# Design Principles

The package structure should:

* Reflect the Orion architecture
* Separate domain logic from infrastructure
* Minimize framework coupling
* Support independent testing
* Support future extensibility

---

# Root Structure

```text
src/
└── orion/
```

---

# Package Layout

```text
src/orion/

├── core/
├── runtime/
├── domain/
├── services/
├── infrastructure/
├── frameworks/
├── dashboard/
├── cli/
├── config/
└── utils/
```

---

# Core

Shared abstractions and common types.

```text
core/

base.py
constants.py
exceptions.py
types.py
```

---

# Runtime

System execution.

```text
runtime/

runtime.py
scheduler.py
workflow.py
```

---

# Domain

Implementation of Orion_Domain_Model.

```text
domain/

framework.py
strategy.py
score.py
state.py
portfolio.py
review.py
event.py
```

---

# Services

Business services shared across frameworks.

```text
services/

configuration_service.py
event_service.py
review_service.py
dashboard_service.py
```

---

# Infrastructure

External integrations.

```text
infrastructure/

market_data/
storage/
logging/
cache/
```

---

# Frameworks

```text
frameworks/

aurora/
moon/
supernova/
phoenix/
```

---

# Aurora

```text
frameworks/aurora/

engine.py
pipeline.py
indicator.py
regime.py
scoring.py
```

---

# Moon

```text
frameworks/moon/

engine.py
pipeline.py
strategy.py
allocation.py
execution.py
```

---

# Supernova

```text
frameworks/supernova/

engine.py
pipeline.py
company.py
theme.py
watchlist.py
```

---

# Phoenix

```text
frameworks/phoenix/

engine.py
pipeline.py
category.py
leader.py
project.py
```

---

# Dashboard

Dashboard view models.

```text
dashboard/

cards.py
summary.py
reports.py
```

---

# CLI

Command-line interface.

```text
cli/

main.py
moon.py
aurora.py
supernova.py
phoenix.py
```

---

# Configuration

Configuration loading.

```text
config/

loader.py
schema.py
validation.py
```

---

# Utilities

Common helper functions.

```text
utils/

dates.py
math.py
serialization.py
```

---

# Testing

Tests mirror the package structure.

```text
tests/

core/
runtime/
domain/
frameworks/
services/
```

---

# Package Dependencies

```text
CLI
 │
 ▼
Runtime
 │
 ▼
Framework Engines
 │
 ▼
Domain Models
 │
 ▼
Infrastructure
```

Frameworks should never depend directly on each other.

Shared functionality should be implemented through Services.

---

# Related Documents

* Orion_Domain_Model.md
* Orion_Runtime.md
* Orion_Engine.md
* Orion_Service_Model.md