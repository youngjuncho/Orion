# Orion Moon / ADM — PCD-04 Empirical Adjusted-Price Parity Protocol Proposal

**Date:** 2026-10-19  
**Status:** Proposal for review only; not an approved policy and not closure evidence.  
**Scope:** Define the evidence needed to compare the selected provider's adjusted-price history with an independently accepted reference without assuming either source is authoritative.

## 1. Current blocker

The adapter maps Alpha Vantage `5. adjusted close` to canonical `adjusted_close` and validates values and response shape. Fixture-based tests prove that mapping and validation behavior. They do not prove the economic interpretation, revision behavior, or parity of historical adjusted prices.

No reference source, parity tolerance, comparison window, or revision-handling acceptance rule is currently approved. This proposal intentionally does not choose them.

## 2. Required decisions before running a parity test

The project owner must explicitly approve:

1. **Reference series:** provider, instrument identifiers, adjustment basis, and why it is sufficiently independent and suitable for comparison.
2. **Instrument coverage:** exact symbols and any symbol/venue mapping rules; do not infer support from general ETF support claims.
3. **Date window:** start/end dates, monthly observation alignment, and minimum number of overlapping observations.
4. **Comparison metric:** for example, pointwise relative price difference and/or return-series difference. Select metrics based on the intended use, not because a threshold makes a test pass.
5. **Tolerance:** numeric threshold and its rationale. No tolerance is implied by this proposal.
6. **Missing/revised observations:** handling of absent months, provider restatements, corporate actions, and observations whose values change between retrievals.
7. **Evidence capture:** retrieval timestamps, source/version metadata where available, symbol, date, field, values, computed differences, and sanitized failure details.

## 3. Suggested deterministic procedure after approval

1. Retrieve both series for the approved symbols and date window; preserve raw responses or an auditable normalized extract according to the project's data-retention rules.
2. Normalize dates and numeric values without forward-filling, interpolating, or substituting raw close for adjusted close.
3. Join only on explicitly aligned observation dates; report missing dates separately instead of silently dropping them.
4. Compute the approved price- and/or return-level metrics using a deterministic script.
5. Evaluate against the approved tolerance and minimum overlap. A missing reference, insufficient overlap, malformed values, or unapproved adjustment-basis mismatch must produce an inconclusive/fail-closed result.
6. Repeat a retrieval after the approved interval if revision behavior is in scope; compare changed historical observations and record retrieval timestamps. Do not treat a single snapshot as proof of point-in-time immutability.
7. Store the result with the exact procedure version, source metadata, inputs, and outcome so it can be reproduced.

## 4. Required result states

- **PASS:** every approved coverage, overlap, metric, tolerance, and data-quality condition is met.
- **FAIL:** at least one approved condition is violated.
- **INCONCLUSIVE:** the comparison cannot validly decide the question (for example, reference unavailable, insufficient overlap, or unresolved methodology mismatch).

Do not collapse `INCONCLUSIVE` into `PASS`. Do not revise thresholds after observing results without recording a separate decision and rerunning the protocol.

## 5. Scope and safety boundaries

- This document is a protocol proposal, not a decision approving a reference source or tolerance.
- No live provider calls were made to create this proposal.
- Existing fixture tests remain useful for parser/adapter correctness but are not empirical parity evidence.
- Until PCD-04 is closed by explicit evidence and approval, describe the series only as the selected adjusted-price research proxy under D-028/D-057; do not claim verified point-in-time total return.
- PCD-02 remains open pending complete live instrument evidence.
- PCD-15/PCD-16 remain open and blocking. `config/moon.yaml` must retain `active_strategies: []`; signal assembly remains fail-closed.
