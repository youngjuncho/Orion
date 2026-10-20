# BAA-G12 Strategy Specification / Implementation Audit

Audit baseline: v1.17 policy and month-end contract update  
Scope: compare `BAA_Research.md`, `BAA_Orion.md`, and the research-only implementation in `src/orion/frameworks/moon/baa.py` with the offline tests.  
Execution boundary: source inspection and synthetic tests only. No provider calls, API credentials, scheduling, runtime activation, or trading.

## Executive result

The core arithmetic and portfolio-selection branches match the documented BAA-G12 formulas and universes. The duplicate-BIL output convention and research signal-date convention are now explicit approved Orion policies, and the input builder requires a final-session attestation. The offline suite includes new fail-closed tests. Provider semantics and the truth of upstream attestations remain unvalidated.

## Rule-by-rule findings

| Rule | Implementation | Audit result | Notes |
|---|---|---|---|
| Canary universe | SPY, VWO, VEA, BND | PASS | Matches the documented G12 baseline. |
| Offensive universe | 12 assets in `BAA_Research.md` | PASS | Matches the documented G12 list. |
| Defensive universe | TIP, DBC, BIL, IEF, TLT, LQD, BND | PASS | Matches the documented list. |
| 13612W formula | 12×1M + 4×3M + 2×6M + 1×12M returns | PASS | Matches the documented unnormalized weighted sum. |
| SMA(12) ranking measure | Current price divided by the mean of current month plus prior 12 months, minus one | PASS | This is a 13-observation mean in the current specification. It should not be silently changed to a 12-observation mean. |
| Canary state | Any score `< 0` => Risk Off; otherwise Risk On | PASS | Zero remains Risk On, as specified. |
| Risk-On selection | Rank Offensive universe by SMA measure; select top six equally weighted | PASS | Deterministic universe-order tie-break. |
| Risk-Off selection | Rank Defensive universe by SMA measure; take top three slots | PASS | Deterministic universe-order tie-break. |
| BIL floor | Replace selected asset when its 13612W score is strictly below BIL's | PASS | Equality does not trigger replacement, matching the implementation specification. |
| Duplicate BIL slots | Preserve three equal-weight slots and aggregate repeated BIL replacements into one ticker | PASS — APPROVED ORION POLICY | This is an approved portfolio-output representation convention, not a claim that the primary source explicitly specifies duplicate-ticker accounting. |
| Signal date | Use the observed date of the verified final US trading session in the target month | PASS — APPROVED RESEARCH CONVENTION | The period label remains `YYYY-MM`; `signal_date` is the actual verified session date. This does not authorize execution. |
| Monthly observation selection | Require `month_end_session_verified=true` and one common observed session date across all 17 symbols for each month | PASS WITH ATTESTATION LIMIT | The builder fails closed when the attestation is absent or dates disagree. It does not independently validate whether the adapter made a truthful calendar/source check. |
| Data source / TR semantics | Caller-supplied `adjusted_close`; provider identity and total-return equivalence not established by the signal module | BLOCKED BY DESIGN | Correctly documented as unvalidated; no empirical source approval is implied. |
| Fail-closed data checks | Missing months, duplicates, invalid values/dates, and non-USD observations rejected | PASS WITH SCOPE LIMIT | These are structural checks; they do not validate source freshness or final-trading-session sampling. |
| Runtime and execution isolation | No provider calls, Moon runtime registration, asset mapping, scheduling, or order submission in this module | PASS | Output remains `research-only-not-executable`. |

## Remaining gates before operational sign-off

1. **Validate the month-end attestation producer.** The upstream adapter/quality gate must set `month_end_session_verified=true` only after checking the provider timestamp against the final valid US market session. The builder verifies presence and cross-symbol date alignment but cannot independently prove the flag is truthful.
2. **Keep provider approval separate.** Validate symbol identity, coverage, timestamps, adjustment behavior around distributions/splits, and history revisions before selecting a source. No provider is approved by this audit.
3. **Keep execution separate.** Signal-date policy does not define or authorize order timing, runtime registration, scheduling, or trading.

## Verification

- Full offline test suite: validation recorded in the v1.17 bundle manifest.
- New targeted BAA tests verify unverified month-end metadata and cross-symbol date disagreement fail closed.
- No live API calls or data collection were performed.

## Conclusion

The mathematical selector and approved Orion output conventions are documented consistently. Operational sign-off remains blocked on empirical provider validation and verification of the upstream final-session attestation. This audit is research documentation, not authorization to activate BAA or collect live data.
