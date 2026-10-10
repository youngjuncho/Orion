# Orion Blocker Registry

Version: 2.0

Date: 2026-10-10

## Core Architectural Blockers

**0**

The Core Architecture Review is closed by `CORE-001` through `CORE-020`.

## Reclassified Historical Blockers

| Historical ID | Current classification | Current status |
|---|---|---|
| B-003 | Implementation | Portfolio architecture resolved by D-027 / CORE-019. Snapshot, valuation, weight-based RebalancePlan, and explicit-input ExecutionOrder construction exist; account aggregation, Runtime handoff, end-to-end rebalance, and broker lifecycle remain |
| B-004 | Future / Implementation | In-memory StateStore/EventStore is sufficient for MVP; durable persistence/replay are future scope |
| B-005 | Implementation | Public in-memory Runtime lifecycle exists; production persistence and broader consumer integration remain |
| B-006 | Implementation | API error mapping remains; public contract is resolved by CORE-018 |
| B-007 | Framework Specification | Aurora methodology, not Core architecture |
| B-008 | Framework Specification | Supernova/Phoenix review inputs, not Core architecture |
| B-009 | Data Implementation | source/freshness/collector work, not Core architecture |

## Current Implementation Blockers by Workstream

### Core Runtime

No architecture decision is blocking implementation. Public framework orchestration and the optional decision/state/event lifecycle exist as an in-memory MVP. Remaining work includes the standardized client-facing error mapping and future durable persistence.

### Data

Source adapters, collectors, source-specific semantic validation, freshness thresholds, and source-failure/fallback behavior remain to be implemented/specifed within the Data contract. Runtime accepts a canonical `MarketDataSet` directly or from a provider; it does not implement collection or normalization orchestration.

### Moon

Portfolio architecture is resolved. `PortfolioSnapshot`, valuation, `RebalancePlan`, and explicit-input `ExecutionOrder` materialization exist. Account aggregation, authoritative current-state handoff, end-to-end Runtime integration, sizing policy, and broker execution/fills/settlement remain.

### Aurora / Supernova / Phoenix

Framework-specific methodology and governance remain owned by those Frameworks. Core must not invent those rules.

## Working Rule

A framework-specific unresolved decision does not block unrelated Core work. A historical blocker is removed from the Core blocker count once its architecture has been resolved, even if implementation remains.
