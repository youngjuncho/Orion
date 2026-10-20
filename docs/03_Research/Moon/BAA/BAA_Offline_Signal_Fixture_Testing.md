# BAA-G12 Offline Signal Fixture Testing

## Purpose

This document defines the offline acceptance checks for BAA-G12 signal calculation. Tests use deterministic synthetic monthly prices only. They do not download market data, read API credentials, register the strategy with the Moon runtime, schedule a run, or submit orders.

## Coverage

- Momentum formulas: weighted 1/3/6/12-month momentum and SMA12 momentum.
- Input contract: 13 monthly observations for every required asset; malformed, missing, non-USD, duplicate, non-positive, and non-numeric observations fail closed.
- Month-end date contract: observations require `month_end_session_verified=true`; all required symbols must share the same verified final-session date within each month. The returned signal date is the verified observation date, not calendar month-end.
- Regime boundary: a negative canary momentum switches to `Risk Off`; zero is not negative and therefore remains `Risk On`.
- Offensive selection: `Risk On` ranks the offensive universe by SMA12 momentum and selects the top six with equal weights.
- Defensive selection: `Risk Off` ranks the defensive universe by SMA12 momentum, selects three slots, and applies the BIL absolute-momentum floor using 13612W momentum. Multiple BIL replacements preserve the three equal-weight slots and aggregate to one BIL holding under the approved Orion output convention.
- Deterministic ties: equal SMA12 scores preserve the declared universe order. Equality with BIL's 13612W score does not trigger replacement because the rule is strictly `<`.
- Output contract: selected assets are unique, weights are non-negative and sum to one, and results remain marked `research-only-not-executable`.

## Running the offline tests

From the repository root:

```bash
pytest -q tests/orion/frameworks/moon/test_baa.py
```

The full suite can be run with:

```bash
pytest -q
```

These tests are synthetic fixtures, not empirical validation of any provider or of live market performance. A passing test suite does not approve a provider or authorize live data collection.
