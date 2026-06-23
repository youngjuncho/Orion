# Architecture Consistency Report

Date: 2026-06-23

Scope:

* Documentation under `docs/`
* Current source tree under `src/` and `tests/`

Authoritative references:

* `docs/05_Decisions/Decision_Log.md`, D-023
* `docs/01_Architecture/Orion_Operating_Architecture.md`
* `docs/01_Architecture/Orion_Technical_Architecture.md`

Architecture baseline:

* Aurora = Monitoring Framework
* Moon = ETF Portfolio Engine
* Supernova = Equity Portfolio Engine
* Phoenix = Digital Asset Portfolio Engine
* Dashboard = presentation layer only
* Investment logic must not live inside dashboard modules
* Framework logic belongs inside `src/moon`, `src/aurora`, `src/supernova`, and `src/phoenix`
* Dashboard code belongs inside `src/dashboard`

---

## Executive Summary

The repository source structure is aligned with the current implementation baseline:

```text
src/
  core/
  data/
  moon/
  aurora/
  supernova/
  phoenix/
  dashboard/
  cli/

tests/
  core/
```

No source-tree refactor is required at this stage.

The main consistency issues are in documentation. Most conflicts appear to be older design language that predates D-023. The highest-risk issue is `Orion_Technical_Architecture.md` assigning strategy execution, signal generation, and state generation to the Dashboard Layer. That directly conflicts with the current rule that dashboards are presentation-only.

---

## Documentation Findings

### 1. Dashboard Layer Owns Investment Logic

File: `docs/01_Architecture/Orion_Technical_Architecture.md`

Section: `Dashboard Layer`

Issue:

The Dashboard Layer responsibilities are listed as:

* Strategy execution
* Signal generation
* State generation

This conflicts with the current architecture baseline. Dashboard is a presentation layer only. Strategy execution, signal generation, and state generation belong in the framework modules, not dashboard modules.

Recommended Fix:

Revise the Dashboard Layer responsibilities to presentation-only responsibilities such as:

* Dashboard rendering
* Visualization
* Summary display
* Navigation
* Consumption of framework outputs

Move or restate strategy execution, signal generation, and state generation under the relevant framework engine sections.

Severity: Critical

---

### 2. Technical Architecture Treats All Four Frameworks as Primary Engines

File: `docs/01_Architecture/Orion_Technical_Architecture.md`

Section: `System Overview`

Issue:

The document states that "Orion OS consists of four primary engines" and lists Moon, Aurora, Supernova, and Phoenix as equivalent engines.

This conflicts with D-023 and `Orion_Operating_Architecture.md`, which define:

* One Monitoring Layer: Aurora
* Three Portfolio Engines: Moon, Supernova, Phoenix

Recommended Fix:

Replace "four primary engines" with language aligned to D-023:

* Orion OS consists of one Monitoring Framework and three Portfolio Engines.
* Aurora is the Monitoring Framework.
* Moon, Supernova, and Phoenix are Portfolio Engines.

Severity: Major

---

### 3. Singular vs Plural Dashboard Directory Conflict

File: `docs/01_Architecture/Orion_Technical_Architecture.md`

Section: `Directory Structure`

Issue:

The technical architecture lists:

```text
src/
  dashboards/
```

The newer repository structure document and current source tree use:

```text
src/
  dashboard/
```

This creates a singular/plural naming conflict.

Recommended Fix:

Update `Orion_Technical_Architecture.md` to use `src/dashboard/`, matching `Orion_Repository_Structure.md`, `Environment_Setup.md`, and the current source tree.

Severity: Major

---

### 4. Technical Architecture Places `tests/` Under `src/`

File: `docs/01_Architecture/Orion_Technical_Architecture.md`

Section: `Directory Structure`

Issue:

The displayed directory tree appears to place `tests/` under `src/`:

```text
src/
  core/
  data/
  dashboards/
  cli/
  tests/
```

The authoritative repository structure and current implementation place `tests/` at the repository root.

Recommended Fix:

Update the directory tree so `tests/` is a top-level repository directory, parallel to `src/`.

Severity: Major

---

### 5. Technical Architecture Uses Dashboard-Centric Scoring Language

File: `docs/01_Architecture/Orion_Technical_Architecture.md`

Section: `Scoring Engine`

Issue:

The document states:

```text
All dashboards should use a common scoring framework.
```

This can be read as making dashboards consumers or owners of scoring behavior. Under the current architecture, scoring logic belongs in framework/core logic, while dashboards consume rendered output.

Recommended Fix:

Clarify that framework engines and shared core utilities use common scoring models, and dashboards only display resulting scores.

Severity: Major

---

### 6. Supernova Described as a Monitoring Engine

