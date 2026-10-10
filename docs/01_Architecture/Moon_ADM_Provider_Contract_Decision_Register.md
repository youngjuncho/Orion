# Moon ADM Provider Contract Decision Register

Version: 1.0
Status: Open — D-057 selects Alpha Vantage for a limited private-use adapter; signal activation remains gated
Last Updated: 2026-10-10

## Purpose

This register tracks source and governance decisions that must be resolved before provider data can enter ADM signal assembly or Moon activation. It is a decision-tracking artifact, not itself an approval record. Listing a candidate or acceptance test does not authorize a use beyond the scope recorded in the Decision Log.

The provider-neutral adapter and fixture-based acceptance tests are implemented. D-055 approves the SGOV/strict-greater-than methodology. D-056 approves provider-independent endpoint selection and fail-closed defaults. D-057 selects Alpha Vantage's monthly adjusted series for private individual research and an opt-in data adapter. Signal assembly and live ADM activation remain gated. Core Runtime remains frozen, and Moon's `active_strategies` remains unchanged (`[]`).

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
| Alpha Vantage | Its monthly adjusted endpoint documents last-trading-day monthly bars, adjusted close, and monthly dividend; its core time-series APIs cover stocks, ETFs, and mutual funds. Its support page documents split and cash-dividend adjustments. | Selected by D-057 for a private individual research adapter. General ETF support does not confirm VTI, VEU, and SGOV individually; exact live coverage and adjusted-history parity remain unverified. | Selected within D-057 scope |
| Massive | Its aggregate bars are split-adjusted by default; its FAQ states they are not dividend-adjusted. | Does not meet D-028's adjusted-price total-return proxy requirement as-is. Could only be reconsidered with a separately validated dividend adjustment calculation. | Not suitable as-is |
| Yahoo Finance | No reviewed official evidence in this assessment establishes a supported API contract, adjustment methodology, or permitted use for this project. | Existing research-list mention is not sufficient evidence for production selection. | Unassessed; not approved |

Alpha Vantage's Terms of Service grant personal, non-commercial use and define
private, individual investment analysis and research as within that scope;
organizational use and third-party access can require commercial approval.
D-057 selects the provider only for the user's private individual research.
The provider's current standard limit is 25 requests per day, and one complete
ADM data load uses three. Entitlements and quotas must be rechecked before
scheduled or broader use; this is not a legal determination.

