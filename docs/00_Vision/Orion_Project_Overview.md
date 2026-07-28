# Orion Project Context

Version: 1.0

Status: Active

Last Updated: 2026-07-28

---

# Purpose

This document provides a high-level overview of the Orion OS project.

It serves as the primary onboarding document for developers and AI assistants.

Anyone joining the project should read this document before contributing.

---

# What is Orion?

Orion OS is a personal investment operating system.

Its objective is not to predict markets.

Its objective is to organize investment decisions into a structured, transparent, and reproducible system.

Orion is designed as a long-term decision support platform rather than an automated trading system.

---

# Core Philosophy

Documentation First

Domain First

Architecture First

Original First

Implementation follows documentation.

Every major architectural decision should be documented before coding.

---

# Primary Frameworks

Orion consists of four major frameworks.

## Moon

Tactical Asset Allocation

Purpose:

Allocate capital using academically validated investment strategies.

Current Strategies:

* ADM
* BAA
* VAA
* HAA
* BDA

---

## Aurora

Market Regime Analysis

Purpose:

Evaluate market conditions using macro and technical indicators.

Output:

Market regime and indicator scores.

---

## Supernova

Equity Research

Purpose:

Evaluate companies based on long-term investment themes.

Output:

Approved companies, watchlists, and theme evaluations.

---

## Phoenix

Digital Asset Research

Purpose:

Evaluate blockchain sectors and digital assets.

Output:

Category leadership and candidate rankings.

---

# Repository Structure

The repository is organized into several layers.

```text
docs/
config/
src/
tests/
```

Documentation is the source of truth.

Python implementation follows the documentation.

---

# Documentation Structure

## 00_Vision

Project vision and long-term goals.

---

## 01_Architecture

Overall system architecture.

---

## 02_Investment_Framework

Production investment framework specifications.

---

## 03_Research

Research documents preserving original methodologies.

---

## 04_Roadmap

Long-term project evolution.

---

## 05_Decisions

Architectural decision records.

---

## 06_Implementation

Implementation specifications.

This directory bridges architecture and code.

---

# Current Project Status

Completed

* Vision
* Architecture
* Research Documentation
* Framework Specifications
* Interface Specifications
* Runtime Documentation
* Engine Documentation
* Pipeline Documentation
* Domain Model Documentation
* API Documentation
* Python Package Structure
* Migration Plan

Current Phase

Beginning Python implementation.

---

# Development Order

Implementation should proceed in the following order.

1. Domain Models
2. Services
3. Runtime
4. Infrastructure
5. Framework Engines
6. CLI
7. Dashboard
8. Production Release

---

# Coding Principles

Architecture defines implementation.

Domain models should remain framework-independent.

Frameworks should communicate through services.

Configuration should be externalized.

Business logic should never be hardcoded.

Every implementation should map back to the documented architecture.

---

# AI Collaboration Guidelines

AI assistants should follow these principles.

* Preserve documented architecture.
* Do not introduce undocumented architectural changes.
* Maintain consistency across documents.
* Prefer extending existing models rather than creating parallel structures.
* Keep implementation aligned with Orion documentation.

When proposing changes:

1. Update documentation first.
2. Review architectural impact.
3. Implement code.
4. Update tests.
5. Update implementation status.

---

# Current Priority

Priority A

* Python package migration
* Domain models
* Configuration system
* Runtime
* Service layer
* Moon Engine
* ADM implementation

Priority B

* Aurora
* Supernova
* Phoenix

Priority C

* REST API
* Web Dashboard
* Cloud deployment
* Automation

---

# Important Documents

Vision

* Vision_Summary.md

Architecture

* Orion_Operating_Architecture.md
* Orion_Technical_Architecture.md
* Orion_API.md

Implementation

* Implementation_Roadmap.md
* Orion_Runtime.md
* Orion_Service_Model.md
* Orion_Domain_Model.md
* Python_Package_Structure.md

Status

* Implementation_Status_Report.md

---

# Project Goal

The long-term objective is to build a maintainable, transparent, and extensible investment operating system.

Every design decision should support this objective.

Orion should remain understandable, reproducible, and evolvable over time.