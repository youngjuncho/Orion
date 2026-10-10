# Moon ADM Data Readiness and Closure Matrix

Version: 1.0
Status: Engineering Baseline - D-055 Comparison Approved; D-057 Source Adapter Implemented; D-058 Freshness Approved; D-059 Revision Policy Approved
Last Updated: 2026-10-10

## Purpose

This matrix separates approved ADM methodology, the D-057 source-adapter scope, and remaining data/activation gates. D-055 closes the absolute-momentum benchmark/operator decision. D-057 selects Alpha Vantage's monthly adjusted endpoint for private individual research; D-058 approves a seven-day maximum age for selected observations; D-059 approves per-invocation revision handling and fail-closed duplicate rejection. The target-date helper remains an engineering default. None of these decisions activates ADM.

## Existing approved methodology

The following points are grounded in existing decisions or the current ADM implementation specification. They are constraints for engineering, not permission to activate ADM in production.

| Item | Current baseline | Boundary |
|---|---|---|
| Return measurement | D-028 approves adjusted-price-based total-return measurement; D-055 applies it to risk asset and SGOV; D-057 selects Alpha Vantage monthly adjusted close mapping | D-059 selects each invocation's latest response; empirical adjusted-history parity remains to be validated |
| Momentum horizon | `ADM_Orion.md` specifies trailing 12-month return; D-055 requires the same horizon for the risk asset and SGOV | The engineering helper aligns monthly endpoints; execution-date mapping remains open |
| Risk universe | VTI and VEU | Do not add assets without a separate methodology decision |
| Selection behavior | ADMStrategy compares precomputed relative momentum and absolute-momentum inputs | It does not calculate them from market observations |
| Allocation output | Current specification selects one asset at 100% of ADM strategy allocation | Moon-level aggregation and execution remain outside ADM |
| Activation control | D-026 separates registered and active strategies; initial allowlist is empty | Registration does not mean production-active |

## Documented but still requiring approval or validation

These items are not closed sufficiently to authorize end-to-end production calculation.

| Item | Current document state | Required closure |
|---|---|---|
| Absolute-momentum benchmark/operator | D-055 approves SGOV and strict selected-risk-return greater-than-benchmark; equality is false | Adjusted-history parity, target/execution calendar, configured defensive holding, and activation remain separate gates; D-058 age limit is approved |
| Adjusted-price semantics | D-057 maps Alpha Vantage's `5. adjusted close`; provider documents split and cash-dividend adjustments | Do not add the separate monthly dividend field; exact adjustment/reinvestment method, history parity, and point-in-time semantics are unverified |
| Twelve-month endpoint selection | D-056 prior-observation-on-or-before; D-058 implements the last-completed-month-end helper as an engineering default | Target generation is not signal-timing approval; selected observations must be no more than seven calendar days from each target |
| Monthly signal date | Research spec says last trading day; execution spec says next trading day | Confirm how the signal date is represented and how the next trading day is identified across calendars |
| Missing/stale observations | Provider batch fails closed; D-058 approves seven calendar days for all selected endpoints | Integrated monthly assessment applies the seven-day limit; low-level validation still takes an explicit caller value |
| Historical revisions | D-059 approved | Use the complete latest response per invocation and never merge across retrievals; durable snapshots and historical replay remain unimplemented |
| Provider choice | D-057 selects Alpha Vantage monthly adjusted data for private individual research | Verify live symbol coverage and use only within the approved private individual scope |

## 2. Provider-specific contract decisions

These are not global investment-methodology rules. They must be stated in the adapter/source contract once a provider is selected.

- Exact instrument identifiers and mapping for VTI, VEU, and SGOV as the D-055 comparison benchmark; any configured defensive holding is a separate mapping.
- Provider field-to-canonical-field mapping, including the precise meaning of its adjusted-price field.
- Timestamp format, timezone, trading calendar, and the interpretation of daily bars.
- How the provider represents absent bars, delayed data, and corrected history; duplicates fail closed under D-059 and the adapter contract.
- Retrieval provenance and the metadata required to reproduce which two observations were selected for each return calculation.
- Provider access limits, failure behavior, and any retry/cache policy, if later authorized.

No provider-specific behavior should be generalized to other sources without a separate contract.

## 3. Implementable engineering work after closure

The following work is mechanically implementable, but the portions dependent on unresolved decisions must remain gated.

1. Implemented in Step 27: exact observation-pair selection from a validated dataset, with caller-supplied timestamps and policy identifier. Step 28 adds deterministic selection of the latest available observation on or before each explicit target date; it records target dates and selected source dates. Step 28 also calculates return directly from the selected pair.
2. Implemented in Step 28: calculate adjusted-price return from an auditable selected observation pair using the existing validated formula; invalid/non-positive/non-finite inputs are rejected.
3. Derive relative momentum for VTI and VEU from the same approved measurement convention.
4. Step 32 prepares comparable returns for an explicitly supplied risk asset and benchmark. D-055 approves the comparison rule; deriving an ADM signal still requires source semantics, freshness, and orchestration gates to close.
5. Construct `ADMSignalInput` only when every required value passes validation; otherwise return a typed validation failure rather than a partial signal.
6. Implemented in Steps 27–28: deterministic tests cover exact selection, prior-observation selection, future-bar exclusion, missing endpoints, invalid prices, identical endpoints, date-format validation, and selection-policy provenance. Duplicate identities fail closed in the provider parser and `MarketDataSet`; D-058 applies the freshness limit and D-059 defines per-invocation revision handling. Provider-calendar validation remains open.
7. Implemented by D-057: Alpha Vantage monthly adjusted provider maps complete VTI/VEU/SGOV responses to the canonical data contract. Provider I/O remains outside `ADMStrategy`.

The adapter performs network access only when explicitly configured with a key. This list does not authorize persistence, scheduled collection, trading, or production activation.

## 4. Implementation gate

Pure calculation/selection utilities use the explicit prior-observation-on-or-before rule. D-057 implements Alpha Vantage monthly data for private research. D-058 applies the approved seven-day observation-age gate; target-date generation remains an engineering default. D-059 defines per-invocation revision selection, while empirical provider coverage/adjustment parity and governance gates remain open. SGOV comparison is approved by D-055.

Until then:

- `ADMStrategy` remains a consumer of precomputed `ADMSignalInput`.
- `config/moon.yaml` active-strategy controls remain authoritative.
- Alpha Vantage access remains limited to D-057's private individual research scope.
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
not a signal: unresolved adjusted-price and provider quality/calendar policy gates remain listed and `signal_ready` is always false.


## Step 35 status — comparison policy reconciliation

D-055 approves SGOV as the benchmark and strict greater-than comparison of the selected risk asset trailing-12-month return. Equal returns are false (Risk Off). Adjusted-price semantics and production data policy remain open; no signal boolean is emitted.


## Step 36 status — absolute-momentum comparison contract

`Moon_ADM_Absolute_Momentum_Comparison_Contract.md` defines a three-state comparison result: `TRUE`, `FALSE`, and `UNAVAILABLE`. With no explicit policy, the helper applies D-055's SGOV/strict-greater-than rule; a benchmark mismatch returns `UNAVAILABLE`. The comparison result is not converted to `ADMSignalInput`, and Core Runtime and the active-strategy allowlist remain unchanged.
