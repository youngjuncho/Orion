# Orion Decision Queue

Version: 2.0

Date: 2026-10-10

## Purpose

Working queue only. Permanent decisions belong in `docs/05_Decisions/Decision_Log.md` and the relevant contract documents.

## Current Status

The baseline reports Core Architecture as resolved by `CORE-001` through
`CORE-020`. Per-ID evidence and numbering are under traceability audit; see
the open item below.

Therefore the following historical queue items are closed at the architecture level:

| Historical ID | Current status |
|---|---|
| DQ-DOMAIN-001 | Architecture resolved by CORE-019; exact Python reconciliation is implementation work |
| DQ-RUNTIME-001 | Resolved by CORE-004/012; in-memory public Runtime lifecycle implemented, production hardening/persistence deferred |
| DQ-RUNTIME-002 | Resolved by CORE-003; execution-correlated in-memory EventStore integration implemented |
| Runtime persistence | Resolved as MVP in-memory / durable storage future by CORE-005/015 |
| API error contract | Resolved by CORE-018; standardized client-facing error mapping remains |

## Remaining Open Items

### Decision Status

| Draft ID | Topic | Current evidence / unresolved choice |
|---|---|---|
| D-051 | ADM signal-to-execution mapping | **Approved 2026-10-10:** ADM identity mappings VTI->VTI, VEU->VEU, and SGOV->SGOV. This resolves mapping only; `config/moon.yaml` still has `active_strategies: []`, so ADM activation remains separate. |
| D-052 | Runtime failure and commit semantics | **Approved 2026-10-10 and implemented:** stage/validate state and events, commit both stores together, mark failed sessions `Error`, enforce one public run per Runtime, and validate snapshot/transition correlation. |
| D-053 | Portfolio cash valuation and target semantics | **Approved 2026-10-10 and implemented:** use `system.currency` as valuation currency; value `PortfolioState.cash` with caller-supplied positive finite FX rates; include cash in the total-value denominator while keeping it outside the fully invested target; reject duplicate account/currency balances and remove the separate `cash_value` input. |
| D-054 | Default acceptance of rebalance plan proposals | **Approved 2026-10-10:** retain D-050 candidate-type-agnostic Auto-Approval. Moon target and rebalance plan proposals are accepted independently by default; callers may provide a handler to reject or conditionally accept either. Acceptance does not execute orders. |
| D-055 | ADM absolute-momentum signal policy | **Approved 2026-10-10 and implemented:** SGOV benchmark; selected risk asset's trailing-12-month adjusted-price return must be strictly greater than SGOV's, with equality false. Source semantics, calendar/freshness, and production approval gates remain open; ADM stays inactive. |

`D-051` through `D-055` are approved. See the Decision Log and relevant contracts for evidence.

### Core Decision Traceability

* The Core baseline lists twenty topics in sequence but does not provide an explicit `CORE-001`…`CORE-020` topic-to-evidence crosswalk. The Decision Log has no individual CORE records. Reconcile the provenance and numbering, including the D-029 gap, before treating the numbered closure claim as fully auditable. Do not invent historical decisions to fill the gaps.

### Documentation Consistency

* Audit stale or missing metadata and mark retained historical reports as superseded or historical at the document itself.
* Reconcile old test-count statements with dated verification records; do not present a historical count as the current suite size.
* Add canonical glossary definitions for Recommendation, DecisionCandidate, AcceptedDecision, and StateTransition, and distinguish human review decisions from Runtime acceptance.
* Review the long Decision Log's unnumbered D.1/D.2 section and the D-029 gap; preserve the existing record until its provenance is established.

### Data Implementation / Specification

* production collectors and provider-specific field semantics
* freshness thresholds, timestamp parsing/order, and missing-data policy
* source failure/fallback behavior and live-provider approval
* canonical identity and symbol normalization policy (including provider/source identity)
* default ADM signal assembly remains gated by freshness, comparison, and activation policy; a context-aware Moon factory can now receive `RuntimeContext.market_data` and configuration

### Moon Implementation

* Account aggregation and authoritative PortfolioState projection
* Runtime handoff of current PortfolioState/current weights
* end-to-end Moon rebalance integration
* Execution sizing policy and broker lifecycle (outside current MVP)

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
