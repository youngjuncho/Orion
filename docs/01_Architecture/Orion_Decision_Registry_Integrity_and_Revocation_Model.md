# Step 47 — Decision Registry Integrity & Revocation Model

## Purpose

Define local, deterministic rules for decision-record lineage, invalidation impact, and audit-history preservation. This is not an identity provider, trusted authority, remote registry, or strategy-activation mechanism.

## Rules

1. Decision records are immutable snapshots. A changed decision is represented by a new record; do not edit the historical record in place.
2. `superseded_by` must reference a record present in the same registry snapshot, and the successor must identify the predecessor through `supersedes`.
3. Self-supersession, missing successors, non-reciprocal links, and supersession cycles fail closed.
4. Historical records remain in the registry for audit purposes. A superseded or invalidated record cannot authorize new use.
5. Invalidating a decision requires review of every direct and transitive dependent. `invalidate_dependents()` reports the impact set deterministically but does not mutate records or automatically approve/revoke them.
6. Existing authorization resolution continues to require all dependencies to be valid, approved, and in the requested scope. A dependency that is invalidated or superseded cannot satisfy that requirement.
7. A digest detects content/digest mismatch only. It does not prove identity, authority, timestamp authenticity, or that a registry snapshot is complete and current.

## Implemented surface

- `validate_registry_lineage(registry)`: validates each record and checks reciprocal supersession links and cycles.
- `invalidate_dependents(registry, invalidated_ids)`: returns sorted transitive dependents that require review.
- Existing `resolve_approved_decisions(...)`: remains fail-closed for invalidated/superseded records, missing dependencies, non-approved dependencies, scope mismatch, and dependency cycles.
- `resolve_registry_approved_decisions(...)`: validates the supplied snapshot's full supersession lineage before resolving required approvals and dependencies. Use this entry point when the caller asserts the snapshot is complete.

The lineage validator checks both directions: a predecessor's `superseded_by` must match the successor's `supersedes`, and a successor's `supersedes` must point to a predecessor that reciprocally names it. The wrapper is stricter than the lower-level resolver because it requires a coherent complete snapshot.

## Non-goals and constraints

- No remote registry, signature infrastructure, authentication, network access, persistence, or automatic mutation.
- No automatic cascade changes to status. Impacted decisions are surfaced for explicit review.
- No provider selection, price-field semantics, freshness threshold, or Moon activation. D-055 separately approves the SGOV comparison benchmark and strict greater-than operator.
- Core Runtime remains frozen; `active_strategies: []` remains unchanged.

## Acceptance tests

Tests cover reciprocal lineage, missing/non-reciprocal links in both directions, supersession cycles, deterministic transitive invalidation impact without mutation, invalidated/superseded ancestors blocking descendant resolution, valid replacement chains, and unaffected independent branches. The full suite is the acceptance gate for the snapshot.
