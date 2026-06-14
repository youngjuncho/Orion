# ADM Research Specification

Version: 0.1

Status: Research

Author: Orion OS

Last Updated: 2026-06-14

---

# Overview

ADM (Absolute Dual Momentum) is a rules-based investment strategy developed by Gary Antonacci.

The strategy combines:

1. Relative Momentum
2. Absolute Momentum

to improve risk-adjusted returns while reducing major drawdowns.

ADM is the foundational strategy selected for Moon v1.0 because of its simplicity, transparency, and extensive historical validation.

---

# Source Material

Primary Source:

Dual Momentum Investing

Author:

Gary Antonacci

Publication Year:

2014

Supporting Research:

* Relative Strength Strategies
* Absolute Momentum Research
* Risk Premia Harvesting Through Dual Momentum

---

# Research Objective

Determine whether investors should allocate capital to:

* US Equities
* International Equities
* Defensive Assets

based on relative and absolute momentum signals.

---

# Core Concepts

## Relative Momentum

Relative Momentum compares the performance of multiple risky assets.

The strongest-performing asset is selected.

Question:

Which risk asset has performed better?

---

## Absolute Momentum

Absolute Momentum evaluates whether the selected asset has generated positive performance relative to a risk-free alternative.

Question:

Is the selected asset strong enough to own?

---

# Original GEM Framework

GEM = Global Equities Momentum

The original implementation uses:

Risk Assets:

* US Equities
* International Equities

Defensive Asset:

* Cash or Treasury Bills

---

# Original Decision Process

Step 1

Compare:

US Equity Momentum

vs

International Equity Momentum

Winner:

Highest Momentum Asset

---

Step 2

Compare:

Winner Momentum

vs

Cash Return

If Winner > Cash

Invest in Winner

Else

Move to Defensive Asset

---

# Momentum Measurement

Original Methodology:

Trailing 12-Month Total Return

Lookback Window:

12 Months

Evaluation Frequency:

Monthly

---

# Rebalancing Rules

Evaluation Date:

Last trading day of each month

Execution Date:

Next trading day

Rebalancing Frequency:

Monthly

---

# Portfolio States

## State A

Risk On

Asset:

US Equity

Condition:

US Momentum > International Momentum

AND

US Momentum > Cash

---

## State B

Risk On

Asset:

International Equity

Condition:

International Momentum > US Momentum

AND

International Momentum > Cash

---

## State C

Risk Off

Asset:

Cash / Treasury

Condition:

Winner Momentum <= Cash

---

# Expected Benefits

Historical research suggests that ADM may provide:

* Higher risk-adjusted returns
* Lower drawdowns
* Reduced bear market exposure
* Simpler decision framework

---

# Known Limitations

## Limited Asset Universe

Original GEM uses only a small number of assets.

---

## Trend Following Risk

Momentum strategies may experience whipsaw periods.

---

## Tax Considerations

Monthly rebalancing may create taxable events.

---

## Implementation Differences

Results may vary depending on:

* ETF selection
* Data source
* Total return calculations
* Execution timing

---

# Research Questions

RQ-001

Should Orion implement the original GEM universe first?

Status:

Open

---

RQ-002

What is the preferred defensive asset?

Candidates:

* BIL
* SHY
* SGOV

Status:

Open

---

RQ-003

Should dividends be included in return calculations?

Status:

Open

---

# Research Conclusion

ADM is approved as the first Moon strategy for further implementation research.

The original methodology should be preserved before any Orion-specific modifications are introduced.

Principle:

Original First

Customization Later

---

# Next Document

ADM_Orion.md

Purpose:

Define Orion-specific implementation details while preserving the original ADM methodology.

