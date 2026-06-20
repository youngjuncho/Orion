# BDA Research Specification

Version: 1.0

Status: Research

Author:

Orion OS

Last Updated:

2026-06-20

---

# Overview

BDA (Bond Dynamic Allocation) is a tactical bond allocation framework.

The objective is to allocate capital among bond asset classes based on momentum and trend characteristics.

Unlike equity-focused momentum strategies, BDA operates primarily within a bond universe.

The strategy seeks to:

* Preserve capital
* Improve risk-adjusted returns
* Reduce duration-related risk
* Adapt to changing interest-rate environments

---

# Research Objective

Determine which bond assets should be held based on relative strength and trend conditions.

Primary Question:

Which bond asset class currently offers the strongest risk-adjusted opportunity?

---

# Core Concepts

## Relative Momentum

Compare bond asset classes against each other.

Question:

Which bond sector is strongest?

---

## Absolute Momentum

Evaluate whether the selected bond asset remains attractive relative to cash equivalents.

Question:

Should the selected bond asset be owned at all?

---

## Duration Rotation

Different bond categories react differently to changes in interest rates.

BDA attempts to allocate toward the most favorable duration profile.

---

# Candidate Bond Universe

## Cash Equivalents

Examples:

* BIL
* SGOV
* SHY

---

## Short Duration Bonds

Examples:

* VGSH
* SHY

---

## Intermediate Treasuries

Examples:

* IEF
* VGIT

---

## Long Treasuries

Examples:

* TLT
* VGLT

---

## Inflation Protected Bonds

Examples:

* TIP
* SCHP

---

## Investment Grade Corporate Bonds

Examples:

* LQD
* VCIT

---

## High Yield Bonds

Examples:

* HYG
* SPHY

---

## International Bonds

Examples:

* BWX
* BNDX

---

## Emerging Market Bonds

Examples:

* EMB
* VWOB

---

# Original Methodology

Status:

Research In Progress

The original methodology used in the current Python implementation requires documentation and validation.

---

# Momentum Measurement

Status:

Pending Validation

Potential Approaches:

* 1 Month
* 3 Month
* 6 Month
* 12 Month
* Weighted Momentum

Final methodology remains under review.

---

# Evaluation Frequency

Monthly

---

# Rebalancing Frequency

Monthly

---

# Expected Benefits

Historical research suggests that tactical bond allocation may provide:

* Better capital preservation
* Improved downside protection
* Reduced drawdowns
* Adaptive duration exposure

---

# Known Limitations

## Rising Rate Environments

Many bond assets may decline simultaneously.

---

## Correlation Shifts

Bond relationships can change across market regimes.

---

## Methodology Sensitivity

Results may vary significantly depending on:

* Asset universe
* Lookback periods
* Momentum calculations

---

# Research Questions

RQ-201

Identify the original source strategy for Orion BDA.

Possible candidates:

* Defensive Asset Allocation (DAA)
* Keller methodology
* Allocate Smartly implementation
* Kang Hwan-guk adaptation

Status:

Open

---

RQ-202

Final bond universe definition.

Status:

Open

---

RQ-203

Momentum formula.

Status:

Open

---

RQ-204

Cash equivalent definition.

Status:

Open

---

RQ-205

Relationship to other Moon strategies.

Status:

Open

---

# Research Conclusion

BDA is approved for further implementation research.

The existing Orion implementation must be documented and validated before any modifications are introduced.

Principle:

Document First

Modify Later

---

# Next Document

BDA_Orion.md

Purpose:

Define the Orion-specific implementation while preserving the validated methodology.
