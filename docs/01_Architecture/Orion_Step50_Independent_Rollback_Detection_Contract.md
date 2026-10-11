# Orion Step 50 Independent Rollback-Detection Contract

**Status:** Requirements only; implementation and provider choice are not approved  
**Date:** 2026-10-11  
**Scope:** Detection of a valid but stale SQLite HWM/journal backup after restoration

## 1. Problem statement

The SQLite high-water mark (HWM) and acceptance journal live in the same database. SQLite transactions can preserve consistency within the active database, but restoring an older, internally valid database also restores its older HWM and journal. The restored file contains no trustworthy evidence of the newer state that existed before restoration.

Therefore, the current SQLite store alone cannot guarantee detection of valid-stale-backup rollback. Corruption checks, file hashes stored beside the same database, WAL settings, and ordinary compare-and-swap do not solve this threat if the same restoration can roll those artifacts back together.

## 2. Required acceptance invariant

For a given exact identity `(authority_ref, registry_type, canonical scope)`, an accepted snapshot must satisfy all of the following:

1. `snapshot_version` is a positive integer. Strings, booleans, floats, zero, and negative values are invalid.
2. The version must be strictly greater than the latest trusted committed version. Equality is replay and must be rejected.
3. The comparison must use the strongest available trusted state, not merely the HWM read from a potentially restored SQLite file.
4. If the independent rollback-detection service is unavailable, ambiguous, inconsistent, or reports a state that cannot be reconciled, acceptance fails closed. It must not silently fall back to the SQLite HWM alone.
5. A compare-and-swap conflict requires re-reading current trusted state and re-validating the snapshot. Stale validation results must not be blindly retried.

The current snapshot validator and SQLite store already enforce strict positive-integer typing and monotonicity against the state they receive. They do **not** satisfy item 3 when the only state supplied is the restored database.

## 3. Independence and trust requirements

The future rollback anchor must be independently protected from the SQLite restore operation. At minimum, its design review must answer:

- What component owns the monotonic state, and who is authorized to change or restore it?
- Which exact authority/registry/canonical-scope identity keys the state?
- How is anchor authenticity and integrity verified?
- What access controls prevent the same operator or recovery action from rolling back both anchor and SQLite state?
- What are its availability, durability, backup, retention, and incident-recovery assumptions?
- How are anchor state and local HWM/journal reconciled after a crash at every commit boundary?
- How are concurrent acceptors serialized, and how does the protocol recover a version reservation after a process crash?
- What happens if the anchor is newer than local SQLite, local SQLite is newer than the anchor, or the journal is inconsistent?

A file or metadata value stored alongside the SQLite database is not independent. No cloud vendor, remote service, hardware security module, consensus system, or other provider is selected by this contract.

## 4. Cross-store crash consistency requirement

A future implementation must explicitly specify the state machine for coordination between the independent anchor and the local atomic HWM-plus-journal transaction. It must cover crashes before and after each durable write, duplicate requests, CAS conflicts, and retry after an ambiguous response.

In particular, advancing the anchor before local commit can leave a version reserved without a local acceptance event; committing SQLite first can leave local state ahead of the anchor. The design must define safe reconciliation for both conditions. It must not solve one ordering hazard by silently weakening strict monotonicity or accepting an unverified snapshot.

Required fault-injection evidence includes:

- restore an older but valid SQLite database after a newer version was accepted;
- prove the old version and same-version replay are rejected using the independent state;
- inject failures at each cross-store write/acknowledgement boundary;
- restart after each injected failure and prove state converges safely or remains fail-closed;
- race two acceptors for the same identity and prove only one monotonic transition wins;
- test unavailable, malformed, stale, or contradictory anchor responses;
- verify that no failure path resets or silently reinitializes the anchor.

## 5. Explicit non-goals and current disposition

This document does not implement an anchor, choose a provider, modify the acceptance API, or authorize production integration. Until an implementation and its recovery protocol are approved and tested, valid-stale-backup rollback detection remains **OPEN — BLOCKING**.

No Core Runtime lifecycle behavior, Runtime/Supernova integration, investment logic, order execution, or Moon strategy configuration is changed. `config/moon.yaml` must continue to contain `moon.active_strategies: []`.
