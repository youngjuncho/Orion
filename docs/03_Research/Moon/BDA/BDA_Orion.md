# BDA Orion Implementation Specification

Version: 0.1

Status: Draft

Last Updated: 2026-06-20

Depends On:

* BDA_Research.md

---

# Purpose

This document defines the Orion-specific implementation of the BDA strategy.

While BDA_Research.md documents the research foundation, this document specifies how BDA is implemented within Orion OS.

---

# Implementation Principles

## Document First

The current implementation must be documented before modifications are introduced.

---

## Preserve Existing Logic

The existing Orion implementation remains the baseline until validation is completed.

---

# Orion BDA Universe

## Cash Equivalents

Signal Assets:

* BIL

Execution Assets:

* SGOV

---

## Treasury Bonds

Signal Assets:

* IEF
* TLT

Execution Assets:

* VGIT
* VGLT

---

## Inflation-Protected Bonds

Signal Assets:

* TIP

Execution Assets:

* SCHP

---

## Investment Grade Bonds

Signal Assets:

* LQD

Execution Assets:

* VCIT

---

## High Yield Bonds

Signal Assets:

* HYG

Execution Assets:

* SPHY

---

## International Bonds

Signal Assets:

* BWX

Execution Assets:

* BNDX

---

## Emerging Market Bonds

Signal Assets:

* EMB

Execution Assets:

* VWOB

---

# Data Source

Primary Source

Yahoo Finance

Reason:

* Free
* Reliable
* Python ecosystem support

---

# Evaluation Frequency

Monthly

---

# Evaluation Date

Last Trading Day

---

# Execution Date

Next Trading Day

---

# Momentum Calculation

Current Status:

Pending validation.

The existing Orion implementation should be treated as the reference implementation until source methodology is identified.

Related Research Question:

RQ-201

---

# Asset Selection

Purpose:

Select the strongest bond asset based on momentum characteristics.

Current Selection Method:

Pending validation.

Status:

Open

---

# Signal Universe

Signal generation uses the original signal ETFs.

Examples:

* IEF
* TLT
* TIP
* LQD
* HYG
* EMB

Signal integrity has priority over execution convenience.

---

# Execution Universe

Execution follows:

docs/02_Investment_Framework/Moon_Execution_Mapping.md

Examples:

* IEF → VGIT
* TLT → VGLT
* TIP → SCHP
* EMB → VWOB

---

# State Model

## Risk On

Condition:

A bond asset is selected.

Output:

State:
Allocated

Asset:
Selected Bond ETF

---

## Defensive State

Condition:

Cash equivalent selected.

Output:

State:
Defensive

Asset:
SGOV

---

# Moon Dashboard Output

Example

Strategy:
BDA

Current Asset:
VGIT

State:
Allocated

Momentum:
Positive

Rebalance Date:
2026-06-30

Next Action:
Hold

---

# CLI Output

Command

orion moon bda

Example

BDA

Current Asset: VGIT

State: Allocated

Next Rebalance: 2026-06-30

---

# Dashboard Score

BDA contributes to the Moon Dashboard.

Score Calculation:

Not Yet Defined

Future Document:

Moon_Scoring_Framework.md

Status:

Pending

---

# Rebalancing Policy

Default Frequency

Monthly

---

Forced Rebalance

Not Allowed

---

Manual Override

Not Allowed

---

# Logging Requirements

Every rebalance event must store:

* Date
* Selected Asset
* Previous Asset
* Momentum Values

---

# Known Open Issues

OI-201

Original source strategy identification.

Status:

Open

---

OI-202

Final momentum methodology.

Status:

Open

---

OI-203

Final asset universe validation.

Status:

Open

---

# Approval Status

Research:
In Progress

Implementation:
Draft

Coding:
Not Started
