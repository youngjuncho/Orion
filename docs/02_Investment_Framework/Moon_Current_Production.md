# Moon Current Production

Version: 1.1

Status: Production

Last Updated: 2026-07-27

Depends On:

* Moon_Interface.md
* Moon_Execution_Mapping.md

---

# Purpose

This document describes the current production implementation of Moon within Orion OS.

Unlike research documents, this file represents the actual portfolio construction process currently used in live operation.

Moon is the ETF Tactical Asset Allocation framework of Orion OS.

---

# Objective

Moon exists to answer a single question:

"What should be held right now?"

The framework seeks to:

* Preserve capital during adverse market conditions
* Participate in major market trends
* Allocate capital systematically
* Reduce discretionary decision making

---

# Investment Universe

Moon invests exclusively through ETFs.

Moon does not invest in:

* Individual Stocks
* Cryptocurrencies

Signal generation uses the original research universe.

Execution ETFs may differ according to:

Moon_Execution_Mapping.md

Principle:

Signal Integrity Has Priority Over Execution Convenience.

---

# Active Strategies

Current production strategies:

* ADM
* BAA
* BDA
* HAA
* VAA

All strategies are evaluated monthly.

Each strategy receives equal portfolio weight.

Moon does not apply discretionary weighting between strategies.

---

# Strategy Weighting

Each active strategy receives equal weight.

Example:

If five strategies are active:

* ADM = 20%
* BAA = 20%
* BDA = 20%
* HAA = 20%
* VAA = 20%

No strategy receives discretionary priority.

---

# Asset Weighting

Within each strategy, selected assets receive equal weight.

Example:

BAA selects:

* SPY
* QQQ

Result:

* SPY = 50%
* QQQ = 50%

within BAA.

---

# Aggregation Method

Moon uses Strategy Consensus Allocation.

Strategy results are aggregated into a unified portfolio allocation.

Assets selected by multiple strategies naturally receive larger portfolio weights.

Example:

ADM:

* SPY

BAA:

* SPY
* QQQ

Strategy Weights:

* ADM = 50%
* BAA = 50%

Final Allocation:

* SPY = 75%
* QQQ = 25%

---

# Execution Mapping

Moon separates signal generation from execution.

Signal Assets are used for:

* Research
* Backtesting
* Signal Generation

Execution Assets are used for:

* Portfolio Implementation
* Rebalancing
* Order Generation

Execution mapping is defined in:

Moon_Execution_Mapping.md

Signal generation always remains the canonical reference.

---

# Rebalancing

Frequency:

Monthly

Execution Window:

Last trading day of each month

Execution Process:

1. Execute all strategies
2. Generate Strategy Results
3. Aggregate Consensus Allocation
4. Translate Signal Assets into Execution Assets
5. Generate Final Portfolio Allocation
6. Rebalance Portfolio

---

# Role Within Orion

Moon is responsible for:

* Tactical Asset Allocation
* ETF Selection
* Portfolio Construction
* Risk Management

Moon does not:

* Select individual stocks
* Manage cryptocurrencies
* Predict macroeconomic events

Those responsibilities belong to other Orion frameworks.

---

# Relationship With Other Frameworks

Aurora

Provides market context.

Aurora does not override Moon strategy execution.

---

Moon

Constructs and manages the ETF portfolio.

---

Supernova

Manages long-term individual equity accumulation independently.

---

Phoenix

Manages digital asset allocation independently.

---

Each framework operates independently according to its own investment methodology.

---

# Governance

Changes to:

* Strategy Set
* Strategy Weighting
* Consensus Methodology
* Rebalancing Rules
* ETF Universe
* Execution Mapping

must be recorded in:

docs/05_Decisions/Decision_Log.md

before implementation.

Moon governance is defined in:

docs/02_Investment_Framework/Moon_Governance.md

All material changes require:

* Documentation Update
* Decision Log Entry
* Governance Approval

---

# Related Documents

* Moon_Interface.md
* Moon_Execution_Mapping.md
* Moon_Scoring_Framework.md
* ADM_Orion.md
* Orion_Glossary.md

---

# Status

Status:

Production

Version:

Moon Production v1