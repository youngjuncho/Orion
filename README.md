
## 2026-10-07 Core Architecture Status

Core Architecture is **CLOSED** under `CORE-001` through `CORE-020`. The canonical application execution boundary is **Orion Runtime**; Aurora, Moon, Orbit, Supernova, and Phoenix are Frameworks. Remaining gaps are implementation, validation, Framework-specific specification, or future infrastructure.

Current navigation:

- `docs/05_Decisions/Core_Architecture_Decision_Baseline.md` - Core closure baseline
- `docs/06_Implementation/Orion_Runtime.md` - Runtime lifecycle
- `docs/06_Implementation/Orion_State_Model.md` - State/transition semantics
- `docs/06_Implementation/Orion_Event_Model.md` - Event semantics
- `docs/06_Implementation/Python_Domain_Models.md` - canonical domain -> Python mapping
- `docs/reports/Implementation_Status_Report.md` - current implementation status
- `docs/review/blocker_registry.md` - current blockers (Core architecture: 0)

# Orion

## Personal Investment Operating System

Orion is a personal investment operating system designed to help investors understand market conditions, asset allocation status, megatrend opportunities, and digital asset ecosystems within one minute.

The goal is not to predict the future.

The goal is to observe the current state of markets and make systematic investment decisions.

---

## Core Philosophy

* Observe More, Predict Less
* Systems over Opinions
* Signals over Information
* State over News

---

## Orion Architecture

Orion is organized around five independently governed Investment Frameworks:

### Aurora
Market environment / monitoring framework.

### Moon
Dynamic Asset Allocation framework.

### Orbit
Static Asset Allocation framework.

### Supernova
5D Megatrend equity satellite framework.

### Phoenix
Digital asset category-leader satellite framework.

The common Portfolio Domain is shared by Moon, Orbit, Supernova, and Phoenix.
Aurora remains outside the Portfolio Domain.

The canonical application execution boundary is **Orion Runtime**.
Frameworks return framework results and do not directly mutate StateStore/EventStore.

## Development Roadmap

Phase 1

Documentation closure and Moon ADM vertical slice

Phase 2

Aurora Dashboard

Phase 3

Supernova Dashboard

Phase 4

Phoenix Dashboard

Phase 5

AI Commentary

Phase 6

Web Dashboard

---

## Status

Core architecture is closed; implementation and Framework-specific integration continue.

The repository currently contains tested core contracts, CLI/dashboard
routing, framework scaffolds, and a partial Moon ADM path. Research and
implementation rules that are still marked Draft are not activated by the
operational configuration.