File: `docs/01_Architecture/Orion_Technical_Architecture.md`

Section: `Supernova Architecture`

Issue:

Supernova is described as:

```text
5D Megatrend monitoring engine.
```

D-023 designates Supernova as the Equity Portfolio Engine. "Monitoring engine" understates its portfolio-engine role and creates ambiguity with Aurora, the actual monitoring framework.

Recommended Fix:

Revise the purpose to:

```text
Equity Portfolio Engine for 5D Megatrend companies.
```

Severity: Major

---

### 7. Vision Summary Uses "Dashboard Framework" as the Parent Architecture

File: `docs/00_Vision/Vision_Summary.md`

Section: `Dashboard Framework`

Issue:

The document uses `Dashboard Framework` as the parent heading for Moon, Aurora, Supernova, and Phoenix. This conflicts with the current separation between framework logic and dashboard presentation.

Recommended Fix:

Rename the section to an architecture-neutral heading such as:

```text
Orion Frameworks
```

or:

```text
Operating Frameworks
```

Keep dashboard language only for presentation-layer documents.

Severity: Major

---

### 8. Vision Summary Uses Outdated Phoenix Portfolio Status

File: `docs/00_Vision/Vision_Summary.md`

Section: `Phoenix`

Issue:

The document states:

```text
The long-term portfolio management methodology is currently under review.
```

This conflicts with later approved decisions D-021 and D-022, which define Phoenix scope, core asset separation, and portfolio construction methodology.

Recommended Fix:

Update the Phoenix section to reference the approved D-021 and D-022 architecture:

* Phoenix manages approved altcoin category leaders.
* BTC and ETH are core digital assets outside Phoenix.
* Approved Phoenix category leaders are equally weighted.

Severity: Major

---

### 9. Vision Summary Uses Outdated Engine Labels

File: `docs/00_Vision/Vision_Summary.md`

Section: `Dashboard Framework`

Issue:

The section labels frameworks as:

* Moon: Dynamic Asset Allocation Engine
* Aurora: Market Climate Engine
* Supernova: 5D Megatrend Investment Engine
* Phoenix: Digital Asset Ecosystem Engine

These labels are not fully aligned with D-023's final operating architecture terms.

Recommended Fix:

Use the current architecture terms:

* Aurora: Monitoring Framework
* Moon: ETF Portfolio Engine
* Supernova: Equity Portfolio Engine
* Phoenix: Digital Asset Portfolio Engine

Severity: Minor

---

### 10. IPS Treats Aurora as an Investment Framework

File: `docs/02_Investment_Framework/Orion_IPS.md`

Section: `Portfolio Architecture`

Issue:

The document states:

```text
Orion consists of four independent investment frameworks.
```

This conflicts with D-023 because Aurora is a Monitoring Framework, not an investment framework or portfolio engine.

Recommended Fix:

Revise to:

```text
Orion consists of one Monitoring Framework and three independent Portfolio Engines.
```

Then list:

* Aurora: Monitoring Framework
* Moon: ETF Portfolio Engine
* Supernova: Equity Portfolio Engine
* Phoenix: Digital Asset Portfolio Engine

Severity: Major

---

### 11. IPS Phoenix Policy Is Superseded by Later Decisions

File: `docs/02_Investment_Framework/Orion_IPS.md`

Section: `Phoenix Policy`

Issue:

The document states that Phoenix governance is draft and that long-term accumulation methodology remains under review.

This conflicts with D-021 and D-022, which are approved and define Phoenix scope and portfolio construction.

Recommended Fix:

Update the Phoenix Policy section to reference D-021 and D-022:

* Phoenix manages approved altcoin category leaders.
* BTC and ETH are excluded from Phoenix.
* Challengers and watchlist assets are monitored but not held.
* Approved leaders are equally weighted.

Severity: Major

---

### 12. Aurora Operating Model Uses "Execution Framework" for Moon

File: `docs/03_Research/Aurora/Aurora_Operating_Model.md`

Section: `Relationship With Moon`

Issue:

The document states:

```text
Moon remains the execution framework.
```

D-023 designates Moon as the ETF Portfolio Engine. "Execution framework" is understandable, but it is not the final architecture term and may blur the distinction between execution, portfolio ownership, and framework responsibilities.

Recommended Fix:

Replace with:

```text
Moon remains the ETF Portfolio Engine.
```

Severity: Minor

---

### 13. Technical Architecture Has Encoding-Damaged Diagrams

File: `docs/01_Architecture/Orion_Technical_Architecture.md`

Section: `System Overview`, `Logical Architecture`, `Directory Structure`, `Scoring Engine`

Issue:

