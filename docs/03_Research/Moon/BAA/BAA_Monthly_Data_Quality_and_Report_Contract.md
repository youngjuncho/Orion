# BAA Monthly Data-Quality and Report Contract

Version: 1.0  
Status: Implemented for offline validation; live-provider behavior not empirically validated  
Last Updated: 2026-10-20

## Operating model

BAA is run manually at the monthly evaluation point. There is no scheduler, continuous collection, or background refresh. The operator initiates the workflow when the monthly review is due. This contract defines the checks and report contents; it does not authorize live collection or approve a data provider. The approved research convention is to label the review period `YYYY-MM` separately from the actual final-session `signal_date`; repeated BIL replacements preserve three equal slots and aggregate into one reported BIL holding.

## Automated hard-fail checks

The offline validation runner must fail closed if any of these checks fail:

1. **Universe coverage:** exactly the 17 distinct BAA-G12 symbols are present for each provider: `SPY, QQQ, IWM, VGK, EWJ, VWO, VEA, VNQ, DBC, GLD, TLT, HYG, LQD, TIP, BIL, IEF, BND`.
2. **Observation integrity:** every row has a valid symbol, `YYYY-MM` month, an ISO observation date belonging to that month, finite positive adjusted-close value, and `USD` currency. Duplicate symbol/month rows are rejected.
3. **Final-session attestation:** for signal-builder input, every required symbol/month point must carry `month_end_session_verified=true`, and all 17 symbols must share the same observed session date within each month. Missing attestation or date disagreement fails closed. The attestation must be set only after the adapter/validation step verifies the final valid US trading session; it must not be guessed from calendar month-end.
4. **Panel completeness:** every expected symbol has the same monthly panel within each provider, with at least 13 monthly observations by default.
5. **Cross-provider coverage:** both providers contain matching symbol/month keys; missing observations are reported and fail the comparison.
6. **Date alignment:** provider observation dates for each matched symbol/month agree exactly in the initial screening. A mismatch is surfaced for investigation, not silently normalized away.
7. **Currency consistency:** all normalized observations remain USD; non-USD values are rejected.
8. **Price screening:** the absolute relative difference between adjusted-close values must not exceed the configured 0.05% default tolerance. This is a screening threshold, not an economic equivalence claim.

A hard-fail must remain visible in the JSON and Markdown report. Do not pass by dropping an asset, forward-filling/interpolating, substituting raw close for adjusted close, mixing providers within a signal window, or relaxing a threshold without a separately documented decision.

## Required manual checks

These checks are deliberately not inferred from a generic PASS:

- Verify the latest included observation month is complete and is not the current partial calendar month. The signal month must be a completed month and precede the dataset `as_of` month.
- Verify how `month_end_session_verified=true` was established against a US market calendar and source timestamps. The flag is an attestation gate, not a provider-independent guarantee.
- Confirm provider terms, API entitlement, and request quota for the account and intended use before any live collection.
- Check symbol identity and available history, especially ETF inception dates and any ticker/provider mapping ambiguity.
- Inspect documented split/dividend events and compare adjustment behavior against an independently documented reference.
- Review provider revisions, outage/rate-limit behavior, and whether the source can be used consistently for the entire signal window.
- Record any manual exception and its rationale. A successful screening report alone does not approve a provider.

## Output contract

The offline runner writes the following under its requested output directory:

- `alpha_vantage_normalized.csv`: normalized Alpha Vantage observations.
- `yahoo_finance_normalized.csv`: normalized Yahoo Finance observations.
- `baa_price_validation_report.json`: machine-readable details, panel checks, comparison exceptions, and execution provenance.
- `baa_price_validation_summary.md`: human-readable verdict, coverage counts, automated gates, exceptions, and required manual checks.

The report must state that the validator made zero network requests, read no API keys, and did not approve a provider. `PASS` means only that the configured automated screen passed. It does not certify total-return equivalence, source reliability, provider approval, BAA activation, or trading authorization.

## Execution boundary

`run_baa_monthly_review.py` remains plan-only unless the operator explicitly supplies `--confirm-live-data-fetch`. This project state keeps live collection unexecuted. The monthly process is manual; no scheduler, automatic activation, or order execution is part of this workflow.
