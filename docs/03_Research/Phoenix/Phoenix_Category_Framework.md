# Phoenix Category Framework

Version: 0.2

Status: Draft

Last Updated: 2026-10-05

Depends On:

* Phoenix_Research.md
* D-021
* D-022

---

# Purpose

This document defines the category structure used by Phoenix.

Phoenix evaluates digital assets at the category level before evaluating individual projects.

Principle:

Category First

Leader Second

---

# Design Philosophy

Digital assets compete within ecosystems.

Individual projects should be evaluated relative to peers operating within the same category.

Phoenix therefore evaluates:

Category

↓

Leader

↓

Challenger

↓

Replacement Risk

Phoenix invests only in approved category leaders.

Reference:

D-022

---

# Category Structure

## Category 1

Store of Value

Purpose:

Digital monetary asset.

Primary Functions:

* Wealth preservation
* Monetary settlement
* Reserve asset

Representative Asset:

* BTC

Status:

Reference Only

Production Eligible:

No

Notes:

Store of Value assets are monitored for ecosystem awareness but are outside Phoenix portfolio construction.

Phoenix does not allocate capital to Store of Value assets.

BTC is monitored for ecosystem awareness only.

Reference:

D-021

---

## Category 2

Smart Contract Platforms

Purpose:

General-purpose blockchain infrastructure.

Primary Functions:

* Application execution
* Asset issuance
* Smart contracts

Current Leader:

* SOL

Primary Challenger:

* SUI

Watchlist:

* APT
* SEI

Core Asset (Outside Phoenix):

* ETH

Status:

Competitive

Production Eligible:

Yes

Reference:

D-021

---

## Category 3

Oracle Networks

Purpose:

Provide external data to blockchain systems.

Primary Functions:

* Price feeds
* Off-chain data
* Cross-chain communication

Current Leader:

* LINK

Primary Challenger:

* API3

Watchlist:

* SUPRA

Status:

Established

Production Eligible:

Yes

---

## Category 4

Decentralized Finance

Purpose:

Financial infrastructure without intermediaries.

Primary Functions:

* Lending
* Borrowing
* Trading
* Yield generation

Current Leader:

* AAVE

Primary Challenger:

* MKR

Watchlist:

* MORPHO

Status:

Research

Production Eligible:

No

---

## Category 5

Real World Assets

Purpose:

Connect real-world assets to blockchain systems.

Primary Functions:

* Tokenization
* Treasury products
* Credit markets

Current Leader:

* ONDO

Primary Challenger:

* PENDLE

Watchlist:

* MPL

Status:

Emerging

Production Eligible:

Yes

---

## Category 6

AI Infrastructure

Purpose:

Provide infrastructure for decentralized AI systems.

Primary Functions:

* Compute
* Model training
* AI marketplaces

Current Leader:

* TAO

Primary Challenger:

* RENDER

Watchlist:

* AKT

Status:

Emerging

Production Eligible:

Yes

---

## Category 7

Data Availability

Purpose:

Provide scalable blockchain data storage.

Primary Functions:

* Rollup support
* Data publishing
* Scalability infrastructure

Current Leader:

* TIA

Primary Challenger:

* AVAIL

Watchlist:

None

Status:

Emerging

Production Eligible:

Yes

---

## Category 8

DePIN

Decentralized Physical Infrastructure Networks

Purpose:

Physical infrastructure coordination.

Primary Functions:

* Wireless networks
* Compute networks
* Storage networks

Current Leader:

* RENDER

Primary Challenger:

* HNT

Watchlist:

* AKT

Status:

Emerging

Production Eligible:

No

---

## Category 9

Exchange Ecosystems

Purpose:

Blockchain ecosystems centered around exchanges.

Primary Functions:

* Trading
* Settlement
* Liquidity provision

Current Leader:

* BNB

Primary Challenger:

None

Watchlist:

None

Status:

Established

Production Eligible:

No

---

## Category 10

Payments

Purpose:

Blockchain payment infrastructure.

Primary Functions:

* Settlement
* Transfers
* Cross-border payments

Current Leader:

* XRP

Primary Challenger:

None

Watchlist:

None

Status:

Research

Production Eligible:

No

---

# Leadership States

Each category tracks:

* Leader
* Primary Challenger
* Replacement Risk
* Leadership Trend

Leadership States are defined in:

Phoenix_Operating_Model.md

States:

* Dominant
* Stable
* Competitive
* Transition
* Disrupted

---

# Portfolio Eligibility

Production eligibility is a separate dimension from Category Status.

`Status` describes the category's ecosystem/research condition. `Production Eligible` determines whether the category participates in Phoenix portfolio construction.

Only approved category leaders from Production Eligible categories are eligible for portfolio inclusion.

Primary challengers and watchlist assets are monitored but are not eligible for portfolio inclusion.

Reference:

D-022

---

# Multi-Category Rule

An asset may belong to multiple categories and may have different roles in each category.

Example:

RENDER
  DePIN → Leader
  AI Infrastructure → Challenger

Category roles are evaluated independently.

Portfolio construction operates on unique assets: the same asset may appear only once in the Phoenix portfolio even if it has roles in multiple categories.

# Governance Rules

New categories may be added only when:

* The category demonstrates long-term relevance
* Multiple competing projects exist
* Reliable data sources are available

Changes must be recorded in:

Decision_Log.md

before implementation.

---

# Known Open Issues

OI-401

Final category list approval.

Status:

Closed

Resolution:

Phoenix production construction is currently limited to Smart Contract Platforms, Oracle Networks, Real World Assets, AI Infrastructure, and Data Availability.

---

OI-402

Projects belonging to multiple categories.

Examples:

* RENDER
* LINK

Status:

Closed

Resolution:

Multi-category membership is allowed. Roles are evaluated independently by category, while portfolio construction operates on unique assets.

---

OI-403

Category scoring methodology.

Status:

Open

Resolution:

Scoring methodology is governed by Phoenix_Scoring_Framework.md; quantitative automation remains an open implementation question.

---

OI-404

Should operational category mapping be separated from Category Framework?

Status:

Deferred

---

# Next Document

Phoenix_Operating_Model.md

Purpose:

Define how Phoenix evaluates categories, leaders, challengers, replacement risk, and portfolio eligibility.
