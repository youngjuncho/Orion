# Architecture Reconciliation Summary

Date: 2026-06-23

Source review:

* `docs/reports/Architecture_Consistency_Report.md`
* `docs/05_Decisions/Decision_Log.md`, D-023
* `docs/01_Architecture/Orion_Operating_Architecture.md`
* `docs/01_Architecture/Orion_Technical_Architecture.md`
* `docs/06_Implementation/Orion_Configuration_Schema.md`
* `config/`

Scope:

* Architecture documentation reconciliation
* Configuration schema and production configuration reconciliation

Out of scope:

* Investment logic changes
* Scoring logic changes
* Framework behavior changes
* Source tree refactors
* New framework modules

---

## 1. Documents Modified

### `docs/01_Architecture/Orion_Technical_Architecture.md`

Updated to align with D-023:

* Replaced "four primary engines" with "one Monitoring Framework and three Portfolio Engines."
* Defined Aurora as the Monitoring Framework.
* Defined Moon, Supernova, and Phoenix as Portfolio Engines.
* Replaced `src/dashboards/` with `src/dashboard/`.
* Moved `tests/` out of the displayed `src/` tree and into the repository root.
* Removed dashboard ownership of strategy execution, signal generation, and state generation.
* Defined the Dashboard Layer as presentation-only.
* Clarified that investment logic belongs in framework modules and shared core modules.
* Clarified that dashboards display scores but do not calculate investment logic.
* Updated Supernova purpose from monitoring-engine language to Equity Portfolio Engine language.

### `docs/00_Vision/Vision_Summary.md`

Updated to align with D-023 and D-021/D-022:

* Renamed `Dashboard Framework` to `Orion Frameworks`.
* Defined Aurora as the Monitoring Framework.
* Defined Moon as the ETF Portfolio Engine.
* Defined Supernova as the Equity Portfolio Engine.
* Defined Phoenix as the Digital Asset Portfolio Engine.
* Removed outdated Phoenix language stating that portfolio methodology was still under review.
* Added Phoenix references to D-021 and D-022.
* Clarified that BTC and ETH are outside Phoenix governance.

### `docs/02_Investment_Framework/Orion_IPS.md`

Updated to align with D-023, D-021, and D-022:

* Replaced "four independent investment frameworks" with "one Monitoring Framework and three independent Portfolio Engines."
* Clarified that Aurora does not manage portfolios and does not generate investment recommendations.
* Updated Moon to ETF Portfolio Engine.
* Updated Supernova to Equity Portfolio Engine.
* Updated Phoenix to Digital Asset Portfolio Engine.
* Replaced outdated Phoenix draft/governance-under-review language.
* Added Phoenix portfolio construction policy from approved decisions:
  * BTC and ETH remain outside Phoenix.
  * Phoenix manages approved category leaders.
  * Challengers and watchlist assets are monitored but not held.
  * Approved leaders are equally weighted.

### `docs/06_Implementation/Orion_Configuration_Schema.md`

Updated to make the documented schema directly match production configuration files:

* Rewrote YAML examples as valid, concrete YAML.
* Required documented top-level keys:
  * `system`
  * `moon`
  * `aurora`
  * `supernova`
  * `phoenix`
* Clarified that each configuration file must contain its documented top-level key.
* Updated the production configuration status from future task language to created-file language.

### `src/core/config_loader.py`

Only a stale TODO comment was removed.

No validation logic was weakened.

No investment logic, scoring logic, or framework behavior was changed.

---

## 2. Configuration Files Modified

### `config/system.yaml`

Updated to match schema:

* Added top-level `system` key.
* Fixed nested `logging`, `data`, and `dashboard` indentation.
* Preserved existing values.

### `config/moon.yaml`

Updated to match schema:

* Added top-level `moon` key.
* Converted Markdown-style list entries to YAML list entries.
* Replaced flat boolean flags with nested objects:
  * `signal_assets.enabled`
  * `execution_mapping.enabled`
* Preserved existing Moon operational values.

### `config/aurora.yaml`

Updated to match schema:

* Added top-level `aurora` key.
* Renamed `scoring` to `scoring_range`.
* Replaced `transition_monitoring: true` with `transition_monitoring.enabled`.
* Fixed nested indicator group indentation.
* Preserved existing Aurora values.

