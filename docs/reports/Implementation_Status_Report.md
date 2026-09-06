# Orion Implementation Status Report

Date: 2026-07-26

Status: Draft

---

# Purpose

This report records the current implementation state after the initial Orion OS scaffolding work.

It is not an architecture decision record.

The authoritative architecture remains:

* D-023
* Orion_Operating_Architecture.md
* Orion_Technical_Architecture.md
* Orion_Configuration_Schema.md

---

# Review Scope

Reviewed:

* Current source tree under `src/`
* Current tests under `tests/`
* Current configuration files under `config/`
* Current architecture and implementation reports under `docs/reports/`
* Current CLI, dashboard, and framework scaffolds

---

# Current Git Review Baseline

The most recent implementation commits reviewed were:

* `Connect CLI for dashboard`
* `feat: dashboard scaffold`
* `feat : phoenix scaffold`
* `feat: add supernova scaffold`
* `feat: moon scaffold`
* `feat: add aurora scaffolding`
* `feat: add core models and cli scaffold`
* `chore: stop tracking test scratch directory`
* `feat: add core models and stabilize config tests`
* `chore: reconcile docs, config, and vscode environment`

The working tree was clean at review time.

---

# Implementation Structure Status

The current source tree has been refactored into the packaged Orion layout:

```text
src/
  orion/
    cli/
    core/
    dashboard/
    frameworks/
      aurora/
      moon/
      phoenix/
      supernova/
```

This aligns with the current Python package structure.

`src/orion/dashboard` exists as the presentation layer.

Framework logic is currently located under:

* `src/orion/frameworks/aurora`
* `src/orion/frameworks/moon`
* `src/orion/frameworks/supernova`
* `src/orion/frameworks/phoenix`

No investment logic was found inside `src/orion/dashboard`.

---

# Implemented Components

## Core

Implemented:

* Strict YAML configuration loader
* Required configuration file validation
* Typed configuration dataclasses
* Core score, state, regime, review, decision, and dashboard card models
* Basic logging configuration utility

Status:

Core scaffolding is usable for early implementation.

## Data Layer

Implemented:

* Immutable normalized observation contract
* Validated market data batch contract
* Required-field and duplicate-observation checks

Status:

The data layer currently defines input contracts only. It does not collect,
normalize, persist, or interpret source data.

## CLI

Implemented:

* `orion version`
* `orion health`
* `orion config`
* `orion dashboard`
* `orion data update`
* `orion data status`
* Framework command shells for Moon, Aurora, Supernova, and Phoenix
* Framework report commands for Moon, Aurora, Supernova, and Phoenix

Status:

CLI routing is in place.

Framework `report` commands call their corresponding framework entry points.

Non-report framework commands remain placeholders until their behavior is implemented from approved documentation.

## Aurora

Implemented:

* Aurora report model
* Indicator and regime models
* Aurora engine scaffold
* Aurora report entry point

Status:

Aurora contains no final scoring or regime logic yet.

TODO comments correctly mark ambiguous or future behavior.

## Moon

Implemented:

* Moon report model
* Strategy, allocation, and portfolio models
* ADM signal selection from precomputed momentum inputs
* Equal-weight strategy consensus allocation
* Documented signal-to-execution asset mapping
* Moon engine scaffold
* Moon report entry point

Status:

ADM selection follows the documented relative and absolute momentum rules.

Consensus allocation applies equal strategy weighting, aggregates overlapping
assets, and produces normalized allocation output.

Market data loading, total-return calculation, defensive-asset approval,
consensus allocation, and rebalance logic are not implemented.

TODO comments correctly mark ambiguous or future behavior.

## Supernova

Implemented:

* Supernova report model
* Theme, candidate company, and approved company models
* Supernova engine scaffold
* Supernova report entry point

Status:

Supernova contains no final scoring, leadership, or replacement logic yet.

TODO comments correctly mark ambiguous or future behavior.

## Phoenix

Implemented:

* Phoenix report model
* Category, candidate asset, leader, and challenger models
* Phoenix engine scaffold
* Phoenix report entry point

Status:

Phoenix contains no final category, leadership, or replacement logic yet.

TODO comments correctly mark ambiguous or future behavior.

## Dashboard

Implemented:

* Dashboard presentation models
* Read-only Orion dashboard composition layer
* Textual dashboard rendering function
* CLI dashboard command connected to dashboard renderer

Status:

Dashboard remains presentation-only.

