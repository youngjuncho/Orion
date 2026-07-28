# Documentation Guidelines

Version: 1.0

Status: Active

Last Updated: 2026-07-28

Depends On:

* Development_Principles.md

---

# Purpose

Defines documentation standards for Orion OS.

Documentation should evolve together with the implementation.

---

# Philosophy

Documentation is part of the software.

Outdated documentation is considered a defect.

---

# Documentation Levels

Orion documentation is organized into:

* Vision
* Architecture
* Investment Framework
* Research
* Roadmap
* Decisions
* Implementation
* Coding

Each level has a distinct responsibility.

---

# Code Documentation

Public classes and functions should include docstrings.

Use Google Style docstrings.

---

# Markdown Style

Use Markdown for all project documentation.

Prefer:

* Short paragraphs
* Clear headings
* Bullet lists
* Tables where appropriate

---

# Version Header

Each document should include:

* Version
* Status
* Last Updated
* Depends On

---

# Change Management

Significant architectural changes should update:

* Related documents
* Decision Log
* Roadmap (if applicable)

---

# Naming

Document names should use PascalCase with underscores.

Examples:

Orion_Runtime.md

Moon_Engine.md

Phoenix_Pipeline.md

---

# Diagrams

Prefer simple text diagrams.

ASCII diagrams are acceptable.

Complex diagrams should be generated from source files when possible.

---

# Cross References

Reference related documents rather than duplicating content.

---

# Research Documents

Research documents preserve original methodologies.

Implementation documents define Orion-specific behavior.

The distinction should remain clear.

---

# Documentation Review

Before merging changes:

- Verify accuracy.
- Remove obsolete information.
- Update related references.
- Maintain consistent terminology.

---

# Related Documents

* Development_Principles.md
* Decision_Log.md