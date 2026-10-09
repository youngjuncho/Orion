# Moon ADM Absolute-Momentum Policy Boundary

Version: 1.0  
Status: Engineering Boundary — Comparison Rule Not Yet Approved  
Last Updated: 2026-10-09

## Purpose

This note separates what the existing ADM research says about absolute momentum from the exact comparison rule needed to produce `absolute_momentum_positive`. It is not an investment-methodology approval and does not activate ADM.

## Existing research statements

The current ADM research describes absolute momentum as assessing whether the selected risk asset has performed positively relative to a risk-free alternative. It also specifies a trailing 12-month return formula based on an adjusted-price series treated as a total-return proxy, while marking the measurement standard as pending validation.

The implementation specification lists SGOV as the primary defensive-asset candidate and BIL / SHY as backups, with final approval pending. Therefore, the research establishes the broad purpose of absolute momentum but does not close the exact benchmark instrument or source-specific adjusted-price semantics.

## Decisions still open

The following must remain explicit, separately tracked decisions:

1. **Benchmark identity:** which approved instrument supplies the risk-free/defensive comparison return.
2. **Comparison expression:** whether the boolean is based on the selected risk asset's return being greater than zero, greater than the benchmark return, or another formally specified expression. The prose phrase “positive performance relative to a risk-free alternative” is not precise enough to infer this silently.
3. **Measurement consistency:** whether risk and benchmark returns must use the same target dates, lookback endpoint convention, price-field semantics, source approval status, and freshness limits. Engineering should enforce matched conventions when approved, not invent their values.
4. **Equality boundary:** the outcome when the two compared values are equal, if the final rule compares the two returns.
5. **Failure behavior:** behavior when either return is unavailable, stale, invalid, or fails source-semantic validation. The current engineering posture is fail-closed; no boolean should be emitted from incomplete inputs.
6. **Validation status:** the research specification currently marks the trailing-12-month measurement as pending validation. Code implementation does not change that status.

## Current implementation boundary

`calculate_adm_absolute_momentum_inputs(...)` may calculate and retain comparable returns for a caller-specified risk asset and benchmark. It does not approve that benchmark, compare the returns, emit `absolute_momentum_positive`, or construct `ADMSignalInput`.

Do not add an implicit SGOV default, do not treat a configured defensive holding as automatically approved as the comparison benchmark, and do not change `ADMStrategy`'s existing consumer contract as part of this boundary review.

## Observation-date convention

For deterministic selection utilities, selecting the latest available observation on or before an explicit target date is the current engineering convention. When the target falls on a non-trading day, this means the selector can choose a prior observation rather than a future observation. This convention alone does not establish that the selected observation is valid under a provider's exchange calendar or within an approved freshness limit.

The monthly research description (“last trading day” and execution on the “next trading day”) still needs a source/calendar contract before production scheduling. The 12-month anniversary endpoint rule, provider calendar, freshness threshold, and adjusted-price semantics remain distinct validation gates.

## Closure criteria

The absolute-momentum boolean may be implemented only after the methodology owner has explicitly approved:

- the benchmark instrument and its relationship to the configured defensive holding;
- the exact comparison expression and equality behavior;
- the return horizon and adjusted-price acceptance criteria;
- matched date-selection and freshness rules for both inputs;
- fail-closed behavior for any invalid input;
- deterministic test cases that cover positive, negative, equal, missing, stale, and invalid return inputs.

Until then, retain return inputs as data, not as a signal. No source adapter, external network access, persistence, scheduled collection, strategy activation, broker execution, or Core Runtime change is authorized by this document.

## Related documents

- `Moon_ADM_Data_Contract.md`
- `Moon_ADM_Data_Readiness_and_Closure.md`
- `Moon_ADM_Data_Implementation_Boundary.md`
- `Orion_Framework_Data_Contracts.md`
- `Orion_Data_Pipeline.md`
- `../03_Research/Moon/ADM/ADM_Orion.md`
- `../03_Research/Moon/ADM/ADM_Research.md`
- `../05_Decisions/Decision_Log.md` (D-026 and D-028)

## Step 35 — research reconciliation of the comparison concept

`Moon_ADM_Absolute_Momentum_Comparison_Policy_Closure_Review.md` reconciles
the research description with the original GEM decision process. The research
direction is benchmark-relative comparison against cash/defensive return, not
an implicit comparison against zero. The benchmark instrument, exact comparison
operator, equality behavior, adjusted-price acceptance criteria, and production
data policies remain open. No comparison boolean or signal is implemented.

## Step 34 — data readiness does not imply policy approval

The implementation now has a cross-input readiness audit for relative-momentum
freshness and caller-supplied absolute-momentum returns. Matching target dates,
field, selection-policy provenance, and an explicit shared freshness limit are
required. The audit records the absolute-input freshness checks but deliberately
keeps `signal_ready` false and lists unresolved investment/source policy gates.
This does not approve SGOV or any other benchmark and does not define the
absolute-momentum comparison expression.
