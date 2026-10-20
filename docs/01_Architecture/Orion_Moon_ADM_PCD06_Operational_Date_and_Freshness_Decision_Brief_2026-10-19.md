# Orion Moon / ADM — PCD-06 Operational Date and Freshness Decision Brief

- Date: 2026-10-19
- Status: **PARTIALLY APPROVED — R2/R3/R4/R6 approved; R1 request-triggered evaluation model and manual-reprocessing policy selected; R5 remains open**
- Scope: Operational semantics around monthly evaluation cutoffs, source observations, data readiness, and signal/execution dates.
- Evidence basis: Current repository code/tests; D-058 and D-059; PCD-04/PCD-06 evidence-boundary and test-coverage audits; approved PCD-05 US ETF mapping policy.

## 1. Executive finding

The repository has deterministic helpers for deriving monthly targets, selecting observations on or before those targets, and checking selected-observation age. D-058 approves a maximum age of seven calendar days for every required current and trailing observation across VTI, VEU, and SGOV. D-059 selects the complete latest provider response for each invocation and rejects duplicate identities. These decisions do **not** define the operational clock, provider publication SLA, signal-effective timestamp, or executable trading date.

This brief proposes explicit fail-closed boundaries for review. It does not change source code, schedule jobs, connect the approved PCD-05 calendar adapter to ADM runtime, or authorize signal assembly.

## 2. Terms that must remain distinct

| Term | Meaning | Current state |
|---|---|---|
| Evaluation target date | Calendar boundary used to identify eligible monthly observations | `derive_adm_monthly_target_dates()` uses last completed **calendar** month-end and prior-year corresponding calendar month-end as an engineering default |
| Market session date | Exchange-local date on which a market session occurs | PCD-05 mapping policy approved: VTI/VEU/SGOV use `XNYS` for cutoff session resolution; adapter remains isolated |
| Observation date | Date label supplied by the data provider for a bar, currently expected as date-only ISO | Selector chooses latest observation on or before target; it does not itself prove the label is a valid session |
| Provider availability/publication time | When the source first made the observation available to the client | No approved SLA or timestamp contract found |
| Assessment `as_of` date/time | Point at which an assessment determines which month is complete | Current helper accepts a date string; authoritative timezone and scheduler semantics are unresolved |
| Signal-effective date/time | When a calculated signal is deemed effective | Unresolved; do not infer from the evaluation target or data bar date |
| Execution-eligible date | First approved date on which an execution plan could use a signal | Unresolved; research spec's “last trading day” and execution spec's “next trading day” require reconciliation |

## 3. Existing approved controls — preserve unchanged

1. **D-058 freshness:** Every selected current and trailing observation must be no more than seven calendar days older than its corresponding target. One common cap applies across required observations; any violation fails closed. Do not fall back silently to an older monthly bar when the expected latest month is absent.
2. **D-056 selection:** Select the latest observation on or before the target; never select a future observation.
3. **D-059 revisions:** Use the complete latest history returned by one provider invocation. Do not merge observations across retrievals or silently combine revisions.
4. **PCD-05 calendar mapping:** VTI, VEU, and SGOV map to `XNYS` for evaluation-cutoff session resolution. This does not prove provider publication time or adjusted-price correctness.
5. **Activation/governance:** `config/moon.yaml` must retain `active_strategies: []`; G-01 remains `DEFERRED — BLOCKING`; PCD-15/PCD-16 and PCD-04 remain separate blockers.

## 4. Operational rules and approval record

### R1 — Request-triggered evaluation and operational timezone (partially approved)

**User decision recorded on 2026-10-19 and clarified on 2026-10-20:** use `Asia/Seoul` as the operational timezone, but trigger an assessment in response to an explicit evaluation request rather than assuming a fixed monthly date or wall-clock time. Requests may occur at month-end, early in the following month, or at another date/time. The request instant is the actual assessment trigger; the evaluation target month-end remains independently derived under the approved `XNYS` cutoff rule. This selects the request-triggered model but does not authorize scheduler registration or ADM runtime integration.

No fixed monthly schedule, default morning time, or provider-readiness SLA is implied. The user explicitly notes that evaluation requests are not guaranteed to occur in the morning. The request timestamp must be captured explicitly, interpreted using `Asia/Seoul` for operational reporting, and normalized to UTC for persistence/comparison. The user previously selected **manual reprocessing** for failed or missed runs (see R1e).

#### R1a — Request and timestamp contract proposal

