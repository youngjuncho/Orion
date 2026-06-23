# Supernova Interface Specification

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

---

# Purpose

Defines the operational interface for Supernova.

---

# Responsibilities

Supernova is responsible for:

* Theme evaluation
* Company evaluation
* Leadership monitoring
* Replacement risk assessment

---

# Inputs

Candidate Universe

Financial Data

Theme Data

Scoring Rules

---

# Core Objects

Theme

CandidateCompany

ApprovedCompany

ReviewRecord

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

Company Name

Theme

Score

Status

---

# Leadership Interface

Required Fields

Leader

Challenger

Replacement Risk

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
