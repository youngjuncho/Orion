# BAA-G12 Market Data Source Assessment

Version: 1.2

Status: Research assessment — no provider approved

Last Updated: 2026-10-20

## Decision Summary

This is a **documented provider comparison, not an empirical price-data validation**. No provider API was called and no API key was available in this step. Therefore symbol-by-symbol coverage and adjusted-price values remain unverified.

For a controlled BAA research prototype, **Alpha Vantage is the preferred candidate to validate first**, because its official API documents a dedicated monthly-adjusted endpoint with explicit month-end timestamps and dividend fields. This is not yet provider approval. Yahoo Finance is better treated as an independent cross-check than as the default automated source because the commonly used `yfinance` package is an unofficial wrapper around Yahoo's publicly available APIs, intended for personal/research use, and its behavior can be affected by rate limiting and API changes.

The existing Orion Alpha Vantage source is tailored to the ADM universe (`VTI`, `VEU`, `SGOV`) and must not be reused unchanged for BAA.

The BAA-G12 signal universe requires 17 unique tickers:

`SPY, QQQ, IWM, VGK, EWJ, VWO, VEA, VNQ, DBC, GLD, TLT, HYG, LQD, TIP, BIL, IEF, BND`.

No live provider calls were made during this assessment. Symbol-by-symbol coverage, returned history, and price-series values have not been tested.

## Same-universe Provider Comparison

The 17 unique BAA-G12 symbols to check are:

`SPY, QQQ, IWM, VGK, EWJ, VWO, VEA, VNQ, DBC, GLD, TLT, HYG, LQD, TIP, BIL, IEF, BND`.

| Criterion | Alpha Vantage | Yahoo Finance via `yfinance` | Current evidence |
|---|---|---|---|
| Monthly data | Official `TIME_SERIES_MONTHLY_ADJUSTED` endpoint | `interval="1mo"` is available in `yfinance`; wrapper/API behavior is not a vendor contract | Documented capability only |
| Month-end date | Vendor says monthly bars are dated at the last trading day of the month | Monthly bars can be retrieved, but output dates and sampling behavior must be checked against daily observations | Alpha Vantage documentation is more explicit |
| Distribution adjustment | Monthly adjusted close and monthly dividend are returned; Alpha Vantage describes split/cash-dividend adjustments | Yahoo defines adjusted close using split and dividend multipliers; `yfinance` defaults have changed, and `auto_adjust` must be explicitly controlled | Similar broad intent; not proven numerically equivalent |
| Batch/request pattern | One symbol per monthly adjusted request; 17 symbols means 17 calls for one refresh | `yfinance.download()` can accept multiple symbols in one call, but it still depends on Yahoo's public endpoints and may be rate-limited | Alpha Vantage request budget is easier to count; neither has been load-tested here |
| Free access / limits | Support page currently states 25 requests/day for most free stock datasets; endpoint entitlement and quotas should be confirmed on the account before implementation | Yahoo's website CSV download is documented as requiring Gold; `yfinance` is unofficial and its access should not be treated as a guaranteed free service | Confirm actual terms/entitlement before use |
| 17-symbol coverage | **Not tested** | **Not tested** | No API calls or symbol lookup were performed |
| Total-return equivalence to BAA source | **Not validated** | **Not validated** | Requires fixed-sample comparison around dividend/split events |
| Runtime reliability | Formal API and explicit JSON fields, but request limits apply | Unofficial wrapper, changing defaults, observed rate-limit failures in project discussions/issues | Prefer AV for first controlled validation; do not rely on Yahoo as a silent fallback |

### Alpha Vantage — documented properties

Official documentation:

- API documentation: <https://www.alphavantage.co/documentation/>
- Support and request limits: <https://www.alphavantage.co/support/>

The official `TIME_SERIES_MONTHLY_ADJUSTED` description says the endpoint returns monthly observations dated at the last trading day of each month, including adjusted close and monthly dividend, with more than 25 years of monthly history in general. Alpha Vantage describes its stock time-series adjustments as reflecting splits and cash dividends.

Constraints:

