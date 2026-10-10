# Moon ADM Data Pipeline Contract Consolidation

Version: 1.0  
Status: Engineering Contract - D-055 Methodology Approved; Provider Policies Open
Last Updated: 2026-10-10

## Purpose

This document consolidates the current Moon ADM data-path contracts into one implementation map. It records which transitions are implemented, which checks are repeated at boundaries, and which conditions still block a production signal. D-055 approves SGOV as the benchmark and strict greater-than comparison with equality false. This document does not approve a data provider or strategy activation.

## Canonical implemented path

```text
MarketDataSet
  -> select_adm_price_observations_on_or_before
  -> calculate_adm_observation_pair_return
  -> calculate_adm_relative_momentum (VTI and VEU)
  -> validate_adm_relative_momentum_freshness
  -> calculate_adm_absolute_momentum_inputs (caller-specified risk asset and SGOV benchmark)
  -> prepare_adm_signal_assembly_readiness
  -> compare_adm_absolute_momentum_returns (D-055 default; explicit mismatched benchmark returns UNAVAILABLE)
  -> guard_adm_comparison_for_signal_assembly
  -> [NO ADMSignalInput conversion in this implementation]
```

The arrows describe available building blocks and their intended ordering, not an automatic production orchestrator. The caller remains responsible for passing consistent inputs qualified under the applicable source and production data gates.

## Contract matrix

| Stage | Main contract | Enforced invariant | Does not establish |
|---|---|---|---|
| Dataset boundary | `MarketDataSet` / `MarketDataPoint` | Structural types and duplicate identity constraints | Provider correctness, field meaning, exchange calendar |
| Observation selection | `ADMPriceObservationPair` | Selected observations are at or before explicit target dates; source dates and selection policy ID are retained | Exact 12-month calendar convention, provider source-calendar validity |
| Return calculation | `calculate_adm_observation_pair_return` | Finite positive prices and deterministic arithmetic | Total-return equivalence of a provider's adjusted field |
| Relative momentum | `ADMRelativeMomentumResult` | Exactly VTI and VEU; shared target dates, field, and selection policy | Which winner should become the absolute-momentum risk input; strategy signal |
| Freshness gate | `ADMRelativeMomentumFreshnessResult` / `ADMObservationFreshnessResult` | Explicit maximum calendar-day age; all required observations must pass | Production-approved threshold, exchange-calendar correctness |
| Absolute inputs | `ADMAbsoluteMomentumInputs` | Explicit risk asset and SGOV benchmark with comparable endpoints and retained observations | Which risk-asset winner to select or whether observations meet source requirements |
| Readiness | `ADMDataAssemblyReadiness` | Relative and absolute inputs share dates, field, policy ID, and age threshold; absolute observations pass freshness checks | Source qualification, production approval, or a ready signal |
| Comparison | `ADMAbsoluteMomentumComparisonResult` | Defaults to D-055 policy; explicit benchmark mismatch returns `UNAVAILABLE` | Authoritative source and production-readiness evidence |
| Integration guard | `ADMComparisonSignalGuardResult` | Blocks unavailable results, mismatched inputs, unresolved source/data gates, missing production readiness status/reference | Independent verification of governance records; `ADMSignalInput` creation |

## Cross-stage invariants

1. **No silent substitution.** A missing observation, field, or price is not repaired by selecting a different field or fabricating a value. A mismatched benchmark returns `UNAVAILABLE`; D-055 establishes SGOV as the default comparison benchmark.
2. **No future observations.** The generic selector chooses only observations on or before each target date.
3. **One explicit measurement convention per comparison.** Relative and absolute input contracts must agree on target dates, field, selection-policy ID, and maximum age.
4. **Freshness is not source validity.** The age gate is calendar-day arithmetic only; it does not validate a provider's trading calendar or data revisions.
5. **`UNAVAILABLE` is not `FALSE`.** A mismatched benchmark or invalid/unavailable input cannot be interpreted as a negative momentum signal. Under D-055, equal risk and SGOV returns produce `FALSE`.
6. **Data readiness is not investment approval.** A readiness object may pass structural and freshness checks while remaining blocked by unresolved source and production governance gates.
7. **Caller-supplied approval is only an attestation.** A non-empty reference does not prove that an authoritative decision exists; production use must bind approval to the governance source of truth.
8. **No strategy side effects.** These utilities do not mutate Runtime state, activate Moon strategies, execute trades, or construct `ADMSignalInput`.

## Known boundary: risk-asset selection

`calculate_adm_relative_momentum(...)` computes returns for VTI and VEU. `calculate_adm_absolute_momentum_inputs(...)` accepts one explicitly named risk asset and one benchmark. The caller must not infer that an arbitrary risk asset is the relative-momentum winner. D-055 specifies how a selected risk asset is compared with SGOV, but does not select the winner or assemble the signal. The existing `ADMStrategy` consumes precomputed values and remains separate from these data utilities. Any future orchestration must reuse the approved ADM selection rule rather than introduce a competing winner-selection implementation.

## Remaining production gates

- Qualify the configured defensive holding separately; D-055 approves SGOV as the absolute-momentum comparison benchmark.
- Validate the provider's adjusted-price field as the required total-return proxy.
- Close exact monthly evaluation-date, provider calendar, timezone, and endpoint-selection semantics.
- Approve freshness thresholds and missing, stale, revised, or conflicting observation behavior.
- Select and approve the provider/source contract.
- Bind D-055 and future data-source approvals to authoritative governance records.
- Only then consider a separately reviewed signal-assembly adapter; do not bypass the existing `ADMStrategy` contract or Moon active-strategy allowlist.

## Step 39 — provider adapter readiness review

`Moon_ADM_Provider_Adapter_Readiness_Review.md` classifies adapter readiness by
canonical mapping, instrument identity, adjusted-price semantics, timestamp and
calendar behavior, freshness, missing/revised data, provenance, and governance.
The decision is to keep live provider integration blocked while allowing a
provider-neutral interface and fake-provider fixture design. The prior-observation
on-or-before target-date rule remains the engineering default, but does not certify
source-calendar validity or data freshness.

## Related documents

- `Moon_ADM_Data_Contract.md`
- `Moon_ADM_Data_Implementation_Boundary.md`
- `Moon_ADM_Data_Readiness_and_Closure.md`
- `Moon_ADM_Absolute_Momentum_Comparison_Contract.md`
- `Moon_ADM_Comparison_Signal_Integration_Guard.md`
- `Moon_ADM_Provider_Adapter_Readiness_Review.md`
- `Orion_Data_Pipeline.md`
