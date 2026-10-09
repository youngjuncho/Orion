# Orion Data Pipeline

Version: 1.1

Status: MVP Implemented — Moon ADM Data Utilities, Integration Guards, and Provider-Neutral Adapter Added

Last Updated: 2026-10-09

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
for production collection. The current `src/data` package provides canonical observation/batch contracts plus deterministic source-agnostic normalization and structural validation. Moon ADM’s precomputed-input boundary is recorded in `Moon_ADM_Data_Contract.md`; its unresolved methodology approvals, provider-specific contract decisions, and implementation gates are classified in `Moon_ADM_Data_Readiness_and_Closure.md`. The current policy-explicit utilities also provide exact return calculation, prior-observation selection, VTI/VEU relative-momentum calculation, caller-threshold-based observation-age validation, explicit absolute-momentum inputs/comparison contracts, readiness checks, and a fail-closed signal-integration guard. These are composable utilities, not an automatic production orchestrator. Source-specific freshness, semantic field rules, authoritative policy approval, and production collection remain intentionally open; see `Moon_ADM_Data_Pipeline_Contract_Consolidation.md` and `Moon_ADM_Provider_Adapter_Readiness_Review.md`. The provider-neutral `ProviderNeutralMarketDataAdapter` in `src/data/adapters.py` normalizes a fake/source-provided raw batch into `MarketDataSet` and fails closed on malformed or duplicate batches. Its fixture tests do not require network access. This generic adapter does not authorize a live provider adapter or network access; see `Moon_ADM_Provider_Neutral_Adapter_Contract.md`.

| Framework | Data readiness |
|---|---|
| Moon | D-028 establishes adjusted-price-based total-return proxy; Step 28 implements prior-observation-on-or-before target selection; source compatibility, freshness, provider-calendar validation, and defensive benchmark identity, exact comparison operator/equality behavior, and source policies remain open; research direction is benchmark-relative to cash/defensive return |
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

The generic ADM utilities can validate observation age against an explicit caller-supplied threshold. This does not close production freshness policy or prove provider-calendar/data quality; the production threshold and source contract remain open.

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


Moon ADM implementation boundary: `docs/01_Architecture/Moon_ADM_Data_Implementation_Boundary.md`.


Moon ADM absolute-momentum comparison contract: `Moon_ADM_Absolute_Momentum_Comparison_Contract.md`. The contract distinguishes `UNAVAILABLE` from `FALSE`, requires an explicit caller-supplied operator, and does not approve an investment policy or activate ADM. Signal integration is separately guarded by `Moon_ADM_Comparison_Signal_Integration_Guard.md`; unresolved policy gates block progression and the guard does not construct `ADMSignalInput`.


Moon ADM contract consolidation: `Moon_ADM_Data_Pipeline_Contract_Consolidation.md` maps the implemented stages, cross-stage invariants, and remaining production gates. It does not activate ADM or construct `ADMSignalInput`.


Moon ADM provider-neutral adapter contract: `Moon_ADM_Provider_Neutral_Adapter_Contract.md`. The generic adapter wraps a raw batch source, normalizes into canonical contracts, and propagates source failures; it adds no retries, caching, field inference, or fallback behavior. Provider approval and provider-specific semantic/data-quality contracts remain prerequisites for live integration.