- Represent each evaluation request and actual start as timezone-aware instants; record the operational timezone as `Asia/Seoul` and convert instants to UTC for persistence/comparison. Never use the host machine's implicit local timezone.
- Record at least the request instant, actual start instant, run identifier, intended evaluation target, and snapshot boundary. Keep request time, actual start, data availability time, and target date separate.
- For source availability, record retrieval/ingestion time separately from provider publication time. If the provider does not supply a trustworthy publication timestamp, mark publication time as unknown; do not relabel retrieval time as publication time.
- Only observations that have been retrieved and validated by the assessment's defined data-snapshot boundary may participate. Data arriving after that boundary must not silently mutate an in-progress run; it may be considered only by a separately authorized retry/new run policy.
- Preserve R3/D-058: no grace period, retry window, or stale-bar substitution is implied. If required data is not ready at the assessment boundary, fail closed.

#### R1b — DST and cross-market calendar handling proposal

- `Asia/Seoul` currently has no seasonal daylight-saving clock changes. The scheduler must still use an IANA timezone database identifier rather than a fixed `UTC+09:00` offset, so timezone rules remain explicit and auditable.
- US market DST is a separate concern from the Seoul scheduler. Do not hardcode a fixed Seoul-to-New-York offset; resolve US sessions through the approved `XNYS` calendar implementation and use timezone-aware timestamps when comparing instants.
- The approved `XNYS` session date determines the market evaluation cutoff. It does not itself specify the Seoul trigger time, provider publication SLA, signal-effective time, or execution time.

#### R1c — Month-boundary contract proposal

- Compute the request's operational date from the request instant converted to `Asia/Seoul`; never derive it from the host timezone or UTC date by truncation.
- Do not infer the evaluation target month solely from the request date. Preserve an explicit target month/target date, then derive its cutoff using the approved `XNYS` month-end rule. If target selection is ambiguous, require clarification rather than silently choosing a month.
- Keep calendar month-end, the PCD-05 previous-valid-session cutoff, provider observation date, and assessment execution instant as distinct fields.
- For month-end falling on a weekend or exchange holiday, use the approved PCD-05 rule for the relevant instrument calendar: calendar month-end when it is a session, otherwise the immediately preceding session. Do not substitute the provider's bar label for the target.
- For December/January rollover and leap-year February, use calendar arithmetic and explicit tests; do not assume every month has the same number of days.
- The current helper's prior-year comparison target remains an engineering default until its methodology is separately approved. This R1 decision does not silently change it.

#### R1d — Boundary and test contract proposed for review

Once the exact wall-clock time and frequency are approved, add deterministic tests for:

1. An instant immediately before, exactly at, and immediately after the scheduled trigger in `Asia/Seoul`.
2. The same instant represented in UTC, proving that conversion preserves the instant and does not change the intended Seoul operational date.
3. US DST transition weeks, proving no fixed Seoul/New York offset is used and session lookup remains tied to `XNYS`.
4. Month-end on a session, on a weekend, and on a US market holiday; December/January rollover; leap-year and non-leap-year February.
5. Data retrieved before the run snapshot boundary versus data arriving after it; unknown provider publication time; missing/late required data; and no implicit grace-period retry.
6. A request made around Seoul midnight or month/year boundaries does not accidentally change the explicit evaluation target.
7. A request arriving while required data is not ready fails closed; no automatic wait, retry, or replay occurs.

R1 remains **partially approved** because implementation evidence and R5 signal/execution date semantics remain open. These are design contracts only; no scheduler, runtime behavior, or signal/execution timing is implemented by this document.


#### R1e — Failed/missed run recovery decision (approved policy; not implemented)

**User decision recorded on 2026-10-20:** select **A. Manual reprocessing**. Do not automatically retry or replay a failed/missed assessment.

- Record the original run as failed, blocked, or missed with its run identifier, scheduled instant, actual start (if any), and reason. Preserve its audit record; do not overwrite it with a later attempt.
- A retry/reprocessing attempt requires an explicit operator request after the cause and data readiness are reviewed.
- Treat reprocessing as a distinct run with a new run identifier and its own actual start/snapshot boundary. Preserve the intended evaluation target; do not silently roll it forward to a different month or change the target to match newly arrived data.
- Re-run all applicable input-contract, target-selection, calendar, and D-058 freshness checks. If required data remains missing, stale, malformed, duplicated, future-dated, or otherwise invalid, fail closed again. Manual reprocessing does not waive gates or authorize stale-data substitution.
- Do not infer provider publication SLA, grace period, retry count, automatic scheduler misfire handling, or execution authorization from this decision.
- This is a policy decision only. No scheduler registration, automatic retry, replay facility, runtime wiring, signal assembly, or strategy activation is authorized.