It consumes framework outputs and does not generate investment decisions.

---

# Test Status

The following command passed at review time:

```powershell
pytest tests\orion -q
```

Result:

```text
45 passed
```

---

# Documentation Status

Existing reports that should be retained:

* `docs/reports/Architecture_Consistency_Report.md`
* `docs/reports/Architecture_Reconciliation_Summary.md`
* `docs/reports/Implementation_Status_Report.md`

The architecture reconciliation reports explain why the current framework and dashboard boundaries exist.

This implementation status report explains what has actually been scaffolded so far.

---

# Documentation Items Resolved

## Environment Setup

File:

`docs/06_Implementation/Environment_Setup.md`

Issue:

The document described only a generic `venv` setup and did not capture the current local conda workflow.

The current working development setup uses VSCode with a conda `orion` environment and Python 3.10.

Resolution:

Updated the document to include the Windows + VSCode + conda `orion` workflow, current Python 3.10 usage, repository-local pytest temp/cache guidance, and the current CLI dashboard command.

Severity:

Resolved

## Repository Structure Encoding

File:

`docs/01_Architecture/Orion_Repository_Structure.md`

Issue:

The tree diagram contains garbled characters.

Resolution:

Replaced the repository and source layout diagrams with plain ASCII.

Severity:

Resolved

## Testing Strategy Encoding And Flow Language

File:

`docs/06_Implementation/Testing_Strategy.md`

Issue:

Some integration examples contain garbled arrow characters.

The old integration flow wording could also be read as dashboard-centric unless clarified.

Resolution:

Replaced the garbled arrows with plain ASCII and clarified that dashboards consume framework outputs but do not own investment logic, scoring logic, allocation logic, or regime logic.

Severity:

Resolved

---

# Remaining Implementation Issues

## Non-Report Framework CLI Commands Are Not Yet Wired To Framework Engines

Current State:

`orion dashboard` calls the dashboard renderer.

Framework report commands now call their corresponding framework entry points:

* `orion moon report`
* `orion aurora report`
* `orion supernova report`
* `orion phoenix report`

Non-report commands such as `orion moon allocation`, `orion aurora indicators`, `orion supernova watchlist`, and `orion phoenix categories` still return placeholder messages.

Recommended Next Step:

Wire non-report commands only after their output contracts and framework behavior are documented.

Severity:

Minor

## Engine Outputs Are Placeholder Reports

Current State:

Aurora, Moon, Supernova, and Phoenix engines return typed placeholder reports.

Recommended Next Step:

Implement framework behavior only when the corresponding design document gives enough detail.

If design details are missing, keep TODO comments instead of inventing logic.

Severity:

Major

## ADM Execution Mapping Is Incomplete

Current State:

The approved execution mapping document does not define mappings for ADM's
current signal assets `VTI` and `VEU`, and defines `SGOV` only as the execution
asset for `BIL`. The mapper therefore rejects unmapped assets instead of
silently treating signal assets as executable assets.

Recommended Next Step:

Approve the missing ADM execution mappings through the Moon governance process
before connecting ADM output to portfolio execution.

Severity:

Major

## Data Layer Has Input Contracts But No Collectors

Current State:

The data layer now exposes immutable contracts for normalized observations and validated input batches.

It still has no data collection, normalization pipeline, persistence, or source-specific adapters.

Recommended Next Step:

Implement collection and normalization only after source-specific fields, freshness rules, and storage behavior are approved.

Severity:

Minor

## Dashboard Is Textual Only

Current State:

The dashboard renderer prints a simple textual summary.

Recommended Next Step:

Keep dashboard read-only.

Add richer rendering only after framework reports and data contracts are stable.

Severity:

Minor

---

# Recommended Next Work Order

1. Approve ADM execution mappings through Moon governance.
2. Resolve ADM total-return and dividend methodology before implementing market-data calculations.
3. Keep Aurora, Supernova, and Phoenix at scaffold level until their implementation rules are fully specified.
4. Implement data collection and normalization only after their source contracts are documented.
5. Wire non-report CLI commands only after their framework output contracts are documented.

---

# Guardrails

Future implementation should preserve these rules:

* Dashboard remains presentation-only.
* Investment logic belongs inside framework modules or shared core utilities.
* Data modules do not contain investment logic.
* Configuration validation remains strict.
* Framework behavior should not be invented from placeholders.
* Ambiguous design gaps should remain as TODO comments until resolved by documentation.
