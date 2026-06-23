# Orion Data Pipeline

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

Depends On:

* Orion_Data_Model.md

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

---

# Normalization Layer

Responsibilities:

* Field mapping
* Date standardization
* Currency standardization

---

# Validation Layer

Responsibilities:

* Missing value checks
* Duplicate checks
* Data freshness checks

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