1. **Request budget:** At 17 symbol-specific requests, a 25-request/day allowance would leave eight requests for retries, other instruments, or unrelated Orion work. The current plan's endpoint entitlement and actual quota must be verified before coding a provider run.
2. **Universe coverage:** Broad ETF support is documented, but none of the 17 symbols has been queried in this assessment. Do not assume all symbols resolve to the intended instrument or have sufficient history.
3. **Total-return semantics:** Split/dividend-adjusted close is a plausible proxy, not a certification that the vendor series exactly matches the original paper's total-return data. The exact methodology and historical revisions have not been independently reconciled.
4. **History length:** Individual ETF histories begin at their own inception/listing dates; the provider's general history-depth statement does not make a modern ETF available in the 1970s.
5. **Operational quality:** Freshness, revised observations, retry/backoff, cache persistence, and provider outages remain unapproved.

### Yahoo Finance via `yfinance` — documented properties

References:

- Yahoo Help, adjusted close: <https://in.help.yahoo.com/kb/adjusted-close-sln28256.html>
- Yahoo Help, historical-data download: <https://ca.help.yahoo.com/kb/SLN2311.html>
- `yfinance` documentation and disclaimer: <https://github.com/ranaroussi/yfinance>
- `yfinance.download()` implementation/documentation: <https://github.com/ranaroussi/yfinance/blob/main/yfinance/multi.py>

Yahoo's help page describes adjusted close as adjusted for applicable splits and dividend distributions. However, the Python wrapper is not affiliated with or endorsed by Yahoo and states that Yahoo's API is intended for personal use. The current `yfinance` download interface defaults `auto_adjust=True`, which adjusts OHLC and changes which fields are returned; reproducible code must explicitly pin the chosen behavior and package version. Historical-data CSV downloads from Yahoo's website are documented as a Gold feature, which is distinct from but relevant to the licensing/access review for programmatic use.

Constraints:

1. No symbol-by-symbol lookup or historical-data request was made for the 17 BAA symbols.
2. Monthly bar timestamps and month-end values must be compared with daily bars; simply resampling monthly data is not accepted without a defined convention.
3. `auto_adjust` must be explicit, and `yfinance` version/default changes must be pinned and tested.
4. Rate limiting, partial responses, adjustment delays, and wrapper/API changes need fail-closed tests.
5. Usage terms must be reviewed before automated or persistent use; do not assume the unofficial API is a supported production feed.

## Empirical Validation Status

**Not yet performed:** provider requests, symbol coverage, observation-date audit, cross-provider adjusted-price comparison, dividend/split event checks, or numerical total-return reconciliation. This assessment deliberately does not invent validation results.

When authorized credentials/access are available, use the same sample months and all 17 tickers for both sources. For each symbol:

1. Verify symbol identity, USD currency, inception date, and sufficient 13-month lookback.
2. Compare monthly timestamps with the last actual trading date in daily data; reject partial current-month bars.
3. Compare adjusted-price return ratios around at least one cash distribution event and, where available, a split event. Record tolerances and any vendor methodology differences.
4. Compare the full 13-month signal window, not only the latest price, because a historical adjustment revision can alter momentum rankings.
5. Record provider, retrieval timestamp, package/API version, raw response fingerprint, adjustment field, and validation result.
6. Do not combine providers within one signal window or fill gaps using another source.

## Existing Orion Integration

`src/data/alphavantage.py` already implements `AlphaVantageMonthlyAdjustedSource` and normalizes monthly adjusted-close observations into `MarketDataSet`. Its class-level universe is currently `VTI`, `VEU`, and `SGOV`, for ADM research. It has useful fail-closed response parsing and test coverage, but its hard-coded universe and workflow context make direct use for BAA incorrect.

The BAA builder in `src/orion/frameworks/moon/baa.py` validates the normalized dataset's required symbols, month coverage, USD currency, and numeric prices. It does not currently certify provider identity or the financial semantics of `adjusted_close`; those must be established before passing provider observations to the BAA calculator.

## Required Validation Before Provider Approval

1. Confirm the approved provider and its applicable usage/license terms.
2. Confirm all 17 BAA symbols resolve to the intended US-listed instruments; reject aliases or substitutions unless separately approved.
3. Fetch sample monthly records for multiple assets with different distribution patterns and verify date stamps are the final trading session of each month.
4. Compare adjusted-close return ratios with an independent, documented total-return reference around dividend and split events; record tolerances and known differences.
5. Check currency, missing months, duplicate monthly bars, history start dates, and provider corrections/revisions.
6. Test rate-limit, malformed response, partial batch, and network-failure behavior without accepting partial datasets.
7. Decide cache/re-fetch policy and define a fail-closed response to stale or incomplete data.
8. Run the BAA input builder and calculation against fixed, reviewed fixtures before any backtest or runtime wiring.

