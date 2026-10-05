# Supernova Data Sources

Version: 1.1

Status: Draft

Last Updated: 2026-10-05

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

Reliable Secondary / Financial Data Sources

↓

Priority 3

Analytical Research Sources

↓

Priority 4

Contextual / Supplementary Sources

Source priority informs evidence quality; it does not mechanically determine a score. Material assessments should prefer primary evidence and use secondary or analytical sources when they add necessary context or peer comparison.

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

* Competitive moat
* Leadership position
* Growth quality
* Execution quality
* Business risks and capital allocation context

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

* Strategy and execution review
* Growth initiatives
* Competitive positioning

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

# Evidence Record Requirements

Each material source used in a Company Score review should be identifiable through:

* Source Type
* Source Name
* Reference / Locator
* Publication Date, when available
* Access Date, when relevant
* Relevant Period, when applicable

The source record supports traceability. The assessment remains a judgment supported by evidence rather than an automatic metric-to-score conversion.

---

# Supplementary Sources

## Reddit

Purpose:

Community monitoring.

Usage:

* Sentiment awareness
* Product adoption signals

Context only. Not used as a primary scoring basis.

Priority:

Low

---

## X (Twitter)

Purpose:

Industry awareness.

Usage:

* Early trend detection
* Industry discussion

Context only. Not used as a primary scoring basis.

Not used for scoring.

Priority:

Low

---

# Data Usage Mapping

Data sources support evidence collection and assessment. They do not mechanically generate Company Scores.

## Theme Evaluation

Primary inputs:

* Investor Relations
* Annual reports / company filings
* Earnings calls
* Industry reports

Use:

* Structural persistence
* Adoption
* Economic relevance
* Trend direction

Theme evidence is evaluated separately from Company Score evidence.

---

## Theme Exposure

Primary inputs:

* Investor Relations
* Annual reports / company filings
* Earnings calls
* Industry reports

Use:

* Directness of exposure to approved 5D themes
* Structural relevance
* Durability of the theme-company relationship

---

## Competitive Moat

Primary inputs:

* SEC filings
* Annual reports
* Investor presentations / investor days
* Industry reports

Supporting inputs:

* Koyfin
* Reliable analytical research

Use:

* Competitive advantage
* Switching costs
* Ecosystem effects
* Cost or scale advantages
* Durability versus peers

---

## Leadership Position

Primary inputs:

* Industry reports
* Company disclosures
* Investor presentations

Supporting inputs:

* Finviz
* Koyfin

Use:

* Category leadership
* Relative competitive position
* Challenger emergence
* Market or category share evidence

---

## Growth Quality

Primary inputs:

* SEC filings
* Annual reports
* Investor presentations
* Earnings calls

Supporting inputs:

* Yahoo Finance
* Macrotrends
* Koyfin

Use:

* Long-term growth durability
* Revenue and earnings trajectory
* Cash-flow quality
* Growth drivers and constraints

---

## Execution Quality

Primary inputs:

* SEC filings
* Annual reports
* Earnings calls
* Investor presentations

Use:

* Management execution
* Delivery against stated strategy
* Capital allocation
* Operational consistency

---

# Evidence Provenance Contract

Each material Company Score assessment should preserve enough provenance to allow a later reviewer to understand what supported the judgment.

Minimum provenance fields for a source reference are:

```text
Source Type
Source Name
Reference / Locator
```

Where available, the research record should also retain:

```text
Publication Date
Access Date
Relevant Period
```

`Reference / Locator` may be a filing identifier, report title, document section, or other stable locator. A raw URL may be retained when useful, but a URL alone is not considered an adequate description of the evidence.

Evidence records should distinguish the source from the analyst's Assessment. The source provides provenance; the Assessment explains why the source supports the assigned Score.

## Source Role

* **Primary** — company filings and official disclosures; preferred for material claims.
* **Secondary** — financial data providers and established industry research; used to corroborate or quantify evidence.
* **Analytical** — professional research and comparative analysis; useful for peer and category assessment.
* **Contextual** — market discussion and community sources; useful for awareness or hypothesis generation, but not sufficient by themselves for material scoring claims.

Contextual sources such as Reddit or X may inform research discovery but are not scoring evidence by themselves.

## 13F / Institutional Holdings

Institutional holdings data may be used as contextual evidence for investor positioning, ownership trends, or research prioritization. Because 13F data is delayed and does not directly establish operating performance or competitive advantage, it is not a standalone basis for Company Score, Leadership Role, or Portfolio State decisions.

---

## 13F / Institutional Holdings

Institutional holdings data may be used as contextual evidence for investor positioning, ownership trends, or research prioritization. Because 13F data is delayed and does not directly establish operating performance or competitive advantage, it is not a standalone basis for Company Score, Leadership Role, or Portfolio State decisions.

Usage:

* Observe changes in institutional holdings
* Provide supplementary context for leadership and market-interest research
* Support seasonality / positioning analysis when relevant

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
