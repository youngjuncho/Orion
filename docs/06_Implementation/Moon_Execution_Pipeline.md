# Moon Execution Pipeline

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Orion_Runtime.md
* Moon_Engine.md
* Moon_Object_Model.md
* Moon_Service_Model.md
* Moon_Interface.md

---

# Purpose

This document defines the end-to-end execution workflow of the Moon framework.

The execution pipeline describes how Moon transforms market data into a portfolio recommendation through a sequence of deterministic processing stages.

---

# Design Principles

The Moon execution pipeline follows these principles:

* Deterministic execution
* Strategy independence
* Reproducibility
* Modular processing
* Fail-safe operation

Each stage has a single responsibility and produces a well-defined output.

---

# Pipeline Overview

```text
Scheduler
    │
    ▼
Load Configuration
    │
    ▼
Load Market Data
    │
    ▼
Load Active Strategies
    │
    ▼
Execute Strategies
    │
    ▼
Collect Strategy Results
    │
    ▼
Generate Consensus Allocation
    │
    ▼
Apply Execution Mapping
    │
    ▼
Build Portfolio Target
    │
    ▼
Validate Portfolio Target
    │
    ▼
Publish Results
    │
    ▼
Store Execution History
```

---

# Stage 1

## Load Configuration

Purpose:

Load all runtime configuration required for execution.

Inputs:

* Moon Configuration
* Strategy Configuration

Outputs:

* Runtime Configuration

---

# Stage 2

## Load Market Data

Purpose:

Retrieve market data required by all active strategies.

Responsibilities:

* Download prices
* Validate data completeness
* Normalize timestamps

Outputs:

* MarketData

---

# Stage 3

## Load Active Strategies

Purpose:

Load all enabled strategies.

Responsibilities:

* Read configuration
* Instantiate strategy objects
* Validate compatibility

Outputs:

* Strategy Collection

---

# Stage 4

## Execute Strategies

Purpose:

Execute each strategy independently.

Each strategy receives:

* MarketData
* Strategy Configuration

Each strategy produces:

* StrategyResult

Execution order must not affect results.

---

# Stage 5

## Collect Strategy Results

Purpose:

Aggregate all StrategyResult objects.

Responsibilities:

* Verify completion
* Exclude failed strategies
* Prepare for consensus allocation

Outputs:

* StrategyResult Collection

---

# Stage 6

## Generate Consensus Allocation

Purpose:

Combine multiple strategy outputs into a unified strategy-level allocation.

Responsibilities:

* Aggregate allocations
* Sum duplicated assets
* Normalize portfolio weights

Inputs:

* StrategyResult Collection

Outputs:

* ConsensusAllocation

`ConsensusAllocation` represents strategy-level consensus.

It does not represent current portfolio holdings and does not yet represent
the final execution-asset portfolio target.

---

# Stage 7

## Apply Execution Mapping

Purpose:

Translate signal or monitoring assets into the approved execution assets.

Responsibilities:

* Apply explicit execution mappings
* Preserve the strategy result and consensus semantics
* Validate that all mapped assets are executable

The execution mapping is explicit and must not be inferred or replaced by
the implementation.

Inputs:

* ConsensusAllocation
* Execution Mapping

Outputs:

* Execution-asset allocation

Execution Mapping is maintained separately from the strategy calculation.

---

# Stage 8

## Build Portfolio Target

Purpose:

Construct the desired Moon portfolio using execution assets.

Inputs:

* Execution-asset allocation

Outputs:

* PortfolioTarget

`PortfolioTarget` represents the desired portfolio state.

It does not represent current holdings.

---

# Stage 9

## Validate Portfolio Target

Purpose:

Verify portfolio-target integrity before publication.

Validation includes:

* Total allocation equals 100%
* No duplicate execution assets
* No invalid weights
* All assets are executable

Execution stops if validation fails.

The current portfolio state is represented independently by
`PortfolioSnapshot`.

A future rebalance workflow may derive:

```text
PortfolioTarget + PortfolioSnapshot
            ↓
       RebalancePlan
```

`RebalancePlan` describes required portfolio changes and does not execute
trades.

Actual `ExecutionOrder` generation and broker execution are outside the
current Moon MVP scope.

---

# Stage 10

## Publish Results

Purpose:

Expose execution results to downstream consumers.

Consumers:

* Moon Dashboard
* Orion Dashboard
* CLI
* Reporting Services

Published Objects:

* StrategyResult
* ConsensusAllocation
* PortfolioTarget
* ExecutionReport

---

# Stage 11

## Store Execution History

Purpose:

Persist execution results for auditing and historical analysis.

Stored Information:

* Execution Timestamp
* Strategy Results
* Consensus Allocation
* Portfolio Target
* Runtime Duration
* Errors
* Warnings

---

# Error Handling

Pipeline execution distinguishes between recoverable and critical errors.

Recoverable Errors:

* Strategy execution failure
* Missing optional data
* Partial result generation

Critical Errors:

* Configuration failure
* Missing required market data
* Portfolio validation failure

Critical errors terminate the execution pipeline.

---

# Execution Frequency

Default Frequency:

Monthly

Default Schedule:

Last trading day of each month.

Execution timing is controlled by the Orion Runtime.

---

# Relationship with Runtime

The Orion Runtime initiates the execution pipeline.

The Moon Execution Pipeline performs all portfolio generation tasks.

---

# Relationship with Engine

The Moon Engine orchestrates the execution pipeline.

The pipeline defines the sequence of operations performed by the engine.

---

# Future Enhancements

Potential future improvements:

* Parallel strategy execution
* Incremental market updates
* Cached data loading
* Multi-threaded execution
* Distributed execution
* Automatic retry handling

Status:

Research Only

Not Approved

---

# Related Documents

* Orion_Runtime.md
* Moon_Engine.md
* Moon_Object_Model.md
* Moon_Service_Model.md
* Moon_Interface.md
* Moon_Current_Production.md