# VAA Orion Implementation Specification

Version: 1.1

Status: Research implementation candidate; not production-approved

Last Updated: 2026-10-18

Depends On:

* VAA_Research.md
* docs/02_Investment_Framework/Moon/Moon_Current_Production.md
* docs/02_Investment_Framework/Moon/Moon_Object_Model.md
* docs/06_Implementation/Moon_Interface.md

---

# Purpose

This document defines the Orion-specific implementation of the VAA strategy.

While VAA_Research.md preserves the original Keller methodology, this document specifies how VAA is implemented within Orion OS.

The implementation follows the standard Moon Strategy interface and produces a StrategyResult consumed by the Moon Consensus Allocation engine.

---

# Implementation Principles

## Original First

The original VAA methodology remains the reference implementation.

---

## Practical Execution

The Orion implementation prioritizes:

* Simplicity
* ETF availability
* Monthly execution
* Research reproducibility

---

# Orion VAA Universe

## Source-Method Signal Universe — VAA-G12

Offensive assets: `SPY, IWM, QQQ, VGK, EWJ, VWO, VNQ, GSG, GLD, TLT, HYG, LQD`.

Defensive assets: `SHY, IEF, LQD`.

Parameters: `T=2`, `B=4`. These are the source-method signal assets and
parameters documented in `VAA_Research.md`. They are not a declaration that
all assets have approved Orion execution mappings.

## Execution Mapping Boundary

Execution assets must follow
`docs/02_Investment_Framework/Moon/Moon_Execution_Mapping.md`. No mapping is
created by this specification. Unsupported signal tickers must fail closed
until the mapping is reviewed and recorded in the Decision Log.

# Data Source

Primary Source

Yahoo Finance

Reason:

* Free
* Reliable
* Python ecosystem support

---

Backup Sources

* Stooq
* Alpha Vantage
* Polygon

Status:

Future Review

---

# Evaluation Schedule

## Evaluation Frequency

Monthly

---

## Evaluation Date

Last Trading Day

---

## Execution Date

Next Trading Day

---

# Strategy Interface

VAA implements the standard Moon Strategy interface.

Input:

* Market Data
* Strategy Configuration

Output:

* StrategyResult

The StrategyResult is consumed by the Moon Consensus Allocation engine.

Reference:

docs/06_Implementation/Moon_Interface.md

---

# Breadth Evaluation

Count `b` across the complete 12-asset offensive universe where the 13612W
score is non-positive (`<= 0`). For VAA-G12, `B=4`. The source linear cash
fraction is `min(1, b/B)`; the selected Easy Trading candidate rounds this to
whole `1/T` position units with `T=2`, yielding 0%, 50%, or 100% defensive.

The method definition is source-verified. Independent historical replication,
market-data freshness controls, and production approval remain open.

---

# Momentum Calculation

Use total-return-adjusted monthly prices and `13612W = 12×R1 + 4×R3 + 2×R6 + R12`,
where `Rk = P(t)/P(t-k) - 1`. Use this same score to rank offensive and
defensive assets and to count offensive scores `<= 0`. The code accepts adjusted
close inputs, so the upstream provider's adjustment semantics and monthly
observation selection must be validated before production use.

Source-method formula: documented. Independent numerical replication and
provider-data validation: open.

---

# Asset Selection

Purpose:

Generate a StrategyResult containing the selected offensive and/or defensive assets.

The StrategyResult is passed to the Moon Consensus Allocation engine.

---

If Breadth Conditions are Favorable:

Allocate to the highest-ranked offensive assets.

---

If Breadth Conditions are Deteriorating:

Allocate partially or fully to defensive assets.

---

Number of Selected Assets:

`T=2` for the VAA-G12 + Easy Trading candidate. In Risk On, hold the top two
offensive assets equally. In Partial Defense, hold the top offensive asset and
top non-duplicated defensive asset equally. In Defensive, hold the top defensive
asset only. This candidate behavior is implemented in `vaa.py`; it is not a
production authorization.

---

# Signal Universe

Use the VAA-G12 source-method signal universe listed above without silently
substituting execution tickers. The offensive and defensive universes may share
`LQD`; this overlap is part of the source definition.

Signal integrity has priority over execution convenience.

---

# Execution Universe

Execution assets follow
`docs/02_Investment_Framework/Moon/Moon_Execution_Mapping.md` only when an
explicit approved mapping exists. The examples previously listed here mixed
other candidate universes with VAA-G12 and are removed to avoid implying that
those substitutions are approved. Any unsupported VAA signal ticker must fail
closed until a mapping is reviewed and recorded in the Decision Log.

---

# State Model

## Risk On

Condition:

Breadth conditions are favorable.

Output:

State:
Risk On

Universe:
Offensive

---

## Partial Defense

Condition:

Some offensive assets exhibit negative momentum.

Output:

State:
Partial Defense

Universe:
Mixed

---

## Defensive

Condition:

Broad market weakness detected.

Output:

State:
Defensive

Universe:
Defensive

---

# Moon Dashboard Output

Example

