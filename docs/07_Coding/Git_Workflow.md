# Git Workflow

Version: 1.0

Status: Active

Last Updated: 2026-07-28

Depends On:

* Development_Workflow.md
* Development_Principles.md

---

# Purpose

Defines the Git workflow used by Orion OS.

The workflow emphasizes small, traceable, and reviewable changes.

---

# Branch Strategy

Primary branches:

main

Stable production-ready branch.

develop (optional)

Integration branch for ongoing development.

Feature branches are recommended for significant work.

---

# Commit Philosophy

Each commit should represent a single logical change.

Avoid mixing unrelated modifications.

---

# Commit Messages

Use imperative mood.

Examples

Add Moon execution pipeline

Refactor configuration loader

Fix dashboard state rendering

Update Orion runtime documentation

---

# Commit Size

Prefer small commits.

Large changes should be divided into logical steps.

---

# Pull Requests

Each pull request should:

* Describe the purpose
* Reference related documents
* Summarize testing
* Identify breaking changes

---

# Code Review Checklist

Verify:

* Architecture compliance
* Coding standards
* Documentation updates
* Test coverage
* Dependency rules

---

# Tags

Use semantic versioning.

Examples

v0.1.0

v0.2.0

v1.0.0

---

# Release Process

Before a release:

* All tests pass.
* Documentation updated.
* Roadmap reviewed.
* Decision Log updated if necessary.

---

# Rollback

Every release should be recoverable through Git tags.

Avoid force-pushing shared branches.

---

# Repository Hygiene

Do not commit:

* Secrets
* API keys
* Temporary files
* Cache directories
* Compiled artifacts

Keep the repository clean and reproducible.

---

# Related Documents

* Development_Workflow.md
* Development_Principles.md