# Orion Authoritative Registry Consumer Integration Audit

**Status:** Consumer review complete; no production integration authorized  
**Date:** 2026-10-11  
**Baseline:** `Orion_Step50_RegistryConsumerAudit.zip`

## 1. Executive decision

The repository contains two governance-adjacent candidates for the authoritative registry snapshot contract, but neither is ready for direct production wiring. Moon has an explicit unresolved authoritative-governance binding gate. Supernova has an approved governance baseline in the Decision Log, but its current runtime report is hard-coded scaffolding and is not loaded from the configured candidate-universe source or an authoritative registry.

**Decision:** do not connect either consumer in this audit. The next implementation must first define the registry payload and caller contract for one specific use case. No Core Runtime, Framework execution, investment policy, or activation behavior is changed.

## 2. Moon ADM

### Evidence

- `config/moon.yaml` keeps `active_strategies: []`.
- `src/orion/frameworks/moon/adm_data.py` explicitly retains `authoritative_governance_binding_not_implemented` as a blocking reason when caller-provided approval claims are supplied.
- `tests/orion/frameworks/moon/test_adm_data.py::test_comparison_signal_guard_blocks_unverified_caller_attestation` verifies that a non-empty approval reference and locally cleared readiness flags do not make the signal eligible.
- `docs/01_Architecture/Moon_ADM_Provider_Contract_Readiness_Audit.md` keeps live provider integration, signal assembly, and activation gated. The provider/data/operational gates are separate from the governance-record binding gap.
- The authoritative snapshot contract currently has only test call sites, not a production Framework/Runtime call site.

### Conclusion

Moon is the clearest future consumer because the code already identifies the missing authoritative governance binding. However, a snapshot validator alone cannot close provider, data semantics, calendar, freshness, provenance, or activation gates. There is no defined Moon-specific registry payload/scope contract or durable atomic high-water store in the current implementation.

**Disposition:** preserve the existing fail-closed blocker; do not connect the snapshot validator to the signal guard until the decision-record schema, expected scope, trusted issuer/key policy, freshness policy, and durable per-scope version state are specified and tested. Do not activate ADM.

## 3. Supernova

### Evidence

- `docs/05_Decisions/Decision_Log.md`, D-049, records approval of the five-company baseline: NVDA, GOOGL, ISRG, PLTR, and CEG. The decision is a governance baseline, not an automatic trade instruction.
- `docs/03_Research/Supernova/Supernova_Universe_Governance.md` requires research review, documentation updates, and a Decision Log entry before universe changes.
- `docs/03_Research/Supernova/Supernova_Candidate_Universe.md` is marked Draft and defines a broader research universe; it is not itself an authoritative approved-company registry.
- `config/supernova.yaml` names `Supernova_Candidate_Universe.md` as the source and separately lists five `approved_companies`.
- `src/orion/core/config_loader.py` parses those values as configuration. It does not resolve them against a signed/versioned authoritative registry.
- `src/orion/frameworks/supernova/engine.py::build_report()` hard-codes five `ApprovedCompany` placeholders with score zero and `Unknown` fields. It does not consume the config or candidate-universe document.
- `docs/reports/Implementation_Status_Report.md` classifies Supernova as partial scaffolding and says the placeholder output is not an authoritative registry.

### Conclusion

Supernova has a human-approved baseline record, but there is no implemented authoritative registry consumer to protect yet. Wiring the snapshot validator into the current engine would be premature: the engine does not load configuration, parse the research universe, or consume registry records, and its placeholder output is not a source-of-truth representation.

**Disposition:** do not connect the validator to `SupernovaEngine` as part of Step 50 follow-up. First define whether the registry should represent the approved-company portfolio state, the candidate universe, or both as separate scoped payloads; then define how D-049 and subsequent review decisions map to versioned records. Do not infer approval for every company in the Draft candidate universe.

## 4. Non-consumers

- `src/orion/core/framework_registry.py` and `src/orion/services/registry.py` are in-memory registries of framework/service objects, not decision-record registries.
- Core Runtime decision/state lifecycle has no current snapshot-validator call site and remains frozen.

Neither is a justified integration target.

## 5. Recommended next work unit

Proceed with a design-only contract for a single registry domain before implementation:

1. Choose the first domain: Moon policy/decision records or Supernova approved-company governance state.
2. Specify record schema, owner/authority, scope keys, signed payload canonicalization, and key trust policy.
3. Specify freshness limits and the trusted durable/atomic high-water storage boundary.
4. Define what a successful validation may and may not authorize. For Moon it must not clear unrelated data/activation gates; for Supernova it must not turn a research candidate into an approved company.
5. Add consumer-level negative tests, including unknown authority, invalid signature, stale snapshot, replay/rollback, missing durable version state, and unrelated/unapproved records.
6. Integrate only after the owner and policy inputs are explicit; keep the Runtime frozen and Moon ADM inactive.

## 6. Scope and verification

This audit changes documentation only. It does not add provider access, network services, cryptographic key infrastructure, persistent storage, new investment rules, or runtime wiring. The audit is not an approval to activate a Framework or trade.
