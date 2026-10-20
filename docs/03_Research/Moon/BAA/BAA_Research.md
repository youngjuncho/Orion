# BAA Research Specification

Version: 1.5

Status: Research

Author:

Wouter Keller

Publication:

Bold Asset Allocation

Last Updated:

2026-10-20

---

# Overview

BAA (Bold Asset Allocation) is a tactical asset allocation framework developed by Wouter Keller. The framework combines a Canary regime filter with momentum-based selection from offensive or defensive asset universes.

This document defines the **BAA-G12 research baseline**. Other variants, including BAA-G4 and third-party adaptations, must be documented and evaluated separately rather than blended into this specification.

# Source Material

Primary reference:

- Wouter Keller, *Bold Asset Allocation* (2022)

Research cross-checks:

- Public summaries and implementations describing BAA-G12 and BAA-G4

Source limitation:

- Before claiming exact numerical replication of Keller's published results, verify formulas, price-adjustment conventions, and test assumptions against the primary paper and its accompanying data/code, where available.
- Third-party implementations are cross-checks, not substitutes for the primary methodology.

---

# Research Objective

Determine whether capital should be allocated to:

- Offensive Assets during Risk-On conditions
- Defensive Assets during Risk-Off conditions

The original methodology must be documented before Orion-specific modifications are introduced.

Principle: **Original First, Customization Later.**

---

# BAA-G12 Investment Universes

## Canary Universe

Used to determine the market regime:

- SPY
- VWO
- VEA
- BND

## Offensive Universe

Used during Risk-On conditions; select the six highest-ranked assets:

- SPY
- QQQ
- IWM
- VGK
- EWJ
- VWO
- VNQ
- DBC
- GLD
- TLT
- HYG
- LQD

## Defensive Universe

Used during Risk-Off conditions; select the three highest-ranked assets before applying the BIL floor rule:

- TIP
- DBC
- BIL
- IEF
- TLT
- LQD
- BND

## BAA-G4 distinction

BAA-G4 is a separate variant, not a shortened name for the G12 offensive universe. Its offensive universe is QQQ, VWO, VEA, and BND. The Canary universe remains SPY, VWO, VEA, and BND. Do not substitute the G4 universe into G12 tests.

---

# Input Data Contract (Orion Research Prototype)

The Orion prototype consumes 13 monthly observations (the signal month plus the prior 12 months) for every asset in the BAA-G12 required universe. Its canonical-dataset builder accepts only `adjusted_close` observations denominated in USD and requires exactly one observation for each required asset in every target calendar month. It rejects missing months, duplicate monthly observations, nonnumeric or non-positive values, and the current `as_of` month. It does not forward-fill, interpolate, or silently substitute raw close.

This is a structural input contract, not evidence of exact paper replication. Calendar-month bucketing does not establish that an observation is the final trading-session price, and the adjusted-close field has not yet been validated as equivalent to the paper's dividend-adjusted / total-return series. Provider selection, data freshness, source-history revisions, and month-end signal finalization remain open.

# Momentum Measures

## 13612W Canary Momentum

For month-end price `P_t`, define:

```text
M13612W(t) =
    12 * (P_t / P_(t-1)  - 1)
  +  4 * (P_t / P_(t-3)  - 1)
  +  2 * (P_t / P_(t-6)  - 1)
  +      (P_t / P_(t-12) - 1)
```

The unnormalized weighted sum is sufficient for the sign test; dividing by the sum of weights does not change its sign.

## SMA(12) Relative Momentum

For ranking assets, use the price relative to the average of the current month-end price and the preceding 12 month-end prices:

```text
SMA12_Momentum(t) = P_t / mean(P_t, P_(t-1), ..., P_(t-12)) - 1
```

Rank each asset universe in descending order by this measure.

## Provider comparison status

`BAA_Data_Source_Assessment.md` compares Alpha Vantage monthly-adjusted data with Yahoo Finance accessed through `yfinance`. Alpha Vantage is the first candidate to validate because the official API explicitly documents last-trading-day monthly bars and adjusted-close/dividend fields. Yahoo Finance may be used as an independent comparison series only after its usage terms and `yfinance` configuration/version are pinned. This is not empirical validation: no API calls or symbol-by-symbol lookups have been performed, and neither provider is approved as the BAA total-return source.

A provider must pass all-17-symbol identity/history checks, monthly timestamp validation against daily observations, and adjusted-return comparisons around distribution/split events. Do not combine sources in a signal window or silently fall back to raw close.

## Price-data convention

The primary paper describes momentum calculations using dividend-adjusted / total-return (TR) monthly prices. For faithful replication, prefer a consistently constructed total-return price series across assets and the full test period.

- A vendor's adjusted-close field may be a practical proxy, but it must not automatically be assumed identical to the paper's TR series.
- Record the provider, field definition, corporate-action treatment, currency, and monthly sampling rule.
- Validate the chosen series against the primary paper/data where possible before treating performance as replicated.
- Raw unadjusted close is not an acceptable default for replication where distributions or splits would distort returns.

---

# Decision and Selection Rules

## Regime decision

Calculate 13612W for each Canary asset:

- **Risk-Off:** at least one Canary asset has 13612W below zero.
- **Risk-On:** all four Canary assets have 13612W greater than or equal to zero.

