# Moon Object Model

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Moon_Current_Production.md
* Moon_Interface.md
* Orion_Domain_Model.md

---

# Purpose

This document defines the core object model used by the Moon Portfolio Engine.

The object model provides the canonical representation of Moon's internal data structures.

Research documents describe investment logic.

The object model defines how that logic is represented in software.

---

# Implemented Result Invariants

The current strategy and consensus contracts enforce the following structural
rules:

* A `StrategyResult` must contain at least one selected asset.
* Selected assets within one result must be unique.
* Result weights must be finite, non-negative numbers.
* A consensus input may contain each strategy only once.
* Consensus normalizes each positive strategy result and the final allocation
  must total 100%.
* Execution mapping must explicitly cover every signal asset.

These are structural validation rules only. They do not choose investment
assets, calculate momentum, or define execution mappings.

---

# Design Principles

The Moon object model follows four principles.

## Strategy Independence

Each strategy operates independently.

Strategies do not access or modify the state of other strategies.

---

## Immutable Results

Strategy outputs are immutable.

Once a strategy produces a result, it should not be modified.

Aggregation always consumes completed results.

---

## Separation of Responsibilities

Objects have clearly defined responsibilities.

| Object | Responsibility |
|---------|----------------|
| Strategy | Generate signals |
| StrategyResult | Represent strategy output |
| Allocation | Represent target weights |
| Portfolio | Represent final portfolio |
| MoonEngine | Coordinate execution |

---

## Configuration Driven

Strategies should read configuration.

Investment logic should not be hardcoded.

---

# Object Relationships

The canonical conceptual flow is:

```text
StrategyResult
    |
    v
Consensus Allocation
    |
    v
Portfolio Target + Portfolio Snapshot
    |
    v
Rebalance Plan
    |
    v
Execution Orders
```

`Portfolio Target` is the desired allocation produced by the current
execution. `Portfolio Snapshot` is the independently observed current
holdings. A `Rebalance Plan` compares those two objects and produces
execution orders. These concepts must not be collapsed into one generic
`Portfolio` container.

```text
Market Data
      │
      ▼
 Strategy
      │
      ▼
StrategyResult
      │
      ▼
Consensus Allocator
      │
      ▼
Allocation
      │
      ▼
Execution Mapping
      │
      ▼
Portfolio
```

---

# Strategy

Represents a single tactical allocation strategy.

Examples:

* ADM
* BAA
* BDA
* HAA
* VAA

## Required Fields

Name

Version

Status

Configuration

## Required Methods

load_data()

calculate_signal()

generate_result()

---

# StrategyResult

Represents the output of a strategy evaluation.

## Fields

Strategy Name

Signal Date

Selected Assets

Target Weights

Metadata

## Example

```text
Strategy: ADM

Assets:

SPY
VGIT

Weights:

50%
50%
```

---

# Allocation

Represents the aggregated signal allocation after combining all strategy
results. It is not yet an order or a current holding.

## Fields

Asset

Weight

Source Strategies

Execution Asset

## Example

```text
SPY

75%

Sources:

ADM
BAA

Execution:

SPYM
```

---

# Portfolio

Represents the executable portfolio target in the current minimal model.

## Fields

Target Holdings

Rebalance Date

Execution Assets

The full target contract also defines `Portfolio Snapshot`, `Rebalance Plan`,
and `Execution Order` as separate concepts. The current Python `Portfolio`
model is a scaffold and does not yet implement those objects.

---

# Consensus Allocator

The Consensus Allocator combines Strategy Results into a unified allocation.

Responsibilities:

* Receive multiple StrategyResults
* Apply strategy weights
* Aggregate identical assets
* Normalize weights
* Produce Allocation

The Consensus Allocator does not execute trades.

---

# Execution Mapper

The Execution Mapper converts Signal Assets into Execution Assets.

Example

```text
SPY

↓

SPYM
```

Execution mappings are defined in:

Moon_Execution_Mapping.md

---

# Moon Engine

The Moon Engine coordinates the complete monthly workflow.

Responsibilities:

1. Load market data
2. Execute all active strategies
3. Collect Strategy Results
4. Run Consensus Allocation
5. Apply Execution Mapping
6. Generate Portfolio
7. Produce reports

The Moon Engine does not implement individual strategy logic.

---

# Object Lifecycle

```text
Load Market Data

↓

Strategy Execution

↓

StrategyResult Creation

↓

Consensus Allocation

↓

Execution Mapping

↓

Portfolio Creation

↓

Reporting
```

---

# Implementation Mapping

| Document | Python Object |
|----------|---------------|
| Moon_Interface.md | Interface Definitions |
| Moon_Current_Production.md | Business Rules |
| Moon_Object_Model.md | Domain Objects |
| Orion_Configuration_Schema.md | Configuration Models |

---

# Related Documents

* Moon_Current_Production.md
* Moon_Interface.md
* Orion_Domain_Model.md
* Orion_Configuration_Schema.md
