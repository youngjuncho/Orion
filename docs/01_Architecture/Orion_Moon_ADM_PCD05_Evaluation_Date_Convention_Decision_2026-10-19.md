# Orion Moon / ADM — PCD-05 Evaluation-Date Convention Decision

- Date: 2026-10-19
- Status: **User-confirmed convention; execution timing remains unresolved**
- Scope: Calendar month-end evaluation date only

## Decision

For monthly ADM evaluation, use the calendar month's final date when that date is a trading day for the relevant instrument/market. If calendar month-end is not a trading day, use the immediately preceding trading day for that instrument/market.

In short:

```text
Calendar month-end is a trading day?
  Yes -> evaluate as of that date
  No  -> evaluate as of the immediately preceding trading day
```

The convention applies to the evaluation cutoff. It does not authorize a trade at that day's closing price.

## Data and signal constraints

- Only observations dated on or before the evaluation cutoff may be used.
- The signal must not be treated as available until all required observations have actually become available and passed the applicable data-readiness checks.
- A date printed on a price observation is not proof that the observation was available to a decision-maker at that time.
- Do not backdate execution to the evaluation cutoff or assume a same-day closing fill without a separately approved execution model.

## Explicitly unresolved

This decision does **not** specify:

- timezone or the operational timestamp at which monthly evaluation runs;
- how to determine data publication/availability timestamps;
- how to handle delayed, corrected, or missing observations;
- whether a multi-market portfolio uses each instrument's local calendar or a single portfolio calendar for all instruments;
- signal-validity interval, order cutoff, or execution date/time after the signal is confirmed;
- backtest fill price, slippage, transaction costs, or order execution assumptions.

These items must be resolved before this convention can be treated as a complete operational timing contract.

## Required implementation tests once calendar abstraction is specified

1. Month-end is a trading day: retain that date.
2. Month-end is a weekend: choose the immediately preceding trading day.
3. Month-end is a market holiday: choose the immediately preceding trading day, including consecutive holidays.
4. Year boundary and leap-year February cases.
5. Instrument/market calendar differences, if per-instrument calendars are approved.
6. Reject observations dated after the evaluation cutoff.
7. Do not finalize a signal while required data is unavailable or fails readiness checks.
8. Assert that the evaluation cutoff does not implicitly become an execution timestamp.

## Governance status

This is a narrow date-convention decision based on the user's confirmation. It does not close PCD-04, PCD-02, PCD-15, or PCD-16. Authoritative governance binding remains unimplemented; G-01 remains `DEFERRED — BLOCKING`; `config/moon.yaml` must retain `active_strategies: []`; signal assembly remains fail-closed.
