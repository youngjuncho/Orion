# Moon ADM Absolute Momentum Comparison Policy Closure Review

Version: 1.0  
Status: Research Reconciliation - D-055 Methodology Approved; Data Gates Open
Last Updated: 2026-10-10

## Purpose

This review reconciles the existing ADM research wording with the implementation boundary. D-055 now approves SGOV and the strict benchmark-relative comparison; provider adjusted-price validation and ADM activation remain open.

## Findings from the existing research

`docs/03_Research/Moon/ADM/ADM_Research.md` describes absolute momentum as assessing whether the selected asset has performed positively relative to a risk-free alternative. Its original GEM decision process explicitly says to compare the winning risk asset's momentum with the cash return. `ADM_Orion.md` carries forward a trailing 12-month adjusted-price total-return formula and lists SGOV as the primary defensive-asset candidate, with BIL and SHY as backups; the defensive instrument is marked pending final approval.

The research direction is **benchmark-relative comparison against a cash/defensive return**, rather than comparison against zero. D-055 approves SGOV as the benchmark and strict greater-than comparison, with equality false. The return-measurement standard remains pending source validation.

## Classification of policy items

| Item | Finding | Status |
|---|---|---|
| Comparison concept | Compare the selected risk asset's trailing momentum return with a cash/defensive benchmark return | Approved by D-055; provider measurement remains pending |
| Benchmark instrument | SGOV | Approved by D-055 |
| Comparison operator | Selected risk return strictly greater than SGOV; equality is false | Approved by D-055 |
| Return horizon | Trailing 12-month adjusted-price total-return proxy | Specified in research; validation remains pending |
| Adjusted-price semantics | Must represent the intended total-return proxy | Open per provider/source contract |
| Date selection and freshness | Use explicit target dates, prior-observation-on-or-before selection, and explicit freshness validation in engineering utilities | Engineering behavior exists; calendar and production thresholds remain open |
| Invalid or missing input | No boolean should be generated from incomplete inputs | Engineering fail-closed constraint |
| Configured defensive holding vs benchmark | May be the same instrument, but that relationship is not established automatically | Open — explicit mapping/approval required |

## Implementation consequence

The methodology items below are resolved by D-055. Before production signal integration, data/governance gates still require:

1. acceptance criteria for the provider's adjusted-price series;
2. matched endpoint selection and approved freshness limits for both returns;
3. fail-closed handling for missing, stale, invalid, or source-incompatible inputs;
4. negative tests through the actual orchestration path before activation.

D-055 comparison behavior is implemented and covered for greater, equal, and lower returns. Keep signal assembly and activation blocked until the remaining data gates are closed.

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