Strategy:
VAA

Selected Assets:

SPY

EEM

State:
Risk On

Breadth:
Healthy

Rebalance Date:
2026-06-30

Next Action:
Hold

---

# CLI Output

Command

orion moon vaa

Example

VAA

State:
Risk On

Breadth:
Healthy

Selected Assets:

SPY

EEM

Next Rebalance:

2026-06-30

---

# Dashboard Score

VAA contributes to the Moon Dashboard.

Score Calculation:

Not Yet Defined

Future Document:

Moon_Scoring_Framework.md

Status:

Pending

---

# Rebalancing Policy

Default Frequency

Monthly

---

Forced Rebalance

Not Allowed

---

Manual Override

Not Allowed

---

# Logging Requirements

Every rebalance event must store:

* Date
* StrategyResult
* Selected Assets
* Previous Assets
* Breadth Score
* Momentum Values

---

# Known Open Issues

OI-401 — Independent historical replication of the source-method signal and
Easy Trading rounding. Status: Open.

OI-402 — Provider data adjustment semantics, month-end trading-date alignment,
source provenance, and freshness SLA. Status: Open.

OI-403 — Review and approval of signal-to-execution mappings for every ticker.
Status: Open; unsupported mappings must fail closed.

OI-404 — Governance approval and activation criteria. Status: Open.

OI-405 — Resolve terminology references in any remaining docs or reports:
use “Easy Trading (ET)” for the source's whole-position rounding variant; do
not use “Easy Investing” unless a distinct, citable methodology is identified.
Status: Documentation reconciliation.

# Approval Status

Research method definition: Source-verified for VAA-G12 + Easy Trading.

Independent backtest/data validation: In Progress / Open.

Implementation: Research candidate; code and unit tests exist.

Production approval and activation: Not approved. `config/moon.yaml` remains
inactive for VAA, and no execution mapping or governance approval is inferred.

---

# Related Documents

* Moon_Current_Production.md
* Moon_Object_Model.md
* Moon_Interface.md
* Moon_Execution_Mapping.md
* Moon_Scoring_Framework.md
## Current Orion Working Rule — G12 + Easy Trading

This section records the current implementation candidate; it does not activate
VAA or authorize new execution-ETF mappings.

### Momentum score

Use monthly adjusted closes from the last completed month-end. For asset price
series `P`, calculate `13612W = 12 × R1 + 4 × R3 + 2 × R6 + R12`, where
`Rk = P(t) / P(t-k) - 1`. The input series must contain at least 13 monthly
observations, ordered oldest to newest. Missing observations, invalid prices, or
incomplete universes fail closed; no universe shrinking is permitted.

### G12 universes

Offensive: `SPY, IWM, QQQ, VGK, EWJ, VWO, VNQ, GSG, GLD, TLT, HYG, LQD`.
Defensive: `SHY, IEF, LQD`.

### Easy Trading breadth rule

Let `b` be the count of offensive assets whose 13612W score is less than or
equal to zero. With `T=2` and `B=4`, the defensive fraction is
`min(1, floor(b × T / B) / T)`: `b=0–1` gives 0%, `b=2–3` gives 50%, and
`b>=4` gives 100% defensive allocation. The allocation is two top-ranked
offensive assets at 50% each, one top-ranked offensive plus one top-ranked
non-duplicated defensive asset at 50% each, or the top-ranked defensive asset
at 100%, respectively. Rank ties follow the declared universe order. `LQD`
overlaps both universes, so mixed-mode selection explicitly skips a defensive
asset already selected offensively.

### Scope and execution gate

The signal implementation is separate from market-data retrieval and execution
mapping. The upstream data layer must supply complete, date-aligned monthly
adjusted-close observations for every required ticker and enforce month-end
selection/freshness. The signal date is the completed observation date; actual
execution is a later trading-day concern and is not inferred by this module.

The existing execution mapping is intentionally unchanged. `VGK`, `EWJ`, `VWO`,
and `GSG` do not all have approved signal-to-execution mappings in the current
mapping table. Until mappings are reviewed and recorded in the Decision Log,
execution mapping should continue to fail closed for unsupported tickers.
`config/moon.yaml` remains inactive for VAA.



## Dated Monthly Adjusted-Close Input Builder — Engineering Candidate

`build_vaa_signal_input()` now converts a mapping of ticker to ordered
`(observation_date, adjusted_close)` pairs into a complete `VAASignalInput`.
It requires all unique G12/defensive tickers, at least 13 observations per
ticker, strictly increasing dates, no missing calendar months, a common set of
observation dates, and a latest observation in the last completed calendar
month before `as_of_date`. It computes the 13612W scores only after these
checks pass.

This is a pure validation/calculation boundary: it does not fetch prices,
verify exchange calendars, define a numeric publication-age SLA, infer the
next execution session, persist source provenance, or activate VAA. The
month-end fixture tests use calendar month-end dates; production provider data
will normally label observations with the last trading day of each month.
The caller must supply consistent month-end trading observations and should
not pass an incomplete current-month bar.
