# Orion Review

## 1. Purpose

The `review/` directory is a temporary working area for reviewing the current state of Orion during an implementation phase.

Its purpose is to:

* identify gaps between the documented design and the implementation,
* distinguish decisions from specifications and implementation tasks,
* identify issues that actually block further implementation,
* determine what should be decided, documented, implemented, or deferred,
* provide a controlled feedback loop between design and implementation.

The `review/` directory is **not a permanent source of truth for Orion**.

The permanent source of truth remains the appropriate documents under `docs/`.

---

## 2. Core Principle

> **Review is temporary. Decisions are permanent.**

A review may identify a missing decision, an incomplete specification, a documentation inconsistency, or an implementation problem.

These must not all be treated as the same kind of problem.

Each issue should be classified before action is taken.

| Classification | Meaning                                                                     | Typical Action                                             |
| -------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `DECIDED`      | Already decided                                                             | Do not reopen unless new evidence requires reconsideration |
| `DECISION`     | A genuine design/investment-policy decision is required                     | Human decision                                             |
| `SPEC`         | Direction is decided but implementation-level specification is insufficient | Complete specification                                     |
| `IMPLEMENT`    | Specification is sufficient                                                 | Coding agent implements                                    |
| `RECONCILE`    | Documents and/or code are inconsistent                                      | Reconcile                                                  |
| `DEFER`        | Valid issue but not required for the current stage                          | Defer                                                      |

A missing document does **not** automatically mean that a new decision is required.

A feature being incomplete does **not** automatically mean that the project is blocked.

---

## 3. Relationship with the Permanent Documentation

Orion's permanent knowledge belongs in the appropriate documentation area.

The main documentation structure is:

```text
00_Vision
01_Architecture
02_Investment_Framework
03_Research
04_Roadmap
05_Decisions
06_Implementation
07_Coding
reports
study
```

The `review/` directory exists alongside these areas to coordinate the current review and implementation cycle.

When a review produces a valid and durable decision, that decision must be promoted to `05_Decisions` and any affected permanent documents must be updated.

For example:

```text
Review
  ↓
Decision identified
  ↓
Human decision
  ↓
05_Decisions
  ↓
Affected Framework / Research / Implementation documents
  ↓
Source Code
```

The review document should not become the permanent home of the decision.

---

## 4. Review → Decision → Implementation Workflow

The Orion development process follows a feedback loop rather than a one-way documentation process.

```text
Vision
  ↓
Architecture
  ↓
Investment / Research
  ↓
Roadmap / Decisions
  ↓
Implementation Specification
  ↓
Source Code
  ↓
Test / Real-world Implementation
  ↓
Review
  ↓
 ┌───────────────┬───────────────┬───────────────┐
 │               │               │               │
Decision        Specification   Implementation   Defer
required        required        required
 │               │               │
 ↓               ↓               ↓
05_Decisions    docs            Code
 │
 └───────────────┴───────────────┘
                    ↓
                 Re-review
```

Implementation is therefore not merely the final step after documentation.

Implementation is also a means of validating whether the documented design is sufficiently precise, coherent, and implementable.

---

## 5. Human and Coding-Agent Responsibilities

### Human / ChatGPT

The human decision process is responsible for:

* Orion's overall direction,
* investment philosophy,
* architecture decisions,
* methodology decisions,
* interpretation of research,
* resolving important ambiguities,
* deciding whether a genuine design decision is required.

ChatGPT is used primarily for discussion, analysis, review, and design reasoning.

### Codex / Coding Agent

The coding agent is responsible for:

* reading the repository documentation,
* understanding the current implementation,
* implementing sufficiently specified designs,
* refactoring code,
* running tests,
* identifying implementation-level inconsistencies,
* reporting newly discovered blockers.

The coding agent should **not invent investment methodology or silently make unresolved strategic decisions** merely to make the code run.

When a genuine decision is required, it should be recorded as a blocker and returned for human resolution.

---

## 6. Blocker Principle

> **A blocked feature is not necessarily a blocked project.**

If one part of a Framework cannot proceed because a decision is unresolved, independent work should continue whenever possible.

