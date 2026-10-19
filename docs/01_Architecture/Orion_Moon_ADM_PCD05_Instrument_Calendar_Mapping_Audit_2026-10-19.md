# Orion Moon / ADM PCD-05 — Instrument Calendar Mapping Audit

Date: 2026-10-19  
Status: Evidence audit only; no calendar policy or provider approved

## Scope

Review the configured ADM instruments `VTI`, `VEU`, and `SGOV` against public listing evidence to inform calendar-provider selection. This document does not select a calendar package, define production exchange identifiers, or connect a calendar to ADM.

## Findings

| Instrument | Role in ADM | Public listing evidence reviewed | Calendar implication |
|---|---|---|---|
| VTI | Relative-momentum risk asset | Vanguard product page identifies NYSE Arca as the ETF exchange; SEC summary prospectus also describes listing on NYSE Arca. | NYSE Arca listing venue is evidence, but the calendar package's code must be independently mapped and verified. |
| VEU | Relative-momentum risk asset | Vanguard product page identifies NYSE Arca as the ETF exchange. | Same caution: listing venue and provider calendar code are separate identifiers. |
| SGOV | Absolute-momentum comparison benchmark | iShares supplement dated 2026-01-16 says the primary listing changes from NYSE Arca to NYSE on or around 2026-02-23. | Historical listing venue changes; any instrument metadata should be time-aware if exact venue identity matters. |

## Public references

- VTI, Vanguard official product page: https://advisors.vanguard.com/investments/products/vti/vanguard-total-stock-market-etf
- VTI, SEC summary prospectus (2026-04-28): https://www.sec.gov/Archives/edgar/data/36405/000003640526000197/f44849d1.htm
- VEU, Vanguard official product page: https://advisors.vanguard.com/investments/products/veu/vanguard-ftse-all-world-ex-us-etf
- SGOV listing change, SEC-hosted supplement (2026-01-16): https://www.sec.gov/Archives/edgar/data/1100663/000119312526015356/d35944d497.htm

## Engineering conclusions (not governance decisions)

1. The three instruments are US-listed ETFs. A common US-equity session calendar is a plausible candidate for month-end session resolution, but is not yet an approved Orion policy.
2. Do not equate listing venue strings (`NYSE Arca`, `NYSE`) with a library's calendar identifiers without explicit provider documentation and tests.
3. Verify the chosen calendar's treatment of holidays, early closes, historical schedules, exceptional closures, and version changes before production use.
4. The data provider's monthly bar date and the calendar-derived evaluation cutoff are distinct facts. They must be reconciled by explicit validation; neither should silently overwrite the other.
5. Since ADM currently consumes monthly adjusted observations, a calendar package must not be treated as proof of provider data freshness or adjusted-price correctness.
6. No package was installed; no source code or ADM runtime was changed; no live market-data API call was made.

## Status and next step

PCD-05 and PCD-06 remain open. The v36 injected calendar interface remains a prototype and is not wired into ADM. Next, compare calendar package identifiers and historical-session behavior against the needs above, then document a recommendation before adding a dependency or integrating runtime behavior.

`config/moon.yaml` must continue to retain `active_strategies: []`. No governance gate is closed by this audit.