## Current Recommendation

1. Validate Alpha Vantage first as the primary candidate for a controlled research prototype because its official monthly-adjusted endpoint and timestamp semantics are documented.
2. Use Yahoo Finance only as an independent comparison series during validation, subject to access terms and explicit `yfinance` version/configuration.
3. Do not approve either provider until all 17 symbols have been checked and adjusted-price behavior has been tested against a documented reference around corporate actions.
4. Do not implement silent fallback. If the selected provider fails or a symbol is missing, suppress the new BAA signal and surface a data-quality failure until a separately approved policy says otherwise.

Until empirical validation is complete:

- no provider is certified as the BAA total-return source;
- Alpha Vantage is a preferred validation candidate only, not an approved provider;
- do not combine providers in one signal window;
- do not silently replace missing data or fall back from adjusted close to raw close;
- do not activate BAA, schedule it, or connect it to order execution.

## Monthly manual review operation

The quality gates and output contract are specified in `BAA_Monthly_Data_Quality_and_Report_Contract.md`. The offline validation runner now emits both `baa_price_validation_report.json` for machine review and `baa_price_validation_summary.md` for operator review. Automated PASS remains a screening result; month freshness, provider terms/entitlement, corporate-action adjustment semantics, and provider approval require explicit review.


BAA is intended to be run manually at the monthly evaluation point, not continuously. No scheduler or always-on collector is required. The monthly entrypoint `scripts/baa/run_baa_monthly_review.py` makes the workflow easy to invoke while remaining plan-only by default. Running it without an explicit live-fetch flag prints the plan only: it makes no network requests, reads no API key, and creates no output directories.

Plan-only preview (safe; no collection):

```bash
python scripts/baa/run_baa_monthly_review.py --run-month 2026-10
```

When YJ explicitly decides to perform that month's collection, the same command can be invoked with `--confirm-live-data-fetch`. The script then checks for `ORION_ALPHA_VANTAGE_API_KEY` in the local environment, collects the two providers into a month-specific directory, and runs the offline comparison. This is a manual command, not a scheduled job. The live path has not been executed in this project session. Existing files are not overwritten unless `--overwrite` is explicitly supplied. If collection fails partway through, no validation report is produced and any already collected raw exports must be treated as incomplete.

```bash
# Only when live collection for this month is explicitly approved
python scripts/baa/run_baa_monthly_review.py --run-month 2026-10 --confirm-live-data-fetch
```

Outputs are grouped under `./data/baa/monthly/YYYY-MM/`, with raw provider exports separated from the offline validation report. A successful data comparison is still only a screening result; it does not approve a provider, activate BAA, schedule future runs, or place orders. The default 17-symbol universe and 13-month minimum remain in force unless a documented decision changes them.

## Offline empirical comparison harness

The repository includes the offline normalizer `scripts/baa/normalize_provider_price_exports.py`, comparator `scripts/baa/compare_monthly_price_exports.py`, one-command offline runner `scripts/baa/run_baa_price_validation.py`, and opt-in local collector `scripts/baa/collect_provider_price_exports.py`. The normalizer and comparator never make network requests or read API keys. The collector is plan-only by default; it makes no network request and does not read the API key unless `--confirm-live-data-fetch` is supplied. No live collection has been performed as part of this change. The normalizer converts one-ticker Alpha Vantage or Yahoo Finance CSV exports to the comparator's common schema:

```bash
python scripts/baa/normalize_provider_price_exports.py --provider alpha_vantage --input ./exports/alpha_vantage --output av_normalized.csv --source alpha_vantage
python scripts/baa/normalize_provider_price_exports.py --provider yahoo_finance --input ./exports/yahoo_finance --output yf_normalized.csv --source yahoo_finance
python scripts/baa/compare_monthly_price_exports.py av_normalized.csv yf_normalized.csv --left-label alpha_vantage --right-label yahoo_finance --tolerance-pct 0.05 --json
```

