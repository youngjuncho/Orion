# Step 48 — Governance Revocation Integration Tests

## Purpose

Prove that registry integrity and revocation-impact analysis compose with the authorization-resolution path. These tests use local deterministic fixtures only; they do not represent real Provider or investment-policy approvals.

## Authorization entry point

Use `resolve_registry_approved_decisions(registry, required_ids, requested_scope)` when the caller claims to provide a complete registry snapshot. It first validates record schemas, content digests, and reciprocal supersession lineage, then resolves the requested decisions and their dependency closure using fail-closed approval rules.

The lower-level `resolve_approved_decisions(...)` remains available for focused resolution tests and compatibility, but it does not independently establish that all supersession links in the full snapshot are coherent.

## Integration invariants

1. A dependent record marked `Approved` cannot authorize use if any transitive dependency is invalidated or superseded.
2. A superseded predecessor remains in history but cannot satisfy a new authorization request.
3. A valid successor can be used when the dependent record explicitly references the successor and reciprocal lineage is coherent.
4. `invalidate_dependents(...)` returns an impact set without mutating records; authorization remains blocked only when the authoritative snapshot represents the relevant invalidation/supersession state.
5. Invalidating one dependency branch does not automatically block an unrelated branch.
6. A successor's `supersedes` claim without a reciprocal predecessor link is rejected by the registry-level entry point.

## Limits

These tests do not prove the caller's registry snapshot is authoritative, complete, fresh, signed, or authenticated. They do not implement automatic status mutation, remote registry access, runtime suspension, or strategy activation. Those remain separate controls and must not be inferred from passing fixture tests.

## Acceptance result

The integration test module is `tests/data/test_governance_integration.py`. The full repository test suite is the acceptance gate for this step.
