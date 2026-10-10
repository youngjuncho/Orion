# Moon ADM Comparison-to-Signal Integration Guard

Version: 1.0  
Status: Engineering Contract - D-055 Approved; Production Data Gates Open
Last Updated: 2026-10-10

## Purpose

Define the fail-closed boundary between a typed absolute-momentum comparison result and any future ADM signal assembly. The guard is a readiness decision only: it does not construct `ADMSignalInput`, mutate framework state, or activate a strategy.

## Contract

`src/orion/frameworks/moon/adm_data.py` provides:

- `ADMPolicyApprovalStatus`: `APPROVED`, `NOT_APPROVED`, `UNKNOWN`.
- `ADMComparisonSignalGuardResult`: eligibility, comparison status, caller-supplied approval provenance, and explicit blocking reasons.
- `guard_adm_comparison_for_signal_assembly(...)`: validates comparison/readiness consistency and evaluates the integration gates.

The guard blocks when any of these apply:

1. Comparison status is `UNAVAILABLE`.
2. The comparison's risk asset, benchmark, or returns do not match the freshness-checked absolute-momentum inputs in the readiness object.
3. Data quality has not passed.
4. Any readiness policy gate remains unresolved.
5. The caller-attested policy approval status is not explicitly `APPROVED`.
6. An approval reference is missing.
7. Available comparison policy provenance is missing.

`UNAVAILABLE` is never treated as `FALSE`. `TRUE` and `FALSE` comparison outputs are not sufficient on their own to proceed.

## Governance provenance limitation

The comparison methodology is approved by D-055. The guard's approval status and reference are still supplied by the caller; it records that attestation but does not independently verify a decision log, document, or external governance system. Production integration must bind this value to an authoritative governance record before relying on it.

## Readiness closure

`ADMDataAssemblyReadiness.signal_ready` is true only when its `unresolved_policy_gates` collection is empty. The default readiness path retains unresolved gates and therefore remains blocked. Tests may simulate a closed policy set to exercise the positive guard path; that fixture does not approve production policy.

## Scope guardrails

- No `ADMSignalInput` conversion is implemented.
- D-055 supplies SGOV and strict greater-than comparison by default; no provider/source semantics or data-freshness policy is inferred.
- No external data provider, network I/O, persistence, scheduler, broker execution, or strategy activation is introduced.
- `config/moon.yaml`, `ADMStrategy`, Core Runtime, and framework orchestration remain unchanged.

## Related documents

- `Moon_ADM_Absolute_Momentum_Comparison_Contract.md`
- `Moon_ADM_Absolute_Momentum_Policy_Boundary.md`
- `Moon_ADM_Data_Readiness_and_Closure.md`
- `Moon_ADM_Data_Implementation_Boundary.md`
- `Orion_Data_Pipeline.md`
