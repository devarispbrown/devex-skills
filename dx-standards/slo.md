# DX SLOs

The suite-wide DX service level table. Each SLO has exactly one home for its value (in `metrics.md` or `community.md`); this file maps SLOs to their owning skills without restating values.

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

## SLO ownership

The owning skill defines and measures its SLO; auditor skills enforce. Values are never restated with different numbers in hand-written skill files — reference the constant by name.

Skills without a measurable service interface have no SLO row; their area scores are UNVERIFIED per the verdict vocabulary in `severity.md`.
