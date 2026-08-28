<!-- GENERATED FILE - do not edit by hand. Source: dx-standards/. Regenerate with: python3 scripts/sync-standards.py -->

# Severity and Verdict Vocabulary

Canonical severity levels and verdict vocabulary for every skill in the suite.

## Severity levels

- **P0 Blocker:** unsafe, impossible, materially incorrect, data/security/production risk.
- **P1 Critical:** blocks first success, breaks a hard gate (magic path, local dev), or incorrectly documents a public contract.
- **P2 Major:** important missing workflow, stale example, API/SDK mismatch, poor error recovery, substantial drift.
- **P3 Minor:** clarity, navigation, terminology, maintainability.
- **P4 Polish:** presentation/style only.

Prioritize defects that prevent developers from succeeding over cosmetic completeness.

## Verdict vocabulary

Every release or audit verdict returns exactly one of:

- **PASS:** no P0/P1 gate failures; required hard gates pass.
- **PASS WITH DEBT:** no hard gate failure, but P2/P3 backlog remains.
- **FAIL:** one or more P0/P1 gates fail.
- **UNVERIFIED:** evidence is insufficient to prove critical gates; do not convert this to PASS based on assumptions.

A high numerical score cannot override a hard-gate failure.

## Report labeling

Every score and timing reported by any skill must carry its evidence label (Observed / CI-observed / Estimated). Unlabeled numbers are UNVERIFIED.

## Evidence hierarchy

Prefer, in order:

1. observed execution against a clean/representative environment
2. implementation/tests/specs
3. generated/current interface output such as `--help`
4. package/release metadata
5. examples
6. prose docs

When sources disagree, report the contradiction.


## Evidence labels

- **Observed**: a human or agent actually executed the path from a clean or representative environment.
- **CI-observed**: automation executed the product steps; may undercount human reading/signup time.
- **Estimated**: steps analyzed but not executed.
- An estimate can never prove a PASS. A metric without an evidence label is UNVERIFIED.


## Workflow feedback budgets

Inner/outer loop feedback budgets (guidance; one exceeded = P2, two or more = P1):

- `FEEDBACK_FORMATTER_MAX_S` = 2 — formatter/linter feedback.
- `FEEDBACK_INCREMENTAL_COMPILE_MAX_S` = 5 — incremental compile.
- `FEEDBACK_UNIT_TEST_MAX_S` = 10 — unit test result.
- `FEEDBACK_FOCUSED_INTEGRATION_MAX_S` = 60 — focused integration result.
- `FEEDBACK_LOCAL_RELOAD_MAX_S` = 3 — local reload.
- `FEEDBACK_CI_FIRST_SIGNAL_MAX_MIN` = 3 — CI first useful signal.
- `FEEDBACK_FULL_CI_MAX_MIN` = 10 — full CI.

Any forced wait >30 seconds between edit and feedback breaks flow state (P2).


## SLO table

| SLO constant | Defined in | Owning skill |
|---|---|---|
| `MAGIC_PATH_MAX_MIN` | metrics.md | developer-onboarding (design) / developer-experience-auditor (measure) |
| `LOCAL_DEV_MAX_MIN` | metrics.md | local-development |
| `FIRST_CONTRIBUTION_TARGET_MIN` | metrics.md | contributor-experience |
| `ARCHITECTURE_COMPREHENSION_MAX_MIN` | metrics.md | architecture-experience |
| `TTR_TARGET_MIN` | metrics.md | error-experience |
| `FEEDBACK_FORMATTER_MAX_S` | metrics.md | developer-workflow-auditor |
| `FEEDBACK_INCREMENTAL_COMPILE_MAX_S` | metrics.md | developer-workflow-auditor |
| `FEEDBACK_UNIT_TEST_MAX_S` | metrics.md | developer-workflow-auditor |
| `FEEDBACK_FOCUSED_INTEGRATION_MAX_S` | metrics.md | developer-workflow-auditor |
| `FEEDBACK_LOCAL_RELOAD_MAX_S` | metrics.md | developer-workflow-auditor |
| `FEEDBACK_CI_FIRST_SIGNAL_MAX_MIN` | metrics.md | developer-workflow-auditor |
| `FEEDBACK_FULL_CI_MAX_MIN` | metrics.md | developer-workflow-auditor |
| `SANDBOX_COVERAGE_GATE` | metrics.md | sandbox-experience |
| `COMMUNITY_ONBOARDING_PATH_MAX_MIN` | community.md | developer-community-auditor |
| `COMMUNITY_ISSUE_RESPONSE_P50_H` | community.md | developer-community-auditor |
| `COMMUNITY_ISSUE_RESPONSE_P90_H` | community.md | developer-community-auditor |
| `COMMUNITY_FIRST_PR_REVIEW_P50_H` | community.md | developer-community-auditor |
| `COMMUNITY_FIRST_PR_REVIEW_P90_H` | community.md | developer-community-auditor |
| `COMMUNITY_USEFUL_ANSWER_P90_H` | community.md | developer-community-auditor |
| `COMMUNITY_UNACKNOWLEDGED_PR_MAX_DAYS` | community.md | developer-community-auditor |
