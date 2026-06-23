# Phoenix Interface Specification

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

---

# Purpose

Defines the operational interface for Phoenix.

---

# Responsibilities

Phoenix is responsible for:

* Category evaluation
* Leader selection
* Challenger monitoring
* Replacement risk assessment

---

# Inputs

Candidate Universe

Market Data

On-Chain Data

Category Definitions

Scoring Rules

---

# Core Objects

Category

CandidateAsset

Leader

Challenger

ReviewRecord

---

# Category Interface

Required Fields

Category Name

Score

State

Trend

---

# Asset Interface

Required Fields

Ticker

Name

Category

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

Category Health

Leader Status

Challenger Status

Replacement Risk

---

# Dashboard Consumers

Phoenix Dashboard

Orion Dashboard

---

# CLI Consumers

orion phoenix report

orion phoenix leaders

orion phoenix categories
