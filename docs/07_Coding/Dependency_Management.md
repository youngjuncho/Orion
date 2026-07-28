# Dependency Management

Version: 1.0

Status: Active

Last Updated: 2026-07-28

Depends On:

* Python_Package_Structure.md
* Orion_Architecture.md
* Development_Principles.md

---

# Purpose

Defines dependency management rules for Orion OS.

The objective is to minimize coupling, simplify testing, and maintain a stable architecture.

---

# Design Principles

Dependencies should be:

* Explicit
* Minimal
* Stable
* Replaceable

External libraries should never dictate Orion architecture.

---

# Dependency Direction

Dependencies must always flow downward.

CLI

↓

Runtime

↓

Framework Engines

↓

Domain Models

↓

Infrastructure

Dependencies must never flow upward.

---

# Framework Independence

Frameworks are independent.

Moon must not import:

* Aurora
* Phoenix
* Supernova

Aurora must not import:

* Moon
* Phoenix
* Supernova

The same rule applies to every framework.

Shared functionality belongs in Services.

---

# External Libraries

Prefer mature libraries.

Avoid unnecessary dependencies.

Before adding a new dependency, verify:

* Active maintenance
* Documentation quality
* Community adoption
* License compatibility

---

# Approved Core Libraries

Examples

* pandas
* numpy
* pydantic
* PyYAML
* typer
* rich

Additional libraries require architectural review.

---

# Infrastructure Isolation

Infrastructure libraries should remain isolated.

Examples

Yahoo Finance

SQLite

Redis

Requests

These libraries should not appear inside domain models.

---

# Dependency Injection

Prefer dependency injection over direct object construction.

Example

Good

Runtime → DataService

Bad

Runtime → requests.get()

---

# Circular Dependencies

Circular imports are prohibited.

If circular dependencies appear:

* Move shared logic into Services.
* Introduce interfaces.
* Refactor responsibilities.

---

# Optional Dependencies

Optional functionality should remain optional.

Example

Plotting libraries should not be required for core execution.

---

# Version Management

Dependencies should be pinned.

Example

requirements.txt

or

pyproject.toml

Avoid floating major versions.

---

# Updating Dependencies

Before upgrading:

* Review release notes.
* Verify backward compatibility.
* Run the complete test suite.

---

# Security

Regularly review dependencies for known vulnerabilities.

Remove abandoned packages whenever possible.

---

# Related Documents

* Python_Package_Structure.md
* Orion_Runtime.md
* Development_Principles.md