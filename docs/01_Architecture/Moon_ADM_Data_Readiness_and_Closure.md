# Moon ADM Data Readiness and Closure Matrix

Version: 1.0  
Status: Engineering Baseline — Relative Momentum and Absolute-Momentum Inputs Implemented; Source Policies Still Open  
Last Updated: 2026-10-09

## Purpose

This matrix separates the existing ADM methodology from unresolved governance choices, provider-specific contract requirements, and implementation work. It is a closure plan, not an approval of a provider or a change to ADM's investment methodology.

## 1. Existing approved methodology

The following points are grounded in existing decisions or the current ADM implementation specification. They can be treated as constraints for future engineering, not as permission to activate ADM in production.

| Item | Current baseline | Boundary |
|---|---|---|
| Return measurement | D-028 approves adjusted-price-based total-return measurement; distributions are not recalculated inside ADM | Data layer must supply a suitable adjusted-price series |
| Momentum horizon | `ADM_Orion.md` specifies trailing 12-month return | The research document marks validation as pending; implementation must preserve this distinction |
| Risk universe | VTI and VEU | Do not add assets without a separate methodology decision |
| Selection behavior | Existing `ADMStrategy` compares precomputed relative momentum values and applies a precomputed absolute-momentum boolean | It does not calculate those values from market observations |
| Allocation output | Current specification selects one asset at 100% of ADM strategy allocation | Moon-level aggregation and execution remain outside ADM |
| Activation control | D-026 separates registered strategies from active strategies; initial active allowlist is empty | ADM must not be treated as production-active merely because it is registered |

## 2. Documented but still requiring approval or validation

These items appear in the current research/implementation documents but are not closed sufficiently to authorize an end-to-end production calculation.

| Item | Current document state | Required closure |
|---|---|---|
| Defensive asset / absolute-momentum benchmark | SGOV is primary candidate; BIL and SHY are backups; final approval pending. Research direction is comparison against cash/defensive return, not an implicit zero-return threshold | Approve benchmark identity and its relationship to the configured defensive holding; explicitly define comparison operator and equality behavior; see `Moon_ADM_Absolute_Momentum_Comparison_Policy_Closure_Review.md` |
| Adjusted-price semantics | `adjusted_close` is a candidate canonical field; D-028 requires a suitable adjusted-price series | Approve acceptance criteria for the source's adjustment methodology and validate it against the intended total-return proxy |
| Twelve-month endpoint selection | Step 28 implements latest available observation on or before each explicit target date | The prior-observation rule is the engineering default; provider calendar validity and maximum observation age remain separate gates |
| Monthly signal date | Research spec says last trading day; execution spec says next trading day | Confirm how the signal date is represented and how the next trading day is identified across calendars |
| Missing/stale observations | Not specified | Approve fail-closed or other explicit behavior; do not silently forward-fill or fabricate observations |
| Historical revisions | Not specified | Decide whether recalculation uses latest revised history or preserves an as-observed snapshot, and what reproducibility means for MVP |
| Provider choice | Yahoo Finance is a candidate primary source; alternatives are listed for future review | Explicitly approve a provider for the intended use before production collection |

## 3. Provider-specific contract decisions

These are not global investment-methodology rules. They must be stated in the adapter/source contract once a provider is selected.

- Exact instrument identifiers and mapping for VTI, VEU, and the approved defensive instrument.
- Provider field-to-canonical-field mapping, including the precise meaning of its adjusted-price field.
- Timestamp format, timezone, trading calendar, and the interpretation of daily bars.
- How the provider represents absent bars, duplicate bars, delayed data, corrected data, and conflicting responses.
- Retrieval provenance and the metadata required to reproduce which two observations were selected for each return calculation.
- Provider access limits, failure behavior, and any retry/cache policy, if later authorized.

No provider-specific behavior should be generalized to other sources without a separate contract.

## 4. Implementable engineering work after closure

The following work is mechanically implementable, but the portions dependent on unresolved decisions must remain gated.

