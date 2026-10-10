# Moon ADM Provider Adapter Readiness Review

Version: 1.0  
Status: Readiness Review — Provider-Neutral Boundary Implemented; Production Provider Integration Not Authorized  
Last Updated: 2026-10-10

## Purpose

This review determines whether the current Moon ADM data contracts are sufficient to begin implementing a provider-specific adapter. It separates reusable adapter structure from source-dependent behavior and the D-055-approved comparison methodology. It does not approve Yahoo Finance or another provider, authorize network access, or activate ADM.

## Decision

**A provider-neutral adapter boundary may be designed, but a production provider adapter must not yet be implemented or connected.** The reusable `MarketDataProvider` protocol and canonical `MarketDataSet` envelope exist. Step 40 adds `ProviderNeutralMarketDataAdapter`, a fixture-tested wrapper that normalizes raw batches and propagates source errors. However, provider selection, adjusted-price semantics, calendar and timestamp rules, data-quality behavior, historical revision expectations, and source measurement for the D-055-approved SGOV comparison remain open.

The current engineering date-selection default is retained: for each explicit target date, select the latest observation in the supplied dataset whose date is on or before the target. This avoids future observations and matches the chosen prior-observation rule. It does not certify that the provider's observation is an official exchange trading-day bar or sufficiently fresh.

## Readiness classification

| Area | Current state | Adapter readiness requirement | Status |
|---|---|---|---|
| Canonical envelope | `MarketDataPoint` and `MarketDataSet` exist | Map provider records explicitly to canonical fields and validate every batch | Reusable contract exists |
| Instrument identity | ADM risk assets are VTI and VEU; D-055 comparison benchmark is SGOV | Define provider identifiers and confirm instrument identity for every symbol | Open |
| Price field | `adjusted_close` is a candidate field under D-028 | Document provider adjustment methodology and validate suitability as total-return proxy; never silently substitute `close` | Open |
| Timestamp and timezone | Canonical `observed_at` is a string | Specify timestamp format, timezone, date extraction, and whether bars represent session close | Open |
| Calendar and endpoints | Prior-observation-on-or-before target is the engineering default | Define source calendar and confirm that selected records represent valid observations; document 12-month target construction | Partially defined |
| Freshness | Generic validators accept caller-supplied maximum age | Approve production threshold and define how weekends/holidays differ from missing or stale bars | Open |
| Missing/duplicate data | Duplicate canonical identity is rejected; missing requested endpoints fail closed | Define provider-specific absent-bar and duplicate-response handling; no silent fill/interpolation | Partially defined |
| Revisions/corrections | No as-observed snapshot or revision policy | Decide whether results use latest revised history or preserve retrieval-time snapshots; define reproducibility metadata | Open |
| Source failure and retry | No provider I/O or retry policy | Specify timeout, rate-limit, retry, cache, and failure semantics only after provider approval | Open |
| Provenance | Canonical `source` and string metadata are available | Record provider, requested/returned identifiers, retrieval timestamp, selected observation dates, field semantics, and adapter version | Contract design required |
| Absolute momentum | Inputs can be compared using D-055 SGOV/strict-greater-than policy | Provider source semantics, freshness, and calendar approval remain open |
| Governance | Caller-supplied approval reference is an attestation only | Bind production approval checks to authoritative decision records | Open |

## Required source contract before implementation

A provider-specific adapter may start only after a named provider is approved for the intended use and its contract records:

1. Provider name, access method, licensing/usage constraints, and approved intended use.
2. Exact identifiers and identity checks for VTI, VEU, and SGOV as the D-055 comparison benchmark.
3. Canonical mapping for `symbol`, `field`, `observed_at`, `value`, `source`, `currency`, and metadata.
4. The exact meaning of the provider's adjusted-price field, adjustment treatment for distributions/splits, and evidence that it is acceptable for D-028.
5. Timezone, daily-bar timestamp meaning, provider/exchange calendar, evaluation-date convention, and trailing-12-month endpoint convention.
6. Explicit behavior for absent bars, duplicate bars, stale values, delayed publication, corrections, revised history, and conflicting responses.
7. Approved freshness thresholds and whether thresholds differ by data role or instrument.
8. Retrieval provenance and deterministic replay/reproducibility expectations.
9. Timeout, rate-limit, retry, cache, and outage behavior, if those mechanisms are authorized.
10. Deterministic fixture-based tests that do not require live network access.

## Required adapter acceptance tests

- Valid provider records map to the canonical contract without guessing field semantics.
- Unknown symbols, unsupported fields, malformed timestamps, invalid numeric values, and unexpected currencies fail explicitly.
- No selected observation is later than its target date.
- Weekend/holiday targets follow the documented prior-observation policy, while source-calendar validation remains independently testable.
- Missing, duplicate, stale, revised, and conflicting observations follow explicit source-contract behavior.
- Adjusted-price semantics are asserted in adapter metadata/contract and cannot silently degrade to raw close.
- The selected observations and computed returns can be reproduced from recorded provenance and deterministic fixtures.
- Provider failure cannot produce a partial or successful-looking `MarketDataSet`.
- No network access is required for unit tests.
- Adapter output alone cannot activate ADM, bypass the signal integration guard, or create an `ADMSignalInput` while provider/data and signal-integration gates remain open.

## Implementation boundary

The existing source-agnostic calculation helpers can be reused. Do not place provider I/O inside `ADMStrategy` or the Core Runtime. Do not add a provider dependency, scheduled collection, persistent cache, fallback provider, or automatic source precedence until its source contract is approved. D-055 approves SGOV and strict greater-than comparison; do not infer provider/source approval or signal activation from that methodology decision.

## Recommended next step

The provider-neutral adapter boundary and fake-provider failure tests are now implemented in `src/data/adapters.py` and `tests/data/test_contracts.py`. Keep live provider integration blocked. Step 42 consolidates open items in [`Moon_ADM_Provider_Contract_Decision_Register.md`](Moon_ADM_Provider_Contract_Decision_Register.md). Use it to track authoritative decisions and evidence; do not treat the register itself as approval or add network access before the relevant gates are closed.

## Related documents

- `Moon_ADM_Provider_Neutral_Adapter_Contract.md`
- `Moon_ADM_Provider_Contract_Decision_Register.md`
- `Moon_ADM_Data_Contract.md`
- `Moon_ADM_Data_Readiness_and_Closure.md`
- `Moon_ADM_Data_Implementation_Boundary.md`
- `Moon_ADM_Data_Pipeline_Contract_Consolidation.md`
- `Orion_Framework_Data_Contracts.md`
- `Orion_Data_Pipeline.md`
- `docs/03_Research/Moon/ADM/ADM_Orion.md`


## Acceptance evidence

The provider-neutral boundary acceptance scenarios and remaining provider-specific gates are tracked in [`Moon_ADM_Provider_Adapter_Acceptance_Test_Matrix.md`](Moon_ADM_Provider_Adapter_Acceptance_Test_Matrix.md). Passing fixture tests does not approve a provider or close outstanding policy decisions.
