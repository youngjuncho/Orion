# Orion Moon / ADM — PCD-06 As-of and Freshness Deterministic Test Specification

- Date: 2026-10-20
- Status: **PARTIALLY IMPLEMENTED — AS-OF HELPERS, D-058 7-DAY ACCEPTANCE, AND OPTIONAL XNYS INTEGRATION TESTS ADDED; FULL ACCEPTANCE MATRIX OPEN**
- Scope: Testable acceptance criteria for request-triggered assessment, explicit as-of boundaries, calendar cutoffs, data availability, freshness, and manual reprocessing.
- Governance: No scheduler registration, ADM runtime integration, signal assembly, strategy activation, or live API call is authorized by this document.

## 1. Purpose

Translate approved PCD-06 policy decisions into deterministic test cases. Implemented so far: pure as-of boundary parsing and availability-boundary helpers with fixed fixtures. The full acceptance matrix below is not yet implemented. Tests must not call live market-data APIs or depend on the machine's local timezone.

## 2. Contract under test

1. An assessment is initiated by an explicit request, not by a recurring scheduler.
2. The request explicitly identifies an inclusive end date (`through_date`) or an exact timezone-aware `as_of` instant. Do not infer the target period from request arrival time.
3. Operational interpretation uses the IANA zone `Asia/Seoul`. Instants are normalized to UTC for persistence and comparison; host-local timezone must have no effect.
4. A date-only request such as `through_date=2026-11-02` yields the exclusive availability/snapshot boundary `2026-11-03T00:00:00+09:00`, equal to `2026-11-02T15:00:00Z`. Events at the boundary are excluded; events strictly before it may be considered, subject to all other gates.
5. An exact timestamp request uses that exact instant as the exclusive boundary. If the timestamp includes an offset, preserve its instant; if it is naive, only accept it when the API contract explicitly says to interpret it in `Asia/Seoul`. Reject ambiguous/malformed values.
6. The provider observation date, trustworthy provider publication time (if available), retrieval/ingestion time, snapshot boundary, actual assessment start, and evaluation target/cutoff remain separate fields.
7. The PCD-05 approved evaluation cutoff uses `XNYS` for VTI, VEU, and SGOV: calendar month-end if it is an XNYS session, otherwise the immediately preceding XNYS session. The `as_of` boundary does not replace the market cutoff.
8. D-056 selection remains latest observation on or before target; D-058 freshness remains a maximum age of seven calendar days for every required current and trailing observation; D-059 requires the complete latest history returned by one provider invocation and rejects duplicate identities.
9. Missing, malformed, duplicate, future-dated, late, or stale required inputs fail closed. Do not silently merge provider responses, substitute an older monthly bar, infer publication time from retrieval time, or apply a grace period.
10. Failed/missed runs are not automatically retried or replayed. An explicitly requested manual reprocessing attempt gets a new run ID and snapshot boundary, preserves the original audit record and intended target, and reruns all readiness gates.

## 3. Deterministic acceptance matrix

### A. As-of parsing and timezone

| ID | Setup / input | Expected result |
|---|---|---|
| ASOF-01 | `through_date=2026-11-02` | Exclusive boundary is `2026-11-03T00:00:00+09:00` / `2026-11-02T15:00:00Z`. |
| ASOF-02 | Availability event at `2026-11-02T14:59:59.999999Z` for ASOF-01 | Event is before the boundary and may pass this gate. |
| ASOF-03 | Availability event exactly at `2026-11-02T15:00:00Z` for ASOF-01 | Event is excluded from that snapshot. |
| ASOF-04 | `as_of=2026-11-02T14:30:00+09:00` | Exact instant normalizes to `2026-11-02T05:30:00Z`; no end-of-day expansion. |
| ASOF-05 | Equivalent instant expressed as `2026-11-02T05:30:00Z` | Same normalized instant as ASOF-04. |
| ASOF-06 | Naive timestamp with no declared timezone interpretation | Reject as ambiguous; do not use host timezone. |
| ASOF-07 | Naive timestamp with API contract explicitly declaring `Asia/Seoul` | Interpret in Seoul and normalize to UTC deterministically. |
| ASOF-08 | Invalid date, invalid offset, or malformed timestamp | Reject request with a typed validation error; do not begin evaluation. |
| ASOF-09 | Same instant under different host `TZ` settings | Identical normalized UTC instant and Seoul operational date. |
| ASOF-10 | Request received Nov 3, explicitly targeting “through Nov 2” | Target remains Nov 2; request date must not shift target. |
| ASOF-11 | Request omits target date/month and does not supply an exact `as_of` sufficient to define the period | Ask for clarification / reject as underspecified; do not infer last completed month. |

