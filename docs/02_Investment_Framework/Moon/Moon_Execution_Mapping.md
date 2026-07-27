# Moon Execution Mapping

Version: 0.1

Status: Active

Last Updated: 2026-06-20

Related Decision:

D-012

---

# Purpose

This document defines the mapping between signal-generation assets and execution assets used within Moon.

Moon strategies preserve original research universes whenever possible.

Signal generation should use the original asset definitions.

Execution may use lower-cost equivalent ETFs.

---

# Principle

Signal generation should preserve the original research methodology whenver possible.

Execution may use alternative ETFs operational benefits exist.

Signal integrity has priority over execution convenience.


Signal Universe

Used for:

- Research validation
- Signal generation
- Backtesting
- Strategy comparison

---

Execution Universe

Used for:

- Real portfolio implementation
- Monthly rebalancing
- Cost optimization

---

# Asset Mapping

| Signal Asset | Execution Asset |
|-------------|------------------|
| SPY | SPYM |
| QQQ | QQQM |
| IWM | VTWO |
| EFA | VEA |
| EEM | VWO |
| AGG | BND |
| BIL | SGOV |
| SHY | SCHO |
| IEF | VGIT |
| TLT | VGLT |
| TIP | SCHP |
| LQD | VCIT |
| HYG | SPHY |
| BWX | BNDX |
| EMB | VWOB |
| GLD | GLDM |
| DBC | BCI |
| VNQ | USRT |
| SLV | SIVR |

---

Execution Selection Criteria

Execution ETF selection should prioritize:

1. Similar economic exposure
2. Lower expense ratio
3. Higher tax efficiency
4. Sufficient liquidity
5. Long-term survivability

Signal integrity has priority over execution convenience.

---

# Governance

New mappings require review and approval.

Changes must be recorded in:

docs/05_Decisions/Decision_Log.md

before implementation.

---

# Notes

Signal assets remain the canonical reference for strategy validation.

Execution assets may differ for:

- Lower expense ratios
- Better tax efficiency
- Operational simplicity

Signal integrity has priority over execution convenience.

Review Frequency:

Annual