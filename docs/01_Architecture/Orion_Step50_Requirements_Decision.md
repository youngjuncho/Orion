# Orion Step 50 — Persistence Requirements Decision

**Status:** Design recommendation; requires explicit owner approval before implementation changes  
**Scope:** Isolated Step 50 registry acceptance prototype only  
**Production integration:** Not approved

## 1. Decision question

Does Orion's current product architecture require the Step 50 SQLite high-water-mark store, acceptance journal, and lease-based consumer machinery?

## 2. Evidence from the current Orion architecture

The repository's current Runtime reconciliation addendum states that `RuntimeSession` owns execution-scoped in-memory StateStore and EventStore instances, and that durable State/Event persistence remains a later workstream outside the MVP boundary. The Event Model also states that Event Sourcing is not adopted and the current implementation does not add durable persistence.

The Step 50 persistence assessment found no Runtime, Supernova, or other framework production call site using the SQLite store or acceptance consumer. The implementation remains isolated and its tests prove component behavior, not a product requirement.

These facts support a narrow conclusion: **the current Orion MVP does not establish a need to operationalize this local SQLite subsystem.** They do not establish that Orion can never need durable state in a future release.

## 3. Requirements decision matrix

| Candidate requirement | Current evidence | Recommendation for current MVP |
|---|---|---|
| Cross-session anti-replay / monotonic registry acceptance | No production consumer or explicit product requirement identified | Not required by demonstrated MVP scope; do not add HWM persistence to Runtime |
| Durable asynchronous delivery of accepted snapshots | No production acceptance-journal consumer identified; current Runtime event store is in-memory | Not required by demonstrated MVP scope; do not operationalize journal/leases |
| Durable deduplication of external side effects | No Step 50 downstream production side effect identified | Do not build local deduplication state without a concrete side-effect contract; prefer downstream idempotency where relevant |
| Faster or offline registry reads | No measured latency, rate-limit, or offline requirement supplied | No cache by default; introduce a rebuildable cache only when measured evidence justifies it |
| Runtime StateStore/EventStore durability | Explicitly a later workstream, outside current MVP | Track separately; do not conflate it with registry anti-rollback storage |

## 4. Recommended architecture choice

Use **stateless fetch-and-validate** as the default candidate for the current MVP:

1. Fetch the authoritative registry snapshot when needed.
2. Validate the snapshot against an explicitly approved trust policy.
3. Consume the validated result within the current execution.
4. On transient failure, retry by fetching and validating again, subject to source limits and freshness requirements.
5. Do not claim historical anti-replay protection across sessions unless an independently retained acceptance anchor is later approved.

A rebuildable cache may be added only for a demonstrated latency, availability, rate-limit, or offline requirement. Durable HWM, journal, and lease machinery should be retained only if a future accepted requirement cannot be satisfied by re-fetching, recomputation, or downstream idempotency.

## 5. Security boundary and caveat

Fetching the latest source again does not by itself prove that a previously accepted version cannot be replayed. Stateless fetch-and-validate is appropriate only if cross-session anti-replay is not a required guarantee, or if the authority itself provides a trusted freshness/version guarantee sufficient for the threat model. If monotonic acceptance is mandatory, some independently protected state or trusted remote mechanism is necessary; a HWM stored only in a locally restorable database cannot detect restoration of that same database to an older valid backup.

Signature validation also remains distinct from content hashing: a digest detects content changes but does not establish issuer authority. The trust policy and verifier configuration must be approved independently of the persistence choice.

## 6. Disposition of the existing prototype

The general `data` package no longer re-exports `RegistryAcceptanceService`. This prevents a normal `import data` from eagerly importing the experimental SQLite-backed acceptance layer. The implementation remains available only through its explicit module path for isolated tests and research. An isolation test verifies that importing the general package does not load the HWM store, acceptance service, or consumer modules.


Do not delete the isolated Step 50 implementation as part of this assessment, and do not integrate it into Runtime, Moon, or Supernova. Keep it clearly marked as an experimental prototype until the project owner explicitly decides whether to:

- retire the subsystem from the active product tree;
- retain it in an experimental branch/package; or
- approve a specific durable-state requirement and its operational owner.

The present recommendation is **do not operationalize; prefer stateless validation for the current MVP**. Removal of prototype files is a separate, reversible repository-maintenance decision and is not performed by this document.

## 7. Revisit triggers

Reopen the decision only when at least one concrete requirement is documented:

- the system must reject a previously accepted registry version across process/session restarts;
- accepted work must survive restart and be delivered asynchronously;
- downstream effects cannot be safely recomputed or made idempotent and require durable deduplication;
- measured latency, source rate limits, availability, or offline use justify a rebuildable cache;
- durable Runtime StateStore/EventStore behavior is approved as a separate product workstream.

Any revisit must define the failure model, trust boundary, retention policy, recovery owner, and tests before implementation.

## 8. Non-goals and invariants

This decision does not change Core Runtime lifecycle semantics, StateStore/EventStore implementation, provider selection, investment logic, order execution, Moon configuration (`active_strategies: []`), or Runtime/Supernova production integration.