### B. Calendar cutoff and month boundaries

| ID | Setup / input | Expected result |
|---|---|---|
| CAL-01 | Month-end is an XNYS session | Cutoff is that calendar month-end session. |
| CAL-02 | Month-end is Saturday/Sunday | Cutoff is the immediately preceding XNYS session. |
| CAL-03 | Month-end is an XNYS holiday | Cutoff is the immediately preceding XNYS session. |
| CAL-04 | December target month | Target year and prior/next-year arithmetic do not cross-contaminate the requested month. |
| CAL-05 | Leap-year February | February 29 is handled by calendar arithmetic; cutoff follows XNYS session membership. |
| CAL-06 | Non-leap-year February | February 28 is handled correctly; cutoff follows XNYS session membership. |
| CAL-07 | US DST spring/fall transition week | No fixed Seoul/New York offset is hardcoded; UTC instants and XNYS session lookup remain correct. |
| CAL-08 | Calendar construction, version validation, or session lookup fails | Fail closed; no plain-calendar or latest-observation fallback. |
| CAL-09 | Provider monthly bar label differs from the derived cutoff | Preserve both values; do not rewrite target to match provider label. Apply existing selection/freshness gates. |

### C. Data availability and snapshot isolation

| ID | Setup / input | Expected result |
|---|---|---|
| DATA-01 | Required observation retrieved and validated strictly before snapshot boundary | Eligible for further target, schema, duplicate, and freshness gates. |
| DATA-02 | Observation first retrieved at snapshot boundary | Excluded because boundary is exclusive. |
| DATA-03 | Observation retrieved after snapshot boundary while assessment is running | Does not mutate the current run or its result. |
| DATA-04 | Provider publication time is present and trustworthy | Preserve it separately from retrieval/ingestion time and apply the approved availability policy. |
| DATA-05 | Provider publication time is absent/untrustworthy | Store publication time as unknown; never infer it from retrieval time. |
| DATA-06 | Retrieval time is earlier than snapshot boundary but provider publication time is known to be later | Treat as unavailable for the snapshot if publication time is part of the accepted source-availability contract; do not use retrieval time to bypass it. |
| DATA-07 | Required current or trailing observation missing | Overall assessment not ready; no stale substitution. |
| DATA-08 | One required instrument fails while other instruments pass | Portfolio-level assessment remains not ready; no partial signal-ready result. |
| DATA-09 | Duplicate observation identity in one provider response | Reject response/assessment under D-059; do not deduplicate silently. |
| DATA-10 | Provider correction/revision arrives in a later retrieval | Do not merge histories across invocations; a separate authorized run uses one complete response snapshot. |
| DATA-11 | Observation date is later than target | Reject that observation; D-056 must not select future data. |
| DATA-12 | Observation date is malformed or not valid under the input contract | Fail closed with a typed data-contract error. |

### D. Freshness (D-058) and selection (D-056)

| ID | Setup / input | Expected result |
|---|---|---|
| FRESH-01 | Required current observation age is exactly 7 calendar days | Pass the age gate if all other conditions pass. |
| FRESH-02 | Required current observation age is 8 calendar days | Fail the age gate. |
| FRESH-03 | Required trailing observation age is exactly 7 calendar days | Pass the age gate if all other conditions pass. |
| FRESH-04 | Required trailing observation age is 8 calendar days | Fail the age gate. |
| FRESH-05 | A newer eligible observation exists on or before target | Select the latest eligible observation. |
| FRESH-06 | Only observations after target exist | Fail; do not select a future observation. |
| FRESH-07 | Expected latest completed-month observation is missing but an older bar exists | Do not silently substitute older bar; apply target and freshness policy and fail closed where required. |
| FRESH-08 | Provider response contains a valid-looking observation retrieved after snapshot boundary | Exclude from current run regardless of date label. |

