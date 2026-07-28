# Logging Guidelines

Version: 1.0

Status: Active

Last Updated: 2026-07-28

Depends On:

* Orion_Runtime.md
* Orion_Service_Model.md

---

# Purpose

Defines the logging policy used throughout Orion OS.

Logging should provide operational visibility while remaining concise and consistent.

---

# Logging Philosophy

Logs exist to explain:

* What happened
* When it happened
* Why it happened
* Whether it succeeded

Logs should not expose implementation details unnecessarily.

---

# Logging Levels

DEBUG

Detailed diagnostic information.

Development only.

---

INFO

Normal system operations.

Examples:

* Strategy evaluation
* Portfolio update
* Scheduler execution

---

WARNING

Unexpected but recoverable situations.

Examples:

* Missing optional data
* Retry operation

---

ERROR

Operation failed.

Examples:

* Data download failure
* Configuration error

---

CRITICAL

System cannot continue.

Examples:

* Runtime initialization failure
* Corrupted configuration

---

# Log Format

Each log entry should contain:

* Timestamp
* Level
* Component
* Message

Example

```
2026-07-28 21:30:15 INFO MoonEngine Strategy evaluation completed
```

---

# Component Names

Examples

Runtime

MoonEngine

AuroraEngine

PhoenixEngine

SupernovaEngine

Scheduler

Dashboard

CLI

---

# Structured Logging

Prefer structured values over formatted strings.

Good

```
Strategy=ADM
State=RiskOn
Asset=SPYM
```

Avoid embedding all information in free-form text.

---

# Exception Logging

Log exceptions once.

Do not repeatedly log the same exception as it propagates.

---

# Sensitive Information

Never log:

* API keys
* Passwords
* Tokens
* Personal information

---

# Performance

Avoid excessive logging inside loops.

High-frequency logging should use DEBUG level.

---

# Log Storage

Logs should be written to:

logs/

Example

```
logs/

runtime.log

moon.log

aurora.log
```

---

# Related Documents

* Orion_Runtime.md
* Orion_Service_Model.md