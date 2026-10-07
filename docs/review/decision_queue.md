# Orion Decision Queue

Version: 2.0

Date: 2026-10-07

## Purpose

Working queue only. Permanent decisions belong in `docs/05_Decisions/Decision_Log.md` and the relevant contract documents.

## Current Status

Core Architecture decisions are **resolved** by `CORE-001` through `CORE-020`.

Therefore the following historical queue items are closed at the architecture level:

| Historical ID | Current status |
|---|---|
| DQ-DOMAIN-001 | Architecture resolved by CORE-019; exact Python reconciliation is implementation work |
| DQ-RUNTIME-001 | Resolved by CORE-004/012; implementation pending |
| DQ-RUNTIME-002 | Resolved by CORE-003; implementation pending |
| Runtime persistence | Resolved as MVP in-memory / durable storage future by CORE-005/015 |
| API error contract | Resolved by CORE-018; implementation pending |

## Remaining Open Items

### Data Implementation / Specification

* source-specific fields
* freshness thresholds
* missing-data policy
* source failure/fallback behavior
* collectors and normalization implementation

### Moon Implementation

* PortfolioSnapshot implementation
* RebalancePlan implementation
* end-to-end Runtime integration

### Aurora Framework

* final indicator set
* scoring methodology
* regime thresholds
* transition-risk methodology

### Supernova Framework

Framework governance remains separately managed. Core does not reopen its scoring or replacement rules.

### Phoenix Framework

Framework governance remains separately managed. Core does not reopen category/leader/scoring rules.

## Rules

1. Do not invent unresolved investment methodology.
2. Do not treat configuration as approval.
3. Do not reopen a Core architecture decision merely because implementation is incomplete.
4. Framework-local decisions remain Framework-owned.
5. When a genuinely new cross-framework requirement appears, create a new Core decision rather than silently extending an existing contract.
