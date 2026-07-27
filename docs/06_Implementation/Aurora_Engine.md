# Aurora Engine

Version: 1.0

Status: Draft

Last Updated: 2026-07-27

Depends On:

* Aurora_Interface.md
* Aurora_Operating_Model.md
* Aurora_Regime_Framework.md
* Aurora_Scoring_Framework.md
* Orion_Runtime.md

---

# Purpose

This document defines the execution engine of the Aurora framework.

The Aurora Engine is responsible for collecting market indicators, evaluating market conditions, calculating component scores, and producing the current market regime.

Aurora provides market context for Orion OS.

Aurora does not generate investment recommendations.

---

# Responsibilities

The Aurora Engine is responsible for:

* Loading market indicators
* Evaluating component scores
* Calculating the Aurora Score
* Determining the Market Regime
* Evaluating State Momentum
* Publishing market conditions

The Aurora Engine is not responsible for:

* Portfolio allocation
* Asset selection
* Order execution
* Strategy implementation

---

# Architecture

```text
Aurora Engine

    │

    ├── Indicator Manager

    ├── Scoring Engine

    ├── Regime Evaluator

    ├── State Analyzer

    └── Result Publisher
```

---

# Execution Flow

The Aurora Engine executes the following sequence:

```text
Load Configuration
        │
Load Market Data
        │
Load Indicators
        │
Calculate Component Scores
        │
Calculate Aurora Score
        │
Determine Market Regime
        │
Evaluate State Momentum
        │
Publish Results
```

---

# Indicator Manager

Purpose:

Load and validate all market indicators required by Aurora.

Responsibilities:

* Retrieve indicator values
* Validate completeness
* Normalize timestamps

Output:

Indicator Collection

---

# Scoring Engine

Purpose:

Calculate normalized scores for each Aurora component.

Components:

* Trend
* Liquidity
* Credit
* Volatility

Output:

Component Scores

---

# Regime Evaluator

Purpose:

Determine the current market regime using the Aurora Score.

Outputs:

* Aurora Score
* Market Regime

Possible Regimes:

* Risk On
* Neutral
* Risk Off

---

# State Analyzer

Purpose:

Evaluate directional changes in market conditions.

Outputs:

* Improving
* Stable
* Deteriorating

State Momentum is evaluated independently of the current market regime.

---

# Result Publisher

Purpose:

Expose Aurora results to downstream systems.

Consumers:

* Aurora Dashboard
* Orion Dashboard
* Moon
* Reporting Services

---

# Engine Interfaces

## Input

* Market Data
* Indicator Configuration
* Scoring Configuration

---

## Output

* Indicator Collection
* Component Scores
* Aurora Score
* Market Regime
* State Momentum
* Execution Report

---

# Error Handling

The Aurora Engine should continue processing when optional indicators are unavailable.

Recoverable Errors:

* Missing optional indicators
* Temporary data source failures

Critical Errors:

* Missing required indicators
* Configuration errors
* Score calculation failures

Critical errors terminate the execution cycle.

---

# Logging

Each execution cycle should record:

* Execution Timestamp
* Indicator Values
* Component Scores
* Aurora Score
* Market Regime
* State Momentum
* Execution Duration
* Errors

---

# Relationship with Runtime

The Orion Runtime schedules Aurora execution.

The Aurora Engine performs all market condition analysis.

---

# Relationship with Services

The Aurora Engine depends on:

* MarketDataService
* IndicatorService
* ConfigurationService
* EventService

---

# Future Enhancements

Potential future improvements:

* Parallel indicator evaluation
* Cached market data
* Historical score comparison
* Confidence scoring
* Automated anomaly detection

Status:

Research Only

Not Approved

---

# Related Documents

* Aurora_Interface.md
* Aurora_Operating_Model.md
* Aurora_Regime_Framework.md
* Aurora_Scoring_Framework.md
* Orion_Runtime.md