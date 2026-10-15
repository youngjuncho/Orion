# Moon/ADM Signal Readiness and Governance-Binding Audit — 2026-10-15

## Finding

`ADMMonthlyDataAssessment.signal_assembly_ready` previously returned true when data-policy gates were manually cleared and the comparison was available. However, `guard_adm_comparison_for_signal_assembly` always blocks with `authoritative_governance_binding_not_implemented` because PCD-15 is not integrated. The two public readiness indicators could therefore communicate conflicting states.

## Change

The assessment property now remains false while the authoritative governance binding is unimplemented. A regression test constructs an assessment with all data-policy gates cleared and confirms that the assessment still does not report signal assembly as ready. The dedicated guard remains the detailed source of blocked reasons.

## Scope and limits

- No investment rule, asset selection, benchmark, comparison operator, or strategy activation was changed.
- `config/moon.yaml` remains `active_strategies: []`.
- This is a fail-closed status correction, not implementation or approval of PCD-15.
- Full-suite validation in this temporary extracted bundle is not a substitute for running the project-designated Python 3.12.13 command after selective local merge.
