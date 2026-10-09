# Orion Framework Data Contracts

Version: 1.0  
Status: Contract Review Baseline  
Last Updated: 2026-10-09

## Purpose

This document separates the shared transport contract from framework-specific
field semantics. It is a boundary specification, not approval of any new
investment indicator, scoring rule, data source, or collection schedule.

## Shared canonical envelope

Every normalized observation uses the existing `MarketDataPoint` contract:

| Property | Meaning | Current rule |
|---|---|---|
| `symbol` | Source-independent identity string for the observed entity | Required non-empty string; canonical cross-provider identity rules remain open |
| `field` | Name of the observed attribute | Required non-empty string; semantic registry is defined incrementally below |
| `observed_at` | Time associated with the observation | Required non-empty string; timestamp format, timezone, and effective-time semantics remain open |
| `value` | Scalar observation | `float`, `int`, `str`, or `None`; booleans and non-finite floats are rejected |
| `source` | Source/provider identifier | Required non-empty string; source precedence is not defined |
| `currency` | Currency context where relevant | Optional non-empty string; ISO-code enforcement is not yet part of the contract |
| `metadata` | Source-specific context that does not belong in the shared envelope | String-to-string mapping, copied and made read-only |

`MarketDataSet.as_of` identifies the batch's declared reference time. It is
currently only required to be a non-empty string; it must not be interpreted
as a validated UTC timestamp until a timestamp policy is approved.

The current duplicate key is `(symbol, field, observed_at)`. This is a
structural duplicate check, not a source-priority rule. If two providers
report the same key, the current contract rejects the duplicate rather than
silently choosing a provider.

## Field naming convention

Field names are lowercase `snake_case`. A field name identifies the meaning
of the value, not the provider's raw column name. Provider-specific column
names belong in an adapter and must be mapped explicitly; no implicit aliases
or unit conversions are assumed.

### Candidate market-price vocabulary

The following names are the proposed shared vocabulary for price-like
observations. They become production-semantic fields only when the applicable
source/framework contract specifies units, adjustment semantics, and
validation rules.

| Field | Intended meaning | Boundary / unresolved detail |
|---|---|---|
| `open` | Unadjusted period opening price | Period, venue, and currency must come from the source contract |
| `high` | Unadjusted period high price | Same as above |
| `low` | Unadjusted period low price | Same as above |
| `close` | Unadjusted period closing price | Must not be treated as total return |
| `adjusted_close` | Provider-adjusted closing-price series | Adjustment methodology is provider-specific; the name alone does not guarantee a universal total-return series |
| `volume` | Reported traded volume for the source's period | Units and aggregation interval must be declared by the adapter |

D-028 specifically requires Moon ADM to use the data layer's approved
adjusted-price series for total-return measurement and not to calculate
cash distributions independently inside ADM. This does not establish that
all providers' `adjusted_close` fields are interchangeable. Before production
use, the selected source adapter must document its adjustment methodology
and compatibility with D-028.

No `dividend`, `total_return`, or FX-converted field is inferred or generated
by this contract review.

Moon ADM’s current precomputed-input boundary and minimum source-adapter requirements are detailed in `Moon_ADM_Data_Contract.md` and `Moon_ADM_Data_Readiness_and_Closure.md`. That document records existing requirements without approving a production provider or filling unresolved policy gaps.

## Framework data contract matrix

| Framework | Data domain | Shared-envelope use | Framework-specific semantic contract still required |
|---|---|---|---|
| Aurora | Market and environment monitoring | Macro/market observations identified by explicit `symbol` and `field` | Approved indicator set, formulas, units, observation frequency, release/revision handling, freshness and missing-data behavior |
| Moon | Dynamic asset allocation | Price/return observations and strategy inputs | Strategy-specific history window, trading calendar, adjusted-price source semantics under D-028, missing bars, corporate actions and source precedence |
| Orbit | Static asset allocation | Primarily configuration and portfolio-target inputs; market observations only where an approved function needs them | Do not add a market-data dependency merely to mirror Moon; identify any concrete data consumer first |
| Supernova | Individual-equity satellite | Company/fundamental/review observations where an approved rule consumes them | Approved source contract, reporting-period semantics, units, restatements, freshness and reproducible scoring/replacement inputs |
| Phoenix | Digital-asset satellite | Market, category, on-chain or ecosystem observations where approved rules consume them | Approved category/leader rules, source contract, chain/entity identity, observation windows, freshness and reproducible scoring/replacement inputs |

The matrix does not authorize the implementation to invent the still-open
framework methodology. In particular, source candidates listed in
`Orion_Data_Pipeline.md` are not approved production integrations by virtue
of appearing there.

## Normalization and validation responsibilities

The shared data layer may:

- trim required textual envelope fields;
- validate supported scalar types and finite numeric values;
- freeze metadata and reject duplicate observation identities;
- map a provider's raw field into a canonical field only through an explicit adapter mapping.

The shared data layer must not silently:

- infer entity identity or map ticker/symbol aliases across providers;
- convert currencies or units without a declared rule;
- infer timestamp timezone, trading calendar, or bar interval;
- select a winning source when sources disagree;
- fill missing observations, forward-fill values, or decide freshness without a framework/source policy;
- turn an observation into a score, signal, decision, or portfolio action.

## Required closure before production collectors

For each framework/source pair, document the following before implementing a
production collector:

1. entity identity and symbol mapping;
2. field names, units, and value semantics;
3. timestamp format, timezone, effective time, and period/calendar convention;
4. missing, duplicate, stale, revised, and conflicting-source behavior;
5. source precedence and source-failure behavior;
6. any approved transformation, including adjusted-price methodology;
7. deterministic fixtures and validation tests.

Until those items are closed, the existing source-agnostic normalization and
structural validation remain the supported MVP boundary. No external API,
network dependency, scoring logic, or investment rule is introduced by this
document.


Moon ADM implementation boundary: `docs/01_Architecture/Moon_ADM_Data_Implementation_Boundary.md`.
