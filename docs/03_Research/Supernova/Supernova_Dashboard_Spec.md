# Supernova Dashboard Specification

Version: 1.2

Status: Draft

Last Updated: 2026-10-05

---

# Purpose

The Supernova Dashboard monitors the health and leadership status of approved companies.

The dashboard is designed for long-term ownership monitoring rather than short-term trading.

---

# Dashboard Layout

## Portfolio Summary

Display:

* Approved Company Count
* Average Score
* Theme Coverage
* Replacement Risk Summary

---

## Approved Companies

For each company display:

Ticker

Theme

Score

Leadership Status

Replacement Risk

Trend

---

Illustrative example only. Example values are not approved company review results.

```text
Company: <Ticker>
Theme: <Theme>
Score: <Reviewed Score>
Leadership Status: <Role>
Replacement Risk: <Reviewed Risk>
Trend: <Trend>
```

---

## Theme Health

Display:

Theme

Leader

Challenger

Theme Score

Trend

---

Illustrative example only. Theme and company values must come from reviewed records.

```text
Theme: <Theme>
Leader: <Leader>
Challenger: <Challenger when applicable>
Theme Score: <Reviewed Theme Assessment>
Trend: <Trend>
```

---

## Replacement Risk Monitor

Display:

Company

Risk Level

Primary Risk Driver

Reason / Evidence Summary

Review Status

The monitor reflects a governance assessment, not a price-risk indicator.
Replacement Risk is independent of Company Score and may escalate without a
challenger being present.

---

Illustrative example only. Replacement Risk values must come from a reviewed Governance Record.

```text
Company: <Ticker>
Replacement Risk: <Risk Level>
Primary Risk Driver: <Driver>
Reason / Evidence Summary: <Summary>
Review Status: <Status>
```

---

## Review Queue

Display companies requiring additional review.

States:

* Watch
* Review
* Replacement Candidate

---

# Color Bands

90-100 Exceptional

80-89 Strong

70-79 Healthy

60-69 Stable

50-59 Neutral

40-49 Weak

30-39 Danger

0-29 Critical
