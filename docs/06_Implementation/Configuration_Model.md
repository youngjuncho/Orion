# Orion Configuration Model

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

---

# Purpose

Defines configuration management within Orion OS.

---

# Principles

Configuration should be externalized.

Investment logic must not be hardcoded.

---

# Configuration Categories

System

Data

Moon

Aurora

Supernova

Phoenix

---

# Directory Structure

```text id="hzzlzy"
config/

system.yaml

moon.yaml

aurora.yaml

supernova.yaml

phoenix.yaml
```

---

# System Configuration

Examples:

* Log level
* Data directory
* Cache settings

---

# Moon Configuration

Examples:

* Active strategies
* Rebalance frequency

---

# Aurora Configuration

Examples:

* Indicator weights
* Regime thresholds

---

# Supernova Configuration

Examples:

* Theme settings
* Review frequency

---

# Phoenix Configuration

Examples:

* Category settings
* Review frequency

---

# Secrets

API keys must never be stored in repository configuration files.

Use:

```text id="aj1k78"
.env
```

for secrets management.

---

# Future Extensions

Database configuration

Cloud configuration

Notification settings
