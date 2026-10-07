# Orion Repository Structure

Version: 2.0

Status: Approved V1 Baseline

Last Updated: 2026-10-07

## Purpose

Defines the repository and source structure that is actually implemented. This document is the canonical package baseline for V1; future package decomposition must not be treated as a current requirement.

## Repository Layout

```text
orion/
戍式式 docs/
戍式式 src/
弛   戍式式 data/
弛   戌式式 orion/
弛       戍式式 cli/
弛       戍式式 core/
弛       戍式式 dashboard/
弛       戍式式 frameworks/
弛       弛   戍式式 aurora/
弛       弛   戍式式 moon/
弛       弛   戍式式 phoenix/
弛       弛   戌式式 supernova/
弛       戌式式 services/
戍式式 tests/
戍式式 config/
戍式式 requirements.txt
戌式式 README.md
```

## `src/orion/core`

Owns cross-framework Core contracts and runtime-oriented scaffolding, including configuration, state/event contracts and stores, registries, execution metadata, and API/result contracts.

Core does not own Framework investment methodology.

## `src/data`

Shared normalized data-contract package.

It contains:

* observation contracts
* MarketDataSet contracts
* validation boundary

It does not contain:

* investment logic
* scoring
* strategy selection
* portfolio decisions
* state/events

Source collection and normalization implementation remain future work.

## `src/orion/frameworks/<framework>`

Framework-owned implementation:

* `aurora/` ? market-climate monitoring
* `moon/` ? ETF portfolio framework
* `supernova/` ? equity portfolio framework
* `phoenix/` ? digital-asset portfolio framework

Each Framework may contain its own Engines, Strategies, models, and governance implementation.

## `src/orion/dashboard`

Read-only presentation boundary. It consumes Runtime/Framework outputs and builds presentation models. It does not calculate investment decisions or mutate State.

## `src/orion/cli`

Command routing and application entry-point handling. Business methodology belongs to Frameworks, not CLI commands.

## `src/orion/services`

Current service registry/infrastructure scaffolding. Do not create generic services without a concrete responsibility.

## Future Package Evolution

The following are possible future refactors, not current V1 requirements:

```text
src/orion/
戍式式 runtime/
戍式式 domain/
戍式式 infrastructure/
戍式式 config/
戌式式 utils/
```

Do not perform another package migration solely to make the directory tree match an abstract architecture diagram.
