# Orion Configuration Model

Version: 1.1

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Orion_Domain_Model.md
* Orion_Technical_Architecture.md

---

# Purpose

This document defines how Orion OS manages configuration.

Configuration controls system behavior without changing application code.

Investment logic should remain independent of configuration.

---

# Configuration Principles

## Externalized Configuration

Configuration should be stored outside application code.

Investment rules should be configurable whenever practical.

---

## Separation of Responsibilities

Research documents define methodology.

Configuration defines operational parameters.

Implementation consumes configuration.

---

## Environment Independence

The same application code should support multiple environments by loading different configuration files.

---

# Configuration Hierarchy

```text
Configuration

├── System
├── Moon
├── Aurora
├── Supernova
└── Phoenix
```

---

# Directory Structure

```text
config/

system.yaml

moon.yaml

aurora.yaml

supernova.yaml

phoenix.yaml
```

---

# System Configuration

Controls global application behavior.

Examples:

- Logging
- Data Directory
- Cache
- Time Zone

Example Fields:

```yaml
log_level: INFO
timezone: UTC
cache_enabled: true
data_directory: ./data
```

---

# Moon Configuration

Controls Moon execution.

Typical Settings:

- Active Strategies
- Rebalance Frequency
- Execution Mapping
- Portfolio Constraints

Example:

```yaml
strategies:
  - ADM
  - BAA
  - VAA
  - HAA
  - BDA
active_strategies: []

rebalance_frequency: monthly
```

`strategies` lists registered strategies. `active_strategies` is the explicit
execution allowlist and must be a subset of the registered list. Draft or
otherwise unresolved strategies remain registered but inactive.

---

# Aurora Configuration

Controls market monitoring.

Typical Settings:

- Component Weights
- Regime Thresholds
- Indicator Enable Flags

Example:

```yaml
weights:
  trend: 30
  liquidity: 30
  credit: 20
  volatility: 20

risk_on: 70
risk_off: 50
```

---

# Supernova Configuration

Controls company evaluation.

Typical Settings:

- Review Frequency
- Theme Activation
- Scoring Thresholds

---

# Phoenix Configuration

Controls digital asset evaluation.

Typical Settings:

- Active Categories
- Review Frequency
- Leadership Thresholds

---

# Object Configuration

Configuration should map directly to Orion object models.

Examples:

Strategy

```yaml
name: ADM
enabled: true
rebalance: monthly
```

StrategyResult

No persistent configuration.

Generated at runtime.

Portfolio

```yaml
max_position_size: 0.30
min_position_size: 0.05
```

Aurora

```yaml
indicator_refresh: daily
```

---

# Runtime Configuration

Configuration is loaded during application startup.

Each Framework receives only its own configuration.

Example:

```text
System
    │
    ├── Moon Config
    ├── Aurora Config
    ├── Supernova Config
    └── Phoenix Config
```

---

# Configuration Validation

Every configuration file should support validation.

Validation includes:

- Required Fields
- Allowed Value Ranges
- Duplicate Detection
- Schema Compatibility

Invalid configuration should prevent execution.

---

# Secrets Management

Sensitive information must never be stored in repository configuration files.

Use:

```text
.env
```

Examples:

- API Keys
- Database Credentials
- Authentication Tokens

---

# Future Enhancements

Potential future additions:

- Environment Profiles
- Remote Configuration
- Dynamic Reloading
- Configuration Versioning

Status:

Research Only

Not Approved

---

# Related Documents

* Orion_Domain_Model.md
* Orion_Technical_Architecture.md
* Moon_Object_Model.md
* Decision_Log.md