A missing or invalid Canary observation must not silently be interpreted as a healthy signal. The operational fallback for missing data is an Orion implementation policy and remains to be approved.

## Risk-On selection

1. Calculate SMA(12) relative momentum for the 12 Offensive assets.
2. Rank in descending order.
3. Select the top six assets.
4. Assign equal target weights to the selected assets.

## Risk-Off selection

1. Calculate SMA(12) relative momentum for the seven Defensive assets.
2. Rank in descending order and take the top three.
3. For each selected asset whose absolute 13612W momentum is below BIL's 13612W momentum, replace that asset with BIL.
4. Apply the BIL floor to each selected slot whose absolute 13612W momentum is below BIL's 13612W momentum. SMA(12) is still used to rank the Defensive universe.
5. The primary method uses SMA(12) to rank the Defensive universe and a separate absolute-momentum test (13612W) to compare each selected defensive asset with BIL. The source rule confirms replacement by BIL, but the accessible primary-source text does not unambiguously specify how duplicate BIL slots are represented in a holdings table. For Orion, the approved accounting convention is to preserve three equal-weight slots (one-third each), map every replaced slot to BIL, and aggregate weights for duplicate tickers. This is mathematically equivalent to holding the same total allocation while listing BIL only once. It is an explicit Orion representation policy, not a claim that the primary source spells out duplicate-ticker aggregation.

---

# Evaluation Convention

The research signal is calculated from monthly observations. The operational convention for when month-end data is considered final and when a trade may be executed belongs in `BAA_Orion.md`.

A backtest must avoid look-ahead bias: a signal may only use data available at the signal calculation time, and execution prices must reflect the declared execution convention.

---

# Known Limitations and Replication Checks

Results can differ due to:

- Price adjustment and dividend-reinvestment conventions
- Month-end data availability and holiday handling
- Missing or invalid observations
- Transaction costs, spreads, and execution-price assumptions
- Tie-breaking and the exact BIL replacement / weight-allocation behavior
- Differences between Keller's original methodology and third-party variants

Published performance figures must not be presented as replicated until these assumptions are aligned and tested.

---

# Research Questions

## RQ-101 — Final Canary Universe Definition

Status: Defined for BAA-G12 baseline; primary-source replication check pending.

Definition: SPY, VWO, VEA, BND.

## RQ-102 — Exact Momentum Formula

Status: Formula documented; primary-source replication check pending.

Definition: 13612W for Canary regime detection and SMA(12) for relative ranking, as specified above.

## RQ-103 — Final Offensive Universe

Status: Defined for BAA-G12 baseline; primary-source replication check pending.

Definition: SPY, QQQ, IWM, VGK, EWJ, VWO, VNQ, DBC, GLD, TLT, HYG, LQD.

## RQ-104 — Final Defensive Universe

Status: Defined for BAA-G12 baseline; primary-source replication check pending.

Definition: TIP, DBC, BIL, IEF, TLT, LQD, BND.

## RQ-105 — Number of Assets Selected

Status: Selection count and duplicate-slot accounting convention documented; aggregation preserves three equal-weight slots and is an approved Orion output representation policy.

Definition: six Offensive assets in Risk-On; three Defensive slots before BIL replacement in Risk-Off. Defensive ranking uses SMA(12), while the BIL floor compares each selected asset's 13612W absolute momentum with BIL's 13612W absolute momentum. When more than one slot maps to BIL, aggregate the resulting equal-slot weights into one BIL holding. This is the approved Orion output representation policy, not a separately verified source instruction.

## RQ-107 — Price series convention

Status: Primary paper indicates dividend-adjusted / total-return monthly prices; exact vendor-series equivalence remains to be validated.

Definition: use a consistent TR price series for replication. Adjusted close may be evaluated as a proxy, but must not be presumed identical without validation.

## RQ-106 — Keller original methodology versus Easy Investing implementation

Status: Open.

Action: Compare version-specific universes, formulas, selection rules, execution assumptions, and performance methodology. Do not treat the variants as interchangeable.

---

# Research-Only Code and Tests

A first isolated signal-calculation prototype is available in `src/orion/frameworks/moon/baa.py`, with regression coverage in `tests/orion/frameworks/moon/test_baa.py`. It implements the documented G12 universes, 13612W and SMA(12) calculations, Canary regime selection, defensive BIL absolute-momentum replacement, and target weights.

Scope and limitations:

- The module accepts caller-supplied monthly price series; the canonical input builder requires a verified-final-session metadata attestation and cross-symbol date alignment, but does not independently validate the upstream attestation, fetch live provider data, or prove total-return semantics.
- It is not registered in the Moon runtime, does not perform execution-asset mapping, and cannot submit orders.
- Duplicate BIL slots are aggregated into a unique ticker with the corresponding combined weight under the approved Orion output representation policy.
- Passing unit tests establishes behavior against the current specification, not historical performance replication or approval for live use.

# Research Conclusion

The BAA-G12 rule baseline is now documented for continued research. It is not yet an approved live strategy and has not been performance-replicated in Orion.

Orion-specific data handling, execution behavior, missing-data handling, and operational controls are specified separately in `BAA_Orion.md`.

# Next Document

`BAA_Orion.md`

Purpose: Define Orion-specific implementation behavior while preserving the research baseline above.