### E. Manual reprocessing and auditability

| ID | Setup / input | Expected result |
|---|---|---|
| REPROC-01 | Run fails due to missing/stale data | Record failure/block reason and original run ID; no automatic retry. |
| REPROC-02 | Scheduler/missed-run event is simulated | No scheduler/replay behavior is introduced; record missed/blocked state only if invoked by a caller. |
| REPROC-03 | Operator explicitly requests manual reprocessing | Create a new run ID and snapshot boundary; preserve original run and intended target. |
| REPROC-04 | Manual reprocessing still has missing/stale required data | New run fails closed again; manual authorization does not bypass gates. |
| REPROC-05 | New data arrives after original boundary and before manual reprocessing | Original run remains unchanged; new run may consider it only if retrieved/validated before the new boundary and all gates pass. |
| REPROC-06 | Attempt to reuse original run ID for reprocessing | Reject or enforce a new immutable run identity; never overwrite original audit record. |

## 4. Test implementation guidance

- Use frozen, explicit timezone-aware datetimes and deterministic fixtures. No sleeping, wall-clock dependence, or live network calls.
- For DST tests, compare equivalent instants and use IANA zone data; do not assert a fixed Seoul/New York hour difference.
- Calendar tests should use the pinned `exchange-calendars==4.13.2` adapter only in isolated adapter tests. If dependency/version/calendar resolution fails, assert fail-closed behavior.
- Make boundary inclusivity explicit: snapshot/availability boundary is exclusive. The date-only request maps to the next Seoul midnight, not to a precision-dependent `23:59:59` timestamp.
- Test both per-instrument gates and the portfolio-level all-required-input gate.
- Assert audit records preserve request instant, actual start instant, intended target, cutoff, snapshot boundary, observation date, publication-time-known/unknown state, retrieval time, and failure reason as separate fields.
- Test that no source code path registers a scheduler, triggers a live provider request, enables `active_strategies`, or wires the adapter into runtime as part of this test-specification change.

## 5. Implementation status (2026-10-20)

Implemented in `src/orion/frameworks/moon/adm_asof.py`, with tests in `tests/orion/frameworks/moon/test_adm_asof.py`:

- Date-only `through_date` becomes the following Seoul midnight as an exclusive boundary and normalizes to UTC.
- Exact timezone-aware `as_of` remains an exact instant; equivalent offsets normalize identically.
- Naive timestamps are rejected unless the caller explicitly enables Asia/Seoul interpretation.
- Malformed dates/timestamps and requests supplying both/neither target forms are rejected.
- Availability timestamps must be timezone-aware and are eligible only strictly before the exclusive boundary.
- Leap-day date-only boundary is covered.

This implementation remains isolated from the provider, dataset snapshotting, ADM assessment pipeline, scheduler, signal assembly, and execution. The D-058 exact-seven-day acceptance case is covered. Optional real-package XNYS integration tests now cover weekend month-end, month-end session, leap/non-leap February, and session membership around US DST transition dates; these require the exact pinned dependency and were skipped in the workspace that had version 4.13.1. Provider response integrity, snapshot immutability, full process-TZ variation, and manual-reprocessing audit persistence remain open.

## 6. Out of scope / unresolved decisions

1. R5 signal-effective timestamp and execution-eligible date semantics remain open.
2. Provider publication SLA remains unverified; no grace period or provider readiness time is inferred.
3. PCD-02 live provider contract, PCD-04 adjusted-price semantics/parity, PCD-15/PCD-16 authoritative registry binding, and G-01 remain separate blockers.
4. This specification does not authorize source/test implementation, scheduler registration, runtime wiring, live API calls, signal assembly, or strategy activation.

## 7. Exit criteria for the implementation phase

The implementation phase can be proposed for approval only after:

- Every applicable test above is implemented or explicitly marked not applicable with rationale.
- Focused tests and the full regression suite pass in the user's Windows Orion environment.
- UTF-8 policy check and bundle integrity checks pass.
- No live API calls occur; no scheduler/runtime wiring or strategy activation is introduced without separate approval.
- Test results and remaining exceptions are recorded in a new evidence note.
