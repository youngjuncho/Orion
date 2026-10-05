# Supernova Scoring Framework

Version: 2.0

Status: Approved

Last Updated: 2026-10-05

Depends On:

* Supernova_Research.md
* Supernova_Watchlist_Framework.md

---

# Purpose

This framework evaluates whether approved companies continue to deserve ownership.

The objective is not to predict short-term price performance.

The objective is to monitor long-term leadership durability.

---

# Scoring Range

0-100

---

# Evaluation Architecture

Supernova separates Theme Evaluation from Company Evaluation. Theme Health is not mathematically combined with Company Score. Company Score is a governance assessment and is not a purchase-timing signal.

Company evaluation follows:

```text
Evidence
    ↓
Assessment
    ↓
5 Scoring Dimensions
    ↓
Company Score
    ↓
Portfolio State / Leadership Role
```

Each reviewed dimension should retain:

* Score
* Evidence
* Assessment
* Review Date

Scores are judgment-assisted by evidence and qualitative anchors. Raw metrics may inform an assessment but do not mechanically determine the score unless a separate rule is explicitly approved.

---

# Scoring Components

## Theme Exposure

Weight:

20%

Question:

How strongly is the company exposed to one or more approved 5D themes?

Assessment should consider directness, structural relevance, and evidence quality. Multi-theme membership does not create an automatic score bonus.

---

## Competitive Moat

Weight:

25%

Question:

How durable is the company's competitive advantage?

---

## Leadership Position

Weight:

25%

Question:

Does the company remain the leader within its category?

---

## Growth Quality

Weight:

15%

Question:

Is long-term growth still intact?

---

## Execution Quality

Weight:

15%

Question:

Is management executing effectively?

---

# Qualitative Anchors

Each dimension uses qualitative anchors appropriate to its maximum contribution. Exact metric-to-score formulas are intentionally not prescribed in v1.

General anchor pattern:

* Exceptional: clearly superior and durable evidence
* Strong: materially above peers with durable evidence
* Moderate: credible but mixed or less durable evidence
* Weak: limited, deteriorating, or uncertain evidence
* Critical: thesis-level deficiency or disproof

The assigned numeric score must be supported by the recorded Evidence and Assessment.

---

# Company Score Aggregation

Company Score is calculated only when all five approved scoring dimensions have a reviewed score. The v1 weights are fixed at:

| Dimension | Weight |
|---|---:|
| Theme Exposure | 20% |
| Competitive Moat | 25% |
| Leadership Position | 25% |
| Growth Quality | 15% |
| Execution Quality | 15% |

The Company Score is the weighted sum of the five 0-100 dimension scores:

```text
Company Score
= Theme Exposure × 0.20
+ Competitive Moat × 0.25
+ Leadership Position × 0.25
+ Growth Quality × 0.15
+ Execution Quality × 0.15
```

The resulting value is rounded to the nearest integer using conventional half-up rounding and remains in the 0-100 range.

## Missing or Invalid Dimensions

* All five dimensions are required for a Company Score.
* Missing dimensions are not imputed.
* Missing dimensions are not compensated by reweighting the remaining dimensions.
* Unsupported dimensions invalidate the aggregation.
* Duplicate dimensions within one Research Record are invalid.
* Dimension reviews must belong to the same company and review date as the Research Record.

A Research Record that fails these conditions cannot produce a Company Score and must return to the research stage.

## Governance Boundary

The aggregate Company Score is an input to governance review. It does not automatically assign Portfolio State, Leadership Role, Replacement Risk, or a buy/sell action.

Governance records the resulting decision explicitly. v1 does not define numeric score thresholds for Leader, Challenger, Approved, Review Required, Replace, or Retire. These outcomes require documented evidence, rationale, and governance approval.

# Score Bands

90-100 Exceptional

80-89 Strong

70-79 Healthy

60-69 Stable

50-59 Neutral

40-49 Weak

30-39 Danger

0-29 Critical

---

# Replacement Risk

Replacement Risk is an independent governance assessment of the likelihood that an
Approved Company will no longer deserve its place in the Supernova portfolio and
may need to be replaced or retired at a future governance review.

Replacement Risk is **not** a measure of short-term price risk, valuation risk, or
market volatility. It is also not a direct function of Company Score.

A challenger is **not required** for Replacement Risk to increase. A company may
reach High or Critical risk because its own moat, leadership, execution, growth
trajectory, or investment thesis has materially deteriorated even when no clear
replacement candidate exists. Conversely, the emergence of a strong challenger
does not by itself imply high replacement risk if the Approved Company's
leadership and thesis remain durable.

## Replacement Risk Assessment Axes

The assessment should consider four evidence-based axes:

* **Leadership Threat** — Is the company's category leadership being materially
  challenged?
* **Moat Deterioration** — Is the durability or defensibility of its competitive
  advantage weakening?
* **Growth / Execution Deterioration** — Is long-term growth quality or execution
  materially deteriorating?
* **Thesis Integrity** — Does the original long-term investment thesis remain valid?

These axes are assessment lenses, not mechanically weighted sub-scores. The final
Replacement Risk level remains a governance judgment supported by Evidence and
Assessment.

## Risk Levels

| Level | Governance meaning |
|---|---|
| **Very Low** | Leadership, moat, execution, growth, and thesis remain strongly intact. No material replacement evidence. |
| **Low** | Some competitive or operating concerns exist, but the long-term thesis and leadership remain durable. |
| **Medium** | Material warning signals are accumulating. Continued monitoring or a focused review is warranted. |
| **High** | One or more core elements of leadership, moat, growth, execution, or thesis have materially weakened. Replacement or retirement is a realistic governance consideration. |
| **Critical** | The investment thesis or structural leadership position is substantially broken. A governance decision to Replace or Retire is warranted unless compelling evidence supports continuation. |

Replacement Risk escalation is a **review trigger, not an automatic trade trigger**.
The final action is determined separately through Governance Decision.

---

# Interpretation

Score bands inform research priority and governance assessment. They do not automatically assign Portfolio State or Leadership Role.

The governance distinction is:

```text
Portfolio State
* Approved
* Watchlist
* Review Required
* Retired

Leadership Role
* Leader
* Challenger
* Candidate
```

A score may support a state or leadership decision, but a governance review is required for the transition.

---

# Evidence Contract

A Company Score review should preserve the following minimum record:

```text
Entity
Dimension
Score
Evidence
Assessment
Review Date
```

Evidence provenance should be retained where practical. Primary company filings and official disclosures should be preferred for material claims, supplemented by reliable secondary or analytical sources when necessary.

Historical assessments should remain traceable across review cycles.

---

# Review Frequency

Company Review:

Monthly

Theme Review:

Quarterly

Framework Review:

Annually
