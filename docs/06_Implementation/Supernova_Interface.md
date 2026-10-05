# Supernova Interface Specification

Version: 1.1

Status: Draft

Last Updated: 2026-10-05

---

# Purpose

Defines the operational interface for Supernova.

---

# Responsibilities

Supernova is responsible for:

* Theme evaluation
* Evidence-backed company evaluation
* Leadership monitoring
* Replacement risk assessment
* Portfolio state management

---

# Inputs

Candidate Universe

Financial Data

Theme Data

Evidence-backed Score Reviews

Company Research Records

Scoring Rules

---

# Core Objects

Theme

CandidateCompany

CompanyScoreReview

CompanyResearchRecord

ApprovedCompany

ReviewRecord
GovernanceDecision

---

# Theme Interface

Required Fields

Theme Name

Score

State

Trend

---

# Company Interface

Required Fields

Ticker

Theme

Company Score (weighted from five reviewed dimensions)

Portfolio State

Leadership Role

Replacement Risk

Trend

---

# Leadership Interface

Required Fields

Leader / Leadership Role

Challenger (when applicable)

Replacement Risk

Primary Risk Driver

Trend

---

# Output Schema

Approved Companies

Theme Health

Leadership Status

Replacement Risk

---

# Dashboard Consumers

Supernova Dashboard

Orion Dashboard

---

# CLI Consumers

orion supernova report

orion supernova leaders

orion supernova watchlist
