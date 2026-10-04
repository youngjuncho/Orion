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

## Portfolio Domain Model

Moon shall distinguish portfolio decision, portfolio state, and execution
concepts as separate domain objects.

The canonical flow is:

```text
StrategyResult
      ↓
ConsensusAllocation
      ↓
PortfolioTarget
      ↓
RebalancePlan
      ↓
ExecutionOrder
```

Current portfolio state is represented independently:

```text
PortfolioSnapshot
      ↓
Current Holdings
```

A `RebalancePlan` is derived from the desired target and the current
portfolio state:

```text
PortfolioTarget + PortfolioSnapshot
            ↓
       RebalancePlan
```

### StrategyResult

Represents the output of one Moon strategy.

It contains the strategy's signal and resulting allocation together with
supporting information required for downstream processing.

`StrategyResult` does not represent the final Moon portfolio.

### ConsensusAllocation

Represents the allocation resulting from aggregation of the active
strategy results.

It represents strategy-level consensus before translation into the final
execution portfolio.

`ConsensusAllocation` does not represent current holdings.

### PortfolioTarget

Represents the desired portfolio allocation using the actual execution
assets.

The target is therefore the portfolio state Moon intends to reach after
execution-asset mapping.

`PortfolioTarget` does not represent current holdings.

The current Python implementation validates non-empty, unique execution
assets, a 100% total allocation, a non-empty rebalance date, and a non-empty
caller-supplied status label. The allowed status vocabulary is not defined.

### PortfolioSnapshot

Represents the actual current portfolio holdings at a specific point in
time.

It is independent from `PortfolioTarget`.

The snapshot is used as the current-state input when determining required
portfolio changes.

### RebalancePlan

Represents the changes required to move the current portfolio represented
by `PortfolioSnapshot` toward the desired allocation represented by
`PortfolioTarget`.

```text
PortfolioTarget + PortfolioSnapshot
            ↓
       RebalancePlan
```

`RebalancePlan` describes required portfolio changes. It does not execute
trades.

### ExecutionOrder

Represents a concrete trade instruction derived from a rebalance plan.

`ExecutionOrder` is part of the canonical domain model, but actual broker
order execution is outside the current Moon MVP scope.

### Portfolio

`Portfolio` shall not be used as a container for all portfolio concepts.

The following concepts remain distinct:

```text
StrategyResult
ConsensusAllocation
PortfolioTarget
PortfolioSnapshot
RebalancePlan
ExecutionOrder
```

If a higher-level portfolio aggregate is required by the implementation,
its responsibility must remain consistent with these canonical domain
boundaries and must not collapse them into a single undifferentiated
object.

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
6. Generate and validate PortfolioTarget
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