### R2 — Target date is not a bar date

Keep target date, selected observation date, and provider availability time as separate values. The selected observation must be on or before its target and pass D-058 freshness. Do not rewrite the target to equal the provider's returned month-end label.

### R3 — Missing or late completed-month data is not repaired silently

If any required current/trailing observation is absent, later than the target, duplicated, malformed, or older than the D-058 cap, the assessment is not ready. Do not substitute a later observation, carry forward an older month, or synthesize a bar. A retry/grace window must not be invented until a publication SLA and retry policy are approved.

### R4 — One run, all required inputs ready

For a future portfolio-level assessment, retain a common run identifier and require all inputs needed by that assessment to pass data-contract, target-selection, and freshness gates before producing a complete assessment result. If any required instrument fails, fail the overall assessment closed rather than publishing a partial ADM result. This is a proposed policy, not current runtime behavior.

### R5 — Signal and execution timing remain separate decisions

Do not infer signal-effective date or next-trading-day execution date from the evaluation cutoff. Approve those semantics separately, including market holidays, delayed data, and the distinction between a computed result and an executable plan. No execution scheduling or signal activation is included here.

### R6 — Calendar failures fail closed

When the approved calendar implementation cannot load, reports a version mismatch, or cannot resolve a requested session, the assessment must not fall back to plain calendar month-end or latest available observation. This is consistent with the isolated PCD-05 adapter; runtime integration remains out of scope.

## 5. Decisions still required

| Decision | Recommendation | Why it remains open |
|---|---|---|
| Authoritative assessment timezone and cutoff instant | Explicitly choose one timezone and deterministic cutoff contract before scheduling | Current helper accepts date-only input; no authoritative timezone is recorded |
| Publication SLA and retry/grace window | Do not define a grace window until evidence supports it; fail closed when data is unavailable | No provider SLA verified; PCD-02 live contract remains uncertain |
| Portfolio readiness semantics | One common run ID; all required inputs ready or overall assessment not ready | Prevents partial cross-asset inputs, but needs explicit policy approval |
| Signal-effective date | Separate decision | Research and execution specifications are not yet reconciled |
| Execution-eligible date / next-session rule | Separate decision using approved market calendar and a defined signal-effective date | PCD-05 cutoff is not an execution timestamp |
| Whether prior-year target is calendar month-end or same-month final session | Preserve current helper as an engineering default until methodology decision | PCD-05 policy currently covers evaluation cutoff; changing the target policy needs a versioned transition |

## 6. Required test cases after policy approval

- `as_of` immediately before and after the approved timezone cutoff.
- January/December rollover and leap-year February.
- Month-end on weekend and exchange holiday, with the previous valid session's observation.
- Exact seven-calendar-day age accepted and eight-day age rejected for both current and trailing observations.
- Missing latest completed-month bar, late publication, malformed date, duplicate observation, and provider correction/revision.
- One required instrument unavailable while the others are valid: overall assessment must not become signal-ready.
- Calendar construction/session lookup failure: no fallback calendar or date-only shortcut.
- Signal-effective and execution-eligible date cases only after those policies are separately approved.

## 7. Implementation boundary

This is a documentation-only decision brief. It adds no runtime behavior and does not close PCD-06. It does not validate PCD-04 adjusted-price semantics or PCD-02 provider reliability. No live API requests were made. No signal assembly, strategy activation, or execution behavior is authorized.

## 8. Approval record and remaining decisions

On 2026-10-19, the user explicitly approved **R2, R3, R4, and R6** as operational data-readiness principles:

- **R2 approved:** target date, selected observation date, and provider availability time remain separate; selected observations must not exceed the target and must pass D-058.
- **R3 approved:** missing, late, duplicate, malformed, future-dated, or stale required observations do not get silently repaired or substituted; no retry/grace window is implied.
- **R4 approved as policy:** a future portfolio assessment uses a common run identifier and all-required-input readiness; any required input failure makes the overall assessment not ready. This is not yet current runtime behavior.
- **R6 approved:** calendar dependency/version/construction/session lookup failures fail closed; no plain-calendar or latest-observation fallback.

**R1 is partially approved; R5 remains open.** The user selected `Asia/Seoul`, an explicit request-triggered evaluation model, and manual reprocessing for failed/missed runs. There is no fixed recurring schedule or default time of day. Signal-effective time and execution-eligible date remain separate decisions. No scheduler, runtime integration, signal assembly, or execution behavior is authorized. PCD-06 remains open until remaining decisions and implementation/test evidence are complete.

