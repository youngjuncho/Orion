# Moon / ADM Latest-Git Audit — 2026-10-18

## Scope and evidence

- Input bundle: `Orion_1018(1).zip`
- Embedded Git branch: `main`
- Embedded HEAD: `109d17db66b2b62f60725e5583e69861bf13c695`
- HEAD commit date: `2026-10-16 21:57:56 +0900`
- HEAD subject: `Update alpha vantage`
- Extracted worktree status at intake: clean
- Validation runtime: Python 3.13.5
- Full automated test suite: `476 passed in 4.23s`
- Live Alpha Vantage calls during this audit: none

This audit distinguishes code/test evidence from prior audit conclusions and from production readiness. The full test result is for the extracted bundle under Python 3.13.5; it is not evidence of a run in the project's designated Windows Conda Python 3.12.13 environment.

## Audit table

| Item | Status | Evidence | Finding |
|---|---|---|---|
| D-055: approved comparison policy ID and operator consistency | 충족 | `src/orion/frameworks/moon/adm_data.py` (`ADMMonthlyDataAssessment.__post_init__`, `guard_adm_comparison_for_signal_assembly`); `tests/orion/frameworks/moon/test_adm_data.py` | Assessment validates both the approved policy ID and operator; the guard independently rejects a policy/operator mismatch. |
| D-058: seven-day freshness cap and bypass resistance | 충족 | `src/orion/frameworks/moon/adm_data.py` (`validate_adm_observation_pair_freshness`, readiness constructors); `tests/orion/frameworks/moon/test_adm_data.py` | Pair-level and higher-level paths reject thresholds above the approved seven-day maximum. |
| ADM readiness: empty policy-gate collection must not falsely open signal readiness | 충족 | `src/orion/frameworks/moon/adm_data.py` (`ADMDataAssemblyReadiness`, `ADMMonthlyDataAssessment.signal_assembly_ready`); `tests/orion/frameworks/moon/test_adm_data.py` | The default policy gates remain unresolved. Even if a caller clears them, `signal_assembly_ready` remains `False`, and the guard keeps a governance-binding blocker. |
| PCD-15 authoritative governance binding | 미충족 | `src/orion/frameworks/moon/adm_data.py` (`guard_adm_comparison_for_signal_assembly`); `docs/01_Architecture/Moon_ADM_PCD15_Governance_Binding_Contract_Proposal.md`; `docs/01_Architecture/Moon_ADM_Governance_Binding_Implementation_Audit.md` | The binding/resolver is explicitly not implemented. This is a known blocking gap, not a completed control. Signal assembly must remain blocked. |
| Governance decision-record validation and registry-event processing | 부분 충족 | `src/data/governance.py`; `tests/data/test_governance.py`; `tests/data/test_governance_integration.py`; `src/data/registry_acceptance_service.py`; `src/data/registry_acceptance_consumer.py` | General record/snapshot validation and registry acceptance components exist with tests, but they are not wired into an authoritative PCD-15 resolver consumed by the ADM signal guard. A generic validator or caller-provided attestation is not proof of authoritative approval. |
| Alpha Vantage diagnostic symbol inclusion | 충족 | `src/data/alphavantage.py`; `tests/test_alpha_vantage_live_contract_script.py`; `tests/data/test_alphavantage.py` | Provider notice errors include the affected symbol (e.g. `for VEU`) and stop before accepting a partial batch. |
| Alpha Vantage live contract / VEU root cause | 검증 불가 | `scripts/check_alpha_vantage_live_contract.py`; `tests/test_alpha_vantage_live_contract_script.py`; inherited live result | The recorded VEU `API_RATE_LIMIT` root cause remains unresolved. No live API calls were made during this audit; VTI/SGOV individual successes do not prove the full contract passes. |
| Designated Python 3.12.13 full-suite run | 검증 불가 | Current audit runtime and full-suite output | The available environment is Python 3.13.5. Run the specified Windows Conda command after synchronizing the bundle. |

## Safety boundary

- `config/moon.yaml` must retain `active_strategies: []`.
- Do not enable signal assembly until PCD-15's authoritative binding is implemented and independently reviewed.
- Do not treat local readiness edits, caller-supplied `APPROVED`, or a non-empty caller-supplied reference as authoritative governance evidence.
- Do not repeatedly retry Alpha Vantage live calls while the rate-limit condition may persist.
- This audit does not change investment methodology, portfolio allocation, strategy activation, order execution, or provider credentials.

## Required next steps

1. Keep PCD-15 as an explicit blocking condition.
2. Obtain and approve the unresolved authority, key/signature verification, currentness/revocation, scope, anti-rollback, and recovery decisions documented in the PCD-15 contract proposal before implementing a resolver.
3. Integrate a typed verified governance resolution into the ADM guard only after those design decisions are approved; caller attestations must not satisfy the binding.
4. Run the full suite using `"$HOME/anaconda3/envs/orion/python.exe" -m pytest -q -p no:cacheprovider` in the designated Windows Git Bash environment.
5. Resolve the Alpha Vantage VEU result only when safe API capacity and appropriate evidence are available.