1. Implemented in Step 27: exact observation-pair selection from a validated dataset, with caller-supplied timestamps and policy identifier. Step 28 adds deterministic selection of the latest available observation on or before each explicit target date; it records target dates and selected source dates. Step 28 also calculates return directly from the selected pair.
2. Implemented in Step 28: calculate adjusted-price return from an auditable selected observation pair using the existing validated formula; invalid/non-positive/non-finite inputs are rejected.
3. Derive relative momentum for VTI and VEU from the same approved measurement convention.
4. Step 32 prepares comparable returns for an explicitly supplied risk asset and benchmark. Step 33 documents the unresolved absolute-momentum policy boundary; derive the boolean only after benchmark identity, comparison expression, equality behavior, and input validation rules are approved.
5. Construct `ADMSignalInput` only when every required value passes validation; otherwise return a typed validation failure rather than a partial signal.
6. Implemented in Steps 27–28: deterministic tests cover exact selection, prior-observation selection, future-bar exclusion, missing endpoints, invalid prices, identical endpoints, date-format validation, and selection-policy provenance. Duplicate identities are rejected by `MarketDataSet`; stale/revised/conflicting data and provider-calendar validation remain open.
7. Add a provider adapter only after the provider and source contract are approved. Keep provider I/O outside `ADMStrategy`.

This list does not authorize network access, persistence, scheduled collection, trading, or production activation.

## 5. Implementation gate

Pure calculation/selection utilities may use the explicit prior-observation-on-or-before rule. The rule selects from the supplied dataset only and does not validate exchange calendars or guarantee freshness; those remain explicit caller/source-contract gates. Provider integration is gated on closure of provider choice, adjusted-price semantics, calendar/date selection, data-quality behavior, and defensive-benchmark relationship.

Until then:

- `ADMStrategy` remains a consumer of precomputed `ADMSignalInput`.
- `config/moon.yaml` active-strategy controls remain authoritative.
- No data source is considered production-approved merely because it appears in a research document or pipeline overview.
- No missing or ambiguous observation is silently repaired.

## Related documents

- `docs/01_Architecture/Moon_ADM_Data_Implementation_Boundary.md`
- `docs/01_Architecture/Moon_ADM_Absolute_Momentum_Policy_Boundary.md`

- `docs/01_Architecture/Moon_ADM_Data_Contract.md`
- `docs/01_Architecture/Orion_Framework_Data_Contracts.md`
- `docs/01_Architecture/Orion_Data_Pipeline.md`
- `docs/03_Research/Moon/ADM/ADM_Orion.md`
- `docs/05_Decisions/Decision_Log.md` (D-026 and D-028)

## Step 34 status — signal assembly readiness

Implemented `ADMDataAssemblyReadiness` and
`prepare_adm_signal_assembly_readiness(...)`. The helper checks that relative
and absolute momentum inputs use the same target dates, field, selection-policy
identifier, and explicit maximum age. Both relative assets must already have
passed their freshness gate; both absolute-input instruments are freshly
validated during readiness preparation. The result is a data-readiness audit,
not a signal: unresolved benchmark, comparison, adjusted-price, and provider
quality/calendar policy gates remain listed and `signal_ready` is always false.


## Step 35 status — comparison policy reconciliation

The existing ADM research describes comparing the winning risk asset momentum
with cash return. This establishes a benchmark-relative research direction, but
does not approve SGOV/BIL/SHY, settle the exact boolean operator or equality
behavior, validate adjusted-price semantics, or close production data policy.
The comparison review records these distinctions; no signal boolean is emitted.


## Step 36 status — absolute-momentum comparison contract

`Moon_ADM_Absolute_Momentum_Comparison_Contract.md` defines a three-state
comparison result: `TRUE`, `FALSE`, and `UNAVAILABLE`. No comparison policy is
assumed when none is supplied; a benchmark mismatch also returns `UNAVAILABLE`.
Strict and inclusive operators have explicit, distinct equality behavior, but
their availability as generic engineering operators does not approve either for
production ADM. The comparison result is not converted to `ADMSignalInput`, and
Core Runtime and the active-strategy allowlist remain unchanged.
