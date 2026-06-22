# Supernova Data Sources

Version: 0.1

Status: Draft

Last Updated: 2026-06-22

Depends On:

* Supernova_Research.md
* Supernova_Scoring_Framework.md

---

# Purpose

This document defines the data sources used by Supernova.

The objective is to ensure consistent, transparent, and reproducible company evaluations.

---

# Design Principle

Supernova prioritizes:

* Reliable
* Public
* Repeatable
* Long-term focused

data sources.

Preference is given to primary sources whenever possible.

---

# Source Hierarchy

Priority 1

Primary Sources

↓

Priority 2

Financial Data Providers

↓

Priority 3

Research Sources

↓

Priority 4

Supplementary Sources

---

# Primary Sources

## SEC Filings

Purpose:

Official company disclosures.

Examples:

* 10-K
* 10-Q
* 8-K

Usage:

* Financial strength
* Management review
* Business risks
* Capital allocation

Priority:

Highest

---

## Investor Relations

Purpose:

Direct company communications.

Examples:

* Earnings presentations
* Annual reports
* Investor days

Usage:

* Strategy review
* Growth initiatives
* Management quality

Priority:

Highest

---

# Financial Data Providers

## Yahoo Finance

Purpose:

General financial data.

Usage:

* Revenue
* Earnings
* Market capitalization
* Historical prices

Priority:

High

---

## Macrotrends

Purpose:

Historical financial analysis.

Usage:

* Revenue trends
* EPS trends
* Cash flow trends

Priority:

High

---

## Finviz

Purpose:

Screening and market overview.

Usage:

* Initial discovery
* Sector analysis
* Market leadership review

Priority:

Medium

---

## Koyfin

Purpose:

Professional company analysis.

Usage:

* Multi-year financial review
* Competitive comparison
* Valuation review

Priority:

Medium

---

# Research Sources

## Earnings Calls

Purpose:

Management commentary.

Usage:

* Strategic direction
* Competitive positioning
* Capital allocation review

Priority:

Medium

---

## Industry Reports

Purpose:

Category analysis.

Usage:

* Market size
* Growth estimates
* Competitive landscape

Priority:

Medium

---

# Supplementary Sources

## Reddit

Purpose:

Community monitoring.

Usage:

* Sentiment awareness
* Product adoption signals

Not used for scoring.

Priority:

Low

---

## X (Twitter)

Purpose:

Industry awareness.

Usage:

* Early trend detection
* Industry discussion

Not used for scoring.

Priority:

Low

---

# Data Usage Mapping

Theme Alignment

Sources:

* Investor Relations
* Earnings Calls

---

Competitive Advantage

Sources:

* Annual Reports
* Industry Reports

---

Market Leadership

Sources:

* Industry Reports
* Finviz
* Koyfin

---

Growth Potential

Sources:

* Macrotrends
* Yahoo Finance

---

Financial Strength

Sources:

* SEC Filings
* Macrotrends

---

Management Quality

Sources:

* Earnings Calls
* Annual Reports

---

Strategic Relevance

Sources:

* Investor Presentations
* Industry Reports

---

# Governance Rules

New data sources may be added when:

* Reliability is verified
* Data quality is consistent
* Information is reproducible

Changes must be recorded in:

Decision_Log.md

before implementation.

---

# Known Open Issues

OI-641

Automated data collection architecture.

Status:

Open

---

OI-642

Future API integration.

Status:

Deferred

---

# Next Document

Supernova_Change_Log.md

Purpose:

Track framework evolution and research decisions.
