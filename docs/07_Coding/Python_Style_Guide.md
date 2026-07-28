# Python Style Guide

Version: 1.0

Status: Active

Last Updated: 2026-07-28

Depends On:

* Python_Package_Structure.md
* Development_Principles.md

---

# Purpose

This document defines the Python coding standards for Orion OS.

All implementation should follow these conventions to ensure consistency, readability, and maintainability.

---

# Design Philosophy

Code should prioritize:

* Readability
* Simplicity
* Explicitness
* Maintainability

Premature optimization should be avoided.

---

# Python Version

Minimum Version

Python 3.12

---

# Formatting

Use:

Black

Line Length:

88

---

# Import Order

Standard Library

↓

Third-Party Libraries

↓

Orion Packages

Example

```python
from dataclasses import dataclass

import pandas as pd

from orion.domain.state import State
```

---

# Type Hints

Always use type hints.

Good

```python
def calculate_score(data: list[float]) -> float:
```

Avoid

```python
def calculate_score(data):
```

---

# Dataclasses

Prefer dataclasses for domain models.

Example

```python
@dataclass(slots=True)
class Score:
    value: float
```

---

# Naming

Classes

PascalCase

Example

MoonEngine

---

Functions

snake_case

Example

calculate_score

---

Variables

snake_case

---

Constants

UPPER_CASE

---

Private Members

Leading underscore

Example

_cache

---

# Function Design

Functions should:

* Have one responsibility
* Remain short
* Avoid side effects when possible

Prefer returning values over mutating inputs.

---

# Exceptions

Raise specific exceptions.

Avoid

```python
except:
```

Prefer

```python
except ValueError:
```

---

# Logging

Use the Orion logging service.

Avoid print() in production code.

---

# Configuration

Configuration must not be hardcoded.

Load values through the configuration service.

---

# Domain Models

Domain models should remain independent of:

* pandas
* requests
* databases
* file systems

---

# Framework Independence

Moon should not import:

Aurora

Phoenix

Supernova

Framework communication should occur through shared services.

---

# Comments

Explain why.

Avoid comments that simply describe what the code already states.

Good

```python
# Monthly rebalancing follows the original ADM paper.
```

Avoid

```python
# Increment i
i += 1
```

---

# Docstrings

Public classes and functions should include docstrings.

Use Google Style.

Example

```python
def calculate_score(value: float) -> float:
    """Normalize score.

    Args:
        value: Raw score.

    Returns:
        Normalized score.
    """
```

---

# Testing

Every new module should include corresponding unit tests.

Tests should mirror the package structure.

---

# Dependency Rule

Dependencies should flow downward.

CLI

↓

Runtime

↓

Frameworks

↓

Domain

↓

Infrastructure

Never reverse this direction.

---

# Code Review Checklist

Before merging:

- Code passes formatting.
- Type hints added.
- Tests pass.
- Documentation updated.
- No hardcoded configuration.
- Logging added where appropriate.
- No duplicated logic.

---

# Related Documents

* Python_Package_Structure.md
* Orion_Runtime.md
* Orion_Domain_Model.md
* Development_Principles.md