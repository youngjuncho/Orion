# Moon ADM Provider Contract Decision Register

Version: 1.0
Status: Open — decision inventory; D-055 approves comparison methodology; no provider approved
Last Updated: 2026-10-10

## Purpose

This register consolidates decisions that must be resolved before a concrete market-data provider adapter can be implemented or connected to Moon ADM. It is a decision-tracking artifact, not itself an approval record. Listing a candidate or an acceptance test does not authorize that candidate or close a policy gate.

The provider-neutral adapter and fixture-based acceptance tests are implemented. D-055 approves the SGOV/strict-greater-than methodology. D-056 approves limited provider-independent engineering defaults for endpoint selection and fail-closed handling; it does not close provider-specific gates. The live provider boundary remains closed. Core Runtime remains frozen, and Moon's `active_strategies` remains unchanged (`[]`).

## D-056 engineering defaults

For explicit evaluation and trailing targets, the engineering selector may use
the latest eligible observation on or before each target and must never use a
future observation. VTI, VEU, and the SGOV comparison input use the same field,
targets, and selection rule. Missing, invalid, caller-defined stale, or
conflicting required observations fail closed without fills, interpolation,
or partial success. The calculation boundary retains selected-observation
identity and source metadata where supplied.

These defaults do not choose target dates, a calendar or timezone, numeric
freshness limits, provider conflict or revision precedence, a source, or
adjusted-price semantics. No provider, live collection, signal assembly, or
ADM activation is approved. See D-056 in the Decision Log.

## Provider candidate evidence (not an approval)

Official provider materials reviewed on 2026-10-10 support this limited
engineering assessment:

| Candidate | Relevant documented behavior | Assessment for ADM | Status |
|---|---|---|---|
| Alpha Vantage | Its Daily Adjusted endpoint documents adjusted close and historical split/dividend events. Its support page says adjusted OHLCV accounts for splits and cash dividends. | Best documented first candidate for a fixture-based semantics and coverage review against D-028. This does not establish point-in-time behavior, VTI/VEU/SGOV coverage, or permission for this project's use. | Candidate only; PCD-01/02/04 remain open |
| Massive | Its aggregate bars are split-adjusted by default; its FAQ states they are not dividend-adjusted. | Does not meet D-028's adjusted-price total-return proxy requirement as-is. Could only be reconsidered with a separately validated dividend adjustment calculation. | Not suitable as-is |
| Yahoo Finance | No reviewed official evidence in this assessment establishes a supported API contract, adjustment methodology, or permitted use for this project. | Existing research-list mention is not sufficient evidence for production selection. | Unassessed; not approved |

Alpha Vantage's Terms of Service describe the default license as personal,
non-commercial use and define investment analysis/research among activities
that may constitute commercial use. Its market-data policy separately
describes entitlements and onboarding. The project's intended use and the
applicable plan or written permission must therefore be confirmed before
selection; this register makes no legal conclusion. Do not add credentials,
network access, or a provider adapter as a consequence of this candidate
assessment.

Sources: [Alpha Vantage Daily Adjusted API documentation](https://www.alphavantage.co/documentation/), [Alpha Vantage adjustment-method support](https://www.alphavantage.co/support/), [Alpha Vantage Terms of Service](https://www.alphavantage.co/terms_of_service/), [Alpha Vantage Market Data Policies](https://www.alphavantage.co/realtime_data_policy/), and [Massive stock-data FAQ](https://massive.com/knowledge-base/categories/faq).

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

1. Close PCD-01 through PCD-07 before provider-specific observations can be qualified.
2. Close PCD-08 through PCD-12 to define data quality, revision, provenance, and operations.
3. PCD-13 and PCD-14 are approved by D-055; do not reopen them to unblock provider work.
4. Close PCD-15 and PCD-16 before end-to-end signal integration or activation review.

D-056 supplies engineering defaults only; it does not close PCD-01 through
PCD-12. A numeric freshness limit and provider-specific response/revision
semantics still require evidence and explicit resolution.

This order does not require all decisions to be made in one session and does not imply that any particular provider is preferred.

## Explicit non-goals

This register does not select a provider or approve a provider's adjusted-price series, select the configured defensive holding, set a freshness threshold, add live API access, retries, caching, fallback sources, persistence, or scheduling, assemble an ADM signal, activate ADM, or modify Core Runtime. D-055 already approves SGOV as comparison benchmark and strict greater-than operator. The candidate evidence above is not provider approval.

## Related documents

- `Moon_ADM_Provider_Adapter_Readiness_Review.md`
- `Moon_ADM_Provider_Adapter_Acceptance_Test_Matrix.md`
- `Moon_ADM_Provider_Decision_Evidence_and_Closure_Workflow.md`
- `Moon_ADM_Provider_Contract_Readiness_Audit.md`
- `Moon_ADM_Provider_Neutral_Adapter_Contract.md`
- `Moon_ADM_Data_Contract.md`
- `Orion_Data_Pipeline.md`
- `docs/05_Decisions/Decision_Log.md`
