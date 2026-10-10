# Orion Repository Structure

Version: 2.1

Status: Current source snapshot

Last Updated: 2026-10-10

## Purpose

Describes the package structure present in the current source tree. It is a snapshot of implementation, not an approval that every package is production-ready.

## Repository Layout

```text
orion/
+-- docs/
+-- src/
|   +-- data/
|   |   +-- adapters.py
|   |   +-- contracts.py
|   |   +-- governance.py
|   |   +-- pipeline.py
|   +-- orion/
|       +-- cli/
|       +-- core/
|       |   +-- account/
|       |   +-- asset/
|       |   +-- portfolio/
|       |   +-- ids.py
|       |   +-- runtime and state/event contracts
|       +-- dashboard/
|       +-- frameworks/
|       |   +-- aurora/
|       |   +-- moon/
|       |   +-- orbit/
|       |   +-- phoenix/
|       |   +-- supernova/
|       +-- services/
+-- tests/
+-- config/
+-- requirements.txt
+-- README.md
```

## Core Packages

`src/orion/core` owns cross-framework identifiers, Account and Asset models,
Common Portfolio Domain models and operations, Runtime contracts, state/event
stores, registries, and API/result contracts. It does not own Framework
investment methodology.

`src/data` provides canonical market observation contracts, deterministic
source-agnostic normalization and structural validation, and a provider-neutral
adapter boundary. Production source collection, source-specific semantics,
freshness policy, and fallback behavior remain open implementation work.

## Framework Packages

Framework-owned code resides under `src/orion/frameworks/<framework>`:

* `aurora/` -> market and environment monitoring
* `moon/` -> tactical asset allocation
* `orbit/` -> static asset allocation
* `supernova/` -> equity research and portfolio governance
* `phoenix/` -> digital-asset research and portfolio governance

Each Framework may contain its own Engines, Strategies, models, and governance
implementation. Framework membership does not imply that every methodology is
production-ready or active.

## Presentation and Services

`src/orion/dashboard` is a read-only presentation boundary. It consumes Runtime
outputs and does not calculate investment decisions or mutate State.

`src/orion/cli` owns command routing and application entry points.

`src/orion/services` currently provides an in-memory service registry. Add
services only for concrete responsibilities.

## Future Package Evolution

The following are possible future refactors, not current requirements:

```text
src/orion/
+-- runtime/
+-- domain/
+-- infrastructure/
+-- config/
+-- utils/
```

Do not migrate packages solely to make the source tree match a conceptual
diagram.