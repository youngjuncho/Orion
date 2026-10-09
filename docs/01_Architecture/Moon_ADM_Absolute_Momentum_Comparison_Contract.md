# Moon ADM Absolute Momentum Comparison Contract

Version: 1.0  
Status: Engineering Contract — Investment Policy Not Approved  
Last Updated: 2026-10-09

## Purpose

Define the typed boundary for comparing already-calculated risk-asset and benchmark returns without silently choosing an investment rule. This contract does not approve a benchmark, comparison operator, adjusted-price source, or ADM activation.

## Contract types

`src/orion/frameworks/moon/adm_data.py` provides:

- `ADMAbsoluteMomentumComparisonStatus`: `TRUE`, `FALSE`, and `UNAVAILABLE`.
- `ADMAbsoluteMomentumComparisonOperator`: explicit strict `risk_return > benchmark_return` and inclusive `risk_return >= benchmark_return` operators.
- `ADMAbsoluteMomentumComparisonPolicy`: requires a caller-supplied policy ID, benchmark symbol, and operator. The policy ID is provenance only; it is not proof of governance approval.
- `ADMAbsoluteMomentumComparisonResult`: retains status, both symbols, both returns, policy/operator provenance, and an unavailable reason where relevant.
- `compare_adm_absolute_momentum_returns(...)`: performs a comparison only when a policy is explicitly supplied.

## Semantics

When no policy is supplied, the result is `UNAVAILABLE` with reason `comparison_policy_not_supplied`. If the policy benchmark does not match the benchmark in the return inputs, the result is `UNAVAILABLE`; it is not silently remapped.

With an explicitly supplied operator, strict greater-than returns `FALSE` for equal values; greater-than-or-equal returns `TRUE` for equal values. These are generic operator semantics, not a selection or approval of either policy for production ADM.

`UNAVAILABLE` must never be interpreted as `FALSE` or converted to `ADMSignalInput.absolute_momentum_positive`. Even a `TRUE`/`FALSE` result under a caller-supplied policy is only the output of that explicit comparison contract. It does not itself certify the policy's approval, benchmark validity, price-field total-return semantics, observation freshness, or production readiness.

## Signal integration guard

`Moon_ADM_Comparison_Signal_Integration_Guard.md` defines the fail-closed boundary between comparison results and future signal assembly. An available comparison cannot proceed unless its inputs match the freshness-checked readiness object, all policy gates are closed, approval status is explicitly supplied as approved, and an approval reference is present. The guard does not create `ADMSignalInput`; approval provenance is caller-supplied and must be bound to an authoritative governance record in production.

## Still open for governance

1. Final benchmark instrument and whether it must equal the configured defensive holding.
2. Approved comparison operator and equality behavior.
3. Approved adjusted-price source semantics and trailing-12-month measurement convention.
4. Production freshness thresholds, provider calendar, and stale/revised/missing-data policy.
5. Explicit approval reference and integration criteria before a comparison can feed the strategy input.

## Scope guardrails

This step does not change `ADMStrategy`, `ADMSignalInput`, `config/moon.yaml`, the empty active-strategy allowlist, Core Runtime, or framework orchestration. No provider I/O, network dependency, persistence, scheduler, or broker execution is introduced.

## Related documents

- `Moon_ADM_Comparison_Signal_Integration_Guard.md`
- `Moon_ADM_Absolute_Momentum_Policy_Boundary.md`
- `Moon_ADM_Absolute_Momentum_Comparison_Policy_Closure_Review.md`
- `Moon_ADM_Data_Readiness_and_Closure.md`
- `Moon_ADM_Data_Implementation_Boundary.md`
- `Orion_Data_Pipeline.md`
