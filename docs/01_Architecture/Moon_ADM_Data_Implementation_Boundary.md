# Moon ADM Data Implementation Boundary

Version: 1.0
Status: Engineering Baseline — Policy-Explicit Utilities Only
Last Updated: 2026-10-09

## Purpose

This document records the first implementation step after the ADM readiness review. It distinguishes safe, deterministic data operations from policy choices that remain unresolved. It does not approve a provider, close research validation, or activate ADM.

## Implemented in this step

`src/orion/frameworks/moon/adm_data.py` adds `calculate_adm_asset_return(...)`. The caller must supply:

- the already normalized `MarketDataSet`;
- the exact symbol and canonical field to use;
- the exact current observation timestamp;
- the exact trailing observation timestamp.

The helper performs exact-key lookup only, rejects missing observations and non-numeric, non-finite, zero, or negative prices, and delegates the arithmetic to the existing `calculate_adjusted_price_return` function. It does not select dates or substitute another field.

This explicit-input design is intentional: it provides a reusable calculation seam without hard-coding an unresolved endpoint-selection policy.

## Step 27 — explicit observation pair selection

`src/orion/frameworks/moon/adm_data.py` now also exposes
`select_adm_price_observations(...)` and the immutable
`ADMPriceObservationPair` result. The caller must provide both exact observation
identifiers and a non-empty `selection_policy_id`; the result retains the two
source observations and that identifier for traceability. The selector reuses
the strict numeric-price validation, rejects identical endpoints, and never
chooses a nearby observation. The policy identifier is provenance only: it does
not mean that the policy has been approved.

The function deliberately performs no calendar arithmetic. In particular, it
does not decide whether a 12-month anniversary that falls on a non-trading day
should use the previous trading day, the next trading day, or another approved
convention. Those remain governance/source-contract decisions.

## Explicitly not implemented

- calendar-aware trailing-12-month endpoint selection;
- provider or ticker alias resolution;
- approval of `adjusted_close` semantics for any provider;
- freshness thresholds, forward filling, or stale-data acceptance;
- provider precedence, retries, cache, network access, or persistence;
- absolute-momentum benchmark choice or comparison logic;
- construction of `ADMSignalInput` from raw observations;
- strategy activation, portfolio decisions, or execution.

## Contract and failure behavior

The function fails closed if either exact observation is absent or its value is not a finite positive number. It never searches for the nearest available date. `field` is required rather than defaulted so callers cannot mistake a canonical field name for an approved financial meaning.

The function accepts caller-selected timestamps as opaque identity strings. It does not validate date syntax or claim that the timestamps are exactly twelve months apart. Those responsibilities remain gated by the approved calendar and endpoint policy.

## Test coverage

Deterministic tests cover exact endpoint calculation, no implicit field substitution, missing endpoints, invalid price values, rejection of an alternate nearby date, preservation of explicit selection provenance, and rejection of identical endpoints. The shared `MarketDataPoint` contract rejects non-finite float values at construction.

## Next gate

Before end-to-end ADM input construction or a provider adapter, close the outstanding decisions recorded in `Moon_ADM_Data_Readiness_and_Closure.md`: approved defensive instrument and absolute-momentum benchmark relationship, adjusted-price acceptance criteria, endpoint/calendar rules, data-quality behavior, historical revision/reproducibility expectations, and provider selection.

## Related documents

- `docs/01_Architecture/Moon_ADM_Data_Contract.md`
- `docs/01_Architecture/Moon_ADM_Data_Readiness_and_Closure.md`
- `docs/01_Architecture/Orion_Framework_Data_Contracts.md`
- `docs/01_Architecture/Orion_Data_Pipeline.md`
- `docs/03_Research/Moon/ADM/ADM_Orion.md`


## Step 29 — relative-momentum calculation for VTI and VEU

`src/orion/frameworks/moon/adm_data.py` now exposes
`calculate_adm_relative_momentum(...)` and the immutable
`ADMRelativeMomentumResult`. The helper calculates returns for exactly the two
ADM risk assets (`VTI`, `VEU`) using the same field, target dates, and selection
policy identifier. Both selected observation pairs and computed returns are
retained for auditability.

This calculation layer does not calculate absolute momentum, choose its
comparison benchmark, select a defensive asset, or construct `ADMSignalInput`.
The result is intentionally not a strategy signal. A missing endpoint or an
invalid price causes the calculation to fail closed; the helper does not fill,
interpolate, or silently replace data.

The current prior-observation selector is a deterministic data-level rule: it
selects the latest observation date on or before each supplied target date. It
does not certify the provider's exchange calendar, enforce a maximum age, or
approve the semantics of `adjusted_close`. Those remain source-contract and
governance gates before production integration.

## Step 30 — explicit observation-age validation

