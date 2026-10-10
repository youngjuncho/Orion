# Orion Review

## Current Status

The 2026-10-07 review declared the Core Architecture closed. The decision
baseline's per-ID evidence crosswalk is now under audit; the topic list alone
does not establish which source record supports each `CORE-xxx` identifier.

The reported canonical baseline is:

```text
CORE-001 … CORE-020
```

See:

* `../05_Decisions/Core_Architecture_Decision_Baseline.md`
* `implementation_review.md`
* `../reports/Implementation_Status_Report.md`
* `blocker_registry.md`

## Purpose of This Directory

`review/` is a temporary coordination area. It is not a competing source of truth.

Durable decisions belong in `docs/05_Decisions/`. Core contract semantics belong in their respective architecture/implementation documents. Framework methodology belongs in Framework specifications.

## Post-Closure Rule

Do not create another Core architecture decision merely because implementation is incomplete. Reopen Core architecture only for a genuinely new cross-framework requirement not covered by `CORE-001` through `CORE-020`.

## Current Work Frontier

```text
Core Architecture
      CLOSED
        ↓
Core Runtime Implementation
        ↓
Canonical Data Pipeline
        ↓
Moon End-to-End
        ↓
Framework-specific Implementation
        ↓
CLI / Dashboard Integration
```
