# Aurora Operating Model

Version: 1.0

Status: Draft

Last Updated: 2026-07-26

Depends On:

* Aurora_Research.md
* Aurora_Regime_Framework.md
* Aurora_Scoring_Framework.md

---

# Purpose

This document defines how Aurora converts market observations into market climate assessments.

Aurora is the environmental intelligence layer of Orion OS.

Aurora does not generate investment recommendations.

Aurora provides context.

---

# Core Objective

Aurora seeks to identify:

* Current Market Regime
* Regime Direction
* Cross Asset Confirmation

Aurora answers:

"What environment are we investing in?"

---

# Operating Philosophy

## Observe More, Predict Less

Aurora measures observable conditions.

Aurora does not forecast prices.

---

## State Over News

Aurora evaluates market structure rather than headlines.

---

## Transition Awareness

The most important market events often occur during regime transitions.

Aurora therefore evaluates:

* Current State
* State Momentum

---

# Aurora Architecture

Aurora consists of two layers.

```text
Aurora

├─ Core Layer
└─ Cross Asset Layer
```

---

# Core Layer

The Core Layer determines the primary market regime.

The Core Layer uses the following components:

* Trend
* Liquidity
* Volatility
* Credit

These components are scored and combined through the Aurora scoring framework.

---

## Trend

Purpose:

Measure market direction.

Examples:

* SPY Trend
* QQQ Trend
* Market Breadth

---

## Liquidity

Purpose:

Measure financial system liquidity.

Examples:

* Federal Reserve Balance Sheet
* M2 Growth
* Financial Conditions Index

---

## Volatility

Purpose:

Measure market stress.

Examples:

* VIX
* MOVE Index

---

## Credit

Purpose:

Measure risk appetite.

Examples:

* HYG
* Credit Spreads
* Corporate Bond Strength

---

# Cross Asset Layer

The Cross Asset Layer provides environmental confirmation.

Cross Asset indicators do not determine the regime directly.

Cross Asset indicators do not contribute directly to Aurora Score.

They provide additional context for interpretation.

---

## Dollar

Purpose:

Monitor global liquidity conditions.

---

## Gold

Purpose:

Monitor defensive demand.

---

## Oil

Purpose:

Monitor growth and inflation pressures.

---

## Bitcoin

Purpose:

Monitor speculative and liquidity-sensitive behavior.

---

# Regime Framework

Aurora evaluates three primary regimes.

The regime is derived from the Aurora Score mapping defined in Aurora_Regime_Framework.md.

---

## Risk On

Characteristics:

* Positive Trend
* Healthy Liquidity
* Lower Stress
* Healthy Credit

Typical Environment:

Economic expansion

---

## Neutral

Characteristics:

* Mixed Signals
* Uncertain Direction
* Transition Risk

Typical Environment:

Market consolidation

---

## Risk Off

Characteristics:

* Weak Trend
* Liquidity Deterioration
* Elevated Volatility
* Weak Credit

Typical Environment:

Defensive conditions

---

# State Momentum

Aurora evaluates whether conditions are improving or deteriorating.

State Momentum is independent of Market Regime.

State Momentum describes the direction of change in the Aurora Score over time.

---

## Improving

Conditions are becoming stronger.

Examples:

* Liquidity improving
* Credit improving
* Volatility declining

---

## Stable

No significant directional change.

---

## Deteriorating

Conditions are weakening.

Examples:

* Liquidity contracting
* Credit weakening
* Volatility rising

---

# Example Outputs

## Example 1

Regime:

Risk On

State Momentum:

Stable

Interpretation:

Strong environment with no major change.

---

## Example 2

Regime:

Risk On

State Momentum:

Deteriorating

Interpretation:

Strong environment but conditions are weakening.

Potential transition risk exists.

---

## Example 3

Regime:

Risk Off

State Momentum:

Improving

Interpretation:

Conditions remain weak but internal recovery may be beginning.

Potential transition opportunity exists.

---

# Relationship With Moon

Moon determines allocation.

Aurora determines context.

Aurora never overrides Moon signals.

Moon is the ETF Portfolio Engine.

---

# Relationship With Supernova

Aurora may provide environmental context for long-term equity accumulation.

Aurora does not determine Supernova purchases.

---

# Relationship With Phoenix

Aurora may provide macro context for digital assets.

Aurora does not determine Phoenix allocations.

---

# Candidate Future Enhancements

Potential future additions:

* Global Liquidity Score
* Economic Surprise Index
* Yield Curve Analysis
* Stablecoin Flow Monitoring
* On-Chain Liquidity Indicators

Status:

Research Only

Not Approved

---

# Related Documents

* Aurora_Research.md
* Aurora_Regime_Framework.md
* Aurora_Scoring_Framework.md
* Orion_IPS.md
