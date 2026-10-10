# Orion Common Portfolio Domain Contract

Version: 1.0

Status: Approved contract — partial implementation

## Purpose

Defines the implementation contract for the common Orion Portfolio Domain. This document is a design boundary, not an instruction to implement the full domain immediately.

## Scope

The common domain is shared by the Orion-managed portfolios of Moon, Orbit, Supernova, and Phoenix. It does not model out-of-scope assets or accounts such as Planet KRW, Planet USD, Deep AN/PN/DC, or Asteroid.

## Canonical Objects

### Asset

Represents the identity/reference of an investable instrument. Asset must not contain framework-specific scores, strategy outputs, or portfolio state.

Core fields:

* asset_id
* symbol / identifier
* name
* asset_type
* currency
* status

### Position

Represents the actual holding of an Asset in an Account. Position is the canonical source for quantity. Holding-level market value is derived from Position plus current valuation data.

Core fields currently implemented:

* position_id
* account_id
* asset_id
* quantity

Quantity must be finite and non-negative. NaN and infinity are invalid because
they make valuation results undefined.

### Account

Represents a custody/accounting boundary. An Account contains Positions and a Cash balance. A Portfolio may own one or more Accounts; the canonical relationship is `Account.portfolio_id`.

### Cash

Cash is an Account-level balance, not a normal Position. Portfolio-level cash exposure may be derived from the Account cash balance.

### Portfolio

Represents a logical investment unit managed by an Investment Framework. Portfolio is not synonymous with Account.

Core fields:

* portfolio_id
* framework_id
* name
* status

### PortfolioTarget

Represents the desired allocation for a Portfolio. Target Allocation is canonical here.

Core fields:

* portfolio_id
* effective_date
* allocations
* version

### PortfolioState

Represents the current state of a Portfolio, derived from the relevant Account Positions and Cash at a valuation timestamp.

It may include:

* portfolio_value
* current_allocation
* position references
* cash exposure
* valuation_timestamp
* state/status metadata

Portfolio Value and Current Allocation are derived values, not independent sources of truth.

### PortfolioSnapshot

Represents a historical, time-stamped capture of PortfolioState. It is not the canonical current state.

### RebalancePlan

Represents the changes required to move PortfolioState toward PortfolioTarget.
Each asset may appear at most once in the current-allocation input; duplicate
asset entries are rejected instead of silently overriding an earlier weight.

```text
PortfolioTarget + PortfolioState
            ↓
       RebalancePlan
```

### ExecutionOrder

Represents a concrete trade instruction produced from a RebalancePlan. It is downstream of portfolio decision logic.

`ExecutionSizingInput` is the explicit handoff for already-resolved executable quantities and order identities. The common Portfolio Domain materializes `ExecutionOrder` from those inputs but does not calculate sizing policy, prices, fees, lot sizes, fractional-share rules, or broker constraints.

### Transfer

Represents movement of an asset or value between portfolios/accounts. Transfer is distinct from Rebalance.

```text
Source Portfolio
      ↓
   Transfer
      ↓
Destination Portfolio
```

## Canonical Relationships

```text
Investment Framework
        ↓
    Portfolio
        ↓
     Account
      /    \
 Position  Cash
    ↓
  Asset
```

And the rebalance lifecycle is:

```text
PortfolioTarget
      +
PortfolioState
      ↓
RebalancePlan
      ↓
ExecutionOrder
      ↓
Actual Trade
      ↓
Position / Cash updated
      ↓
New PortfolioState
```

## Framework-Specific Boundary

Moon-specific objects such as StrategyResult and ConsensusAllocation remain inside Moon. They may produce a PortfolioTarget but are not part of the common Portfolio Domain.

Supernova and Phoenix governance objects remain framework-specific. This contract does not redefine their governance models.

## Implementation Constraint

The common Portfolio Domain now owns the canonical `Allocation`, `Portfolio`, and `PortfolioTarget` models. Moon-specific StrategyResult and ConsensusAllocation remain framework-local; Moon does not define a second Portfolio/PortfolioTarget/Validator model.

Orbit and Moon both produce the Common `PortfolioTarget`. Full rebalance/execution lifecycle remains a later implementation step. `ExecutionOrder` is now represented by the canonical common-domain contract; broker execution remains out of scope.
