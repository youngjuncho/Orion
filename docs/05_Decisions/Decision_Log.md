# Orion Decision Log

This document records all material architectural, investment, governance, and operational decisions made within Orion OS.

---

## D-001

### Decision

Moon does not create proprietary investment strategies.

### Rationale

Moon is designed to implement academically researched or publicly validated investment strategies rather than inventing new methodologies.

### Status

Approved

### Date

2026-06-14

---

## D-002

### Decision

Moon is used for actual portfolio rebalancing.

### Rationale

Moon serves as the tactical asset allocation engine of Orion and directly supports investment decisions.

### Details

Rebalancing Frequency:

* Monthly

### Status

Approved

### Date

2026-06-14

---

## D-003

### Decision

Supernova is a long-term equity portfolio based on the 5D Megatrend Framework.

### Details

5D Themes:

* Decoupling
* Deglobalization
* Demographics
* Decarbonization
* Digital Transformation

### Status

Approved

### Date

2026-06-14

---

## D-004

### Decision

Supernova follows a monthly accumulation model.

### Details

Holdings are intended for long-term ownership.

Replacement occurs only when the approved company list changes.

### Status

Approved

### Date

2026-06-14

---

## D-005

### Decision

Phoenix is a digital asset observation and investment framework focused on category leaders outside BTC, ETH, and SOL.

### Initial Watchlist

* TAO
* LINK
* AAVE
* SUI
* RENDER
* WLD
* ONDO

### Status

Draft

### Date

2026-06-14

---

## D-006

### Decision

Rename DAA to BDA.

### Rationale

The strategy operates exclusively within a bond ETF universe and does not represent a generic Dynamic Asset Allocation framework.

The new name improves clarity and reduces ambiguity within Orion documentation.

### Impact

All future references should gradually migrate from DAA to BDA.

### Status

Approved

### Date

2026-06-20

---

## D-007

### Decision

Supernova operates as a long-term Dollar Cost Averaging (DCA) framework.

### Rationale

Short-term market conditions are not considered a reliable basis for timing purchases within long-term megatrend investments.

### Details

Investment Frequency:

* Monthly

Purchases continue regardless of market volatility.

### Status

Approved

### Date

2026-06-20

---

## D-008

### Decision

Moon uses Equal Strategy Weighting.

### Rationale

No single strategy is assumed to be consistently superior.

Equal weighting reduces model risk and prevents discretionary strategy selection.

### Details

All active Moon strategies receive equal portfolio weight.

### Status

Approved

### Date

2026-06-20

---

## D-009

### Decision

Moon allows overlapping asset exposure.

### Rationale

When multiple independent strategies select the same asset, the overlap is interpreted as a stronger consensus signal.

### Details

Asset duplication is not removed.

Repeated selections increase final portfolio weight.

### Status

Approved

### Date

2026-06-20

---

## D-010

### Decision

Moon aggregates strategy outputs through Consensus Allocation.

### Rationale

Final portfolio weights should reflect agreement across independent strategies rather than arbitrary optimization.

### Details

Strategy outputs are combined and normalized to produce final portfolio allocations.

### Status

Approved

### Date

2026-06-20

---

## D-011

### Decision

Aurora is an observational framework and does not generate investment recommendations.

### Rationale

Aurora exists to provide market context rather than act as an investment allocation engine.

This separation preserves the independence of Moon, Supernova, and Phoenix.

### Status

Approved

### Date

2026-06-20

---

## D-012

### Decision

Moon separates signal assets from execution assets.

### Rationale

Academic research and published strategies are defined using
specific benchmark ETFs.

To preserve methodological integrity, signal generation shall
use the original asset universe whenever possible.

Execution may use lower-cost equivalent ETFs.

### Example

Signal Asset:
SPY

Execution Asset:
SPYM

Signal Asset:
BIL

Execution Asset:
SGOV

### Status

Approved

### Date

2026-06-20

---

## D-013

Moon execution ETF mappings shall be reviewed annually.

Review criteria include:

- Expense ratio
- Liquidity
- Assets under management
- Tracking quality
- Tax efficiency

### Date

2026-06-20

---
