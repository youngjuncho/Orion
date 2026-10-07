# Portfolio Architecture Checkpoint — 2026-10-07

## Purpose

This checkpoint records the first **actual code migration** after the Portfolio Architecture Review. It is based on the persisted `Orion_Wip_Portfolio_Architecture_Updated_v2.zip` baseline.

## Implemented

- Added typed Common Domain identifiers (`core/ids.py`).
- Added canonical Asset reference model (`core/asset/`).
- Added Account, CashBalance, and Position custody models (`core/account/`).
- Added Common Portfolio Domain models:
  - `Allocation`
  - `Portfolio`
  - `PortfolioTarget`
  - `PortfolioState`
  - `PortfolioSnapshot`
  - `RebalancePlan` / `RebalanceChange`
  - `Transfer`
- Moved Moon executable `Allocation` / `PortfolioTarget` semantics to the Common Domain.
- Replaced Moon-local `PortfolioValidator` with Common `PortfolioTarget` invariants.
- Changed `MoonEngine.build_portfolio_target()` to require explicit `PortfolioId` and `TargetId` plus the target effective date.
- Kept Moon execution mapping framework-specific.
- Added the first Orbit implementation skeleton that creates the approved static Orbit allocation as a Common `PortfolioTarget`.
- Updated Dashboard access to the new Common `Allocation.asset_id` field.
- Confirmed Aurora remains outside the Portfolio Domain; no Aurora portfolio model was added.

## Deliberately not completed yet

- Full `RebalancePlan → ExecutionOrder → Fill → Ledger → PortfolioState` runtime lifecycle.
- Transfer routing / conversion settlement runtime.
- PortfolioState projection from multiple Accounts.
- Supernova/Phoenix integration into Common `PortfolioTarget`.
- Final stale-terminology cleanup across all historical documents.

## Verification

`PYTHONPATH=src pytest -q` → verification is rerun after the Core reconciliation; this checkpoint remains an implementation checkpoint, not a claim that the full Portfolio runtime lifecycle is complete.

This checkpoint is therefore an implementation checkpoint, not a claim that the entire Portfolio Domain migration is complete.
