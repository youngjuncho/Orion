# Orion Configuration Schema

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

Depends On:

* Orion_Data_Model.md
* Configuration_Model.md

---

# Purpose

This document defines the configuration schema used by Orion OS.

Configuration files represent the operational state of Orion.

Framework logic should be driven by configuration whenever possible.

Investment logic should not be hardcoded.

---

# Configuration Architecture

```text
config/
  system.yaml
  moon.yaml
  aurora.yaml
  supernova.yaml
  phoenix.yaml
```

---

# Configuration Principles

## Principle 1

Documentation defines policy.

Configuration defines operational state.

---

## Principle 2

Configuration may change without requiring code changes.

---

## Principle 3

Frameworks should read configuration rather than embed assumptions.

---

# system.yaml

Purpose:

Global Orion settings.

---

## Schema

```yaml
system:
  version: "1.0"
  environment: production
  timezone: Asia/Seoul
  currency: KRW
  logging:
    level: INFO
  data:
    retention_days: null
  dashboard:
    refresh_minutes: 60
```

---

# moon.yaml

Purpose:

Moon operational configuration.

---

## Schema

```yaml
moon:
  enabled: true
  rebalance_frequency: monthly
  strategies:
    - ADM
    - BAA
    - BDA
    - HAA
    - VAA
  strategy_weighting: equal
  execution_mode: consensus
  signal_assets:
    enabled: true
  execution_mapping:
    enabled: true
```

---

# aurora.yaml

Purpose:

Aurora operational configuration.

---

## Schema

```yaml
aurora:
  enabled: true
  update_frequency: daily
  scoring_range:
    min: 0
    max: 100
  indicator_groups:
    core:
      - trend
      - liquidity
      - volatility
      - credit
    cross_asset:
      - dollar
      - gold
      - oil
      - bitcoin
  transition_monitoring:
    enabled: true
```

---

# supernova.yaml

Purpose:

Supernova operational configuration.

---

## Schema

```yaml
supernova:
  enabled: true
  review_frequency: monthly
  framework: five_d
  approved_companies:
    - NVDA
    - GOOGL
    - PLTR
    - ISRG
    - CEG
  candidate_universe:
    source: Supernova_Candidate_Universe.md
  replacement_policy:
    enabled: true
  scoring:
    range: 0-100
```

---

# phoenix.yaml

Purpose:

Phoenix operational configuration.

---

## Schema

```yaml
phoenix:
  enabled: true
  review_frequency: monthly
  core_assets:
    btc_weight: 0.60
    eth_weight: 0.40
  portfolio_construction: equal_weight
  categories:
    smart_contracts:
      leader: SOL
      challenger: SUI
    oracle:
      leader: LINK
      challenger: API3
    rwa:
      leader: ONDO
      challenger: PENDLE
    ai_infrastructure:
      leader: TAO
      challenger: RENDER
    data_availability:
      leader: TIA
      challenger: AVAIL
  replacement_policy:
    enabled: true
  leadership_monitoring:
    enabled: true
```

---

# Validation Rules

Required:

* All configuration files must be valid YAML.
* Each configuration file must contain its documented top-level key.
* Missing required fields should raise validation errors.
* Invalid enum values should raise validation errors.

---

# Change Management

Configuration changes that alter investment behavior should be reviewed.

Major configuration changes may require:

* Documentation updates
* Decision Log updates

---

# Future Extensions

Potential additions:

* database.yaml
* notifications.yaml
* api.yaml
* ai.yaml

---

# Relationship With Documentation

Documentation defines intent.

Configuration defines execution.

When conflicts occur:

Documentation takes precedence.

Configuration should be updated to match approved documentation.

---

# Next Step

Production configuration files have been created:

* system.yaml
* moon.yaml
* aurora.yaml
* supernova.yaml
* phoenix.yaml

These files represent the initial operational state of Orion OS.