For example:

```text
Framework
├── Component A     IMPLEMENT
├── Component B     IMPLEMENT
├── Component C     DECISION REQUIRED
└── Component D     IMPLEMENT
```

The unresolved Component C should not automatically stop A, B, and D.

A blocker should therefore always answer two questions:

1. What exactly cannot proceed?
2. What other work can proceed independently?

---

## 7. Decision Promotion

A decision discovered during Review follows this lifecycle:

```text
OPEN
  ↓
Discussed
  ↓
DECIDED
  ↓
Recorded in 05_Decisions
  ↓
Affected documents updated
  ↓
Implementation enabled
```

Once a decision has been promoted to the permanent documentation, the temporary Review entry may be marked as resolved.

The Review directory must not become a second, competing decision repository.

---

## 8. Review Lifecycle

A Review corresponds to a development stage or implementation milestone.

For example:

```text
Alpha
  ↓
Implementation Review
  ↓
Decisions
  ↓
Documentation Update
  ↓
Implementation
  ↓
Alpha Completion
```

When the Alpha review is complete, the `review/` directory may be:

* cleaned up,
* archived if useful for the development process,
* or reused for the next development stage.

A future Beta review does not require preserving the Alpha review workspace.

What **must** survive is the resulting project knowledge:

* decisions,
* architecture changes,
* methodology changes,
* implementation specifications,
* research conclusions,
* and other durable project knowledge.

Therefore:

> **Review history may be temporary; project decisions and knowledge are permanent.**

---

## 9. Review Directory Rules

The `review/` directory should contain only information necessary to manage the current review and implementation cycle.

It should not become another large documentation hierarchy.

Temporary review documents should be concise and action-oriented.

Recommended files:

```text
review/
├── README.md
├── implementation_review.md
├── decision_queue.md
└── codex_next_work.md
```

Their responsibilities are:

### `implementation_review.md`

Describes the current state of Orion:

* implementation status,
* design completeness,
* implementation completeness,
* inconsistencies,
* blockers,
* independently executable work,
* current development frontier.

### `decision_queue.md`

Contains only genuine decisions that require resolution.

It should distinguish:

* decisions already made,
* decisions currently open,
* decisions that can be deferred.

### `codex_next_work.md`

Contains the current actionable instructions for the coding agent.

It should answer:

> **What should Codex do next?**

It should not contain the entire history of Orion.

---

## 10. Avoiding Documentation Explosion

The existence of `review/` must not restart the documentation expansion that Orion has already experienced.

The purpose of Review is to reduce ambiguity, not create more documents.

Before creating a new document, determine whether the information belongs in:

* an existing permanent document,
* an existing Decision,
* an implementation specification,
* the current Review,
* or nowhere yet.

In particular:

> **Do not create a new document merely because an existing document is incomplete.**

First determine whether the missing information is:

* a genuine decision,
* a missing specification,
* a missing research result,
* an implementation task,
* or simply unnecessary at the current stage.

---

## 11. Definition of Done for a Review Item

A review item is complete when one of the following is true:

### Decision

```text
Decision made
→ ADR recorded
→ affected documents updated
→ implementation can proceed
```

### Specification

```text
Existing decision confirmed
→ implementation specification completed
→ implementation can proceed
```

### Implementation

```text
Specification sufficient
→ implementation completed
→ tests pass
→ status updated
```

### Reconciliation

```text
Conflict identified
→ authoritative interpretation established
→ documents/code reconciled
```

### Deferred

```text
Issue understood
→ explicitly deferred
→ no longer blocks current milestone
```

---

## 12. Final Principle

Orion should continuously move information through the following pipeline:

```text
Discussion
    ↓
Review
    ↓
Decision / Specification
    ↓
Permanent Documentation
    ↓
Implementation
    ↓
Validation
    ↓
Review
```

The goal of this process is not to make the documentation perfect before implementation.

The goal is to maintain a system in which:

> **important decisions are explicit, permanent knowledge is documented, implementation is executable, and unresolved issues do not silently become implementation assumptions.**
