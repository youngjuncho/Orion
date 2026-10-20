# BAA Orion Implementation Specification

Version: 1.5

Status: Draft — Research Baseline Documented; Implementation Policies Pending

Last Updated: 2026-10-20

Depends On:

- `BAA_Research.md`
- `Moon_Current_Production.md`
- `Moon_Object_Model.md`

---

# Purpose

This document specifies how BAA is represented as a Moon strategy within Orion OS. `BAA_Research.md` defines the BAA-G12 research baseline; this document defines the Orion integration boundary and operational policies.

Documenting a rule here does not authorize code changes, scheduling, runtime activation, or live trading. Those actions require separate approval.

---

# Role Within Moon

BAA is an independent Moon strategy. Its responsibility is to:

- Load the required market data
- Evaluate Canary conditions
- Calculate momentum measures
- Rank candidate assets
- Select target assets and weights
- Produce a `StrategyResult`

BAA does not:

- Aggregate portfolio allocations
- Execute trades
- Apply execution asset mappings

Those responsibilities belong to the Moon Engine.

---

# Strategy Lifecycle

```text
Load Market Data
      ↓
Validate Data Coverage
      ↓
Evaluate Canary Conditions
      ↓
Calculate Momentum
      ↓
Rank Candidate Assets
      ↓
Select Target Assets and Weights
      ↓
Generate StrategyResult
```

---

# Research Baseline Reference

Unless an explicitly versioned alternative is approved, BAA research and backtests use the BAA-G12 baseline defined in `BAA_Research.md`.

- Canary universe: SPY, VWO, VEA, BND
- Offensive universe: the 12 assets defined in `BAA_Research.md`
- Defensive universe: the seven assets defined in `BAA_Research.md`
- Canary measure: 13612W
- Relative ranking: SMA(12)
- Risk-On selection: top six Offensive assets, equal weight
- Risk-Off selection: top three Defensive assets, with the BIL replacement rule

Do not use the prior draft's seven-asset Offensive list or four-asset Defensive list as if they were the BAA-G12 original universe. Any reduced universe must be separately named, justified, and tested as an Orion variant.

---

# Data Source and Data Quality

Provider decision: **not approved**. The current documented comparison recommends validating Alpha Vantage first as the primary research candidate and using Yahoo Finance via `yfinance` only as an independent comparison series. This is a research priority, not a provider approval. See `BAA_Data_Source_Assessment.md` for the same-17-symbol comparison and empirical validation checklist.

The existing Alpha Vantage implementation is configured for ADM symbols and is not a BAA provider integration. Neither source has yet been queried for all 17 BAA symbols in this assessment. Do not treat provider capability documentation as evidence of symbol coverage or numerical total-return equivalence.

## Research Input Contract (Implemented; Not a Provider Integration)

`build_baa_signal_input()` in `src/orion/frameworks/moon/baa.py` converts an already normalized `data.contracts.MarketDataSet` into the 13-month input required by the research calculator. It currently enforces:

- explicit `signal_month` in `YYYY-MM` format and an ISO-date `dataset.as_of`; the signal month must precede the dataset's `as_of` month so the current potentially incomplete month is not accepted;
- exactly one `adjusted_close` observation per required asset in each of the 13 calendar-month buckets ending at the requested signal month;
- numeric, finite, positive values and `USD` currency;
- fail-closed behavior for missing months, duplicate monthly observations, invalid dates, wrong currency, and attempts to substitute raw `close`.

The builder aligns observations by calendar month and additionally requires `month_end_session_verified=true` for every selected observation. It rejects missing attestations and any month in which the required symbols do not share one observed date. The flag must be set only after an upstream adapter or validation step verifies the final valid US market trading session. The builder does not independently prove the attestation truthful, validate source freshness or provider identity, or certify `adjusted_close` as a total-return series. Those remain source-contract and governance gates. The caller must provide a complete dataset and a historical/completed `signal_month`. No provider is called and no missing data is filled.

## Policies Pending Approval

1. **Price series:** The primary paper describes dividend-adjusted / total-return (TR) monthly prices. Use a consistent TR series for replication where available; adjusted close is only a candidate proxy until its semantics are validated against the chosen source.
2. **Insufficient history:** Do not generate a new signal if the required 12-month lookback is incomplete.
3. **Missing/invalid Canary data:** Do not treat missing data as a positive Canary signal. Suppress the new signal and raise an explicit data-quality status until a fallback policy is approved.
4. **Candidate data gaps:** Define whether an individual candidate is excluded, the signal is suppressed, or a prior target is retained. No silent fallback.
5. **Source fallback:** No automatic cross-provider fallback is approved. If a selected provider returns incomplete or invalid data, suppress the new signal and report a data-quality failure unless a future policy explicitly authorizes another behavior.
6. **Provider validation:** Before choosing a provider, confirm all 17 symbol identities and history ranges, audit monthly timestamps against daily bars, and compare adjusted-return ratios around dividend/split events. Do not assume Yahoo and Alpha Vantage adjusted series are numerically interchangeable.

---

# Evaluation and Execution Timing

Intended cadence: monthly.

Approved monthly signal-date and observation convention:

- Evaluation period: label the review month as `YYYY-MM` separately from the actual observation date.
- Signal date: use the last valid US market trading session of the month, after that session has closed and the data has been validated.
- Input builder: every required symbol/month observation must carry `month_end_session_verified=true` metadata from a source adapter or validation step that verified the session date. All required symbols must share one observed session date within each month. Missing attestation or inconsistent dates fails closed.
- The resulting `signal_date` is the verified observation date for the target month, not the calendar month's final calendar date.
- Execution date: no execution policy is implemented or authorized. Any future backtest must not assume a close-based signal can be filled at the same close without a separately justified execution model.

