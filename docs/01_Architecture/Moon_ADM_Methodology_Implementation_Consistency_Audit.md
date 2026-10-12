# Moon ADM Methodology–Implementation Consistency Audit

Version: 1.0  
Status: Offline engineering audit; live provider validation and production gates remain open  
Date: 2026-10-12

## Purpose and scope

This audit compares the current Moon ADM calculation path with `ADM_Orion.md`, decisions D-028 and D-055 through D-059, and the data-readiness contracts. It uses source inspection and synthetic tests only. It does not call Alpha Vantage, validate real-world adjusted-price accuracy, approve a signal, or authorize strategy activation.

## Checks and conclusions

| Area | Implementation check | Result / boundary |
|---|---|---|
| Return formula | `calculate_adjusted_price_return` calculates current adjusted price divided by trailing adjusted price, minus one | Consistent with the documented trailing-12-month return formula, assuming the selected field is a valid total-return proxy |
| Target endpoints | `derive_adm_monthly_target_dates` excludes the `as_of` month and targets the prior calendar month-end plus the same month-end one year earlier | Consistent with D-058's engineering default; this does not settle signal timestamp, timezone, or next-trading-day execution mapping |
| Observation selection | The selector chooses the latest matching observation on or before each target; future observations are not selected | Consistent with D-056; provider-calendar validity remains a separate gate |
| Freshness | Monthly assessment applies the approved seven-calendar-day maximum to both endpoints for VTI, VEU, and the selected risk asset/SGOV pair | Consistent with D-058; freshness alone does not validate price-series semantics |
| Relative momentum | VTI and VEU use the same field, target dates, and selection-policy identifier; the larger return wins; ties fail closed | Consistent with the current specification's defined winner rule and explicit tie boundary |
| Absolute momentum | The selected risk asset's trailing return is compared with SGOV's trailing return using D-055's strict `>` operator; equality is false | Consistent with D-055; comparison result is not converted into `ADMSignalInput` |
| Revision handling | The provider consumes a complete response batch per invocation, rejects duplicate JSON keys and duplicate monthly bars, and does not merge retrievals | Consistent with D-059's per-invocation rule; historical snapshots and point-in-time replay remain unimplemented |
| Signal/activation boundary | The data workflow returns an assessment, not `ADMSignalInput`; the comparison guard remains fail-closed because authoritative governance binding is not implemented | Consistent with the stated activation boundary; no active strategy or Runtime integration is authorized |

## Finding addressed in this audit

`ADMMonthlyDataAssessment` validated the types and several pairwise fields of its components, but its constructor did not independently prove that:

1. `selected_risk_asset` was the actual winner in its retained VTI/VEU relative-momentum result; and
2. the `readiness` object referred to the same relative- and absolute-momentum inputs retained by the assessment.

The normal `assess_adm_monthly_dataset()` factory assembled these values consistently, but a manually constructed or replaced typed assessment could mix components from separate inputs and still pass some constructor checks. This weakened the composite object's invariant at a public data boundary.

The constructor now rejects a relative-momentum tie, recomputes the expected winner from the retained returns, and verifies that both readiness inputs match the assessment inputs. Regression tests cover cross-batch readiness substitution and a selected asset that does not match the relative-momentum winner.

A further provider-boundary check found that Python's numeric conversion treats JSON `true` as `1.0`. The Alpha Vantage parser now rejects boolean and non-scalar JSON values before numeric conversion, preventing malformed adjusted-close values from being accepted as plausible positive prices. Fixture tests cover booleans, null, arrays, and objects. This is a parser-hardening result, not evidence about live provider behavior.

## Remaining open items

- Live Alpha Vantage response shape and actual VTI/VEU/SGOV history coverage have not been verified in this environment because `ORION_ALPHA_VANTAGE_API_KEY` is not configured.
- Empirical adjusted-price history parity and point-in-time/revision behavior remain unverified.
- Provider calendar, publication-time SLA, signal-date representation, timezone, and next-trading-day execution mapping remain separate policy/validation gates.
- The current workflow is an in-memory data assessment only. It does not construct a strategy signal, activate ADM, invoke Runtime, place orders, or persist data.

## Verification

The audit's new regression tests use synthetic data and require no network access. Full-suite, UTF-8 policy, compilation, and archive-integrity results are recorded with the package produced for this audit.
