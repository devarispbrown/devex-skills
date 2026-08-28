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


# Community Standards

Community is another developer interface. A technically excellent project with hostile contribution mechanics, unanswered PRs, opaque governance, or no path to maintainership has poor DX. These standards are the canonical community vocabulary for the suite; verdicts and severities follow `severity.md`.

## Community magic path

- `COMMUNITY_ONBOARDING_PATH_MAX_MIN` = 30. Hard gate: a competent developer goes from discovering the contribution process to producing a valid contribution **ready for maintainer review** in 30 minutes or less. Implementation time is excluded; the metric measures project-imposed contribution friction.
- Bands: ≤10 min exceptional; >10 to ≤20 strong; >20 to ≤30 pass; >30 min P1 FAIL. No newcomer-usable issue available = P2.
- Funnel (12 steps, each with its owning artifact): discover (README) → understand (CONTRIBUTING) → ask (SUPPORT/chat) → find (labels) → setup (dev env) → first PR (templates) → review (review SLA) → accepted (merge policy) → return (recognition) → review others (reviewer path) → own area (ladder) → maintainer (governance).

## Community response SLOs

Measurement window: trailing 30 days. Denominators: all non-bot activity. Bots never count toward responsiveness (`COMMUNITY_BOT_RESPONSE_EXCLUDED`).

- `COMMUNITY_ISSUE_RESPONSE_P50_H` = 24 and `COMMUNITY_ISSUE_RESPONSE_P90_H` = 72 — first human response on new issues.
- `COMMUNITY_FIRST_PR_REVIEW_P50_H` = 24 and `COMMUNITY_FIRST_PR_REVIEW_P90_H` = 72 — first human review on first-time-contributor PRs.
- `COMMUNITY_USEFUL_ANSWER_P90_H` = 48 — first useful answer on community questions; a "useful answer" is a response that addresses the asker's stated question (answered or resolved), not an acknowledgment, redirect without substance, or bot reply.

## Community stage gates

Stages gate requirements, not scores. Counting method: unique human authors over a trailing 90-day window, bots excluded. Counts are targets (P2 when missed); named gates carry the hard-FAIL burden. Ratio indicators per stage:

| Stage | Name | Indicators | Required |
|---|---|---|---|
| 0 | Founder-led | bus factor <2 | CONTRIBUTING.md, CODE_OF_CONDUCT.md, issue/PR templates, documented dev environment |
| 1 | Early community | bus factor ≥2, non-employee contribution share growing | + response SLO monitoring, good-first-issue labels, triage process |
| 2 | Growing | closure ratio ≥0.7, multiple reviewers | + GOVERNANCE.md, maintainer ladder, recognition program |
| 3 | Scale | multiple owners per critical area | + contributor analytics, delegation, moderation, CoC enforcement |
| 4 | Foundation | succession defined | + foundation governance, security response team |

## Community hard gates

| Gate constant | Severity | Fails when |
|---|---|---|
| `NO_CONTRIBUTING_WHILE_WELCOMING` | P1 | README/docs claim contributions welcome and no CONTRIBUTING.md exists |
| `NO_CODE_OF_CONDUCT` | P1 | community-facing repo at Stage ≥1 lacks a Code of Conduct |
| `UNRESPONSIVE_ISSUES` | P1 | issue first-response P50 exceeds `COMMUNITY_ISSUE_RESPONSE_P50_H` over the trailing 30 days |
| `UNREVIEWED_FIRST_PR` | P1 | first-time-PR first-review P50 exceeds `COMMUNITY_FIRST_PR_REVIEW_P50_H` |
| `BROKEN_CONTRIBUTION_PATH` | P1 | Community Magic Path exceeds `COMMUNITY_ONBOARDING_PATH_MAX_MIN` |
| `DEAD_END_COMMUNITY` | P1 | non-maintainer PRs routinely receive no review and never merge |
| `OPAQUE_GOVERNANCE` | P1 | Stage ≥2 without GOVERNANCE.md and a maintainer ladder, or governance documentation describes an aspirational structure rather than how the project actually operates |
| `STALE_GOOD_FIRST_ISSUES` | P1 | newcomer-labeled issues open >90 days without activity, or queued newcomer PRs sit unreviewed |
| `NO_GOOD_FIRST_ISSUES` | P2 | Stage ≥2 soliciting contributions with no genuinely usable newcomer tasks (context, scope, acceptance criteria, pointers) |
| `NO_RECOGNITION_PATH` | P2 | Stage ≥2 with no contributor recognition |

