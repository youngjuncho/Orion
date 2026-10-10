# Moon ADM Provider-Neutral Adapter Contract

Version: 1.0  
Status: Implemented — Fixture-tested; no live provider integration authorized  
Last Updated: 2026-10-09

## Purpose

Define a stable boundary between a source-specific fetch mechanism and Orion's canonical `MarketDataSet`, without selecting a provider or interpreting financial semantics.

## Implemented boundary

- `RawMarketDataSource.fetch()` returns one raw batch mapping.
- `ProviderNeutralMarketDataAdapter.load()` checks the batch envelope and normalizes observations through `src/data/pipeline.py`.
- Output is a canonical `MarketDataSet` and therefore inherits required-field, value-type, finite-number, and duplicate-identity validation.
- A source exception propagates; malformed or duplicate batches raise an error. No partial or success-looking dataset is returned.
- The adapter does not retry, cache, interpolate, substitute fields, infer symbols, reinterpret timestamps, or choose a fallback source.

## Raw batch shape

The provider-neutral boundary expects `as_of` and `observations`. Each observation must explicitly provide `symbol`, `field`, `observed_at`, `value`, and `source`; `currency` and string-to-string `metadata` are optional. This is an envelope contract, not an approved provider-specific mapping.

## Provenance

The canonical contract retains `source` and string metadata. A concrete provider adapter must document and map the provider identifier, requested/returned instrument identifiers, provider field name and field semantics, observation timestamp meaning, retrieval timestamp when available, adapter version, and any revision/snapshot identifier required for reproducibility. This generic layer does not fabricate missing provenance.

## Failure behavior

- Fetch exceptions propagate to the caller.
- Missing batch keys, invalid observation shapes, malformed required fields, unsupported values, and duplicate canonical identities fail closed.
- No retry, timeout, rate-limit, cache, or fallback behavior is defined here; those require a provider-specific approved contract.
- A structurally valid dataset is not thereby fresh, source-calendar-valid, semantically suitable for D-028, or approved for investment-signal use.

## Test coverage

The fake-source tests cover a valid two-instrument batch, normalization and metadata preservation, source exceptions, missing envelope keys, malformed observations, and duplicate records. Tests use local fixtures only and do not require network access.

## Explicit non-goals

This contract does not approve Yahoo Finance or any other source, validate `adjusted_close` as a total-return proxy, set freshness thresholds, select a defensive benchmark, calculate the ADM absolute-momentum comparison, construct `ADMSignalInput`, or activate a Moon strategy.

## Next gate

Before any provider-specific adapter is implemented, approve the provider and document instrument identity, field semantics, timestamps/calendar, correction/revision policy, freshness, missing/stale/duplicate response handling, provenance, and network failure behavior. The acceptance matrix is maintained in `Moon_ADM_Provider_Adapter_Acceptance_Test_Matrix.md`. Keep Core Runtime and Moon strategy activation unchanged.

## Related documents

- `Moon_ADM_Provider_Adapter_Readiness_Review.md`
- `Moon_ADM_Data_Contract.md`
- `Moon_ADM_Data_Pipeline_Contract_Consolidation.md`
- `Orion_Framework_Data_Contracts.md`
- `Orion_Data_Pipeline.md`
