# Phoenix Approved Leaders v1

Version: 1.0

Status: Draft Registry

Last Updated: 2026-10-05

## Purpose

This document is the canonical registry of Phoenix category leadership decisions.

It records the current portfolio-eligible leadership state separately from the methodology used to evaluate leaders and from runtime configuration.

This registry does not define leader-selection methodology or scoring rules.

## Governance Boundary

```text
Phoenix_Category_Framework
        ↓
Phoenix_Leader_Framework
        ↓
Phoenix_Scoring_Framework
        ↓
Leadership Decision
        ↓
Phoenix_Approved_Leaders_v1
        ↓
config/phoenix.yaml
        ↓
Phoenix Portfolio
```

Configuration values must not be treated as approval evidence by themselves.

## Production Categories

Phoenix production construction currently covers five categories:

1. Smart Contract Platforms
2. Oracle Networks
3. Real World Assets
4. AI Infrastructure
5. Data Availability

Store of Value remains outside Phoenix under D-021. Other documented categories are not production eligible at this time.

## Current Leadership Registry

| Category | Leader | Registry Status | Challenger | Notes |
|---|---|---|---|---|
| Smart Contract Platforms | SOL | Provisional | SUI | Current configuration reference; formal approval pending evidence review |
| Oracle Networks | LINK | Provisional | API3 | Current configuration reference; formal approval pending evidence review |
| Real World Assets | ONDO | Provisional | PENDLE | Current configuration reference; formal approval pending evidence review |
| AI Infrastructure | TAO | Provisional | RENDER | Current configuration reference; formal approval pending evidence review |
| Data Availability | TIA | Provisional | AVAIL | Current configuration reference; formal approval pending evidence review |

## Registry Status Definitions

### Provisional

The asset is the current reference leader used by configuration or existing Phoenix documentation, but the current methodology has not yet been used to record an explicit formal approval decision.

A Provisional leader is not, by this status alone, authorization to introduce new portfolio logic.

### Approved

The leader has been explicitly approved under the current Phoenix leadership methodology, with supporting evidence recorded in the leadership review.

Only Approved leaders are eligible for formal Phoenix portfolio construction under D-022.

### Retired

The asset is no longer the approved leader for the category and must not remain in the active portfolio after the applicable replacement cycle.

## Multi-Category Rule

An asset may belong to multiple categories and may have different roles in each category.

Example:

RENDER
  DePIN → Leader
  AI Infrastructure → Challenger

Category roles are evaluated independently.

Portfolio construction operates on unique assets: the same asset may appear only once in the Phoenix portfolio even if it has roles in multiple categories.

## Leadership Change

A challenger becoming the approved leader is a governance decision, not a price-driven portfolio event.

When a leadership replacement is formally approved:

1. Update this registry.
2. Record the decision and evidence.
3. Update runtime configuration.
4. Rebalance the Phoenix portfolio during the applicable review cycle.

Price movement alone does not change registry status.

## Evidence Requirement

Each Approved entry should retain, at minimum:

- Review date
- Leader score
- Challenger score where applicable
- Replacement Risk / Leadership State under the canonical Phoenix rule
- Principal evidence supporting the assessment
- Decision rationale
- Replaced leader, if applicable

## Related Documents

- `Phoenix_Category_Framework.md`
- `Phoenix_Leader_Framework.md`
- `Phoenix_Scoring_Framework.md`
- `Phoenix_Operating_Model.md`
- `Decision_Log.md`
- `config/phoenix.yaml`

## Known Open Issues

- Formal approval evidence for the five provisional leaders has not yet been recorded.
- The canonical Replacement Risk / Leadership State mapping must remain identical across all Phoenix production-facing documents.
- Metric-to-score automation is not required for v1; scoring remains judgment-assisted-by-metrics unless separately approved.
