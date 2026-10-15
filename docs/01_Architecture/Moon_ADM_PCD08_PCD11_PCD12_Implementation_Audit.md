# Moon ADM PCD-08 / PCD-11 / PCD-12 Implementation Audit

**Status:** Audit only; no operational policy closed by this document  
**Date:** 2026-10-15  
**Scope:** Alpha Vantage monthly adjusted-price adapter, canonical market-data pipeline, and in-memory ADM assessment workflow.  
**Out of scope:** Live API calls, retry/cache/scheduling, durable raw-payload storage, signal assembly, Runtime integration, and strategy activation.

## Summary

The existing implementation is consistent with the currently approved fail-closed and isolated-workflow boundaries. This audit does not recommend adding retries, caching, persistence, or provider fallback while PCD-12 remains open. One PCD-11 semantic issue requires an explicit decision before claiming stable reproducibility: `selected_input_digest` currently fingerprints selected observations **and their metadata**, including `retrieved_at`.

## PCD-08 — Missing, partial, and malformed responses

### Implemented and fixture-tested

- The provider requests `VTI`, `VEU`, and `SGOV` sequentially and rejects the full load when a required response fails.
- Provider notice payloads (`Error Message`, `Note`, `Information`) fail closed with sanitized diagnostic codes.
- Response instrument identity must match the requested symbol.
- The monthly adjusted series must exist and contain at least 13 valid observations.
- Dates are parsed as canonical `YYYY-MM-DD`; more than one observation in a calendar month is rejected.
- Adjusted close values reject booleans, unsupported JSON types, non-finite values, and non-positive values.
- Duplicate JSON object keys are rejected during parsing; canonical dataset normalization also rejects duplicate observation identities.
- Tests use injected fixture transports; no network request is required.

### Boundary / limitation

The adapter validates the response shape and minimum history, but this does not prove live instrument coverage, provider data quality, or the provider's adjustment convention. It also does not by itself close PCD-02, PCD-04, PCD-05, or PCD-06. Those decisions remain separate gates.

## PCD-11 — Provenance and reproducibility

### Implemented

- Each normalized observation preserves provider identity, requested symbol, provider function/field, adjustment-basis label, currency, and retrieval timestamp in metadata.
- `build_adm_monthly_data_assessment()` computes a SHA-256 `selected_input_digest` over the selected current/trailing observations in canonical JSON form.
- Raw provider payloads are not persisted, so the digest can detect differences but cannot reconstruct an earlier response.

### Finding: digest semantics include retrieval time

The digest payload includes `metadata` for every selected observation. The Alpha Vantage adapter puts `retrieved_at` into that metadata. Therefore, two invocations with identical selected dates/prices but different retrieval timestamps produce different `selected_input_digest` values.

This is not necessarily a defect: the current digest can be interpreted as a fingerprint of selected values **plus retrieval provenance**. However, it is not a stable fingerprint of selected market observations alone. The contract should choose and document one of these interpretations before PCD-11 is closed:

1. **Combined fingerprint:** Keep current behavior and explicitly define the digest as covering both selected observations and retrieval metadata.
2. **Observation fingerprint plus provenance:** Compute the observation digest only from identity/date/value/source/currency and expose retrieval provenance separately, optionally with a second provenance digest.

Neither option is implemented by this audit. Do not change digest semantics until the intended replay/reproducibility use case is decided, because downstream consumers may treat digest equality as identity.

### Limitation

No durable source payload or selected-observation snapshot is stored. Historical replay and exact reconstruction are therefore not supported, regardless of digest design.

## PCD-12 — Timeout, rate limits, retries, cache, and outage

### Implemented

- Three sequential HTTP requests are made per complete load.
- The default timeout is 15 seconds per request and is passed to the transport.
- Timeout configuration now rejects booleans, non-numeric values, non-finite numbers, and non-positive values.
- No retry, cache, fallback source, scheduling, or durable persistence is implemented.
- Any failed request/response rejects the complete load; transport exceptions are sanitized so a credential-bearing URL is not exposed.
- Live contract validation is a separate, explicitly invoked operation; fixture tests do not count as live-provider evidence.

### Operational consequence

The per-request timeout does not establish a strict end-to-end load deadline. Three sequential requests can consume approximately three timeout intervals, plus connection/processing overhead. No scheduling or repeated-use claim is authorized while quota, entitlement, and operational behavior remain open.

Do not add retries, caching, automatic scheduling, or a fallback provider under this audit. Reassess provider quota and entitlement first, then record an explicit operational decision and deterministic tests.

## Recommended next steps

1. Keep PCD-08 implementation as-is unless new deterministic fixtures reveal a concrete contract failure.
2. Resolve the PCD-11 digest interpretation before changing fingerprint behavior.
3. Keep PCD-12 limited to three sequential requests, finite positive timeout, fail-whole-load behavior, and no retry/cache/fallback/scheduling.
4. Continue to keep `config/moon.yaml` at `active_strategies: []`; no signal or Runtime integration is authorized by these provider-contract findings.
5. Do not treat this audit or passing fixture tests as live-provider evidence or a closure of the remaining provider/governance gates.

## Evidence inspected

- `src/data/alphavantage.py`
- `src/data/adapters.py`
- `src/data/contracts.py`
- `src/orion/frameworks/moon/adm_data.py`
- `src/orion/frameworks/moon/adm_workflow.py`
- `tests/data/test_alphavantage.py`
- `tests/orion/frameworks/moon/test_adm_provider_workflow_integration.py`
- `docs/01_Architecture/Moon_ADM_Provider_Contract_Decision_Register.md`
- `docs/01_Architecture/Orion_Data_Workflow_Pilot_Selection.md`
