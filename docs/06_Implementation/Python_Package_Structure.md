# Python Package Structure

Version: 2.1

Status: Current source snapshot

Last Updated: 2026-10-10

Depends On:

* Orion_Domain_Model.md
* Orion_Runtime.md
* Orion_Service_Model.md

## Purpose

This document records the Python package layout currently present in Orion.
It separates implemented boundaries from future package evolution.

## Current Package Layout

```text
src/
  data/
    adapters.py
    contracts.py
    governance.py
    pipeline.py
  orion/
    cli/
    core/
      account/
      asset/
      portfolio/
      ids.py
    dashboard/
    frameworks/
      aurora/
      moon/
      orbit/
      phoenix/
      supernova/
    services/
```

The `src/orion/core` package contains shared identifiers, Account and Asset
models, Common Portfolio Domain models and operations, Runtime contracts, and
in-memory state/event stores. Framework-specific investment logic belongs in
`src/orion/frameworks/<framework>`.

The `src/data` package provides canonical observation and `MarketDataSet`
contracts, source-agnostic normalization and structural validation, plus a
provider-neutral adapter boundary. It does not contain investment logic.
Production collection, source-specific semantic rules, freshness policy, and
fallback behavior remain pending.

## Current Responsibilities

| Package | Responsibility | Current status |
|---|---|---|
| `orion.core` | Shared domain and Runtime contracts, registries, in-memory state/event stores, API result contracts | MVP implementation; failure semantics review is open |
| `orion.frameworks.aurora` | Aurora models, engine, and report entry point | Scaffold; methodology not finalized |
| `orion.frameworks.moon` | Strategy, consensus, execution mapping, common PortfolioTarget proposal | Partial; ADM mapping gap tracked by D-051 |
| `orion.frameworks.orbit` | Static allocation and common PortfolioTarget proposal | Initial implementation |
| `orion.frameworks.supernova` | Supernova models, engine, and report entry point | Scaffold; framework governance remains authoritative |
| `orion.frameworks.phoenix` | Phoenix models, engine, and report entry point | Scaffold; framework governance remains authoritative |
| `orion.dashboard` | Read-only presentation models and renderer | Presentation boundary implemented; Runtime integration partial |
| `orion.cli` | Command routing and report commands | Routing implemented; Runtime-backed reporting partial |
| `orion.services` | In-memory service registry | Registry implementation |
| `data` | Canonical observations, normalization, structural validation, provider-neutral adapter | Partial; no production source collection |

## Runtime Flow and Import Direction

The conceptual execution flow is:

```text
CLI / Dashboard -> Orion Runtime -> Framework adapters -> Framework Engines
                                      |                         |
                                      +---- Core contracts -----+
                                      +---- Data contracts -----+
```

This is a runtime flow, not a strict Python import graph. In the current code,
`orion.core.framework_adapters` lazily imports Moon and Orbit engines for
portfolio adapters. Keep this coupling visible when evaluating package
boundaries; do not infer a clean one-way import graph from the conceptual flow.

## Future Package Evolution

The following are design targets, not requirements of the current source tree:

```text
src/orion/
  runtime/
  domain/
  infrastructure/
  config/
  utils/
```

Introduce them only when concrete responsibilities justify the migration.

## Testing Layout

Tests mirror the implemented packages:

```text
tests/
  data/
  orion/
    cli/
    core/
    dashboard/
    frameworks/
      aurora/
      moon/
      orbit/
      phoenix/
      supernova/
    services/
```

## Related Documents

* Orion_Domain_Model.md
* Orion_Runtime.md
* Orion_Engine.md
* Orion_Service_Model.md