# Orion Moon ADM Provider Response Contract Verification

## Purpose

Record the distinction between checking the provider adapter against the documented Alpha Vantage response contract and verifying actual live responses for the pilot symbols.

## Documented contract checked

The official Alpha Vantage documentation describes `TIME_SERIES_MONTHLY_ADJUSTED` as monthly adjusted time-series data labeled by the last trading day of each month, including monthly adjusted close and monthly dividend fields. The response fixture uses the documented JSON field names `Meta Data` / `2. Symbol`, `Monthly Adjusted Time Series`, and `5. adjusted close`.

Reference: https://www.alphavantage.co/documentation/ (section `TIME_SERIES_MONTHLY_ADJUSTED`).

The adapter's contract tests now explicitly verify fail-closed handling for:

- provider-level `Error Message`, `Note`, and `Information` payloads;
- a response whose instrument identity does not match the requested symbol;
- non-finite adjusted-close values;
- malformed JSON and duplicate JSON keys;
- missing/insufficient monthly history and invalid adjusted-close fields;
- transport errors without exposing the credential-bearing URL.

## Live-response status

No live API request was performed during this verification. `ORION_ALPHA_VANTAGE_API_KEY` was not configured in the execution environment. All automated provider tests use deterministic synthetic fixtures and therefore do not prove that VTI, VEU, and SGOV are currently covered by the provider, that the actual response has the expected shape for each symbol, or that the provider's adjusted-price methodology is suitable for the ADM policy.

## Decision

- **Fixture contract verification:** passed when the repository test suite passes.
- **Live provider response verification:** not performed; remains open.
- **Adjusted-price methodology approval:** remains open.
- **Runtime integration, signal assembly, strategy activation, and order execution:** not authorized by this document and remain unchanged.
- **Persistence:** no cache or local database is introduced.

A future live check requires an explicitly configured API key and an approved execution context. It must record only sanitized status/shape information and must never log the credential or full request URL.

## Safe live-check procedure

A manual live check is available via `python scripts/check_alpha_vantage_live_contract.py`.
Set `ORION_ALPHA_VANTAGE_API_KEY` in the invoking shell/environment; do not put the key in command-line arguments, source files, or logs. The script makes one request per configured symbol, has no retry loop, and prints only the batch date, per-symbol observation count, and oldest/latest observation dates. It never prints prices, raw payloads, the credential-bearing URL, or the key. A missing key produces `NOT RUN` and exit code 2; a provider/contract failure produces a sanitized failure and exit code 1.

This script has not been run against the live provider in the current environment because `ORION_ALPHA_VANTAGE_API_KEY` is not configured. Its existence is a safe execution path, not evidence of live verification. Passing it would establish response shape and minimum history coverage only; it would not validate historical price accuracy, monthly adjustment methodology, current data freshness for the ADM decision date, or authorization to produce/activate a signal.

## Offline contract hardening — 2026-10-12

Before live access is available, the fixture-only contract has been hardened in two additional ways:

- The provider rejects two distinct observation dates in the same calendar month for one symbol. The selected Alpha Vantage endpoint is a monthly series; silently accepting multiple bars in one month could make endpoint selection depend on malformed provider output.
- The opt-in live-check CLI rejects observations later than the batch `as_of` date and rejects multiple bars in one calendar month. These checks run across the complete batch before any PASS output is printed.

Automated tests use synthetic payloads and do not make network requests. These safeguards improve response-shape validation but do not prove live symbol coverage, trading-calendar correctness, historical price accuracy, adjusted-price parity, or investment suitability.

See also [`Moon_ADM_Alpha_Vantage_Endpoint_Entitlement_Audit.md`](Moon_ADM_Alpha_Vantage_Endpoint_Entitlement_Audit.md) for a documentation-only review of endpoint entitlement labels.
