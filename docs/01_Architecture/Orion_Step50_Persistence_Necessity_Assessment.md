# Orion Step 50 — Persistence Necessity Assessment

**Status:** Architecture assessment; no production integration approved  
**Decision:** Do not expand or operationalize local SQLite persistence until a concrete requirement demonstrates that it is necessary.

## 1. Question

Step 50 currently contains a file-backed SQLite high-water-mark (HWM) store, an acceptance journal, and lease-based consumer helpers. The source data is expected to be retrievable from an external authority. The relevant question is not whether SQLite works, but which state cannot safely be reconstructed from authoritative sources and therefore needs durable local storage.

## 2. Repository evidence

A source-level inspection of `src/` found:

- `SQLiteHighWaterMarkStore` is defined in `src/data/registry_high_water_store.py`.
- `RegistryAcceptanceService` uses the store to validate against the current HWM and atomically record acceptance.
- The consumer helpers read and acknowledge the acceptance journal.
- No Runtime, Supernova, or other framework source module imports or calls these helpers; no production integration call site was found. `src/data/__init__.py` re-exports the acceptance service, and the store/consumer are referenced by the isolated data-layer modules.
- Tests exercise these primitives, but tests do not establish that production needs them.

Therefore, this is currently an isolated implementation and proposal, not a demonstrated production dependency.

## 3. Data retrievability versus state retrievability

| Item | Usually reconstructible from authoritative source? | Persistence decision |
|---|---|---|
| Current registry payload | Yes, if the authority remains reachable and retains the version | Do not persist solely for correctness; optional cache may be justified by latency/availability |
| Signature and issuer metadata | Often, if returned with the authoritative artifact and the relevant trust policy is independently available | Do not assume local copies are needed; separately define trust/key policy |
| Last accepted version / anti-replay state | Not necessarily. A current payload does not prove which version this consumer previously accepted | Persist only if monotonic acceptance or replay rejection is a real requirement |
| Pending acceptance journal | Only if downstream work cannot be safely rebuilt by re-fetching and reprocessing | Persist only if durable asynchronous delivery is required |
| Consumer completion/deduplication state | Not necessarily, especially when external side effects have already occurred | Persist or delegate to the downstream system if exactly-once-like effects are required; idempotency is still necessary |
| Lease/worker ownership | Ephemeral coordination state | Needed only if concurrent asynchronous workers and recoverable claims are actually required |

## 4. Three viable architecture choices

### A. Stateless fetch-and-validate

Fetch the current authoritative artifact when needed, validate it under an approved trust policy, and use it without retaining acceptance history. Re-fetch and re-validate after failures.

Choose this if historical acceptance, monotonic anti-replay state, and durable asynchronous materialization are not requirements. This is the simplest baseline and should be preferred until a concrete requirement rules it out.

### B. Rebuildable local cache

Keep a local copy for performance or temporary source unavailability, but treat it as disposable. The system must be able to delete and rebuild the cache from the authority, and cache state must not be mistaken for an independent anti-rollback anchor.

Choose this only when measured latency, availability, rate limits, or offline requirements justify it.

### C. Minimal durable security/processing state

Persist only the state that cannot safely be reconstructed: for example, an accepted-version anchor if rollback/replay rejection is required, or a pending-event ledger if downstream effects must be retried durably. Keep raw registry payloads re-fetchable where possible. If anti-rollback must survive restoration of the local database from an older valid backup, the anchor must be protected independently; a HWM stored only inside that database cannot detect its own rollback.

Choose this only after the requirements and ownership of that independent anchor or delivery ledger are approved.

## 5. Costs and risks of the current SQLite design

The current design adds a file path and permissions, SQLite locking/WAL behavior, schema migrations, backup/restore responsibility, corruption handling, operational monitoring, and a rollback-detection gap for a valid stale backup. The journal and leases also add at-least-once delivery and downstream idempotency obligations. Those costs are justified only by requirements that need durable local state.

## 6. Decision and immediate guardrails

1. Do not wire the SQLite store into Core Runtime, Moon, or Supernova as part of this assessment.
2. Do not expand backup/restore machinery until the team decides whether durable anti-replay state is required.
3. Keep the implementation isolated as a tested experiment/contract for now; this assessment does not silently delete it or claim it is production-ready.
4. Before any integration, answer these questions explicitly:
   - Must Orion reject a version it has accepted in an earlier process/session?
   - Must a prior acceptance survive process restart or host replacement?
   - Must a pending downstream side effect be delivered even if Orion restarts?
   - Can downstream effects be idempotent, or does the downstream system provide durable deduplication?
   - Is the authoritative source available on every use, and does it retain the required historical/version metadata?
   - What threat model requires rollback detection, and where can an independent monotonic anchor live?
5. If all answers indicate no historical or durable processing state is required, prefer option A and remove the production need for local SQLite persistence. If only caching is needed, prefer option B. Use option C only for requirements that cannot be met by A or B.

## 7. Conclusion

The repository currently does not demonstrate a production need for local SQLite persistence because no production integration call site uses the Step 50 store or consumer. The correct next step is a requirements decision, not further hardening by default. The current implementation remains isolated, and no Runtime lifecycle, investment logic, provider policy, or Moon strategy activation is changed.

## 8. Isolation guard

Added `tests/data/test_registry_persistence_isolation.py` to fail if Runtime/framework source imports the experimental HWM store, acceptance facade, or acceptance consumer. This is a guard against accidental integration, not proof that persistence will never be needed. A future integration requires an explicit requirements decision and review of the production approval gates. No production code, Runtime lifecycle, provider policy, or Moon configuration was changed by this guard.

## 9. Current recommendation

Given the absence of a demonstrated production consumer, treat stateless fetch-and-validate as the default design candidate. Do not remove the isolated implementation solely on this evidence; retain it as an experiment until the required semantics are explicitly decided. If Orion does not need cross-session anti-replay, durable asynchronous delivery, or historical acceptance, retire the HWM/journal/lease subsystem rather than operationalizing it. If any of those requirements are confirmed, persist only the irreconstructible state and define where its rollback-resistant anchor or idempotency record lives.

## 10. Requirements cross-check against the current Runtime MVP

The current Runtime reconciliation addendum explicitly describes StateStore/EventStore as execution-scoped in-memory stores and durable State/Event persistence as a later workstream outside the MVP boundary. The Event Model states that Event Sourcing is not adopted. Combined with the absence of a production call site for the Step 50 store or consumer, the repository does not currently demonstrate a product requirement for operationalizing SQLite HWM, journal, or lease state.

A separate decision memo, `Orion_Step50_Requirements_Decision.md`, records the current recommendation: use stateless fetch-and-validate as the MVP default candidate, do not operationalize the isolated persistence prototype, and revisit only when a concrete cross-session anti-replay, durable delivery, downstream deduplication, cache, or Runtime persistence requirement is approved. This is not a claim that stateless operation provides cross-session anti-rollback protection.

## 11. Current stateless data-path audit

`Orion_Step50_Stateless_Data_Path_Audit.md` traces the implemented canonical market-data path and its current CLI wiring. The provider path is injectable and fetches only when explicitly invoked; the CLI does not currently auto-wire the Alpha Vantage provider, and the `data update/status` commands remain placeholders. This further supports keeping the Step 50 registry persistence prototype isolated rather than adding it to the current market-data path. The audit also records that current normalization is structural and does not itself close freshness or cross-session anti-replay policy.
