# Phoenix Operating Model

Version: 0.2

Status: Draft

Last Updated: 2026-10-05

Depends On:

* Phoenix_Research.md
* Phoenix_Category_Framework.md

---

# Purpose

Phoenix is the Digital Asset Leadership Framework of Orion OS.

Its purpose is to identify, monitor, and evaluate category leaders within the digital asset ecosystem.

Phoenix focuses on leadership transitions rather than short-term price movements.

---

# Scope

Phoenix manages approved altcoin category leaders.

Phoenix does not manage core digital assets.

Core Digital Assets:

* BTC
* ETH

Reference:

D-021

---

# Core Principle

Phoenix responds to leadership changes.

Phoenix does not respond to price changes alone.

---

# Operating Flow

Category

↓

Leader Identification

↓

Challenger Identification

↓

Replacement Risk Assessment

↓

Portfolio Review

↓

Rebalance Decision

---

# Leadership Model

Each category contains:

* Leader
* Primary Challenger
* Replacement Risk
* Leadership Trend

---

## Leader

The project currently holding the strongest ecosystem position.

Examples:

Oracle Networks

Leader:

LINK

---

AI Infrastructure

Leader:

TAO

---

Real World Assets

Leader:

ONDO

---

## Challenger

The strongest emerging competitor.

Examples:

AI Infrastructure

Leader:

TAO

Challenger:

RENDER

---

Smart Contract Platforms

Leader:

SOL

Challenger:

SUI

---

# Leadership States

Leadership State is derived from the canonical Replacement Risk mapping in Phoenix_Leader_Framework.md.

| Leadership State | Replacement Risk | Condition | Action |
|---|---|---|---|
| Dominant | Low | Score Gap 20+ | Hold |
| Stable | Medium | Score Gap 10–19 | Monitor |
| Competitive | High | Score Gap 0–9 | Review |
| Transition | Critical | Challenger exceeds Leader | Review Required |
| Disrupted | Critical | Promotion Rule satisfied; leadership replacement confirmed | Rebalance Candidate |

`Disrupted` is an event-confirmed state rather than a fifth score-gap band.

Price movement alone never changes Leadership State.

---

# Event Model

## Price Event

Examples:

* LINK +50%
* TAO -30%
* ONDO +80%

Action:

None

Price movement alone does not trigger review.

---

## Leadership Event

Examples:

* Challenger surpasses leader in key metrics
* Ecosystem adoption shifts
* Developer activity shifts
* Market share changes significantly

Action:

Review Required

---

## Replacement Event

Examples:

* Challenger becomes category leader
* Leadership transition confirmed

Action:

Rebalance Candidate

---

# Portfolio Model

Phoenix manages approved altcoin category leaders.

Core digital assets are excluded.

Reference:

D-021

---

## Portfolio Construction

Phoenix is category based.

Only approved category leaders are eligible for portfolio inclusion.

Challengers and watchlist assets are monitored for leadership evalution but are not eligible for portfolio inclusion.

Each approved category contributes one selected leader.

Example:

Smart Contract Platforms

Leader:

SOL

---

Oracle Networks

Leader:

LINK

---

AI Infrastructure

Leader:

TAO

---

Real World Assets

Leader:

ONDO

---

Example Portfolio

SOL

20%

LINK

20%

TAO

20%

ONDO

20%

TIA

20%

---

Allocation methodology:

Equal Weight

All approved category leaders receive equal portfolio weight.

Leadership changes may result in portfolio replacement during the next review cycle.

Version:

Initial Standard

Status:

Approved

Reference:

D-022

---

# Rebalancing Principle

Price appreciation alone shall not trigger rebalancing.

Price declines alone shall not trigger rebalancing.

Leadership changes and replacement risk events may trigger portfolio review and rebalancing.

Reference:

D-021

---

# Existing Capital Allocation

Initial Phoenix capital may be distributed equally among approved category leaders.

Example:

Phoenix Capital:

500,000 KRW

Approved Leaders:

* SOL
* LINK
* TAO
* ONDO
* TIA

Allocation:

* SOL = 20%
* LINK = 20%
* TAO = 20%
* ONDO = 20%
* TIA = 20%

---

# Review Frequency

Leadership Review

Monthly

---

Portfolio Review

Monthly

---

Category Review

Quarterly

---

Framework Review

Annually

---

# Rebalance Triggers

## Trigger A

Leader Replacement

Example:

SOL

↓

SUI

Action:

Rebalance

---

## Trigger B

Replacement Risk Escalation

Threshold:

Not Yet Defined

Action:

Review Required

---

## Trigger C

Category Removal

Action:

Rebalance

---

## Trigger D

New Approved Category

Action:

Portfolio Review

---

# Governance Rules

Portfolio changes require:

* Leadership review
* Category validation
* Decision log entry

before implementation.

---

# Open Issues

OI-501

Final leader selection methodology.

Status:

Closed

Resolution:

Leader selection is governed by the Phoenix Leader and Scoring Frameworks; current leadership state is recorded in the Approved Leaders Registry.

---

OI-502

Replacement Risk scoring framework.

Status:

Closed

Resolution:

The canonical score-gap and Leadership State mapping is defined in Phoenix_Leader_Framework.md.

---

OI-503

Leader evaluation metrics.

Status:

Open

---

OI-504

Category approval process.

Status:

Closed

Resolution:

Production eligibility is explicitly recorded per category in Phoenix_Category_Framework.md.

---

# Relationship With Core Digital Assets

Core Digital Assets are managed separately.

Default Core Allocation:

* BTC 60%
* ETH 40%

Reference:

D-021

Phoenix does not make allocation decisions regarding BTC or ETH.

---

# Next Document

Phoenix_Leader_Framework.md

Purpose:

Define leader selection methodology, challenger evaluation, replacement risk scoring, and leadership transition criteria.
