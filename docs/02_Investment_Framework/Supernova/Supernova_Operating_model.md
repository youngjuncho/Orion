# Supernova Operating Model

## Purpose

This document describes the operational model of Supernova within Orion OS.

Supernova is Orion's long-term equity accumulation framework.

Unlike Moon, which focuses on tactical asset allocation through ETFs, Supernova focuses on owning dominant companies benefiting from long-term structural trends.

---

# Objective

Supernova exists to answer a single question:

"Which companies are most likely to dominate the future?"

The objective is long-term capital appreciation through ownership of category-leading businesses.

---

# Investment Universe

Supernova invests exclusively in individual equities.

ETFs are not used.

Cryptocurrencies are not used.

---

# Framework

Supernova is based on the Orion 5D Megatrend Framework.

The five themes are:

* Decoupling
* Deglobalization
* Demographics
* Decarbonization
* Digital Transformation

Every approved company must have meaningful exposure to at least one theme.

---

# Company Selection Criteria

Companies should satisfy most of the following conditions:

1. Direct exposure to one or more 5D themes
2. Strong competitive position
3. Durable economic moat
4. Long-term earnings growth potential
5. Strategic relevance within future economic infrastructure

---

# Portfolio Construction

Approved companies are the portfolio-eligible universe. Candidate and Watchlist companies are research states and are not eligible for accumulation.

The target weight is equal weight across the current Approved Company set:

```text
Target Weight = 1 / N
```

Supernova does not impose a hard maximum Approved Company count in v1. The current five approved companies remain the current portfolio state, not a hard cap. A future capacity decision must be explicitly recorded in the Decision Log before additional Approved Companies are added beyond the current governance intent.

---

# Investment Method

Investment Method:

Dollar Cost Averaging (DCA)

Frequency:

Monthly

Capital is invested regardless of short-term market conditions. Monthly contributions are allocated preferentially toward underweight Approved Companies to move the portfolio toward equal-weight targets (Smart DCA).

Conceptually:

```text
Deficit_i = max(Target Weight_i - Current Weight_i, 0)

DCA Allocation_i
= Deficit_i / Sum(Deficit) ¡¿ Monthly DCA
```

The Company Score does not determine purchase timing or DCA allocation.

---

# Holding Policy

Temporary price declines are not considered a reason to sell.

Market volatility is not considered a reason to sell.

Valuation fluctuations are not considered a reason to sell.

The default assumption is long-term ownership.

---

# Replacement Policy

Replacement follows three separate stages:

1. Research / Detection
2. Governance Decision
3. Portfolio Transition

A challenger becoming stronger is a review trigger, not an automatic trade trigger. Score alone cannot automatically replace an Approved Company.

A normal replacement is executed at the next regular review cycle after governance approval. An Emergency Review may be used for clear structural thesis failure.

Replacement and Retirement are distinct:

* Replacement: Approved Company A is replaced by Approved Company B.
* Retirement / Exit: Approved Company A is removed without requiring a replacement.

Price movement alone does not trigger replacement.

Replacement decisions must be documented in the Decision Log before implementation.

---

# Relationship With Other Frameworks

Moon:

ETF Tactical Allocation

Supernova:

Long-Term Equity Accumulation

Phoenix:

Digital Asset Exposure

Aurora:

Market Climate Monitoring

Supernova operates independently of Moon allocation decisions.

---

# Governance State Model

Supernova uses two independent dimensions:

```text
Portfolio State
    Approved
    Watchlist
    Review Required
    Retired

Leadership Role
    Leader
    Challenger
    Candidate
```

Only Approved companies are portfolio eligible. Leadership Role is not equivalent to Portfolio State.

---

# Governance

Changes to:

* 5D definitions
* Approved company lists
* Selection criteria
* Replacement rules

must be recorded in:

docs/05_Decisions/Decision_Log.md

before implementation.

---

# Status

Status:

Production

Version:

Supernova Production v1
