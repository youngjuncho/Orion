# Moon ADM Provider Contract Decision Register

Version: 1.0
Status: Open — decision inventory; D-055 approves comparison methodology; no provider approved
Last Updated: 2026-10-10

## Purpose

This register consolidates decisions that must be resolved before a concrete market-data provider adapter can be implemented or connected to Moon ADM. It is a decision-tracking artifact, not itself an approval record. Listing a candidate or an acceptance test does not authorize that candidate or close a policy gate.

The provider-neutral adapter and fixture-based acceptance tests are implemented. D-055 approves the SGOV/strict-greater-than methodology. The live provider boundary remains closed. Core Runtime remains frozen, and Moon's `active_strategies` remains unchanged (`[]`).

## Decision register

| ID | Decision area | Current status | Required decision / evidence | Consequence while open |
|---|---|---|---|---|
| PCD-01 | Provider selection and permitted use | Open | Name the provider and access method; record intended use, licensing/usage constraints, and explicit approval | No provider-specific adapter or live access |
| PCD-02 | Instrument identity | Open | Verify stable provider identifiers for VTI and VEU; identify the D-055-approved SGOV comparison benchmark | No inferred aliases or ticker-only identity assumptions |
| PCD-03 | Canonical symbol/field mapping | Partially defined at generic boundary | Record a reviewed, deterministic mapping from provider fields and identifiers to canonical `symbol`, `field`, `observed_at`, `value`, `source`, `currency`, and metadata; specify unsupported-field behavior | No guessed mappings or silent field substitutions |
| PCD-04 | Adjusted-price semantics | Open | Document provider adjustment methodology, including distributions and splits; provide evidence that the selected series is suitable for D-028's total-return proxy | `adjusted_close` remains a candidate label, not proof of total-return semantics |
| PCD-05 | Timestamp and timezone | Open | Define timestamp format, timezone, date extraction, daily-bar timestamp meaning, and whether the record denotes session close | Preserve source labels; no implicit timezone conversion |
| PCD-06 | Trading calendar and evaluation endpoint | Partially defined | Confirm source/exchange calendar, valid session observations, last-trading-day evaluation convention, and exact trailing-12-month endpoint construction | Prior-observation-on-or-before remains an engineering selection rule only |
| PCD-07 | Freshness and publication delay | Open | Approve freshness threshold(s), age calculation, and handling of weekends, holidays, delayed publication, and stale-but-present observations | No production freshness policy inferred from example thresholds |
| PCD-08 | Missing and partial responses | Generic fail-closed behavior exists; provider semantics open | Define expected response completeness and behavior for missing symbols, fields, dates, or partial batches | No silent fill, interpolation, or success-shaped partial dataset |
| PCD-09 | Duplicate and conflicting observations | Generic duplicate identity rejected; conflict policy open | Define provider-specific handling for conflicting records, overlapping pages, and repeated retrievals | No arbitrary winner selection |
| PCD-10 | Revisions and corrections | Open | Decide whether calculation uses latest revised history or retrieval-time snapshots; define revision identity and correction precedence | No revision selection or durable snapshot behavior implemented |
| PCD-11 | Provenance and reproducibility | Contract design required | Specify provider/source ID, requested and returned instrument IDs, retrieval time, adapter version, field semantics, selected observation identities/dates, and revision/snapshot identifiers where available | Preserve supplied metadata; do not fabricate missing provenance |
| PCD-12 | Timeout, rate limits, retry, cache, outage | Open | Only after provider approval, define timeout, rate-limit, retry, cache, partial-failure, and outage semantics | No network/retry/cache/fallback behavior |
| PCD-13 | Absolute-momentum benchmark | SGOV approved by D-055 | Apply SGOV for the approved comparison; source measurement and configured defensive-holding relationship remain separate |
| PCD-14 | Comparison operator and equality | Approved by D-055 | Selected risk return must be strictly greater than SGOV; equality is false |
| PCD-15 | Governance approval binding | Open | Define how an implementation validates approval against an authoritative decision record; caller-supplied reference alone is only an attestation | No assumption that an arbitrary approval reference closes a gate |
| PCD-16 | End-to-end activation and failure boundary | Open; activation not authorized | Define acceptance evidence showing provider/data failure cannot yield a valid Moon signal and specify the separately approved activation process | No `ADMSignalInput` assembly, ADM activation, or Runtime/Core changes |

## Closure protocol

For each item, a future closure record should include:

1. Decision ID and explicit outcome (`Approved`, `Rejected`, or `Deferred`).
2. Decision owner/authority and decision date.
3. Rationale, evidence, source documentation, and any limitations.
4. Contract/schema or tests affected, with deterministic fixture coverage.
5. Dependencies on other decision IDs and whether downstream gates remain open.

A status change in this register is not sufficient evidence of approval by itself. The authoritative governance record must be updated and linked before implementation treats a decision as closed. D-055 closes PCD-13 and PCD-14; provider implementation and signal integration remain gated by the other open decisions.

## Implementation order (dependency guidance, not approval)

1. Close PCD-01 and PCD-02 before provider-specific identity/mapping work.
2. Close PCD-03 through PCD-07 to define interpretation of the returned observations.
3. Close PCD-08 through PCD-12 to define quality, revision, provenance, and operational behavior.
4. PCD-13 and PCD-14 are approved by D-055; keep provider data qualification as a separate gate.
5. Close PCD-15 and PCD-16 before any end-to-end signal integration or activation proposal.

This order does not require all decisions to be made in one session and does not imply that any particular provider is preferred.

## Explicit non-goals

This register does not select Yahoo Finance, another provider, SGOV, BIL, or SHY; approve a provider's adjusted-price series; set a freshness threshold; define a comparison operator; add live API access, retries, caching, fallback sources, persistence, or scheduling; activate ADM; or modify Core Runtime.

## Related documents

- `Moon_ADM_Provider_Adapter_Readiness_Review.md`
- `Moon_ADM_Provider_Adapter_Acceptance_Test_Matrix.md`
- `Moon_ADM_Provider_Decision_Evidence_and_Closure_Workflow.md`
- `Moon_ADM_Provider_Contract_Readiness_Audit.md`
- `Moon_ADM_Provider_Neutral_Adapter_Contract.md`
- `Moon_ADM_Data_Contract.md`
- `Orion_Data_Pipeline.md`
- `docs/05_Decisions/Decision_Log.md`
