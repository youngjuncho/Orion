# Supernova Watchlist Framework

Version: 1.0

Status: Approved

Last Updated: 2026-10-05

Depends On:

* Supernova_Research.md
* Supernova_Theme_Framework.md

---

# Purpose

This document defines how companies are added, evaluated, promoted, and removed within Supernova.

The watchlist represents the approved universe of companies eligible for Supernova accumulation.

---

# Design Principle

Supernova does not attempt to own every promising company.

The objective is to maintain a curated list of exceptional businesses with long-term exposure to Orion's 5D themes.

Principle:

Quality Over Quantity

---

# Evaluation Structure

Megatrend

↓

Theme

↓

Company Evaluation

↓

Portfolio State + Leadership Role

---

# Company Governance Model

Portfolio State and Leadership Role are separate dimensions.

## Portfolio State

Each company receives one of the following portfolio states.

---

## Approved

Eligible for accumulation.

Companies meeting Supernova quality standards.

Action:

Buy

Hold

---

## Candidate

Under evaluation.

Not eligible for accumulation.

Action:

Monitor

---

## Watchlist

Early-stage monitoring.

Insufficient evidence for promotion.

Action:

Observe

---

## Review Required

Company fundamentals require reassessment.

Action:

Review

---

## Retired

No longer eligible for portfolio inclusion.

Action:

Do Not Buy

---

## Leadership Role

Leadership Role is independent of Portfolio State.

* Leader
* Challenger
* Candidate

Example:

```text
NVDA → Approved + Leader
AMD  → Watchlist + Challenger
```

A Leadership Role does not itself make a company portfolio eligible.

---

# Approved Companies

Approved companies represent the highest-conviction opportunities currently identified by the framework.

Characteristics:

* Strong moat
* Category leadership
* Long-term earnings growth
* Strategic relevance
* 5D alignment

---

# Candidate Companies

Candidate companies are emerging leaders or improving businesses.

Characteristics:

* Strong growth
* Improving competitive position
* Potential future leadership

---

# Watchlist Companies

Watchlist companies are monitored for future promotion.

Characteristics:

* Theme exposure exists
* Evidence remains incomplete
* Competitive position uncertain

---

# Promotion Rules

Promotion is based on explicit eligibility criteria and documented research evidence. Company Score informs the decision but does not automatically trigger promotion.

Minimum Approved eligibility:

* Clear relationship to at least one approved 5D theme
* Theme remains structurally valid
* Competitive position is sufficient
* Long-term growth thesis is credible
* No core thesis disproof
* Rational portfolio-level reason for inclusion relative to the current Approved Universe
* Evidence is recorded
* Governance approval is documented

Promotion Path:

Candidate

↓ Research Qualification

Watchlist

↓ Governance Approval

Approved

---

# Removal Rules

Candidate or Watchlist companies may be retired when:

* Theme relevance is materially lost
* Long-term thesis is invalidated
* Competitive position deteriorates materially
* Evidence is insufficient and research priority is no longer justified

Approved companies enter `Review Required` before a final Retirement decision except in an explicitly documented Emergency Review.

Short-term price movement alone does not trigger removal.

Removal decisions should be documented in Decision_Log.md.

---

# Portfolio Eligibility

Only Approved companies are eligible for accumulation.

Candidates and Watchlist companies are not eligible for portfolio inclusion.

---

# Position Philosophy

Supernova assumes long-term ownership.

Temporary price declines do not trigger removal.

Market volatility does not trigger removal.

Valuation compression alone does not trigger removal.

Business deterioration is required.

---

# Review Frequency

Company Review

Monthly

---

Watchlist Review

Quarterly

---

Framework Review

Annually

---

# Governance Rules

Changes to company status require:

* Theme review
* Company review
* Documentation

before implementation.

---

# Resolved Governance Issues

OI-621 — Resolved by D-038. Company scoring uses the approved 5-dimension framework with qualitative anchors and evidence.

OI-622 — Resolved by D-042. Promotion uses explicit eligibility criteria and governance approval rather than a hard numeric threshold.

OI-623 — Resolved by D-042. Removal uses structural criteria and governance review rather than a hard numeric threshold.

OI-624 — Consolidated with OI-704 and resolved as an explicit governance gap by D-039: no hard maximum is set in v1.

---

# Next Document

Supernova Scoring Framework

Purpose:

Define company scoring methodology and approval thresholds.
