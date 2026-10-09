# Orion Data Pipeline

Version: 1.0

Status: MVP Implemented

Last Updated: 2026-10-08

Depends On:

* Orion_Domain_Model.md
* Orion_Framework_Data_Contracts.md

---

# Purpose

This document defines how data flows through Orion OS.

---

# Pipeline Architecture

```text
External Sources

↓

Collection

↓

Normalization

↓

Validation

↓

Storage

↓

Framework Engines

↓

Dashboards

↓

CLI / Web
```

---

# Collection Layer

Responsibilities:

* API requests
* Scheduled downloads
* Raw data retrieval

---

# Initial Sources

Moon

* Yahoo Finance

Aurora

* FRED
* Yahoo Finance

Supernova

* Yahoo Finance
* Company financial data

Phoenix

* CoinGecko
* CryptoQuant
* Exchange APIs

These are candidate source categories only. Source-specific fields,
freshness rules, normalization rules, and approval status are not yet closed
for production collection. The current `src/data` package provides canonical observation/batch contracts plus deterministic source-agnostic normalization and structural validation. Source-specific freshness, semantic field rules, and production collection remain intentionally open.

| Framework | Data readiness |
|---|---|
| Moon | ETF price inputs are conceptually identified; ADM total-return and dividend rules remain open |
| Aurora | Indicator set, formulas, and source contract remain open |
| Supernova | Analyst review inputs and fundamental source contract remain open |
| Phoenix | Leadership review inputs and on-chain/source contract remain open |

---

# Normalization Layer

MVP implementation: `src/data/pipeline.py`

Responsibilities:

* Map source observations into `MarketDataPoint`
* Trim and canonicalize required textual fields
* Normalize optional currency values
* Build one validated `MarketDataSet` per input batch

The MVP does not infer field semantics, exchange calendars, FX conversions, or source-specific timestamps. Those rules require closed source contracts. The shared envelope, candidate price vocabulary, framework matrix, and production-collector closure checklist are specified in `Orion_Framework_Data_Contracts.md`.

---

# Validation Layer

MVP implementation: `MarketDataPoint` / `MarketDataSet` contracts plus `validate_dataset`.

Responsibilities:

* Required field checks
* Supported value-type checks
* Finite numeric checks
* Duplicate observation checks
* Canonical dataset type checks

Freshness validation is intentionally deferred until framework/source freshness policies are closed.

---

# Storage Layer

Initial Implementation:

```text
data/

raw/

processed/

cache/
```

---

# Update Frequency

Moon

Monthly

---

Aurora

Daily

---

Supernova

Weekly

---

Phoenix

Daily

---

# Data Retention

Historical data should be retained whenever possible.

No automatic deletion in Version 1.

---

# Future Architecture

Potential migration:

CSV

↓

Parquet

↓

Database

↓

Cloud Storage

---

# Next Document

Orion_CLI_Spec.md
