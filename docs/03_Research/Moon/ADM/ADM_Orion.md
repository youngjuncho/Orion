# ADM Orion Implementation Specification

Version: 0.1

Status: Draft

Last Updated: 2026-06-14

Depends On:

* ADM_Research.md

---

# Purpose

This document defines the Orion-specific implementation of the ADM strategy.

While ADM_Research.md preserves the original Gary Antonacci methodology, this document specifies how ADM will be implemented within Orion OS.

---

# Implementation Principles

## Original First

The original ADM methodology remains the reference implementation.

---

## Practical Execution

The Orion implementation prioritizes:

* Simplicity
* ETF availability
* Low maintenance
* Monthly execution

---

# Orion ADM Universe

## Risk Assets

US Equity

Ticker:

VTI

Description:

US Total Stock Market

---

International Equity

Ticker:

VEU

Description:

FTSE All-World ex-US

---

## Defensive Asset

Primary Candidate

Ticker:

SGOV

Description:

0-3 Month US Treasury ETF

Backup Candidates:

* BIL
* SHY

Current Status:

Pending Final Approval

---

# Data Source

Primary Source

Yahoo Finance

Reason:

* Free
* Reliable
* Python ecosystem support

---

Backup Sources

* Stooq
* Alpha Vantage
* Polygon

Status:

Future Review

---

# Signal Calculation

## Evaluation Frequency

Monthly

---

## Evaluation Date

Last Trading Day

Example:

2026-06-30

---

## Execution Date

Next Trading Day

Example:

2026-07-01

---

# Momentum Calculation

Initial Orion Standard

Trailing 12-Month Return

Formula:

Current Price / Price 12 Months Ago - 1

Status:

Pending Validation

---

# State Model

## Risk On

Condition:

VTI selected

Output:

State:
Risk On

Asset:
VTI

---

## International Risk On

Condition:

VEU selected

Output:

State:
Risk On

Asset:
VEU

---

## Risk Off

Condition:

Defensive Asset selected

Output:

State:
Risk Off

Asset:
SGOV

---

# Moon Dashboard Output

Example

Strategy:
ADM

Current Asset:
VTI

State:
Risk On

Relative Momentum:
Positive

Absolute Momentum:
Positive

Rebalance Date:
2026-06-30

Next Action:
Hold

---

# CLI Output

Command

orion moon adm

Example

ADM

Current Asset: VTI

State: Risk On

Momentum: Positive

Next Rebalance: 2026-06-30

---

# Dashboard Score

ADM contributes to the Moon Dashboard.

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

Date

Selected Asset

Previous Asset

Signal

Momentum Values

---

# Future Enhancements

Potential Orion Variants

ADM-US

ADM-Global

ADM-Leveraged

ADM-Rotation

Status:

Research Only

Not Approved

---

# Known Open Issues

OI-001

Final defensive asset selection

Candidates:

* SGOV
* BIL
* SHY

Status:

Open

---

OI-002

Total return calculation methodology

Need verification against original research.

Status:

Open

---

OI-003

Dividend adjustment handling

Need validation.

Status:

Open

---

# Approval Status

Research:
Completed

Implementation:
Draft

Coding:
Not Started
