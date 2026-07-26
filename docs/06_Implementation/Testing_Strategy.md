# Orion Testing Strategy

Version: 1.0

Status: Draft

Last Updated: 2026-07-26

---

# Purpose

This document defines the testing strategy used throughout Orion OS.

---

# Testing Principles

Orion is a deterministic system.

Given identical inputs, identical outputs should be produced.

All calculations should be testable.

Dashboard tests should verify presentation behavior only.

---

# Test Categories

Unit Tests

Integration Tests

Regression Tests

---

# Unit Tests

Purpose:

Validate individual functions and calculations.

Examples:

* Configuration validation
* Core model behavior
* Framework model behavior
* Framework calculations after they are documented and implemented

---

# Integration Tests

Purpose:

Validate interactions between modules.

Examples:

* Data -> Framework engine
* Framework engine -> Dashboard presentation
* Aurora -> Orion Dashboard presentation
* CLI -> Framework entry point
* CLI -> Dashboard renderer

Dashboards consume framework outputs.

Dashboards do not own investment logic, scoring logic, allocation logic, or regime logic.

---

# Regression Tests

Purpose:

Ensure previous results remain stable.

Examples:

* ADM allocation consistency
* Aurora regime consistency

Regression tests should be added only after the relevant framework behavior is implemented from approved documentation.

---

# Directory Structure

```text
tests/
  core/
  data/
  moon/
  aurora/
  supernova/
  phoenix/
  dashboard/
  cli/
  integration/
```

---

# Coverage Target

Version 1 Target:

80%+

---

# Test Execution

```bash
pytest
```

Windows local execution may use repository-local pytest temp and cache paths:

```powershell
pytest -q --basetemp .tmp\pytest -o cache_dir=.tmp\pytest_cache
```

---

# Future Extensions

Backtesting validation

Historical benchmark testing

Performance testing