For a complete local comparison, place one ticker per CSV in each provider directory and name each file `SYMBOL.csv` (or `SYMBOL_*.csv`). The one-command runner normalizes both directories, checks that the same month panel is present for every expected symbol, defaults to requiring at least 13 monthly observations, runs the comparison, and writes `baa_price_validation_report.json`. It is offline-only and never reads credentials. Example:

```bash
python scripts/baa/run_baa_price_validation.py --alpha-vantage-dir ./exports/alpha_vantage --yahoo-finance-dir ./exports/yahoo_finance --output-dir ./exports/baa_validation --minimum-months 13 --tolerance-pct 0.05
```

A `PASS` means only that the configured panel, date, currency, and price-screen checks passed; it is not provider approval or proof of total-return equivalence. A `FAIL` report should be reviewed rather than worked around by dropping assets or relaxing tolerances without a documented decision.

Place one ticker per CSV in each input directory and name each file `SYMBOL.csv` (or `SYMBOL_*.csv`). For a single file, pass `--symbol SPY`. Alpha Vantage exports must contain `timestamp` and `adjusted close`; Yahoo Finance exports must contain `Date` and `Adj Close` (or `Adjusted Close`). Daily Yahoo rows are reduced to the latest observed date in each calendar month. The normalizer rejects missing adjusted-price fields rather than falling back to raw `Close`, invalid prices, duplicate observation dates, and non-USD currency. It is an import adapter, not a downloader. The collector stores raw provider CSV files only; normalize and compare them in separate, explicit local commands.

### Optional local collector (not executed)

The collector supports a default 17-symbol BAA universe and writes raw per-symbol CSV files into a local directory. It uses the Alpha Vantage `TIME_SERIES_MONTHLY_ADJUSTED` endpoint for Alpha Vantage and Yahoo Finance daily chart observations for Yahoo Finance; daily adjusted-close values are exported so the offline normalizer can select the last observed date in each calendar month.

By default it is **plan-only** and does not read `ORION_ALPHA_VANTAGE_API_KEY`, create output files, or make network requests. Actual collection requires the explicit `--confirm-live-data-fetch` flag. For Alpha Vantage, configure `ORION_ALPHA_VANTAGE_API_KEY` in the local shell or secret manager; never paste it into source code or chat. The collector refuses to overwrite existing symbol files unless `--overwrite` is explicitly supplied. Alpha Vantage requests are spaced by 15 seconds by default, but account quotas and endpoint access must still be checked. Yahoo Finance access terms and endpoint stability remain an approval concern.

Plan-only example (safe; no network):

```bash
python scripts/baa/collect_provider_price_exports.py --provider alpha_vantage --output-dir ./exports/alpha_vantage
python scripts/baa/collect_provider_price_exports.py --provider yahoo_finance --output-dir ./exports/yahoo_finance
```

Only after a separate explicit approval, an operator can add `--confirm-live-data-fetch` to the chosen command. Then normalize and compare the raw exports using the offline commands above. Collection is not wired to Orion runtime, scheduling, BAA signal generation, or order execution. A failed/partial collection is not evidence that a provider is approved.

The common CSV schema is:

`source,symbol,month,observed_at,adjusted_close,currency`

- `month` is `YYYY-MM`; `observed_at` is the provider's actual observation date (`YYYY-MM-DD`) and must fall in that month.
- `adjusted_close` must be a finite, positive number; `currency` must be `USD`.
- Duplicate symbol/month observations, malformed rows, and non-USD observations are rejected.
- The default expected symbol set is the 17 distinct BAA-G12 tickers. Both files must cover those symbols and their observed month keys must match. The tool also flags observation-date differences and price differences above the configured tolerance.
- The default tolerance is 0.05% relative price difference. This is a screening threshold, not a claim that two providers' adjustment methods are economically equivalent. Any failure must be investigated, not automatically resolved by selecting one provider.

Example:

`python scripts/baa/compare_monthly_price_exports.py av_normalized.csv yf_normalized.csv --left-label alpha_vantage --right-label yahoo_finance --tolerance-pct 0.05 --json`

The normalizer and comparator are offline tools. No live provider data was downloaded. Empirical conclusions about ticker coverage, adjusted-price differences, dividend/split treatment, or historical revisions therefore remain pending.
