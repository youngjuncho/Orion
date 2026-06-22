# Phoenix Dashboard Specification

Version: 0.1

Status: Draft

Last Updated: 2026-06-22

Depends On:

* Phoenix_Operating_Model.md
* Phoenix_Leader_Framework.md
* Phoenix_Scoring_Framework.md

---

# Purpose

The Phoenix Dashboard provides a consolidated view of digital asset category leadership.

The dashboard is designed to monitor:

* Category Leaders
* Challengers
* Leadership Trends
* Replacement Risk
* Portfolio Exposure

---

# Dashboard Philosophy

Phoenix monitors leadership.

Phoenix does not predict prices.

The dashboard focuses on ecosystem strength and leadership transitions.

---

# Dashboard Layout

Phoenix Dashboard

↓

Portfolio Summary

↓

Category Overview

↓

Leadership Monitoring

↓

Replacement Risk

↓

Review Alerts

---

# Section 1

Portfolio Summary

Displays:

* Number of Categories
* Number of Leaders
* Number of Challengers
* Portfolio Holdings

---

Example

Categories:

4

---

Leaders:

4

---

Portfolio Holdings:

* SOL
* LINK
* TAO
* ONDO

---

Portfolio State:

Healthy

---

# Section 2

Category Overview

Displays all approved categories.

Fields:

* Category
* Leader
* Challenger
* Leader Score
* Challenger Score
* State

---

Example

Smart Contract

Leader:

SOL

Score:

84

---

Challenger:

SUI

Score:

78

---

State:

Competitive

---

# Section 3

Leadership Monitoring

Displays:

* Current Leader
* Leadership Trend
* Previous Leader
* Leader Score Change

---

Leadership Trend States

Improving

Stable

Weakening

---

Example

AI Infrastructure

Leader:

TAO

Trend:

Improving

Score Change:

+7

---

# Section 4

Replacement Risk

Displays:

* Category
* Risk Score
* Risk State

---

Risk States

Dominant

Stable

Competitive

Transition

Disrupted

---

Example

Smart Contract

Risk:

72

State:

Transition

---

# Section 5

Review Alerts

Displays categories requiring review.

---

Review Conditions

Replacement Risk:

60+

---

Leader Score Decline:

10+

---

Leadership Transition Candidate:

Detected

---

Example

Review Required

Smart Contract

Leader:

SOL

Challenger:

SUI

Replacement Risk:

72

---

# Dashboard Health Score

Phoenix generates an overall health score.

Range:

0-100

---

Interpretation

80-100

Healthy

---

60-79

Stable

---

40-59

Competitive

---

20-39

Transition

---

0-19

Disrupted

---

Status:

Experimental

---

# Monthly Output Example

Month:

2026-06

---

Portfolio State:

Healthy

Score:

82

---

Approved Leaders

* SOL
* LINK
* TAO
* ONDO

---

Review Alerts

1

---

Category Requiring Review

Smart Contract

Leader:

SOL

Challenger:

SUI

Risk:

72

State:

Transition

---

# CLI Output

Command

orion phoenix status

---

Example

PHOENIX

Portfolio State: Healthy

Leaders: 4

Review Alerts: 1

Highest Risk Category:

Smart Contract

Leader: SOL

Challenger: SUI

Risk: 72

---

# Dashboard Update Frequency

Leadership Review

Monthly

---

Dashboard Refresh

Monthly

---

# Logging Requirements

Each dashboard update must store:

* Date
* Leader
* Challenger
* Leader Score
* Challenger Score
* Replacement Risk
* State

---

# Governance

Dashboard changes require:

Decision_Log.md entry

before implementation.

---

# Open Issues

OI-801

Final dashboard health score methodology.

Status:

Open

---

OI-802

Visualization design.

Status:

Open

---

OI-803

Historical dashboard retention.

Status:

Open

---

# Next Document

Phoenix_Change_Log.md

Purpose:

Record historical leadership changes, category evolution, and replacement risk events.
