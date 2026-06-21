# Moon Governance Framework

Version: 1.0

Status: Active

Last Updated: 2026-06-21

---

# Purpose

This document defines the governance rules for the Moon tactical asset allocation engine.

Moon Governance determines:

* Which strategies may be included
* How strategies are documented
* How strategies are maintained
* How changes are approved

---

# Mission

Moon provides systematic tactical asset allocation signals.

Moon exists to answer a single question:

"What should be held right now?"

---

# Core Principles

## Research First

Moon does not create proprietary investment strategies.

Strategies must originate from:

* Academic research
* Published methodologies
* Publicly validated frameworks

---

## Original First

Original methodologies must be documented before Orion-specific modifications are introduced.

Research precedes implementation.

---

## Rules Over Opinions

Moon decisions must be driven by explicit rules.

Discretionary overrides are prohibited.

---

## Reproducibility

Given identical inputs, Moon must generate identical outputs.

Deterministic behavior is mandatory.

---

## Signal Integrity

Signal generation should preserve original research methodology whenever possible.

Execution convenience must not alter signal generation.

Principle:

Signal Integrity Has Priority Over Execution Convenience

---

# Strategy Lifecycle

Each Moon strategy progresses through the following stages.

---

## Stage 1

Research

Required Documents:

* Strategy_Research.md

Purpose:

Document original methodology.

Status:

Research

---

## Stage 2

Implementation

Required Documents:

* Strategy_Orion.md

Purpose:

Define Orion implementation details.

Status:

Draft

---

## Stage 3

Validation

Requirements:

* Historical verification
* Rule verification
* Reproducibility testing

Status:

Validation

---

## Stage 4

Production Candidate

Requirements:

* Research complete
* Implementation complete
* Validation complete

Status:

Candidate

---

## Stage 5

Production

Approved for Moon deployment.

Status:

Active

---

# Strategy Admission Rules

A strategy may be added to Moon only if:

1. Public methodology exists.
2. Research documentation exists.
3. Orion implementation documentation exists.
4. Rules can be reproduced programmatically.
5. Strategy contributes unique value.

---

# Strategy Removal Rules

A strategy may be removed if:

* Original methodology becomes unavailable.
* Strategy cannot be reproduced.
* Research foundation is invalidated.
* Governance approval is granted.

All removals must be recorded in:

Decision_Log.md

---

# Approved Strategy Families

Current Categories:

## Equity Momentum

* ADM

---

## Multi-Asset Tactical Allocation

* BAA
* VAA
* HAA

---

## Bond Tactical Allocation

* BDA

---

# Execution Mapping Policy

Moon distinguishes between:

Signal Assets

and

Execution Assets

Signal assets preserve research integrity.

Execution assets optimize:

* Cost
* Liquidity
* Tax efficiency

Reference:

Moon_Execution_Mapping.md

---

# Rebalancing Policy

Default Frequency:

Monthly

---

Evaluation Date:

Last Trading Day

---

Execution Date:

Next Trading Day

---

Manual Override:

Not Allowed

---

Forced Rebalance:

Not Allowed

---

# Data Governance

Approved Sources:

* Yahoo Finance

Candidate Sources:

* Stooq
* Alpha Vantage
* Polygon

Changes require governance review.

---

# Change Management

Material changes require:

1. Documentation Update
2. Decision Log Entry
3. Governance Approval

---

# Required Decision Log Events

The following changes require logging:

* Strategy addition
* Strategy removal
* Universe changes
* Momentum formula changes
* Rebalancing rule changes
* Execution mapping changes
* Data source changes

Reference:

Decision_Log.md

---

# Success Criteria

Moon succeeds when:

1. Signals are reproducible.
2. Strategies remain faithful to original research.
3. Monthly allocations can be generated automatically.
4. Governance history remains fully auditable.

---

# Related Documents

* Orion_IPS.md
* Orion_Technical_Architecture.md
* Moon_Strategy_Catalog.md
* Moon_Execution_Mapping.md
* Decision_Log.md
