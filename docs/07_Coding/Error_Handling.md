# Error Handling

Version: 1.0

Status: Active

Last Updated: 2026-07-28

Depends On:

* Orion_Runtime.md
* Orion_Service_Model.md

---

# Purpose

Defines the error handling strategy for Orion OS.

Errors should be predictable, recoverable when possible, and easy to diagnose.

---

# Principles

Errors should:

* Fail fast
* Be explicit
* Preserve context
* Avoid silent failures

---

# Exception Types

Prefer specific exception classes.

Examples

ConfigurationError

DataSourceError

ValidationError

StrategyExecutionError

RuntimeError

---

# Exception Hierarchy

Application-specific exceptions should inherit from a common OrionError base class.

Example

```
OrionError

├── ConfigurationError
├── DataSourceError
├── ValidationError
└── StrategyExecutionError
```

---

# Recovery

Recover only when recovery is well-defined.

Otherwise, raise the exception to the caller.

---

# Validation

Validate external input as early as possible.

Examples

* Configuration files
* API responses
* User input

---

# User Messages

CLI users should receive concise, actionable error messages.

Internal stack traces should be reserved for DEBUG mode.

---

# Retry Policy

Retry only transient failures.

Examples

* Temporary network errors
* Rate limits

Do not retry invalid configuration or programming errors.

---

# Resource Cleanup

Use context managers whenever possible.

Example

```
with open(...) as file:
```

---

# Assertions

Use assertions only for internal invariants.

Do not rely on assertions for user input validation.

---

# Related Documents

* Orion_Runtime.md
* Development_Principles.md