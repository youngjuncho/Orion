# Moon ADM Guard Result Type-Integrity Audit — 2026-10-15

## Finding

`ADMComparisonSignalGuardResult` is a public frozen dataclass representing the decision from the signal-assembly guard. Its `blocked_reasons` field is declared as a tuple, but prior validation accepted arbitrary iterables. In particular, a string such as `"blocked"` was treated as a sequence of one-character reason strings, while a list was silently normalized. That weakens the boundary contract and can make malformed caller-created result objects appear structurally valid.

## Change

- Require `blocked_reasons` to be a tuple before validating its members.
- Keep the existing invariant that eligibility is true exactly when the blocked-reason tuple is empty.
- Add regression tests for string and list values.

## Scope and limitations

- No comparison policy, threshold, data selection, or investment behavior changed.
- The production signal guard continues to block because PCD-15 authoritative governance binding is not implemented.
- No live API calls were made.
- Full test suite: `442 passed in 3.76s` on Python 3.13.5. This is not a run in the designated Python 3.12.13 environment.
