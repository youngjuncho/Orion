# Orion Moon ADM PCD-05 — Windows Conda Environment Inventory Runbook

Date: 2026-10-19  
Status: Read-only inventory; no dependency installation authorized  
Target: designated Windows Git Bash / Conda `orion` environment, Python 3.12.13

## 1. Why this runbook exists

The current bundle can inspect repository files, but it cannot inspect the user's Windows Conda environment. Therefore Windows compatibility must not be claimed from the container runtime or from package metadata alone. This runbook collects a minimal, read-only inventory before any isolated installability probe is considered.

The designated interpreter path is `$HOME/anaconda3/envs/orion/python.exe`. Use that exact executable rather than relying on whichever `python` happens to be first on `PATH`.

## 2. Read-only inventory commands (Git Bash)

Run from the Orion repository root. These commands do not install, upgrade, or remove packages and do not call market-data APIs.

```bash
printf '%s\n' '--- designated interpreter ---'
"$HOME/anaconda3/envs/orion/python.exe" -c "import sys, platform; print('version:', sys.version); print('executable:', sys.executable); print('platform:', platform.platform())"

printf '%s\n' '--- pip attached to designated interpreter ---'
"$HOME/anaconda3/envs/orion/python.exe" -m pip --version

printf '%s\n' '--- relevant installed packages ---'
"$HOME/anaconda3/envs/orion/python.exe" -m pip show exchange-calendars pandas-market-calendars pandas numpy pyyaml pytest

printf '%s\n' '--- repository dependency declaration ---'
cat requirements.txt
```

If the exact path does not exist or the interpreter reports a version other than Python 3.12.13, stop and report the output. Do not substitute another interpreter silently.

## 3. Optional complete inventory

Only if the environment inventory is needed for troubleshooting, save the package list to a local text file and review it before sharing. It may expose unrelated environment details.

```bash
"$HOME/anaconda3/envs/orion/python.exe" -m pip freeze > orion_environment_freeze.txt
```

This writes a local diagnostic file only; it does not change installed packages. Do not include credentials, `.env` contents, or API keys in any report.

## 4. Decision after inventory

- If Python is not 3.12.13, or the interpreter path is unexpected: stop; resolve environment identity first.
- If either candidate calendar package is already installed: record its exact version and provenance; do not assume it is approved for Orion.
- If neither candidate is installed: do not install into `orion`. The next proposed action is a separate, disposable Conda environment with the exact Python version and one explicitly selected candidate release.
- If `pip` itself is missing or broken: stop and report it; do not repair the working environment as part of this audit.

## 5. Evidence to return

Return the output of Sections 2 and, if needed, a reviewed/redacted inventory from Section 3. The evidence record must include the command output, date, interpreter path, and any errors. Do not share the complete environment freeze unless needed and reviewed.

## 6. Safety and scope

- This runbook does not authorize package installation, dependency pinning, runtime wiring, or changes to the working Conda environment.
- No live market-data API calls are required or authorized.
- `config/moon.yaml` must retain `active_strategies: []`; signal assembly remains fail-closed.
- PCD-05 and PCD-06 remain open. PCD-15/PCD-16 remain blocking; G-01 remains `DEFERRED — BLOCKING`.
