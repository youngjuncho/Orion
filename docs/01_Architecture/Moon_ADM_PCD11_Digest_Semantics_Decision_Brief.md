# Moon ADM PCD-11 — Selected Input Digest Semantics Decision Brief

- Date: 2026-10-15
- Status: **Decision brief only; no policy decision approved**
- Baseline: `Orion_1013.zip`, commit `fea05ba`, plus changes accumulated in Sync Bundle v4
- Scope: documentation and contract analysis only; no source or test code changed

## 1. Verified current behavior

`assess_adm_monthly_dataset()` in `src/orion/frameworks/moon/adm_data.py` builds `digest_payload` from the selected current/trailing observations used by the monthly assessment. For each selected observation it includes:

- `symbol`
- `field`
- `observed_at`
- `value`
- `source`
- `currency`
- `metadata`

The payload is serialized as UTF-8 JSON with sorted object keys, compact separators, `ensure_ascii=False`, and `allow_nan=False`, then hashed with SHA-256. The selected observations are ordered by identity before serialization.

Consequences:

1. Changes to selected price values change the digest.
2. Changes to `source`, `currency`, or any `metadata` field can also change the digest.
3. Alpha Vantage's `retrieved_at` is included when it is stored in observation metadata, so a later retrieval of the same market observation can produce a different digest.
4. `ADMMonthlyDataAssessment` validates that the digest is a lowercase 64-character SHA-256 hex string.
5. The existing test verifies repeatability for identical fixtures and digest change when a selected value changes. It does not separately characterize metadata-only changes.
6. In the audited snapshot, the digest has no downstream persistence, governance approval, or runtime decision consumer. It is currently assessment provenance, not an authorization token.

## 2. The unresolved semantic question

The name `selected_input_digest` does not by itself say whether the digest identifies market-observation content or the entire selected input representation including provenance metadata. Both are legitimate but different contracts.

### Option A — Full selected-input/provenance digest

Keep the current field set. The digest changes if the selected values or their provenance metadata change.

- Benefit: identifies the exact normalized input representation used for the assessment.
- Cost: retrieval timestamps or provider metadata changes can make the digest differ even when market values are unchanged.
- Suitable when: the goal is auditability of the exact assessment input bundle.

### Option B — Observation-content digest

Hash only a documented stable subset of the observation fields, excluding volatile retrieval metadata.

- Benefit: stable across retrievals when the actual observation content is unchanged.
- Cost: no longer identifies the exact provenance-bearing input representation; changes in source or provider revision metadata may not be reflected unless deliberately included.
- Suitable when: the goal is content identity across repeated data retrievals.

### Option C — Separate content and provenance digests

Retain a content digest for stable observation identity and add a separate provenance/input-bundle digest for source, retrieval metadata, and other audit attributes.

- Benefit: separates market-content equality from provenance equality.
- Cost: adds a field, contract surface, tests, and migration/versioning questions. It is not justified until a real consumer needs both identities.

## 3. Recommendation for the current MVP

Do not change the digest algorithm yet. The audited snapshot has no downstream consumer that relies on digest equality, and the current behavior is deterministic for a fixed normalized input bundle. Avoid a speculative schema change.

If/when a consumer needs a stable content identity across retrievals, prefer introducing a separately named content digest rather than silently changing the meaning of `selected_input_digest`. Keep the existing digest as the provenance-bearing selected-input digest unless a formal PCD-11 decision explicitly supersedes that contract.

This recommendation is technical guidance, not an approved policy decision.

## 4. Required acceptance tests before a future contract change

When a decision is approved, add tests for the selected option:

- identical normalized input bundle -> same digest;
- selected value change -> content and full-input digests change as specified;
- `retrieved_at`-only change -> full-input digest changes; content digest remains stable if excluded by contract;
- source/currency/provider-revision change -> expected digest(s) change according to the documented field set;
- mapping insertion order does not change the digest;
- non-JSON values and non-finite numbers fail closed;
- schema/version migration behavior is explicit if digest semantics change.

Do not add a test that freezes one of the unresolved options before the decision is made.

## 5. Non-goals and safety boundaries

- No changes to ADM investment or allocation logic.
- No changes to signal-assembly authorization or strategy activation.
- No live Alpha Vantage API calls.
- `config/moon.yaml` must retain `active_strategies: []`.
- Moon/ADM authoritative governance binding remains incomplete and fail-closed.