**R1e approval record (2026-10-20):** manual reprocessing is approved as policy. Automatic retries/replays are not allowed. A manually authorized reprocessing attempt must have a new run ID, preserve the original failed/missed run record and intended evaluation target, establish a new snapshot boundary, and rerun every readiness gate. This does not authorize implementation or scheduling.


## 9. Provider availability evidence review (2026-10-20)

The official Alpha Vantage documentation for `TIME_SERIES_MONTHLY_ADJUSTED` describes monthly bars labelled by each month's last trading day, but does not state a guaranteed publication time or completed-month data SLA. See `Orion_Moon_ADM_PCD06_Provider_Availability_and_Schedule_Evidence_Review_2026-10-20.md`. Therefore, no exact execution clock time can be justified as a data-readiness guarantee from public documentation alone. The explicit evaluation request, data snapshot boundary, and readiness gates remain separate. No live API request was made; a fixed recurring schedule is not part of the selected operating model.


## 10. Request-triggered model clarification (2026-10-20)

The user rejected a fixed “third business day at 10:00 Asia/Seoul” monthly schedule. Evaluation should be initiated on the day/time the operator requests it; requests are not guaranteed to occur in the morning or near month-end. Record the request instant, actual start instant, and snapshot boundary independently. The evaluation target month and `XNYS` cutoff must remain explicit and must not be inferred solely from the request timestamp. No automatic scheduler is needed for this model, and none is authorized. If required data is unavailable at the request snapshot, fail closed and wait for an explicit manual reprocessing request after review.

## 11. Explicit as-of date/time contract (2026-10-20; target selection clarified)

The user clarified the intended request semantics with the example “evaluation through November 2.” The assessment request must explicitly identify the inclusive evaluation end date or an exact timezone-aware `as_of` instant. The request timestamp itself must not be used to guess the evaluation target.

- **Date-only request:** when the caller specifies an inclusive date such as `2026-11-02` without a time, interpret the data-availability boundary as the start of the following calendar day in `Asia/Seoul` (exclusive boundary: `2026-11-03T00:00:00+09:00`). This avoids precision-dependent `23:59:59` handling. Persist/compare the corresponding instant in UTC as `2026-11-02T15:00:00Z`.
- **Timestamp request:** when the caller provides an exact `as_of` timestamp, it must include a timezone or be explicitly interpreted under the approved `Asia/Seoul` operational timezone. Normalize the instant to UTC for persistence/comparison; do not truncate or reinterpret it using the host machine timezone.
- **Availability gate:** only data retrieved and validated by the run's snapshot boundary may be used. A provider publication timestamp, if available and trustworthy, is recorded separately from retrieval/ingestion time. If publication time is absent, mark it unknown; do not infer it from retrieval time.
- **Market cutoff remains independent:** the inclusive Seoul evaluation date / `as_of` instant does not directly become an `XNYS` session date. PCD-05 independently determines the instrument's market evaluation cutoff using the approved calendar-month-end rule. The selected price observation must satisfy both the explicit as-of boundary and the applicable target/freshness gates.
- **No silent late-data inclusion:** data arriving after the snapshot boundary is excluded from that run. It may be considered only in an explicitly requested manual reprocessing run with a new run ID and new snapshot boundary; all readiness gates run again.
- **Clarification required:** if the request does not specify the target date/month or exact timestamp sufficiently to determine the intended evaluation period, ask the operator to clarify. Do not infer “last completed month” from the request date.

### Deterministic examples

| Request | Availability boundary | Interpretation |
|---|---|---|
| “Evaluate through 2026-11-02” | Exclusive `2026-11-03T00:00:00+09:00` (`2026-11-02T15:00:00Z`) | Data must have been available to the run before the boundary; November 2 is inclusive as a Seoul calendar date |
| `as_of=2026-11-02T14:30:00+09:00` | Exact instant `2026-11-02T05:30:00Z` | Data must satisfy the exact instant boundary, not end-of-day |
| Request received on November 3, target “through November 2” | Target still ends November 2 | Request date does not shift the target to November 3 or infer a different target month |

This section defines a policy contract only. It does not implement parsing, scheduling, snapshot isolation, runtime wiring, signal assembly, or execution behavior. PCD-06 remains open pending implementation evidence, deterministic tests, and separate approval of R5 signal-effective/execution-eligible date semantics.

