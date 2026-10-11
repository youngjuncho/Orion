# Orion Step 50 Final Integration Audit

**Status:** Storage and validation components reviewed; production consumer integration remains unauthorized  
**Audit date:** 2026-10-11  
**Audited baseline:** `Orion_Step50_FaultInjectionInvariants.zip`

## 1. Executive summary

Step 50 now has separate components for authoritative snapshot validation, Supernova-specific schema validation, durable per-scope high-water marks (HWM), an acceptance journal, consumer retry handling, and SQLite lease-based claims. The current test suite passes, but these components are not connected to a production Runtime or Framework consumer.

**Decision:** retain the current fail-closed integration boundary. Do not activate Moon ADM or connect the contract directly to `SupernovaEngine` in this step. The audit does not authorize trades, strategy activation, or a change to Core Runtime lifecycle.

## 2. Trust-boundary trace

1. `src/data/governance.py::validate_authoritative_registry_snapshot` checks required metadata, positive integer version, trusted authority membership, required signature/key metadata, a callable verifier that must return exactly `True`, scope constraints, timestamp freshness/future skew, canonical content digest, and optional generic decision-record lineage. Verifier exceptions fail closed.
2. `src/orion/frameworks/supernova/registry_contract.py::validate_trusted_approved_company_snapshot` composes the generic trust checks with the Supernova approved-company schema and its own lineage rules.
3. `src/data/registry_high_water_store.py::SQLiteHighWaterMarkStore.accept_snapshot` atomically advances the HWM and writes a pending acceptance event in one SQLite transaction. It explicitly does not validate authenticity or freshness; its caller must invoke the validator first.
4. `claim_pending_acceptances` uses a SQLite write transaction to issue temporary leases and prevents a later pending version in the same authority/registry/scope from bypassing an earlier pending event. `acknowledge_claim` requires the current, unexpired lease token.
5. `src/data/registry_acceptance_consumer.py::drain_leased_acceptances` invokes a caller-provided downstream callback and acknowledges only afterward. A crash between the side effect and acknowledgement can redeliver the event, so downstream effects must be idempotent.

## 3. Implemented guarantees and limits

| Area | Current guarantee | Remaining limitation |
|---|---|---|
| Content integrity | Canonical SHA-256 digest is checked separately from issuer signature verification | A digest is not authentication; the signature verifier and key lifecycle are externally supplied |
| Issuer trust | Authority must be in caller-supplied trusted allowlist; missing verifier/metadata and verifier exceptions fail closed | No built-in key distribution, rotation, remote revocation, or trusted-authority configuration lifecycle |
| Freshness | Timezone-aware generation time, maximum age, and future skew are checked | Freshness does not prove latestness or immediate revocation status |
| Anti-rollback | Integer version monotonicity plus SQLite compare-and-swap per authority/registry/scope | Durable guarantees depend on protecting, backing up, and restoring the database without rolling it back |
| Acceptance journal | HWM update and journal insert commit or roll back together | Public `advance()` can update HWM without an event; production callers must use the intended acceptance path consistently |
| Lease ownership | Atomic claim, expiration/reclaim, and token-checked acknowledgement | A lease cannot make an external side effect transactional; clocks and local SQLite are not distributed consensus |
| Consumer recovery | Pending events can be retried; per-scope version order is preserved by lease claims | The downstream callback must be idempotent and should deduplicate by stable event ID or equivalent business key |
| Framework integration | Contract functions and persistence primitives have test coverage | No production Runtime, Moon, or Supernova consumer call site is connected |

## 4. Important operational invariant

For a production registry consumer, the intended order is:

1. Load the candidate snapshot and retrieve the current durable HWM for the exact authority, registry type, and scope.
2. Validate authority, signature, content digest, scope, freshness, schema, and version against that HWM.
3. Call `accept_snapshot` with the previously observed version as `expected_current_version`; on CAS conflict, reload and revalidate rather than retrying the same stale validation result blindly.
4. Materialize the pending event to downstream state idempotently, using the event identity as a deduplication key where possible.
5. Acknowledge only with the current valid lease. If acknowledgement fails after the side effect, retry safely.

The repository does not yet enforce this sequence through one public facade. The ordering is a caller contract, not an end-to-end invariant guaranteed merely by the presence of these independent functions.

## 5. Integration dispositions

### Moon ADM

Keep `config/moon.yaml` `active_strategies: []` and preserve the authoritative-governance binding blocker. Registry validation does not resolve separate provider, data semantics, provenance, freshness, or activation gates. Do not enable ADM.

### Supernova

The approved-company snapshot schema is a contract proposal/validation layer, not the engine's live source of truth. `SupernovaEngine.build_report()` remains scaffolding and does not load signed registry records. Do not wire the snapshot contract into the engine until payload ownership, issuer/key policy, version persistence, revocation/freshness policy, and consumer materialization semantics are approved.

