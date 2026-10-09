# Moon ADM Absolute Momentum Comparison Policy Closure Review

Version: 1.0  
Status: Research Reconciliation — Methodology Direction Identified; Production Policy Still Open  
Last Updated: 2026-10-09

## Purpose

This review reconciles the existing ADM research wording with the implementation boundary. It distinguishes a methodological direction already present in the research from decisions that still require explicit approval. It does not itself approve a benchmark, validate a provider's adjusted-price series, or activate ADM.

## Findings from the existing research

`docs/03_Research/Moon/ADM/ADM_Research.md` describes absolute momentum as assessing whether the selected asset has performed positively relative to a risk-free alternative. Its original GEM decision process explicitly says to compare the winning risk asset's momentum with the cash return. `ADM_Orion.md` carries forward a trailing 12-month adjusted-price total-return formula and lists SGOV as the primary defensive-asset candidate, with BIL and SHY as backups; the defensive instrument is marked pending final approval.

The most faithful reading of the existing research is therefore **benchmark-relative comparison against a cash/defensive return**, rather than silently replacing the benchmark with zero return. However, the exact benchmark instrument is not approved, and the return-measurement standard remains marked pending validation. This research reconciliation is not a new investment-methodology decision.

## Classification of policy items

| Item | Finding | Status |
|---|---|---|
| Comparison concept | Compare the selected risk asset's trailing momentum return with a cash/defensive benchmark return | Documented research direction; formal policy closure still required |
| Benchmark instrument | SGOV primary candidate; BIL and SHY backups | Open — no instrument is approved by this review |
| Comparison operator | Research implies a benchmark-relative comparison, but does not explicitly define the exact boolean expression or tie treatment | Open — do not encode an operator or equality result by inference |
| Return horizon | Trailing 12-month adjusted-price total-return proxy | Specified in research; validation remains pending |
| Adjusted-price semantics | Must represent the intended total-return proxy | Open per provider/source contract |
| Date selection and freshness | Use explicit target dates, prior-observation-on-or-before selection, and explicit freshness validation in engineering utilities | Engineering behavior exists; calendar and production thresholds remain open |
| Invalid or missing input | No boolean should be generated from incomplete inputs | Engineering fail-closed constraint |
| Configured defensive holding vs benchmark | May be the same instrument, but that relationship is not established automatically | Open — explicit mapping/approval required |

## Implementation consequence

Do not implement `absolute_momentum_positive` in this step. `calculate_adm_absolute_momentum_inputs(...)` remains a return-input preparation utility only. The next signal-calculation implementation gate requires a recorded methodology decision that explicitly identifies:

1. the approved benchmark instrument and whether it must match the configured defensive holding;
2. the exact comparison expression and equality behavior;
3. acceptance criteria for the adjusted-price series and confirmation of the intended 12-month horizon;
4. matched endpoint selection and approved freshness limits for both returns;
5. fail-closed handling for missing, stale, invalid, or source-incompatible inputs.

Once those decisions are approved, add deterministic tests for risk return above, below, and equal to benchmark return, as well as missing, stale, non-finite, and invalid inputs. Until then, keep the data-return outputs separate from the strategy input and boolean signal.

## Scope guardrails

This review does not change `ADMStrategy`, `ADMSignalInput`, `config/moon.yaml`, the empty active-strategy allowlist, Core Runtime, or any framework orchestration. It does not approve Yahoo Finance or any other provider and does not authorize network access, scheduled collection, persistence, or broker execution.

## Related documents

- `Moon_ADM_Absolute_Momentum_Policy_Boundary.md`
- `Moon_ADM_Data_Readiness_and_Closure.md`
- `Moon_ADM_Data_Implementation_Boundary.md`
- `Moon_ADM_Data_Contract.md`
- `../03_Research/Moon/ADM/ADM_Research.md`
- `../03_Research/Moon/ADM/ADM_Orion.md`
- `../05_Decisions/Decision_Log.md` (D-026 and D-028)
