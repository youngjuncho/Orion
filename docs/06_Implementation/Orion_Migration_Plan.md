# Orion Migration Plan

Version: 1.0

Status: Draft

Last Updated: 2026-07-28

Depends On:

* Orion_Runtime.md
* Python_Package_Structure.md
* Orion_Domain_Model.md

---

# Purpose

Defines the migration path from the current Orion prototype to the target production architecture.

The migration should be incremental, testable, and reversible whenever possible.

---

# Current Repository

Current source structure:

```text
src/

aurora/
moon/
phoenix/
supernova/
core/
dashboard/
cli/
```

This structure was suitable for the prototype phase but does not fully reflect the Orion architecture.

---

# Target Repository

Target package structure:

```text
src/

orion/

core/
runtime/
domain/
services/
infrastructure/
frameworks/
dashboard/
cli/
config/
utils/
```

---

# Migration Principles

The migration should:

* Preserve existing functionality
* Minimize breaking changes
* Keep documentation synchronized
* Maintain passing tests throughout the process

---

# Migration Phases

## Phase 1

Repository Cleanup

Tasks:

* Remove obsolete files
* Standardize directory structure
* Organize documentation

Status:

Completed

---

## Phase 2

Package Restructuring

Tasks:

* Create src/orion
* Move existing packages
* Update imports

Status:

Planned

---

## Phase 3

Domain Model Implementation

Tasks:

* Implement Python domain classes
* Add serialization support
* Add validation

Status:

Planned

---

## Phase 4

Service Layer

Tasks:

* ConfigurationService
* EventService
* DashboardService
* ReviewService

Status:

Planned

---

## Phase 5

Runtime Layer

Tasks:

* Runtime
* Scheduler
* Workflow

Status:

Planned

---

## Phase 6

Framework Engines

Tasks:

* Moon Engine
* Aurora Engine
* Supernova Engine
* Phoenix Engine

Status:

Planned

---

## Phase 7

Dashboard

Tasks:

* Dashboard models
* Report generation
* Summary views

Status:

Planned

---

## Phase 8

CLI

Tasks:

* Command dispatcher
* Framework commands
* Reporting commands

Status:

Planned

---

# Package Migration

Current

```text
src/moon
```

↓

Target

```text
src/orion/frameworks/moon
```

---

Current

```text
src/aurora
```

↓

Target

```text
src/orion/frameworks/aurora
```

---

Current

```text
src/supernova
```

↓

Target

```text
src/orion/frameworks/supernova
```

---

Current

```text
src/phoenix
```

↓

Target

```text
src/orion/frameworks/phoenix
```

---

Current

```text
src/core
```

↓

Target

```text
src/orion/core
```

---

Current

```text
src/dashboard
```

↓

Target

```text
src/orion/dashboard
```

---

Current

```text
src/cli
```

↓

Target

```text
src/orion/cli
```

---

# Success Criteria

The migration is complete when:

* Documentation matches implementation
* Package structure follows the architecture
* Tests pass successfully
* CLI functions correctly
* Frameworks operate independently

---

# Risks

Potential risks:

* Broken imports
* Circular dependencies
* Inconsistent package naming
* Test failures during migration

Each migration phase should be committed independently to simplify rollback if necessary.

---

# Related Documents

* Orion_Runtime.md
* Orion_Engine.md
* Python_Package_Structure.md
* Orion_Domain_Model.md