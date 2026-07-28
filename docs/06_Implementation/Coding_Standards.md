# Orion Coding Standards

Version: 1.0

Status: Draft

Last Updated: 2026-07-28

Depends On:

* Orion_Domain_Model.md
* Orion_Runtime.md
* Orion_Service_Model.md
* Python_Package_Structure.md

---

# Purpose

This document defines the coding standards for Orion OS.

The objective is to ensure that all implementations are:

* Consistent
* Readable
* Testable
* Maintainable

These standards apply to all Python source code within Orion.

---

# General Principles

## Document First

Architecture and behavior should be documented before implementation.

---

## Simplicity First

Prefer simple, readable code over clever implementations.

Readability has priority over brevity.

---

## Single Responsibility

Each class should have one primary responsibility.

Each function should perform one task.

---

## Composition Over Inheritance

Prefer composition whenever possible.

Inheritance should only be used when a clear "is-a" relationship exists.

---

# Naming Conventions

## Packages

Lowercase.

Example:

```text
frameworks
services
runtime
```

---

## Modules

snake_case.

Example:

```text
configuration_service.py
moon_engine.py
```

---

## Classes

PascalCase.

Example:

```python
MoonEngine
AuroraPipeline
StrategyResult
```

---

## Functions

snake_case.

Example:

```python
run()
load_configuration()
calculate_score()
```

---

## Variables

snake_case.

Example:

```python
strategy_result
portfolio_state
current_regime
```

---

## Constants

UPPER_CASE.

Example:

```python
DEFAULT_LOOKBACK
MAX_RETRY
```

---

# Type Hints

All public methods should include type hints.

Example:

```python
def run(self) -> OrionResult:
    ...
```

---

# Dataclasses

Use dataclasses for immutable domain objects whenever practical.

Example:

```python
@dataclass(frozen=True)
class StrategyResult:
    ...
```

---

# Logging

Use the standard logging module.

Avoid print() in production code.

Log levels:

* DEBUG
* INFO
* WARNING
* ERROR
* CRITICAL

---

# Error Handling

Raise specific exceptions.

Avoid broad exception handling.

Preferred:

```python
raise ConfigurationError(...)
```

Avoid:

```python
raise Exception(...)
```

---

# Dependency Direction

Dependencies should follow the Orion architecture.

```text
CLI

↓

Runtime

↓

Framework Engines

↓

Domain Models

↓

Infrastructure
```

Frameworks should never import each other directly.

Shared functionality belongs in Services.

---

# Testing

Every Engine should have unit tests.

Every Pipeline should have integration tests.

Critical calculations should include regression tests.

---

# Documentation

Every public class should include a docstring.

Example:

```python
class MoonEngine:
    """Executes all Moon strategies and aggregates portfolio allocations."""
```

Complex algorithms should include explanatory comments.

Avoid redundant comments.

---

# Configuration

Configuration values should not be hardcoded.

Use the Configuration Service.

Example:

```python
config.get("moon.rebalance_frequency")
```

---

# State Management

Domain objects should remain immutable whenever possible.

Runtime state should be managed through Runtime Services.

---

# API Design

Public APIs should return domain objects.

Avoid returning dictionaries unless serialization is required.

Preferred:

```python
OrionResult
```

Avoid:

```python
dict
```

---

# Imports

Group imports in the following order:

1. Standard library
2. Third-party libraries
3. Orion packages

Example:

```python
from datetime import datetime

from pydantic import BaseModel

from orion.frameworks.moon.engine import MoonEngine
```

---

# Code Formatting

Formatting should follow:

* Black
* Ruff

Recommended line length:

88 characters

---

# Future Standards

Potential future additions:

* Async programming guidelines
* Database access conventions
* Plugin development guide
* REST API conventions

Status:

Research Only

Not Approved

---

# Related Documents

* Python_Package_Structure.md
* Orion_API.md
* Orion_Runtime.md
* Orion_Engine.md
* Orion_Service_Model.md