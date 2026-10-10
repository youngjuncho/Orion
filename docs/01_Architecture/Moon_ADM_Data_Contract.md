# Moon ADM Data Contract

Version: 1.0  
Status: Contract Baseline - D-055 Comparison Approved; Source Integration Deferred
Last Updated: 2026-10-10

## Purpose

This document records the minimum data requirements implied by the existing ADM implementation specification and D-028. D-055 approves SGOV as the absolute-momentum comparison benchmark and strict greater-than comparison, with equality false. D-056 approves provider-independent engineering defaults for prior-on-or-before selection and fail-closed missing/conflicting data handling. Neither decision approves a provider or authorizes production collection.

## Existing strategy contract

ADM currently consumes `ADMSignalInput`, not raw `MarketDataSet` observations.
The input contains:

- `signal_date`;
- relative momentum values for `VTI` and `VEU`;
- an already evaluated `absolute_momentum_positive` boolean;
- the configured defensive asset.

`ADMStrategy` compares the supplied relative momentum values and applies the
supplied absolute-momentum result. It does not select historical observations,
calculate the absolute-momentum result, determine data freshness, or resolve
source conflicts. A future adapter/calculation component must perform those
responsibilities before constructing `ADMSignalInput`.

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
last trading day. Step 28 implements the engineering default: for
each explicit target date, select the latest available observation whose
`observed_at` date is on or before that target. This avoids selecting a future
bar when a target falls on a weekend or holiday, and records both target dates
and selected observations for auditability.

This is the selected prior-observation policy for the engineering baseline,
not proof that the selected observation is a valid exchange trading day; it
also does not impose a numeric maximum age. Under D-056, the same field,
targets, and selection rule apply to VTI, VEU, and the SGOV comparison input.
Required missing, invalid, stale under an explicit caller policy, or
conflicting observations fail closed; no fill, interpolation, or partial
success is allowed. Provider bar calendars, timezone, numeric freshness
limits, conflict/revision semantics, and adjusted-price semantics remain
separate source-contract decisions. Production collection remains gated on
those decisions and provider approval.

## Defensive benchmark dependency

D-055 approves SGOV as the absolute-momentum comparison benchmark. The configured defensive holding relationship remains separate and is not established by D-055.

## Source and collection boundary

Yahoo Finance is listed as a candidate primary source in `ADM_Orion.md`, but
that document does not constitute production-source approval. No API client,
network dependency, retry behavior, source precedence, cache, or persistence
is introduced by this contract.

## Acceptance criteria for a future adapter

Before an adapter can be considered production-ready, it must:

- map provider fields explicitly to canonical `symbol`, `field`, `observed_at`,
  `value`, `source`, `currency`, and metadata;
- document instrument identity and adjusted-price semantics;
- document evaluation date, trailing-period selection, timezone, and calendar;
- define missing, duplicate, stale, revised, and conflicting observations;
- honor D-055's SGOV comparison benchmark; document any separate configured defensive holding relationship;
- provide deterministic fixtures covering normal and invalid input cases;
- produce `ADMSignalInput` only after required inputs pass validation.

The calculation layer now supports an auditable VTI/VEU relative-momentum result
from a shared field, target-date pair, and prior-observation policy identifier.
It deliberately stops before absolute-momentum calculation and signal-input
construction.

Until the adapter criteria above are met, ADM remains a strategy over precomputed
inputs; there is no claim of end-to-end market-data integration.

## Related documents

- `docs/03_Research/Moon/ADM/ADM_Orion.md`
- `docs/03_Research/Moon/ADM/ADM_Research.md`
- `docs/01_Architecture/Orion_Framework_Data_Contracts.md`
- `docs/01_Architecture/Orion_Data_Pipeline.md`
- `docs/01_Architecture/Moon_ADM_Data_Readiness_and_Closure.md`
- `docs/01_Architecture/Moon_ADM_Provider_Adapter_Readiness_Review.md`


## Implementation boundary

The implemented deterministic calculation and validation stages, including the Step 31 relative-momentum freshness gate, are tracked in [`Moon_ADM_Data_Implementation_Boundary.md`](Moon_ADM_Data_Implementation_Boundary.md). Passing the freshness gate is not approval of provider semantics or an investment signal.
