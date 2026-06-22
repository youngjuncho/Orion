# Supernova Dashboard Specification

Version: 0.1

Status: Draft

Last Updated: 2026-06-22

Depends On:

* Supernova_Research.md
* Supernova_Theme_Framework.md
* Supernova_Watchlist_Framework.md
* Supernova_Scoring_Framework.md

---

# Purpose

This document defines the dashboard structure used by Supernova.

The dashboard provides visibility into:

* Theme exposure
* Company quality
* Watchlist status
* Portfolio composition
* Review requirements

---

# Dashboard Objectives

The dashboard should answer:

1. Which themes are represented?
2. Which companies are approved?
3. Which companies require review?
4. Which candidates may be promoted?
5. Which companies may be removed?
6. How concentrated is the portfolio?

---

# Section 1

Theme Overview

Purpose:

Monitor exposure to Orion 5D themes.

Fields:

| Theme                  | Status | Approved Companies |
| ---------------------- | ------ | ------------------ |
| Decoupling             | Active | 3                  |
| Deglobalization        | Active | 2                  |
| Demographics           | Active | 2                  |
| Decarbonization        | Active | 3                  |
| Digital Transformation | Active | 5                  |

---

# Section 2

Approved Companies

Purpose:

Display current Supernova accumulation candidates.

Fields:

| Company   | Theme                  | Score | Status   |
| --------- | ---------------------- | ----- | -------- |
| NVIDIA    | Digital Transformation | 68    | Approved |
| Microsoft | Digital Transformation | 66    | Approved |
| ASML      | Digital Transformation | 64    | Approved |
| Eli Lilly | Demographics           | 62    | Approved |

---

# Section 3

Candidate Companies

Purpose:

Monitor potential future additions.

Fields:

| Company     | Theme                  | Score | Status    |
| ----------- | ---------------------- | ----- | --------- |
| AMD         | Digital Transformation | 58    | Candidate |
| CrowdStrike | Digital Transformation | 57    | Candidate |
| ServiceNow  | Digital Transformation | 56    | Candidate |

---

# Section 4

Watchlist Companies

Purpose:

Monitor early-stage opportunities.

Fields:

| Company    | Theme        | Score |
| ---------- | ------------ | ----- |
| Rocket Lab | Decoupling   | 45    |
| Tempus AI  | Demographics | 44    |

---

# Section 5

Review Required

Purpose:

Identify companies requiring reassessment.

Fields:

| Company         | Previous Score | Current Score | Status          |
| --------------- | -------------- | ------------- | --------------- |
| Example Company | 61             | 39            | Review Required |

---

# Section 6

Theme Distribution

Purpose:

Measure portfolio diversification across themes.

Fields:

| Theme                  | Companies | Weight |
| ---------------------- | --------- | ------ |
| Digital Transformation | 4         | 40%    |
| Decarbonization        | 2         | 20%    |
| Demographics           | 2         | 20%    |
| Decoupling             | 1         | 10%    |
| Deglobalization        | 1         | 10%    |

---

# Section 7

Promotion Candidates

Purpose:

Track companies nearing Approved status.

Criteria:

Score ≥ 55

Fields:

| Company    | Theme                  | Score |
| ---------- | ---------------------- | ----- |
| AMD        | Digital Transformation | 58    |
| ServiceNow | Digital Transformation | 57    |

---

# Section 8

Removal Candidates

Purpose:

Track companies at risk of removal.

Criteria:

Score < 40

Fields:

| Company         | Theme         | Score |
| --------------- | ------------- | ----- |
| Example Company | Example Theme | 35    |

---

# Section 9

Portfolio Summary

Purpose:

Provide high-level framework status.

Metrics:

Approved Companies

Candidate Companies

Watchlist Companies

Average Score

Highest Score

Lowest Score

Theme Coverage

Last Review Date

---

# Review Frequency

Dashboard Update

Monthly

---

Theme Review

Quarterly

---

Framework Review

Annually

---

# Future Enhancements

Potential additions:

* Revenue Growth Trends
* Earnings Revision Tracking
* Analyst Estimate Trends
* Insider Ownership Tracking
* Capital Allocation Metrics

Status:

Research

---

# Next Document

Supernova_Data_Sources.md

Purpose:

Define data providers, company information sources, and scoring inputs used by Supernova.