Several architecture diagrams and score ranges contain damaged characters such as `?쒋??`, `??`, and `0??00`. This makes architecture diagrams and numeric ranges ambiguous.

Recommended Fix:

Replace damaged tree glyphs and arrows with ASCII-only diagrams. Replace damaged score ranges with explicit ranges such as `0-100`, `90-100`, and `80-89`.

Severity: Minor

---

### 14. Operating Architecture Has Encoding-Damaged Diagrams

File: `docs/01_Architecture/Orion_Operating_Architecture.md`

Section: `Architecture Overview`, `Decision Flow`

Issue:

The operating architecture diagrams contain damaged characters. The prose is clear, but the diagrams are difficult to read and could cause implementation ambiguity.

Recommended Fix:

Replace damaged diagrams with ASCII-only diagrams that preserve the D-023 relationship:

```text
Aurora
  -> Market Context
  -> Investor Interpretation
  -> Moon / Supernova / Phoenix
  -> Portfolio Actions
```

Severity: Minor

---

### 15. Repository Structure Diagram Has Encoding-Damaged Tree Glyphs

File: `docs/01_Architecture/Orion_Repository_Structure.md`

Section: `Repository Layout`, `Source Layout`

Issue:

The repository structure is conceptually correct, but the tree glyphs are damaged. This is less severe than the technical architecture conflict because the directory names themselves remain readable.

Recommended Fix:

Replace damaged tree glyphs with ASCII-only layout blocks.

Severity: Minor

---

## Source Tree Review

Current source tree:

```text
src/
  __init__.py
  aurora/
    __init__.py
  cli/
    __init__.py
  core/
    __init__.py
    config_loader.py
  dashboard/
    __init__.py
  data/
    __init__.py
  moon/
    __init__.py
  phoenix/
    __init__.py
  supernova/
    __init__.py

tests/
  __init__.py
  core/
    __init__.py
    test_config_loader.py
```

### Source Alignment Findings

File or Path: `src/core`

Section: Source tree

Issue:

Aligned. Shared configuration loader lives in `src/core`, which matches the documented responsibility for configuration.

Recommended Fix:

No change.

Severity: Minor

---

File or Path: `src/data`

Section: Source tree

Issue:

Aligned. The package exists and contains no investment logic.

Recommended Fix:

No change.

Severity: Minor

---

File or Path: `src/moon`

Section: Source tree

Issue:

Aligned. The package exists. No misplaced dashboard or data-layer code was found.

Recommended Fix:

No change.

Severity: Minor

---

File or Path: `src/aurora`

Section: Source tree

Issue:

Aligned. The package exists. No misplaced portfolio-engine or dashboard code was found.

Recommended Fix:

No change.

Severity: Minor

---

File or Path: `src/supernova`

Section: Source tree

Issue:

Aligned. The package exists. No misplaced dashboard or data-layer code was found.

Recommended Fix:

No change.

Severity: Minor

---

File or Path: `src/phoenix`

Section: Source tree

Issue:

Aligned. The package exists. No misplaced dashboard or data-layer code was found.

Recommended Fix:

No change.

Severity: Minor

---

File or Path: `src/dashboard`

Section: Source tree

Issue:

Aligned. The package uses the singular `dashboard` name and contains no investment logic.

Recommended Fix:

No change.

Severity: Minor

---

File or Path: `src/cli`

Section: Source tree

Issue:

Aligned. The package exists and contains no framework logic.

Recommended Fix:

No change.

Severity: Minor

---

File or Path: `tests`

Section: Source tree

Issue:

Partially aligned. `tests/` exists at repository root, and `tests/core/test_config_loader.py` mirrors `src/core/config_loader.py`. Framework test directories do not exist yet, but no framework implementation exists yet either.

Recommended Fix:

No change required now. Add `tests/moon`, `tests/aurora`, `tests/supernova`, and `tests/phoenix` when framework implementation begins.

Severity: Minor

---

## Recommendations Summary

1. Update `Orion_Technical_Architecture.md` first. It contains the only Critical issue and multiple Major architecture conflicts.
2. Normalize architecture terminology across vision and IPS documents to D-023:
   * Aurora = Monitoring Framework
   * Moon = ETF Portfolio Engine
   * Supernova = Equity Portfolio Engine
   * Phoenix = Digital Asset Portfolio Engine
3. Standardize repository naming on `src/dashboard/`.
4. Keep dashboard documents presentation-only. Any reference to strategy execution, signal generation, state generation, scoring calculation, allocation, or rebalance logic should point to framework engines or shared core modules.
5. Replace damaged diagram glyphs with ASCII-only diagrams to avoid implementation ambiguity.
6. Do not refactor source code yet. The current source tree is aligned with the requested implementation baseline.
