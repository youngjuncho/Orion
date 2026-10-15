# Orion Governance Required Decision ID Contract Audit

**Date:** 2026-10-15  
**Status:** Implemented input-contract hardening; no authority or approval decisions made

## Finding

`resolve_approved_decisions()` accepted `required_ids` as `Sequence[str]` but did not validate the sequence container. At runtime, a bare string is itself a sequence, so an accidental `"PCD-01"` argument could be iterated character-by-character. An empty sequence could also return an empty successful resolution, which is unsafe for an authorization-oriented API because no required decisions were actually checked.

## Change

- Reject strings, bytes, bytearrays, non-sequences, and empty sequences for `required_ids`.
- Validate each member as non-empty text before lookup.
- Apply this validation in `resolve_approved_decisions()`, which is also used by `resolve_registry_approved_decisions()`.
- Add regression tests for malformed containers and malformed members.

## Security and scope

This is input-contract validation only. It does not establish that a supplied registry is authoritative, current, signed, non-revoked, or rollback-protected. PCD-15 remains open; Moon ADM signal assembly remains fail-closed. No investment logic, provider selection, strategy activation, or live API behavior was changed. `config/moon.yaml` must retain `active_strategies: []`.
