# Moon Engine

Version: 1.0

Status: Draft — Runtime vertical-slice integration added

Last Updated: 2026-07-27

Depends On:

* Moon_Object_Model.md
* Moon_Interface.md
* Moon_Service_Model.md

---

# Purpose

This document defines the execution engine of the Moon framework.

The Moon Engine is responsible for coordinating strategy execution, generating consensus allocations, and producing the portfolio recommendation for each rebalance cycle.

The engine does not implement investment logic directly.

Investment decisions remain encapsulated within individual strategies.

---

# Responsibilities

The Moon Engine is responsible for:

* Loading active strategies
* Executing strategy calculations
* Collecting strategy results
* Building consensus allocations
* Producing portfolio recommendations
* Recording execution results

The Moon Engine is not responsible for:

* Market data retrieval
* Portfolio execution
* Order management
* Strategy implementation details

---

# Architecture

```text
Moon Engine

    │

    ├── Strategy Manager

    ├── Strategy Runner

    ├── Consensus Allocator

    ├── Portfolio Builder

    └── Result Publisher
```

---

# Execution Flow

The Moon Engine executes the following sequence:

```text
Load Configuration
        │
Load Active Strategies
        │
Load Market Data
        │
Execute Strategies
        │
Collect Strategy Results
        │
Generate Consensus Allocation
        │
Build Portfolio
        │
Publish Results
```

---

# Strategy Manager

Purpose:

Load and manage all active Moon strategies.

Responsibilities:

* Register strategies
* Enable or disable strategies
* Validate strategy configuration

Output:

Collection of Strategy objects.

---

# Strategy Runner

Purpose:

Execute every active strategy independently.

Input:

* Market Data
* Strategy Configuration

Output:

StrategyResult

Each strategy executes in isolation.

Strategy execution order must not affect results.

---

# Consensus Allocator

Purpose:

Combine all StrategyResult objects into a single portfolio allocation.

Responsibilities:

* Aggregate strategy allocations
* Normalize weights
* Validate total allocation

Output:

PortfolioAllocation

---

# Portfolio Builder

Purpose:

Generate the final Moon portfolio.

Input:

PortfolioAllocation

Output:

Portfolio

Responsibilities:

* Merge duplicate assets
* Normalize final weights
* Validate allocation totals

---

# Result Publisher

Purpose:

Expose Moon Engine results to downstream systems.

Consumers:

* Moon Dashboard
* Orion Dashboard
* CLI
* Reporting Services

---

# Engine Interfaces

## Input

* MarketData
* Strategy Configuration
* Active Strategy List

---

## Output

* StrategyResult
* PortfolioAllocation
* Portfolio
* ExecutionReport

---

# Error Handling

The Moon Engine should continue operating when individual strategies fail.

If a strategy fails:

* Record the error
* Exclude the failed strategy
* Continue execution

Critical system failures should terminate the execution cycle.

---

# Logging

Each execution cycle should record:

* Execution Timestamp
* Active Strategies
* Strategy Results
* Consensus Allocation
* Final Portfolio
* Execution Duration
* Errors

---

# Relationship with Runtime

The Moon Engine is orchestrated by the Orion Runtime.

The Orion Runtime schedules execution.

The Moon Engine performs strategy coordination.

---

# Relationship with Services

The Moon Engine depends on:

* MarketDataService
* StrategyService
* PortfolioService
* ConfigurationService
* EventService

Service implementations are defined in:

* Moon_Service_Model.md

---

# Future Enhancements

Potential future improvements:

* Parallel strategy execution
* Incremental portfolio updates
* Cached market data
* Distributed execution
* Performance profiling

Status:

Research Only

Not Approved

---

# Related Documents

* Moon_Object_Model.md
* Moon_Interface.md
* Moon_Service_Model.md
* Moon_Execution_Pipeline.md
* Orion_Runtime.md

## Runtime Integration Boundary

The existing Moon lifecycle can be exposed to the canonical Runtime without moving
investment methodology into the Runtime layer:

```text
StrategyResult
    ↓
ConsensusAllocation
    ↓
Execution Asset Mapping
    ↓
PortfolioTarget
    ↓
DecisionCandidate
    ↓
Runtime
```

`MoonPortfolioAdapter` performs this translation. It does not accept decisions,
commit state, create execution orders, or execute trades. Acceptance remains an
explicit Runtime decision boundary.

`RebalancePlan` and `ExecutionOrder` require current portfolio state and executable
quantity inputs that are not part of this adapter's contract, so they remain outside
this vertical slice.