Sources: [Alpha Vantage Monthly Adjusted API documentation](https://www.alphavantage.co/documentation/), [Alpha Vantage adjustment-method support](https://www.alphavantage.co/support/), [Alpha Vantage Terms of Service](https://www.alphavantage.co/terms_of_service/), [Alpha Vantage request limits](https://www.alphavantage.co/premium/), [Alpha Vantage Market Data Policies](https://www.alphavantage.co/realtime_data_policy/), and [Massive stock-data FAQ](https://massive.com/knowledge-base/categories/faq).

The official materials establish the general endpoint contract and adjustment
description, not successful responses for the three selected ETFs. No live
symbol requests were made for this review. PCD-02 therefore remains open until
each exact symbol returns matching metadata and at least 13 valid monthly
adjusted observations under the configured account.

### D-057 selection and integration

D-057 selects Alpha Vantage `TIME_SERIES_MONTHLY_ADJUSTED` for VTI, VEU, and
SGOV. The concrete adapter is `data.alphavantage` and reads
`ORION_ALPHA_VANTAGE_API_KEY` only when configured. It issues three sequential
requests per load, uses a 15-second request timeout, requires at least 13
monthly observations per instrument, retains retrieval and provider-field
provenance, and rejects the whole batch on any provider or validation error.
It consumes three of the documented 25 standard daily requests per load. It
does not retry, cache, persist, calculate an ADM signal, or activate Moon.

The provider terms permit private, individual investment analysis and research
within the personal-use grant. Organizational use or third-party access is not
covered by this decision; obtain written provider approval for those cases.
The documented monthly response is the last trading day of each month. D-058
approves the seven-day selected-observation age; target-date generation and
execution-date/timezone mapping remain engineering/operations items.

## Decision register

| ID | Decision area | Current status | Required decision / evidence | Consequence while open |
|---|---|---|---|---|
| PCD-01 | Provider selection and permitted use | Selected by D-057 for private individual use | Alpha Vantage monthly adjusted endpoint; no organization, redistribution, third-party display, or commercial service without written permission | Adapter available only when explicitly configured; broader-use collection is not authorized |
| PCD-02 | Instrument identity | General ETF support documented; exact live coverage open | Request VTI, VEU, SGOV and require exact response symbol identity plus at least 13 valid monthly observations for each | Fail whole batch on missing/mismatched identity; no live coverage claim until checked |
| PCD-03 | Canonical symbol/field mapping | Implemented | Provider `Monthly Adjusted Time Series` / `5. adjusted close` to canonical `adjusted_close`, date-only observation, USD, and explicit source metadata | No inferred aliases or silent field substitutions |
| PCD-04 | Adjusted-price semantics | Adjusted-close mapping selected by D-057; methodology details and empirical parity open | Use `5. adjusted close` only; do not add the separate monthly dividend field. Provider documents split and cash-dividend adjustments, but the reviewed public materials do not specify exact adjustment-factor/reinvestment convention or revision schedule | Treat as D-028 proxy only; do not claim provider-certified point-in-time total-return history; live signal remains gated |
| PCD-05 | Timestamp and timezone | Monthly date semantics documented; timezone detail open | Use provider's date-only monthly final-trading-day label; preserve it without timezone conversion | No fabricated intraday timestamp or timezone |
| PCD-06 | Trading calendar and evaluation endpoint | Monthly bar convention selected; D-058 target construction proposed | Use last completed month-end and corresponding prior-year month-end; define signal/execution date mapping before activation | D-056 prior-on-or-before remains; helper output is not signal authorization |
| PCD-07 | Selected-observation age | Seven calendar days approved by D-058 | Apply one maximum age to all selected VTI/VEU/SGOV current and trailing observations | Integrated monthly assessment fails closed above seven days |
| PCD-08 | Missing and partial responses | Generic fail-closed behavior implemented | Require all three symbols and at least 13 valid monthly observations each; reject provider notices, malformed values, or any incomplete symbol response | No silent fill, interpolation, or partial dataset |
| PCD-09 | Duplicate and conflicting observations | Duplicate rejection implemented; cross-run policy approved by D-059 | Reject duplicate JSON keys in one provider response and duplicate canonical identities; never merge observations across invocations | Entire malformed/conflicting batch fails; no arbitrary winner selection |
| PCD-10 | Revisions and corrections | Approved by D-059 | For each invocation use the complete latest provider response returned by that invocation; never merge revisions across retrievals. Define any future point-in-time snapshot/correction policy separately. | No durable snapshot, cross-run revision selection, or historical replay guarantee |
| PCD-11 | Provenance and reproducibility | Selected-input fingerprint implemented; durable snapshots open | Preserve adapter provenance and selected observation details; fingerprint the canonical selected observations. A digest detects changed inputs but cannot recover them. | Assessment exposes SHA-256 `selected_input_digest`; source payloads are not persisted |
| PCD-12 | Timeout, rate limits, retry, cache, outage | Initial adapter behavior defined by D-057; operational limits remain open | Three sequential requests; 15-second timeout each; no retry/cache/fallback; fail full load; review provider quota before scheduled use | No automatic scheduling or outage recovery |
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

A status change in this register is not sufficient evidence of approval by itself. The authoritative governance record must be updated and linked before implementation treats a decision as closed. D-055 closes PCD-13 and PCD-14; D-059 closes PCD-10. Provider implementation and signal integration remain gated by the other open decisions.

## Implementation order (dependency guidance, not approval)

1. Close remaining PCD-04 through PCD-07 evidence before provider observations can qualify an ADM signal.
2. Close remaining PCD-08, PCD-11, and PCD-12 to define data quality, provenance, and operations.
3. PCD-13 and PCD-14 are approved by D-055; do not reopen them to unblock provider work.
4. Close PCD-15 and PCD-16 before end-to-end signal integration or activation review.

D-056 supplies provider-independent engineering defaults. D-057 resolves the
initial provider and adapter scope for private individual research. D-058
approves a seven-day selected-observation age limit. D-059 approves a
per-invocation latest-response policy and fail-closed duplicate handling,
without durable revision snapshots.
Publication-time SLA, live instrument coverage, historical replay, and
end-to-end signal activation remain open.

This order does not require all remaining decisions to be made in one session. D-057 has selected Alpha Vantage within its limited private-use scope.

## Explicit non-goals

This register does not select the configured defensive holding, revise D-058's seven-day maximum age, add retries, caching, fallback sources, persistence, or scheduling, assemble an ADM signal, activate ADM, or modify Core Runtime. The adapter's source selection and adjustment mapping are scoped only as D-057 states. D-055 approves SGOV as comparison benchmark and strict greater-than operator.

## Related documents

- `Moon_ADM_Provider_Adapter_Readiness_Review.md`
- `Moon_ADM_Provider_Adapter_Acceptance_Test_Matrix.md`
- `Moon_ADM_Provider_Decision_Evidence_and_Closure_Workflow.md`
- `Moon_ADM_Provider_Contract_Readiness_Audit.md`
- `Moon_ADM_Provider_Neutral_Adapter_Contract.md`
- `Moon_ADM_Data_Contract.md`
- `Orion_Data_Pipeline.md`
- `docs/05_Decisions/Decision_Log.md`
