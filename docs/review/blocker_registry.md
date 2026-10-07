# Orion Blocker Registry

Version: 2.0

Date: 2026-10-07

## Core Architectural Blockers

**0**

The Core Architecture Review is closed by `CORE-001` through `CORE-020`.

## Reclassified Historical Blockers

| Historical ID | Current classification | Current status |
|---|---|---|
| B-003 | Implementation | Portfolio architecture resolved by D-027 / CORE-019; PortfolioSnapshot/RebalancePlan/ExecutionOrder implementation remains |
| B-004 | Future / Implementation | In-memory StateStore/EventStore is sufficient for MVP; durable persistence/replay are future scope |
| B-005 | Implementation | Public Orion Runtime implementation remains |
| B-006 | Implementation | API error mapping implementation remains; public contract is resolved by CORE-018 |
| B-007 | Framework Specification | Aurora methodology, not Core architecture |
| B-008 | Framework Specification | Supernova/Phoenix review inputs, not Core architecture |
| B-009 | Data Implementation | source/freshness/collector work, not Core architecture |

## Current Implementation Blockers by Workstream

### Core Runtime

No architecture decision is blocking implementation. The remaining task is to implement the already-defined Runtime lifecycle and contracts.

### Data

Source-specific fields, freshness thresholds, collectors, and source-failure/fallback behavior remain to be implemented/specifed within the Data contract.

### Moon

Portfolio architecture is resolved. Implementation remains for PortfolioSnapshot, RebalancePlan, and end-to-end Runtime integration.

### Aurora / Supernova / Phoenix

Framework-specific methodology and governance remain owned by those Frameworks. Core must not invent those rules.

## Working Rule

A framework-specific unresolved decision does not block unrelated Core work. A historical blocker is removed from the Core blocker count once its architecture has been resolved, even if implementation remains.
