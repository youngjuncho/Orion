# Aurora Dashboard Specification

Version: 0.1

Status: Draft

Last Updated: 2026-06-21

Depends On:

* Aurora_Research.md
* Aurora_Operating_Model.md
* Aurora_Regime_Framework.md
* Aurora_Scoring_Framework.md
* Aurora_Indicator_Catalog.md

---

# Purpose

This document defines the user-facing dashboard output of Aurora.

Aurora exists to provide a one-minute understanding of the current market climate.

The dashboard prioritizes clarity over complexity.

---

# Primary Objective

Aurora answers:

"What environment are we investing in right now?"

---

# Dashboard Layout

Aurora consists of four sections:

1. Market Regime
2. State Momentum
3. Core Components
4. Cross Asset Signals

---

# Section 1

Market Regime

Display:

```text
Aurora Score: 78

Regime:

RISK ON
```

---

Possible Values:

* Risk On
* Neutral
* Risk Off

---

# Section 2

State Momentum

Display:

```text
State Momentum:

Improving
```

---

Possible Values:

* Improving
* Stable
* Deteriorating

---

Interpretation:

State Momentum measures the direction of market conditions rather than the current regime.

---

# Section 3

Core Components

Display:

```text
Trend:       82
Liquidity:   74
Credit:      79
Volatility:  71
```

---

Purpose:

Show which components are driving the overall Aurora score.

---

# Section 4

Cross Asset Signals

Display:

```text
Dollar:     Weak
Gold:       Neutral
Oil:        Strong
Bitcoin:    Strong
```

---

Purpose:

Provide environmental confirmation.

Cross Asset signals do not determine regime classification.

---

# Transition Monitoring

Aurora highlights potential regime changes.

---

## Bull To Bear Watch

Condition:

Regime:

Risk On

State Momentum:

Deteriorating

Display:

```text
Transition Risk:

Bull → Bear Watch
```

---

## Bear To Bull Watch

Condition:

Regime:

Risk Off

State Momentum:

Improving

Display:

```text
Transition Opportunity:

Bear → Bull Watch
```

---

# Daily Dashboard Example

```text
Aurora

Aurora Score: 76

Regime:
RISK ON

State Momentum:
Improving

Core Components

Trend:       82
Liquidity:   73
Credit:      77
Volatility:  70

Cross Asset

Dollar:      Weak
Gold:        Neutral
Oil:         Strong
Bitcoin:     Strong

Assessment:

Supportive environment.
Conditions continue to improve.
```

---

# CLI Output

Command

aurora

Example

```text
Aurora Score: 76

Regime: Risk On

Momentum: Improving

Trend: 82
Liquidity: 73
Credit: 77
Volatility: 70

Transition Signal:
None
```

---

# Future Dashboard Features

Potential Additions:

* Regime History
* Regime Duration
* Trend Charts
* Liquidity Charts
* Alert System
* Weekly Summary

Status:

Research Only

Not Approved

---

# Related Documents

* Aurora_Research.md
* Aurora_Operating_Model.md
* Aurora_Regime_Framework.md
* Aurora_Scoring_Framework.md
* Aurora_Indicator_Catalog.md
