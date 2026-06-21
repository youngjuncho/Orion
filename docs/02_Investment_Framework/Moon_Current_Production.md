# Moon Current Production

## Purpose

This document describes the current production implementation of Moon within Orion OS.

Unlike research documents, this file represents the actual portfolio construction process currently used in live operation.

Moon is the ETF-based Tactical Asset Allocation framework of Orion.

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

No individual stocks are allowed.

No cryptocurrencies are allowed.

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

All strategies receive equal portfolio weight.

Moon does not apply discretionary weighting between strategies.

---

# Strategy Weighting

Each strategy receives equal portfolio weight.

Example:

If five strategies are active:

* ADM = 20%
* BAA = 20%
* BDA = 20%
* HAA = 20%
* VAA = 20%

No strategy is given discretionary priority.

---

# Asset Weighting

Within each strategy, selected assets receive equal weight.

Example:

BAA selects:

* SPY
* QQQ

Then:

* SPY = 50%
* QQQ = 50%

within BAA.

---

# Aggregation Method

Moon uses Strategy Consensus Allocation.

Final asset weights are calculated by aggregating contributions from all active strategies.

Example:

ADM:

* SPY

BAA:

* SPY
* QQQ

Strategy Weights:

* ADM = 50%
* BAA = 50%

Result:

* SPY = 75%
* QQQ = 25%

Assets selected by multiple strategies naturally receive higher portfolio weights.

---

# Rebalancing

Frequency:

Monthly

Execution Window:

Last trading day of each month

Process:

1. Execute all strategies
2. Collect selected ETFs
3. Calculate strategy contributions
4. Aggregate final asset weights
5. Rebalance portfolio

---

# Role Within Orion

Moon is responsible for:

* Tactical Asset Allocation
* ETF Selection
* Risk Management

Moon does not:

* Select individual stocks
* Manage cryptocurrencies
* Predict macroeconomic events

Those functions belong to other Orion frameworks.

---

# Relationship With Other Frameworks

Moon:

ETF Tactical Allocation

Supernova:

Individual Equity Accumulation

Phoenix:

Digital Asset Allocation

Aurora:

Market Climate Monitoring

Each framework operates independently.

---

# Governance

Changes to:

* Strategy set
* Weighting methodology
* Rebalancing rules
* ETF universe

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

# Status

Status:

Production

Version:

Moon Production v1