Hard gate failures: `NO_CONTRIBUTING_WHILE_WELCOMING`, `NO_CODE_OF_CONDUCT`, `BROKEN_CONTRIBUTION_PATH`, and `DEAD_END_COMMUNITY` force FAIL regardless of any score. Every FAIL sentence in community guidance must map 1:1 to a named gate constant.

## CHAOSS metrics

Community metrics follow CHAOSS definitions; verify names against chaoss.community while authoring and cite them by name, never by paraphrase: `Time to First Response`, `Change Request Acceptance Ratio`, `New Contributors`, `Contributor Retention`, `Bus Factor`, `Elephant Factor`.

## Community standards files

Seven files, each with presence AND quality questions:

- CONTRIBUTING.md — must state: how to find work, how to set up, how to run tests, what an acceptable PR is, how review works, how long review takes, who can help, how decisions are made, how to become more involved.
- CODE_OF_CONDUCT.md — must include a report route and enforcement commitment.
- SECURITY.md — must include a disclosure route.
- SUPPORT.md — must route questions away from the issue tracker.
- GOVERNANCE.md — must describe actual operation, decision authority, and how outsiders gain responsibility.
- MAINTAINERS.md — named maintainers with areas.
- Contributor ladder — responsibilities, privileges, requirements, promotion and removal process per rung, including paths for non-code contributors.

## Community Health Score

Ten weighted dimensions summing to 100: funnel health 15, responsiveness 15, standards presence 10, contribution opportunities 10, governance and ladder 10, review experience 10, contributor retention 10, maintainer sustainability 10, Q&A support 5, recognition and automation 5.

Tiers: ≥85 healthy; 70–84 developing; <70 at risk. Every score carries an evidence label per `metrics.md`; an unlabeled score is UNVERIFIED. A failing community gate forces FAIL regardless of the Community Health Score.


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


## Evidence labels

- **Observed**: a human or agent actually executed the path from a clean or representative environment.
- **CI-observed**: automation executed the product steps; may undercount human reading/signup time.
- **Estimated**: steps analyzed but not executed.
- An estimate can never prove a PASS. A metric without an evidence label is UNVERIFIED.


## Gate identifiers

| Gate constant | Severity | Fails when |
|---|---|---|
| `BROKEN_QUICKSTART` | P1 | magic path exceeds `MAGIC_PATH_MAX_MIN`, no reproducible end-to-end quickstart exists, or manual approval/support is required with no sandbox route |
| `NON_REPRODUCIBLE_BUILD` | P1 | a clean checkout cannot reach the productive state within `LOCAL_DEV_MAX_MIN` using only committed instructions/automation |
| `UNEXPLAINED_ERROR` | P1 | a public, expected error lacks what happened / why / where / how to fix / retry-safety, or a support-correlation identifier |
| `UNDOCUMENTED_BREAKING_API` | P0 | a breaking API/CLI/config change ships without changelog entry and migration guidance |
| `SDK_API_DRIFT` | P1 | a released official SDK is missing operations or contradicts the canonical API |
| `UNTESTED_SUPPORTED_VERSION` | P1 | a version/platform is claimed supported without CI or equivalent evidence |
| `STALE_PUBLIC_REFERENCE` | P1 | generated reference observably disagrees with current behavior |
| `UNSAFE_EXAMPLES` | P1 | security-sensitive examples encourage unsafe credential handling |
| `BROKEN_CANONICAL_INSTALL` | P1 | canonical install/auth path is broken |
