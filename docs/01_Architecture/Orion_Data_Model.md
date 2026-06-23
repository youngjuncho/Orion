# Orion Data Model

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

Depends On:

* Orion_Operating_Architecture.md
* Orion_Technical_Architecture.md
* Orion_Glossary.md

---

# Purpose

This document defines the core logical data model used throughout Orion OS.

The objective is to provide a consistent structure across:

* Moon
* Aurora
* Supernova
* Phoenix

The data model serves as the bridge between research frameworks and software implementation.

---

# Design Principles

Orion is state-driven.

Orion evaluates entities and reports states.

The system does not generate forecasts.

---

# Core Entity Hierarchy

Orion

↓

Framework

↓

Engine

↓

Entity

↓

Score

↓

State

---

# Framework

A major investment domain.

Examples:

* Moon
* Aurora
* Supernova
* Phoenix

---

## Framework Fields

Name

Description

Status

Version

Last Updated

---

# Score

Represents a normalized evaluation.

Range:

0–100

---

## Score Bands

90–100

Exceptional

---

80–89

Strong

---

70–79

Healthy

---

60–69

Stable

---

50–59

Neutral

---

40–49

Weak

---

30–39

Danger

---

0–29

Critical

---

# State

Represents the current condition of an entity.

States are framework-specific.

Examples:

Aurora:

* Bull
* Neutral
* Bear

Phoenix:

* Dominant
* Stable
* Competitive
* Transition
* Disrupted

Supernova:

* Leader
* Watch
* Review
* Replacement Candidate

---

# Moon Data Model

Moon evaluates strategies.

---

## Strategy

Fields:

Name

Version

Status

---

Example

ADM

BAA

BDA

HAA

VAA

---

## Strategy Result

Fields:

Strategy Name

Selected Asset

Weight

Signal Date

---

# Aurora Data Model

Aurora evaluates indicators and regimes.

---

## Indicator

Fields:

Name

Category

Value

Score

Status

---

## Regime

Fields:

Regime Name

Score

Direction

Confidence

---

# Phoenix Data Model

Phoenix evaluates categories and digital assets.

---

## Category

Fields:

Category Name

State

Score

Trend

---

Examples:

AI Infrastructure

Oracle Networks

RWA

DePIN

---

## Candidate Asset

Fields:

Ticker

Name

Category

Status

Score

---

## Leader

Fields:

Asset

Category

Leadership Score

Replacement Risk

Trend

---

## Challenger

Fields:

Asset

Category

Challenge Score

Distance To Leader

---

# Supernova Data Model

Supernova evaluates themes and companies.

---

## Theme

Fields:

Theme Name

State

Score

Trend

---

Examples:

Digital Transformation

Decarbonization

Demographics

Decoupling

Deglobalization

---

## Candidate Company

Fields:

Ticker

Company Name

Theme

Status

Score

---

## Approved Company

Fields:

Ticker

Theme

Leadership Score

Replacement Risk

Trend

---

# Review Model

All frameworks support reviews.

---

## Review Record

Fields:

Date

Framework

Entity

Review Type

Outcome

Notes

---

Review Types:

Monthly

Quarterly

Annual

---

# Decision Model

Material framework changes must be recorded.

---

## Decision Record

Fields:

Decision ID

Date

Status

Category

Title

Description

---

Reference:

Decision_Log.md

---

# Dashboard Model

All dashboards consume normalized entities.

---

## Dashboard Card

Fields:

Entity Name

Score

State

Trend

Last Updated

---

# Future Extensions

Planned support:

* Historical state tracking
* Event records
* Alert system
* Portfolio linkage
* Automated scoring pipelines

---

# Relationship With Implementation

Python models should map directly to this document whenever possible.

Changes to the logical model should be documented before implementation.

---

# Next Document

Orion_Technical_Architecture.md