Status: **Signal-date convention approved for research input validation.** This metadata attestation is a required gate, not independent proof of provider correctness. Provider validation, data-finalization timing, timezone details, and any execution policy remain separate and unresolved.

---

# Signal Calculation and Selection

The formulas and portfolio-selection rules are maintained in `BAA_Research.md` to avoid divergent copies.

A research-only calculation prototype and canonical-dataset input builder exist at `src/orion/frameworks/moon/baa.py`, with tests at `tests/orion/frameworks/moon/test_baa.py`. They are deliberately not registered with the Moon runtime and have no provider-fetch or execution integration. The prototype applies the approved duplicate-BIL aggregation convention solely as a research output representation policy; this does not approve runtime integration.

The eventual strategy implementation must:

1. Validate required observations before calculating signals.
2. Record the signal date and data window.
3. Apply the Canary regime rule exactly as specified by the selected BAA version.
4. Apply relative-momentum ranking within the correct universe.
5. Apply selection, BIL replacement, and target-weight rules deterministically.
6. Emit explicit diagnostics when a signal cannot be produced.

The source rule uses SMA(12) to rank the Defensive universe, then replaces a selected defensive asset with BIL if that asset's absolute 13612W momentum is below BIL's 13612W momentum. The exact representation of duplicate BIL slots is not unambiguously established from the accessible source text. Approved Orion output convention: preserve three equal-weight slots, map each replacement to BIL, and aggregate duplicate BIL weights in the final target. This is an explicit portfolio-reporting convention, not a claim that the source separately specifies duplicate-ticker accounting.

---

# Signal Universe and Execution Universe

Signal generation uses the research ETF universe defined by the selected BAA version. Signal integrity takes priority over execution convenience.

Execution assets are resolved by the Moon Engine using `Moon_Execution_Mapping.md` after `StrategyResult` generation.

Existing mapping examples include:

- SPY → SPYM
- QQQ → QQQM
- EEM → VWO
- DBC → BCI
- BIL → SGOV

These are examples only; validate them against the current mapping document before use. The execution mapping must not change the signal universe or momentum calculation.

---

# Strategy Output

BAA produces a `StrategyResult` containing at minimum:

- Strategy name and version
- Signal date
- Regime state (`Risk On` or `Risk Off`)
- Canary values and status
- Selected signal assets
- Target weights
- Momentum values and ranks
- Data-quality / suppression status
- Metadata sufficient to reproduce the decision

Example (illustrative only):

```text
Strategy: BAA-G12
Signal Date: YYYY-MM-DD
State: Risk On
Selected Assets: <selected signal tickers>
Target Weights: <weights summing to 100%>
```

---

# State Model

## Risk On

Condition: all required Canary observations are valid and all four Canary 13612W values are non-negative.

Universe: Offensive.

## Risk Off

Condition: all required Canary observations are valid and at least one Canary 13612W value is negative.

Universe: Defensive.

## Signal Suppressed

Condition: required data is missing, invalid, or insufficient, or another precondition for a valid calculation is not met.

Action: do not fabricate a Risk-On/Risk-Off result. The operational response (including whether the prior target is retained) requires explicit policy approval.

---

# Rebalancing Policy

- Evaluation frequency: monthly manual review (approved operating cadence); no scheduler or automatic execution.
- Forced rebalance: not allowed.
- Manual override: not allowed under the current draft policy.
- Signal generation and portfolio-level rebalancing are separate operations.

Any change to these rules requires an explicit strategy-policy decision.

---

# Logging Requirements

Each evaluation should record:

- Strategy name and version
- Signal date and data availability timestamp
- Data source and price-series convention
- Canary momentum values and regime result
- Candidate momentum values, ranks, and exclusion reasons
- Selected signal assets and target weights
- BIL replacements and resulting weights
- Data-quality warnings or signal-suppression reason
- Previous target and current target, where available

---

# Known Open Issues

## OI-101 — Primary-source replication check

Status: Open.

Verify the documented BAA-G12 formulas and universes against Keller's primary paper/source materials.

## OI-102 — Price-series convention

Status: Partially resolved; provider implementation remains open.

The primary paper describes dividend-adjusted / total-return monthly prices. Prefer a consistent total-return series for replication. Validate whether the chosen vendor's adjusted-close field is equivalent enough for this purpose; do not silently treat raw close or vendor-adjusted close as the primary paper's exact series.

## OI-103 — Month-end signal finalization and next-session execution

Status: Open.

Specify calendar, timezone, data cutoff, and execution assumptions.

## OI-104 — Missing data and source fallback

Status: Open.

Approve fail-safe behavior for missing Canary data, candidate gaps, insufficient history, and provider discrepancies.

## OI-105 — Defensive BIL replacement edge cases

Status: SMA(12) ranking plus 13612W absolute-momentum BIL floor documented; duplicate-slot representation and weight aggregation are pending Orion policy approval.

The source ranks Defensive assets by SMA(12), then compares selected assets' absolute 13612W momentum with BIL's 13612W momentum. The research-only prototype applies the replacement rule and aggregates duplicate BIL slots into a unique ticker. Confirm the accounting convention before runtime integration; no runtime registration or execution is enabled.

## OI-106 — Keller original versus Easy Investing variant

Status: Open.

Compare and label the variant explicitly; do not blend its rules into the G12 baseline.

---

# Related Documents

- `BAA_Research.md`
- `Moon_Current_Production.md`
- `Moon_Object_Model.md`
- `Moon_Interface.md`
- `Moon_Execution_Mapping.md`
