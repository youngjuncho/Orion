# Phoenix Data Sources

Version: 0.1

Status: Draft

Last Updated: 2026-06-22

Depends On:

* Phoenix_Leader_Framework.md
* Phoenix_Scoring_Framework.md

---

# Purpose

This document defines approved data sources used by Phoenix.

The objective is to ensure scoring consistency and reproducibility.

Phoenix should use a limited number of trusted data providers.

---

# Data Source Principles

Priority Order:

1. Public
2. Transparent
3. Repeatable
4. API Accessible

---

# Source Categories

Phoenix evaluates:

* Adoption
* Ecosystem
* Economics
* Momentum

Each category may use different sources.

---

# Adoption Data

Measures:

* Active users
* Transactions
* Network activity

---

Primary Source

DefiLlama

Usage:

* TVL
* Protocol activity
* Ecosystem metrics

Priority:

P1

---

Secondary Source

Artemis

Usage:

* Active users
* Transactions
* Chain activity

Priority:

P2

---

# Ecosystem Data

Measures:

* Developer activity
* Ecosystem growth
* Application count

---

Primary Source

Electric Capital Developer Report

Usage:

* Developer statistics
* Ecosystem participation

Priority:

P1

---

Secondary Source

GitHub

Usage:

* Repository activity
* Contributor activity

Priority:

P2

---

# Economics Data

Measures:

* Revenue
* Fees
* Economic sustainability

---

Primary Source

Token Terminal

Usage:

* Revenue
* Fees
* Protocol earnings

Priority:

P1

---

Secondary Source

DefiLlama

Usage:

* Fee tracking
* Revenue tracking

Priority:

P2

---

# Momentum Data

Measures:

* Relative strength
* Capital flows
* Market attention

---

Primary Source

CoinGecko

Usage:

* Market capitalization
* Volume
* Price performance

Priority:

P1

---

Secondary Source

CoinMarketCap

Usage:

* Validation
* Cross-checking

Priority:

P2

---

# Category Mapping

## Smart Contract Platforms

Sources

* Artemis
* Electric Capital
* Token Terminal
* CoinGecko

---

## Oracle Networks

Sources

* Artemis
* Token Terminal
* CoinGecko

---

## AI Infrastructure

Sources

* Artemis
* Token Terminal
* CoinGecko

---

## Real World Assets

Sources

* DefiLlama
* Token Terminal
* CoinGecko

---

# Source Priority Rules

If multiple sources disagree:

Use highest priority source.

---

Example

Revenue

Token Terminal

vs

DefiLlama

Result:

Token Terminal wins.

---

# Source Health

Sources are monitored annually.

Criteria:

* Availability
* Reliability
* API support
* Data quality

---

# Approved Sources

P1

* DefiLlama
* Artemis
* Token Terminal
* CoinGecko
* Electric Capital

---

P2

* GitHub
* CoinMarketCap

---

# Prohibited Sources

Phoenix should not rely on:

* Social media sentiment
* Influencer rankings
* Anonymous rankings
* Unverified dashboards

unless explicitly approved.

---

# Future Automation

Future Orion implementations may collect data automatically through APIs.

Manual collection remains acceptable during research phase.

---

# Governance

Adding or removing a source requires:

Decision_Log.md entry

before implementation.

---

# Open Issues

OI-901

API integration design.

Status:

Open

---

OI-902

Historical data retention.

Status:

Open

---

OI-903

Data validation process.

Status:

Open

---

# Related Documents

Phoenix_Leader_Framework.md

Phoenix_Scoring_Framework.md

Phoenix_Dashboard_Spec.md
