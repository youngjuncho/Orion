# Orion Cumulative Sync Bundle — 2026-10-15 (v21)

## Contents

- Cumulative Orion repository snapshot based on uploaded `Orion_1015.zip`, Git baseline commit `44f0caf`.
- Includes the accumulated Moon/ADM implementation audits and tests, the latest VAA research-document commits, and this step's offline Alpha Vantage notice-classification regression coverage.
- This bundle is intended for comparison and selective merging; do not replace a working repository wholesale without reviewing local changes.
- No standalone patch files are included.

## Changes in this step

1. Added regression cases for the remaining Alpha Vantage notice-classification branches: generic request rejection, generic `Note` notices, and multiple notice fields.
2. Added a regression test confirming the provider stops after the first notice and does not continue requesting symbols or return partial data.
3. Refreshed the cumulative manifest and checksum list to include the latest VAA/ADM snapshot and exclude `.git`, transient `test_tmp` directories, Python caches, and the checksum file itself.
4. No production source code or investment/trading logic was changed in this step.

## Validation

- Targeted Alpha Vantage tests and live-contract CLI safety tests: **36 passed**.
- Full test suite: **464 passed in 5.37s**, Python **3.13.5**.
- UTF-8 policy check: **passed** (326 text files, UTF-8 without BOM).
- No live Alpha Vantage API calls were made.

The project's designated Windows Conda environment uses Python 3.12.13. This bundle was independently tested with Python 3.13.5; after merging, verify using the project's designated interpreter:

```bash
"$HOME/anaconda3/envs/orion/python.exe" -m pytest -q -p no:cacheprovider
```

## Checksum scope

`SYNC_BUNDLE_CHECKSUMS.sha256` covers repository files except `.git`, temporary test artifacts, Python/cache directories, and the checksum file itself. After extracting the archive, verify from the repository root with:

```bash
sha256sum -c SYNC_BUNDLE_CHECKSUMS.sha256
```

## Safety and scope

- `config/moon.yaml` must keep `active_strategies: []`.
- PCD-15 authoritative governance binding remains incomplete; signal assembly stays fail-closed.
- No live provider calls, investment decisions, or trading operations were performed.
- Alpha Vantage live-contract validation previously returned `API_RATE_LIMIT`. The precise provider-side cause is not confirmed; do not repeatedly retry while the limit may remain active.