`src/orion/frameworks/moon/adm_data.py` now exposes
`validate_adm_observation_pair_freshness(...)` and the immutable
`ADMObservationFreshnessResult`. The caller must explicitly supply
`max_age_days`; there is no default threshold and no threshold is presented as
an approved investment or data policy. The audit records each target date,
selected observation date, calendar-day age, field, and selection policy ID.

The validator requires both target dates to be retained, verifies that each
selected observation is on or before its target date, and rejects either
observation when its calendar-day age exceeds the caller-supplied limit. The
age calculation is a deterministic guardrail, not proof of a valid exchange
trading day, correct provider calendar, adjusted-price semantics, or acceptable
market-data quality. A production adapter must still supply an approved
threshold and source-specific validation policy.

Tests cover an accepted explicit threshold, an over-age observation, invalid
threshold values, and pairs without target-date provenance. No source adapter,
network access, freshness default, strategy activation, or Runtime change was
introduced.


## Step 31 — relative-momentum data-quality gate

`validate_adm_relative_momentum_freshness(...)` applies one explicitly supplied
`max_age_days` threshold to the selected VTI and VEU observation pairs. It returns
an immutable `ADMRelativeMomentumFreshnessResult` only when both assets pass;
if either asset fails, the aggregate gate fails closed and returns no result.
The per-asset freshness audits preserve selected dates and measured calendar-day
ages for review.

The gate is strictly a data-quality check. It does not certify exchange-calendar
validity, source reliability, adjusted-price total-return semantics, or the
correctness of the chosen age threshold. Passing it does not approve or create
an ADM investment signal, calculate absolute momentum, construct
`ADMSignalInput`, activate a strategy, or invoke Runtime. No default age limit,
provider adapter, network dependency, or Core Runtime change was introduced.


## Step 32 — absolute-momentum return input preparation

`calculate_adm_absolute_momentum_inputs(...)` calculates comparable returns for
a caller-specified risk asset and benchmark using the same field, target dates,
and prior-observation selection policy. `ADMAbsoluteMomentumInputs` retains both
returns and both selected observation pairs for auditability. The benchmark is a
required argument: SGOV, BIL, or SHY is not silently selected.

This step intentionally stops before comparison. Existing research describes
absolute momentum as assessing whether the selected asset performed positively
relative to a risk-free alternative. D-055 now approves SGOV and strict-greater-than comparison, but the utility still emits no `absolute_momentum_positive` boolean and does not construct `ADMSignalInput`. Provider price semantics, freshness, and source quality remain open.

Both returns fail closed if either instrument lacks an eligible observation or
contains an invalid price. Provider calendar validity, freshness validation,
total-return semantics and production data/governance approval remain separate gates. No Runtime,
strategy activation, external provider, or network behavior changed.


## Step 33 — absolute-momentum policy boundary

`Moon_ADM_Absolute_Momentum_Policy_Boundary.md` records the approved D-055 SGOV/strict-greater-than comparison and the data decisions still required before producing `absolute_momentum_positive`. Adjusted-price source semantics, freshness, and calendar policy remain open. No boolean signal, strategy input construction, or activation was added in this step.


## Step 34 — signal assembly readiness boundary

`prepare_adm_signal_assembly_readiness(...)` now cross-checks the relative-
momentum freshness result against caller-supplied absolute-momentum return
inputs. It requires matching target dates, field, selection-policy provenance,
and one explicit calendar-day age limit. It applies that same limit to the
absolute risk-asset/benchmark observation pairs and retains their freshness
audits.

A successful `ADMDataAssemblyReadiness` means only that these specified data
quality and consistency checks passed. It explicitly records unresolved adjusted-price semantics and provider-calendar/data-quality policies. Its `signal_ready` property remains false; it creates neither `absolute_momentum_positive` nor
`ADMSignalInput`. This step does not authorize provider I/O, strategy
activation, or a Core Runtime change.


## Step 35 — comparison-policy reconciliation

The existing research's original GEM decision process compares the winning risk-asset momentum with cash return. D-055 approves SGOV as the benchmark and strict greater-than comparison; equality is false. Adjusted-price acceptance and production freshness/calendar rules remain open. No `absolute_momentum_positive` boolean or `ADMSignalInput` construction was added.
See `Moon_ADM_Absolute_Momentum_Comparison_Policy_Closure_Review.md`.


## Step 36 — explicit absolute-momentum comparison contract

`ADMAbsoluteMomentumComparisonStatus`, `ADMAbsoluteMomentumComparisonOperator`,
`ADMAbsoluteMomentumComparisonPolicy`, and
`ADMAbsoluteMomentumComparisonResult` define the comparison interface.
`compare_adm_absolute_momentum_returns(...)` applies the approved D-055 policy when none is supplied and returns `UNAVAILABLE` if an explicit policy benchmark does not match the calculated return inputs. It retains policy provenance. Policy IDs are not governance evidence; no comparison result is wired to `ADMSignalInput`, strategy activation, or Runtime.