### Core Runtime

No Core Runtime lifecycle or execution behavior is changed. Existing Runtime and framework registry classes are not substitutes for an authoritative decision registry.

## 6. Verification performed for this audit

- `python scripts/check_utf8.py`: passed, 465 text files checked (UTF-8 without BOM).
- `pytest -q`: 383 passed, including guarded facade tests and three architectural boundary guards.
- `python -m compileall -q src tests scripts`: passed.
- The final ZIP archive was checked with `unzip -t` after packaging.

## 7. Exit criteria before production wiring

- Approve one concrete registry domain and its payload/scope contract.
- Specify trusted authority/key configuration, signature canonicalization, key rotation, revocation, and freshness policy.
- Route all accepted snapshots through a single orchestration facade that performs validation and then the HWM CAS + journal transaction; prohibit alternate HWM-only acceptance paths in production.
- Specify and test downstream idempotency and durable state materialization semantics.
- Define database backup/restore and HWM rollback detection procedures.
- Add consumer-level integration tests and obtain explicit approval before any Runtime/Framework wiring or activation change.

**Final decision:** Step 50 storage and validation primitives are suitable for further isolated testing, but end-to-end production trust is not yet established. No production integration or strategy activation is approved by this audit.

## 8. Guarded acceptance facade follow-up

`src/data/registry_acceptance_service.py` provides an isolated orchestration facade. It checks that the candidate authority, registry type, and exact scope match the requested HWM identity; reads the current HWM; injects that value into the configured validator; checks that validation did not rewrite signed identity fields; and only then calls the atomic HWM-plus-journal acceptance transaction. A compare-and-swap conflict is surfaced to the caller, which must reload and revalidate rather than retry stale validation.

The facade reduces accidental ordering mistakes but does not make unsafe alternate storage methods inaccessible, does not select trust policy or a cryptographic verifier, and is not wired into Runtime or Supernova. Production code must route acceptance through the facade and review any use of `advance()` or direct `accept_snapshot()` as a policy bypass. The validator callback is part of the trust boundary and must be configured with approved trust, freshness, and domain-schema policy.

The facade additionally deep-copies the incoming envelope before invoking the validator and recomputes the canonical snapshot digest on the validator result. This prevents an accidental or hostile callback mutation from changing the signed payload after the initial verification while preserving the caller's original object.

## 9. Bypass call-site review and architectural guards

A source-level call-site scan found `SQLiteHighWaterMarkStore.accept_snapshot()` called only by `RegistryAcceptanceService` in production `src/`; no production call site invokes `SQLiteHighWaterMarkStore.advance()` directly. Direct calls to both storage primitives remain technically possible to external callers, so this is a repository convention guarded by tests, not an access-control boundary. The new static tests fail if a production source file adds another `accept_snapshot()` call site or directly calls `advance()`. A separate configuration test pins `moon.active_strategies` to an empty list. These checks do not authorize Runtime/Supernova wiring and do not prove the validator configuration is production-approved.

## 10. Explicit production approval gates

`docs/01_Architecture/Orion_Step50_Production_Approval_Gates.md` now records ten unresolved approval gates covering registry authority/domain, payload and scope, signature/key lifecycle, freshness, HWM backup/restore, acceptance orchestration, consumer idempotency, leases/concurrency, domain integration, and operational ownership. Every gate is marked `OPEN — BLOCKING`; no project policy values or approvers were invented. Production wiring remains NO-GO until the gates are explicitly resolved and a separate integration target is approved.


## 11. Recovery and failure matrix follow-up

`docs/01_Architecture/Orion_Step50_Recovery_Failure_Matrix.md` records which process restart, atomic transaction, CAS, lease, and consumer retry cases have explicit test evidence. A new failure test requires an unreadable SQLite database to fail initialization without replacing it with fresh state. The matrix explicitly leaves rollback detection for an older but valid backup, deployment-specific durability, restore runbooks, and consumer fencing/idempotency policy unresolved. A valid stale backup cannot be detected using only the HWM stored inside that same restored database; any independent monotonic anchor requires a separately approved design.

## 12. Persistence necessity assessment

`docs/01_Architecture/Orion_Step50_Persistence_Necessity_Assessment.md` records that the Step 50 SQLite store and consumer helpers currently have no Runtime/Supernova/framework integration call sites outside their isolated data-layer modules (the acceptance service is re-exported from `src/data/__init__.py`). The document distinguishes reconstructible source payloads from non-reconstructible acceptance/delivery state, compares stateless, cache, and minimal durable-state designs, and recommends not expanding or operationalizing SQLite until a concrete requirement justifies it. This is an architecture assessment, not approval to remove code or integrate it.
