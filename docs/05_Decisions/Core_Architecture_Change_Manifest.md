# Core Architecture Reconciliation — Change Manifest

Date: 2026-10-07

This manifest is a navigation aid for the documents modified during the Core Architecture reconciliation.

## Primary canonical documents

* `docs/05_Decisions/Core_Architecture_Decision_Baseline.md`
* `docs/01_Architecture/Orion_Operating_Architecture.md`
* `docs/01_Architecture/Orion_Technical_Architecture.md`
* `docs/01_Architecture/Orion_Data_Model.md`
* `docs/06_Implementation/Orion_Runtime.md`
* `docs/06_Implementation/Orion_State_Model.md`
* `docs/06_Implementation/Orion_Event_Model.md`
* `docs/06_Implementation/Orion_Engine.md` (legacy compatibility note)

## Domain / package reconciliation

* `docs/01_Architecture/Orion_Repository_Structure.md`
* `docs/06_Implementation/Python_Package_Structure.md`
* `docs/06_Implementation/Python_Domain_Models.md`

## Status / planning reconciliation

* `docs/04_Roadmap/Orion_Roadmap.md`
* `docs/06_Implementation/Implementation_Roadmap.md`
* `docs/reports/Implementation_Status_Report.md`
* `docs/review/blocker_registry.md`
* `docs/review/implementation_review.md`
* `docs/review/decision_queue.md`
* `docs/review/next_requests.md`

## Historical documents

`docs/reports/Architecture_Consistency_Report.md` and `docs/reports/Architecture_Reconciliation_Summary.md` are retained as historical evidence and explicitly point to the current baseline.

## Source code

The 2026-10-07 Core reconciliation also includes implementation scaffolding aligned with the
closed architecture contracts:

* `src/orion/core/account/`
* `src/orion/core/asset/`
* `src/orion/core/portfolio/`
* `src/orion/core/ids.py`
* `src/orion/frameworks/orbit/`
* corresponding Core / Portfolio tests under `tests/`

These changes are implementation work, not new architecture decisions. The canonical
architecture remains defined by `CORE-001` through `CORE-020`.

## 2026-10-07 Integration Reconciliation

The A/B integration review identified implementation drift against already-closed
Core and Portfolio contracts. The controlled reconciliation applied the existing
contracts without creating a new architecture decision:

* Orbit added to the canonical five-Framework Runtime registration and current API/documentation lists.
* Event implementation aligned to the canonical `event_id / event_type / event_category / occurred_at / execution_id / entity_type / entity_id / payload` contract.
* Dashboard decoupled from direct Framework Engine imports and changed to consume `OrionResult.dashboard_data`.
* Moon-local `Portfolio`, `PortfolioTarget`, `Allocation`, and `PortfolioValidator` models removed; Moon now uses Common Portfolio Domain objects for executable allocations/targets while retaining StrategyResult and ConsensusAllocation as framework-specific objects.
* Canonical Common `ExecutionOrder` added as a domain contract, distinct from runtime `ExecutionMetadata`.
* Common Portfolio Domain contract and migration checkpoint reconciled with the implemented model.

These are implementation/documentation reconciliations of existing decisions; no new
Core architecture decision was introduced.