### `config/supernova.yaml`

Updated to match schema:

* Added top-level `supernova` key.
* Converted Markdown-style company list to YAML list entries.
* Added `candidate_universe.source` from the documented schema.
* Replaced `replacement_policy: true` with `replacement_policy.enabled`.
* Replaced `scoring.min/max` with documented `scoring.range`.
* Preserved existing approved company values.

### `config/phoenix.yaml`

Updated to match schema:

* Added top-level `phoenix` key.
* Replaced `BTC` and `ETH` keys with documented `btc_weight` and `eth_weight`.
* Replaced `portfolio_construction.methodology` with documented scalar `portfolio_construction`.
* Removed Markdown code fences from category definitions.
* Renamed category keys to documented schema names:
  * `smart_contracts`
  * `oracle`
  * `rwa`
  * `ai_infrastructure`
  * `data_availability`
* Replaced flat booleans with nested objects:
  * `replacement_policy.enabled`
  * `leadership_monitoring.enabled`
* Preserved existing Phoenix values.

---

## 3. Architecture Issues Resolved

Resolved Critical issue:

* Dashboard Layer no longer owns strategy execution, signal generation, or state generation in `Orion_Technical_Architecture.md`.

Resolved Major issues:

* Technical architecture no longer treats Aurora, Moon, Supernova, and Phoenix as equivalent primary engines.
* Technical architecture now follows D-023:
  * Aurora = Monitoring Framework
  * Moon = ETF Portfolio Engine
  * Supernova = Equity Portfolio Engine
  * Phoenix = Digital Asset Portfolio Engine
* `src/dashboard/` is now the documented dashboard source path.
* `tests/` is documented at repository root rather than under `src/`.
* Scoring language no longer implies dashboard ownership of scoring logic.
* Supernova is now described as an Equity Portfolio Engine.
* Vision Summary no longer uses `Dashboard Framework` as the parent architecture.
* Vision Summary no longer states that Phoenix portfolio methodology is under review.
* IPS no longer treats Aurora as an investment framework.
* IPS Phoenix policy now reflects approved D-021 and D-022 decisions.

---

## 4. Configuration Issues Resolved

Resolved:

* Production config files now include documented top-level keys.
* Production config files are valid YAML.
* Production config files match the documented schema structure.
* Production config files preserve strict validation expectations.
* The schema document now matches production configuration format.
* The strict loader design remains intact.

Validation performed:

```text
pytest tests\core\test_config_loader.py -q
```

Result:

```text
6 passed
```

---

## 5. Remaining Open Issues

Minor documentation issues from `Architecture_Consistency_Report.md` remain intentionally open:

* Some architecture and repository diagrams outside the modified sections may still contain encoding-damaged tree glyphs.
* `Orion_Operating_Architecture.md` still contains encoding-damaged diagrams, though its prose remains aligned with D-023.
* `Orion_Repository_Structure.md` still contains encoding-damaged tree glyphs, though its directory names remain correct.
* `Aurora_Operating_Model.md` still uses "execution framework" language for Moon. This was marked Minor and was not changed in this pass.

These were deferred because the task requested Critical and Major recommendations first, with Minor recommendations ignored unless trivial.

---

## 6. Config Loader TODO Decision

Decision:

The config loader TODO was removed.

Removed text:

```text
Production config files currently omit documented top-level keys.
Keep this strict until docs or config are reconciled by an approved change.
```

---

## 7. Rationale

Removal is safe because the condition described by the TODO is no longer true.

After reconciliation:

* `config/system.yaml` contains top-level `system`.
* `config/moon.yaml` contains top-level `moon`.
* `config/aurora.yaml` contains top-level `aurora`.
* `config/supernova.yaml` contains top-level `supernova`.
* `config/phoenix.yaml` contains top-level `phoenix`.
* `docs/06_Implementation/Orion_Configuration_Schema.md` explicitly documents those top-level keys.
* Strict validation remains in place.

No validation behavior was relaxed.

No required top-level keys were removed.

No investment logic, scoring logic, or framework behavior was modified.
