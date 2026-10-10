# Orion Authoritative Registry Snapshot Contract

**Status:** Implemented local contract validation; external authority and freshness guarantees remain unimplemented.

## Purpose

A structurally valid decision record is not sufficient to establish that its registry is the intended snapshot, current for the requested use, or issued by a trusted authority. This contract defines metadata and checks for a caller-supplied snapshot. It does not fetch, sign, authenticate, or discover a remote registry.

## Required snapshot fields

- `snapshot_id`: stable non-empty identifier for this snapshot.
- `snapshot_version`: non-empty version label.
- `generated_at`: ISO-8601 timestamp with an explicit UTC offset.
- `scope`: non-empty mapping; every requested scope key must match exactly.
- `authority_ref`: non-empty reference to the claimed issuing authority. It is descriptive, not authenticated.
- `records`: non-empty mapping of decision ID to decision record.
- `content_digest`: SHA-256 digest of canonical JSON for all snapshot fields except `content_digest`.

## Validation rules

1. Validate required metadata and types.
2. Require exact matching for every caller-specified scope key.
3. Require an aware `now` value and aware `generated_at` timestamp.
4. Reject snapshots older than caller-supplied `max_age_seconds` or farther in the future than `max_future_skew_seconds`.
5. Verify the snapshot digest.
6. Validate each decision record and all registry supersession links/cycles.
7. Fail closed on any failure; do not return a partially accepted snapshot.

Age limits and allowed future clock skew are caller-supplied engineering parameters, not approved Moon investment policy.

## Trust limitations

A SHA-256 digest detects accidental or unaccompanied content changes; it does not authenticate an issuer. A caller can modify a snapshot and recompute the digest. `authority_ref` is not a signature. A locally fresh snapshot is not necessarily the newest snapshot available. Authenticity, monotonic version guarantees, anti-rollback, completeness, and remote revocation delivery require a separate trusted registry/signature mechanism and are not implemented here.

## Explicit non-goals

- No remote API, database, signature key, certificate, or identity provider.
- No provider selection or financial semantics approval.
- No approval of unresolved Moon ADM benchmark/comparison/freshness investment policies.
- No Runtime integration or strategy activation.
- Core Runtime remains frozen and Moon `active_strategies` remains empty.

## Tests

`tests/data/test_governance.py` covers a fresh valid snapshot, missing metadata, digest tampering, scope mismatch, staleness, missing timezone, and excessive future timestamps. The broader suite verifies that decision record and supersession lineage validation remain in force.
