# PCD-05 `exchange_calendars` Adapter Probe Result — 2026-10-19

## Scope

This record captures user-executed validation in a separate Windows Conda environment. It is evidence for a candidate adapter only; it does not approve a production dependency, asset-calendar mapping, or runtime integration.

## Environment and install evidence

- OS: Windows 11, 64-bit
- Python: 3.12.13 (Anaconda)
- Isolated environment: `orion-calendar-audit`
- `exchange-calendars==4.13.2`: installed and importable
- `pandas==3.0.6`, `numpy==2.5.4`: installed and importable
- `PyYAML==6.0.3`: installed in the audit environment to allow the Orion package import chain
- `pip check`: `No broken requirements found.`
- Conda repeatedly emitted `conda-libmamba-solver (No module named 'conda.reporters')` warnings; environment creation and the listed Python checks nevertheless completed. This is a separate Conda/plugin issue and remains unresolved.

## User-confirmed adapter/cutoff results

The command `conda run --prefix "$HOME/anaconda3/envs/orion-calendar-audit" python scripts/validate_adm_exchange_calendar.py` completed with `RESULT: all adapter and cutoff checks passed`.

| Check | Expected / actual | Result |
|---|---|---|
| XNYS session 2026-10-30 | `True` | Pass |
| XNYS session 2026-10-31 | `False` | Pass |
| XNYS session 2026-11-26 | `False` | Pass |
| XNYS session 2026-11-27 | `True` | Pass |
| XNYS session 2026-11-30 | `True` | Pass |
| May 2026 calendar month-end | 2026-05-31 | Pass |
| May 2026 evaluation cutoff | 2026-05-29 | Pass |
| October 2026 evaluation cutoff | 2026-10-30 | Pass |
| November 2026 evaluation cutoff | 2026-11-30 | Pass |
| Calendar identity/version metadata | `XNYS`, `exchange-calendars==4.13.2` | Pass |

## Interpretation and limits

The isolated Windows/Python 3.12.13 probe confirms that this package version can be installed/imported and that the adapter can satisfy the current provider-neutral protocol for the tested XNYS dates and month-end cutoffs. It does not establish correctness of every historical/future session, an approved mapping for VTI/VEU/SGOV, multi-market portfolio readiness, timezone/publication/freshness policy, or execution timing. The adapter probe is not wired into ADM runtime.

## Recommended next gate

1. Run the existing focused Moon tests in the designated `orion` environment (which already has PyYAML and pytest) to verify the unchanged provider-neutral prototype and data tests.
2. Run the repository's full test suite in the designated environment and record the exact command and output.
3. Review historical session edge cases and asset-calendar mapping evidence before proposing a pinned dependency. Do not add the package to repository requirements until that review is approved.

## Governance state

- No repository dependency pin or package adoption.
- No runtime wiring, strategy activation, or config changes; `config/moon.yaml` must retain `active_strategies: []`.
- No live market-data API calls.
- PCD-05/PCD-06 remain open; PCD-15/PCD-16 remain blocking; G-01 remains `DEFERRED — BLOCKING`.
