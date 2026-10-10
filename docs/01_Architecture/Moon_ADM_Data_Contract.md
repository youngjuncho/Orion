# Moon ADM Data Contract

Version: 1.0  
Status: Contract Baseline - D-055 Comparison Approved; D-057 Provider Adapter Implemented; D-058 Freshness Approved
Last Updated: 2026-10-10

## Purpose

This document records the ADM data boundary implied by the implementation specification and decisions D-028, D-055, D-056, D-057, and D-058. Alpha Vantage's monthly adjusted endpoint is implemented for private individual research under D-057. D-058 approves a seven-day maximum age for selected observations; its target-date convention remains an engineering default. Provider access does not authorize ADM signal assembly or activation.

## Existing strategy contract

ADM currently consumes `ADMSignalInput`, not raw `MarketDataSet` observations.
The input contains:

- `signal_date`;
- relative momentum values for `VTI` and `VEU`;
- an already evaluated `absolute_momentum_positive` boolean;
- the configured defensive asset.

`ADMStrategy` compares the supplied relative momentum values and applies the
supplied absolute-momentum result. `assess_adm_monthly_dataset()` selects the
monthly observations, calculates relative returns, compares the winner to
SGOV, and applies D-058 freshness validation. It returns an auditable data
assessment only; source-revision validation and governance approval remain
required before constructing `ADMSignalInput`.

## Price field and calculation

D-028 and `ADM_Orion.md` specify trailing 12-month total-return measurement
using an adjusted-price series as the data layer's total-return proxy:

`return = adjusted_price_at_evaluation / adjusted_price_at_trailing_period - 1`

The canonical candidate field is `adjusted_close`. The field name alone is
not proof of compatibility: a selected source adapter must document its
adjustment methodology and confirm that it is suitable for the D-028 use.
Raw `close` must not be substituted silently.

## Minimum conceptual observations

For each asset used by the approved ADM calculation, the data calculation
layer needs:

1. an adjusted-price observation corresponding to the evaluation point;
2. an adjusted-price observation corresponding to the 12-month trailing point;
3. enough source metadata to reproduce which observations were selected.

The strategy's research specification describes monthly evaluation on the
last trading day. `derive_adm_monthly_target_dates(as_of_date)` implements the
D-058 engineering target rule: use the last calendar day of the month preceding
the `as_of` month and the same month's end one year earlier. This excludes a
possibly incomplete current-month bar and handles leap-month ends. This is an
engineering default, not an independently approved signal-timing policy. For each
explicit target, select the latest available observation on or before it,
never a future observation, and retain targets plus selected observations.

This is the selected prior-observation policy for the engineering baseline,
not proof that the selected observation is a valid exchange trading day; it
also does not impose a maximum age in the low-level selector. D-058 approves
seven calendar days for every selected endpoint; `assess_adm_monthly_dataset`
applies that limit by default. Lower-level callers must pass an explicit
threshold. Under D-056, the same field,
targets, and selection rule apply to VTI, VEU, and the SGOV comparison input.
Required missing, invalid, stale under an explicit caller policy, or
conflicting observations fail closed; no fill, interpolation, or partial
success is allowed. Provider publication-time SLA, conflict/revision semantics,
and empirical validation of the provider's adjusted-price history remain
separate source-contract gates. Production signal
assembly remains gated on those decisions and governance approval.

## Defensive benchmark dependency

D-055 approves SGOV as the absolute-momentum comparison benchmark. The configured defensive holding relationship remains separate and is not established by D-055.

## Source and collection boundary

D-057 selects Alpha Vantage `TIME_SERIES_MONTHLY_ADJUSTED` for private
individual research. The adapter is opt-in through
`ORION_ALPHA_VANTAGE_API_KEY`, returns canonical monthly observations for VTI,
VEU, and SGOV, and fails the full batch on provider or validation errors.
Monthly data are last-trading-day labels; they are date-only and are preserved
without timezone conversion. The adapter makes no retries, cache, persistence,
signal assembly, or activation.

## Acceptance criteria for a future adapter

Before ADM signal assembly can be considered ready, it must:

- map provider fields explicitly to canonical `symbol`, `field`, `observed_at`,
  `value`, `source`, `currency`, and metadata;
- document instrument identity and adjusted-price semantics;
- review the D-058 engineering target-date convention and document the
  execution-date/timezone mapping; apply the approved D-058 freshness limit;
- define missing, duplicate, stale, revised, and conflicting observations;
- honor D-055's SGOV comparison benchmark; document any separate configured defensive holding relationship;
- provide deterministic fixtures covering normal and invalid input cases;
- produce `ADMSignalInput` only after required inputs pass validation.

The data layer supports the Alpha Vantage provider boundary, auditable VTI/VEU
relative-momentum calculation, D-055 absolute-momentum comparison inputs, and
explicit freshness checks. It deliberately stops before constructing
`ADMSignalInput` or activating ADM.

The provider adapter is implemented, but ADM remains a strategy over precomputed
inputs; there is no claim of end-to-end signal integration.

## Related documents

- `docs/03_Research/Moon/ADM/ADM_Orion.md`
- `docs/03_Research/Moon/ADM/ADM_Research.md`
- `docs/01_Architecture/Orion_Framework_Data_Contracts.md`
- `docs/01_Architecture/Orion_Data_Pipeline.md`
- `docs/01_Architecture/Moon_ADM_Data_Readiness_and_Closure.md`
- `docs/01_Architecture/Moon_ADM_Provider_Adapter_Readiness_Review.md`


## Implementation boundary

The implemented deterministic calculation and validation stages, including the Step 31 relative-momentum freshness gate, are tracked in [`Moon_ADM_Data_Implementation_Boundary.md`](Moon_ADM_Data_Implementation_Boundary.md). Passing the freshness gate is not approval of provider semantics or an investment signal.
