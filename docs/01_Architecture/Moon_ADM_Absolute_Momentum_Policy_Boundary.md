# Moon ADM Absolute-Momentum Policy Boundary

Version: 1.0  
Status: Engineering Boundary — D-055 Comparison Rule Approved; Data Gates Open
Last Updated: 2026-10-10

## Purpose

This note separates what the existing ADM research says about absolute momentum from the exact comparison rule needed to produce `absolute_momentum_positive`. It is not an investment-methodology approval and does not activate ADM.

## Existing research statements

The current ADM research describes absolute momentum as assessing whether the selected risk asset has performed positively relative to a risk-free alternative. It also specifies a trailing 12-month return formula based on an adjusted-price series treated as a total-return proxy, while marking the measurement standard as pending validation.

The implementation specification listed SGOV as the primary defensive-asset candidate and BIL / SHY as backups. D-055 now approves SGOV as the comparison benchmark; this does not approve a provider's adjusted-price series or production data semantics.

## Decisions still open

1. **Adjusted-price source:** confirm that the chosen provider's adjusted-price field meets D-028/D-055 total-return requirements.
2. **Date/calendar policy:** define production calendar interpretation, endpoint selection, and observation freshness thresholds.
3. **Failure and revision behavior:** define stale, missing, invalid, corrected, and revised observation handling; retain fail-closed behavior.
4. **Activation and provenance:** bind the approved D-055 policy and data-source evidence to authoritative governance records before signal integration or activation.
## Current implementation boundary

`calculate_adm_absolute_momentum_inputs(...)` calculates comparable returns for an explicit risk asset and benchmark. `compare_adm_absolute_momentum_returns(...)` uses the D-055 SGOV/strict-greater-than rule by default. The data-readiness and caller-attested governance guard still block signal assembly until source and freshness gates are closed.

Do not treat the D-055 policy approval as approval of a provider's adjusted-price semantics, production readiness, or strategy activation. `ADMStrategy` remains a consumer of validated precomputed inputs.

## Observation-date convention

For deterministic selection utilities, selecting the latest available observation on or before an explicit target date is the current engineering convention. When the target falls on a non-trading day, this means the selector can choose a prior observation rather than a future observation. This convention alone does not establish that the selected observation is valid under a provider's exchange calendar or within an approved freshness limit.

The monthly research description (“last trading day” and execution on the “next trading day”) still needs a source/calendar contract before production scheduling. The 12-month anniversary endpoint rule, provider calendar, freshness threshold, and adjusted-price semantics remain distinct validation gates.

## Closure criteria

Production signal integration may proceed only after the data/governance owner has explicitly closed:

- the adjusted-price source acceptance criteria for D-028/D-055;
- matched date-selection and freshness rules for both inputs;
- the provider calendar and missing/stale/revised-data behavior;
- fail-closed behavior for any invalid input;
- end-to-end negative tests before Runtime signal integration or activation.

Until then, retain return inputs and comparison results behind the existing readiness guard; no provider adapter, external network access, persistence, scheduled collection, signal integration, strategy activation, broker execution, or Core Runtime change is authorized by this document.

## Related documents

- `Moon_ADM_Data_Contract.md`
- `Moon_ADM_Data_Readiness_and_Closure.md`
- `Moon_ADM_Data_Implementation_Boundary.md`
- `Orion_Framework_Data_Contracts.md`
- `Orion_Data_Pipeline.md`
- `../03_Research/Moon/ADM/ADM_Orion.md`
- `../03_Research/Moon/ADM/ADM_Research.md`
- `../05_Decisions/Decision_Log.md` (D-026 and D-028)

## Step 35 — D-055 methodology approval

D-055 approves SGOV as the absolute-momentum benchmark and strict selected-risk-return greater-than-benchmark comparison, with equality false. The approved comparison helper uses this rule by default. This closes the benchmark/operator question only.

## Step 34 — data readiness boundary

The readiness audit still keeps `signal_ready` false by default because adjusted-price source semantics and provider calendar/data-quality policy remain open. D-055 does not approve a price provider, freshness threshold, signal assembly, or strategy activation.
