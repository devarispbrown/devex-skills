# DX Metrics and Thresholds

Canonical metrics for the entire skills suite. Skills reference these constants by name; they must never be restated with different values inside a skill's hand-written files.

## Magic path thresholds

- `MAGIC_PATH_MAX_MIN` = 15. Hard gate: a brand-new developer with zero product knowledge reaches a meaningful, verified, end-to-end product outcome in 15 minutes or less.
- Bands: ≤5 min exceptional; >5 to ≤10 min strong; >10 to ≤15 min pass; >15 min P1 FAIL. No reproducible E2E quickstart: P1 FAIL. Manual approval/support required with no sandbox: P1 FAIL.
- The timer includes installation, signup/auth when required, configuration, execution, waiting, and verification. Setup cannot be moved into "prerequisites" to game the metric.
- Targets (P2 when exceeded): `MAGIC_PATH_MAX_COMMANDS` = 8 interactive commands, `MAGIC_PATH_MAX_CREDENTIALS` = 2 credentials the user must create or find, `MAGIC_PATH_MAX_CONTEXT_SWITCHES` = 4 switches between docs, terminal, and browser.
- Per-segment budget (guidance, not gates): orientation ≤1 min, install ≤2, auth ≤3, config ≤3, execute ≤3, verify ≤1, buffer ≥2.

## Local development thresholds

- `LOCAL_DEV_MAX_MIN` = 10. Hard gate: a clean clone reaches the productive state — tests run, the dev loop is exercised — using only committed instructions and automation.
- Bands: ≤3 min exceptional; >3 to ≤6 strong; >6 to ≤10 pass; >10 min P1 FAIL.
- Targets (P2 when exceeded): `LOCAL_DEV_MAX_COMMANDS` = 4 commands from clone to first successful run.
- Budget (guidance): clone ≤1 min, toolchain ≤2, dependencies ≤2, services ≤2, first success ≤2, buffer ≥1.

## Contribution thresholds

- `FIRST_CONTRIBUTION_TARGET_MIN` = 30. Target, not a hard gate: fork to first PR-ready change. 30–60 min = PASS WITH DEBT signal; >60 min = P2.

## Recovery thresholds

- `TTR_TARGET_MIN` = 5. Time to Recovery target for expected errors: from hitting the error to completing the corrective action. >10 min = P2.

## Evidence labels

- **Observed**: a human or agent actually executed the path from a clean or representative environment.
- **CI-observed**: automation executed the product steps; may undercount human reading/signup time.
- **Estimated**: steps analyzed but not executed.
- An estimate can never prove a PASS. A metric without an evidence label is UNVERIFIED.
