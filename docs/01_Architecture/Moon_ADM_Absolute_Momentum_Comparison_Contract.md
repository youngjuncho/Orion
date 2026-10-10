# Moon ADM Absolute Momentum Comparison Contract

Version: 1.0  
Status: Engineering Contract - D-055 Comparison Policy Approved; Data Gates Open
Last Updated: 2026-10-10

## Purpose

Define the typed boundary for comparing already-calculated risk-asset and benchmark returns. D-055 approves the default benchmark and operator; source-specific measurement and activation remain separate gates.

## Contract types

`src/orion/frameworks/moon/adm_data.py` provides:

- `ADMAbsoluteMomentumComparisonStatus`: `TRUE`, `FALSE`, and `UNAVAILABLE`.
- `ADMAbsoluteMomentumComparisonOperator`: explicit strict `risk_return > benchmark_return` and inclusive `risk_return >= benchmark_return` operators.
- `ADMAbsoluteMomentumComparisonPolicy`: requires a caller-supplied policy ID, benchmark symbol, and operator. The policy ID is provenance only; it is not proof of governance approval.
- `ADMAbsoluteMomentumComparisonResult`: retains status, both symbols, both returns, policy/operator provenance, and an unavailable reason where relevant.
- `compare_adm_absolute_momentum_returns(...)`: uses the approved D-055 policy by default; callers may supply an explicit policy for non-production analysis.

## Semantics

When no policy is supplied, D-055 compares the selected risk return strictly greater than the SGOV return. If an explicit policy benchmark does not match the benchmark in the return inputs, the result is `UNAVAILABLE`; it is not silently remapped.

Under the approved D-055 strict operator, equal returns produce `FALSE` (Risk Off). The inclusive operator remains available for explicit analysis but is not the approved ADM policy.

`UNAVAILABLE` must never be interpreted as `FALSE` or converted to `ADMSignalInput.absolute_momentum_positive`. Even a `TRUE`/`FALSE` result under a caller-supplied policy is only the output of that explicit comparison contract. It does not itself certify the policy's approval, benchmark validity, price-field total-return semantics, observation freshness, or production readiness.

## Signal integration guard

`Moon_ADM_Comparison_Signal_Integration_Guard.md` defines the fail-closed boundary between comparison results and future signal assembly. An available comparison cannot proceed unless its inputs match the freshness-checked readiness object, all policy gates are closed, approval status is explicitly supplied as approved, and an approval reference is present. The guard does not create `ADMSignalInput`; approval provenance is caller-supplied and must be bound to an authoritative governance record in production.

## Still open for governance

1. Approved adjusted-price source semantics and validation of the trailing-12-month series.
2. Production freshness thresholds, provider calendar, and stale/revised/missing-data policy.
3. Explicit approval provenance and end-to-end integration criteria before a comparison can feed a production strategy input.

## Scope guardrails

This step does not change `ADMStrategy`, `ADMSignalInput`, `config/moon.yaml`, the empty active-strategy allowlist, Core Runtime, or framework orchestration. No provider I/O, network dependency, persistence, scheduler, or broker execution is introduced.

## Related documents

- `Moon_ADM_Comparison_Signal_Integration_Guard.md`
- `Moon_ADM_Absolute_Momentum_Policy_Boundary.md`
- `Moon_ADM_Absolute_Momentum_Comparison_Policy_Closure_Review.md`
- `Moon_ADM_Data_Readiness_and_Closure.md`
- `Moon_ADM_Data_Implementation_Boundary.md`
- `Orion_Data_Pipeline.md`
