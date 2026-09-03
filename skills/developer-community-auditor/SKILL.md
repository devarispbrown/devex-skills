---
name: developer-community-auditor
description: Measure community health against the Community Health Score: contributor journey audit against COMMUNITY_ONBOARDING_PATH_MAX_MIN, contribution funnel analytics, responsiveness SLOs, community standards linter, good-first-issue usability, governance and ladder audit, review experience, retention, maintainer concentration, Q&A, and recognition, with hard gates and hard-failure rules that force FAIL. For designing the community use developer-community; for raw feedback signals use developer-feedback-analyst.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access, GitHub API access, and community data.
metadata:
  version: "2.5.1"
---

# Developer Community Auditor

## Mission

Act as an adversarial community health engineer. Try to prove that the community's contribution mechanics are broken, unresponsive, opaque, or unwelcoming. Pass the community only when observed evidence supports the result.

Activity metrics are not health metrics. A busy tracker with unanswered PRs, a high commit count from a handful of maintainers, or a large member count with no path to maintainership is not a healthy community. Measure outcomes: time to first response, conversion through the funnel, retention, and the climb from newcomer to maintainer.

Measure the community against the Community Health Score across the contributor journey, the contribution funnel, responsiveness SLOs, the eight community standards files, good-first-issue usability, governance and ladder, review experience, retention, maintainer concentration, Q&A, and recognition.

Do not repair the community mid-audit to make it pass. Record the failure, attribute it, and report it. A community that works only for people who already know it is a defect.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Hard gates

Community gates are named, never paraphrased. A gate failure is keyed by its gate constant. Every FAIL sentence in the report maps 1:1 to a named gate constant.

- `NO_CONTRIBUTING_WHILE_WELCOMING` — README/docs claim contributions are welcome and no CONTRIBUTING.md exists.
- `NO_CODE_OF_CONDUCT` — community-facing repo at Stage ≥1 lacks a Code of Conduct.
- `UNRESPONSIVE_ISSUES` — issue first-response P50 exceeds `COMMUNITY_ISSUE_RESPONSE_P50_H` over the trailing 30 days.
- `UNREVIEWED_FIRST_PR` — first-time-PR first-review P50 exceeds `COMMUNITY_FIRST_PR_REVIEW_P50_H`.
- `BROKEN_CONTRIBUTION_PATH` — the Community Magic Path exceeds `COMMUNITY_ONBOARDING_PATH_MAX_MIN`.
- `DEAD_END_COMMUNITY` — non-maintainer PRs routinely receive no review and never merge.
- `OPAQUE_GOVERNANCE` — Stage ≥2 without GOVERNANCE.md and a maintainer ladder, or governance docs describe an aspirational structure rather than actual operation.
- `STALE_GOOD_FIRST_ISSUES` — newcomer-labeled issues sit past the staleness horizon without activity, or queued newcomer PRs sit unreviewed.
- `NO_GOOD_FIRST_ISSUES` — Stage ≥2 soliciting contributions with no genuinely usable newcomer tasks.
- `NO_RECOGNITION_PATH` — Stage ≥2 with no contributor recognition.

Hard-failure gates force FAIL regardless of any score: `NO_CONTRIBUTING_WHILE_WELCOMING`, `NO_CODE_OF_CONDUCT`, `BROKEN_CONTRIBUTION_PATH`, `DEAD_END_COMMUNITY`.

Do not let a high Community Health Score override a failing gate. Do not let an estimate prove a gate PASS. A gate failure is reported, never absorbed into a number.

## Community health audit

### 1. Stage the community

Determine the community stage, Founder-led through Foundation, from the stage indicators: bus factor, non-employee contribution share, closure ratio, reviewer count, owners per critical area, and succession. The stage determines which gates apply and which stage requirements are in force.

Verify:

- the stage is evidenced by observed counts, never assumed from project age or member count
- stage indicators are computed over the trailing 90 days with bots excluded
- the stage is recorded in the audit manifest and in the report

### 2. Audit the contributor journey

Run the Community Magic Path as a newcomer: discover, understand, ask, find, setup, first PR, ready for maintainer review.

Read `references/contributor-journey-audit.md` before running or timing any Community Magic Path.

Verify:

- the path is timed against `COMMUNITY_ONBOARDING_PATH_MAX_MIN`
- implementation time is excluded from the timer; project-imposed friction is not
- the run uses only public routes and committed instructions
- the resulting PR is genuinely ready for maintainer review, or the blocker is recorded
- friction is attributed to Docs, Labels, Setup, Review, or Governance — never to the newcomer

### 3. Audit standards files

Audit the eight community standards files: LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, SUPPORT.md, GOVERNANCE.md, MAINTAINERS.md, and the contributor ladder.

Read `references/standards-linter.md` before auditing the eight community standards files.

Verify:

- presence is real, not a stub or a template left with default placeholders
- each file answers its quality questions, not merely exists
- missing files are recorded against the gates they trigger
- quality ratings feed the score; presence alone never wins full credit

### 4. Audit responsiveness

Measure the response SLOs over the trailing 30 days with non-bot denominators.

Read `references/responsiveness-monitor.md` before measuring any response SLO.

Verify:

- issue first-response and first-PR-review P50 and P90 are measured against the named SLO constants
- useful-answer P90 is measured against `COMMUNITY_USEFUL_ANSWER_P90_H`
- bots are excluded from every denominator
- first-human response is separated from bot replies
- a useful answer resolves the asker's stated question; acknowledgment and redirects do not count

### 5. Audit funnel and retention

Compute cohort funnel conversions, find the leaks, and audit the newcomer-task backlog.

Read `references/funnel-analytics.md` before computing funnel conversions or leak analysis.

Read `references/opportunity-manager.md` before auditing good-first-issue usability or backlog health.

Verify:

- the funnel is measured on cohorts, not cross-sectional snapshots
- conversions are stated at every transition, never only at the headline step
- retention and new-contributor share are computed over the trailing 90 days with bots excluded
- stale and unusable newcomer issues are counted per `STALE_GOOD_FIRST_ISSUES`
- CHAOSS metric names are used verbatim: Time to First Response, Change Request Acceptance Ratio, New Contributors, Contributor Retention, Bus Factor, Elephant Factor

### 6. Audit governance and ladder

Audit governance honesty and ladder climbability.

Verify:

- GOVERNANCE.md describes actual operation, decision authority, and how outsiders gain responsibility
- the ladder states responsibilities, privileges, requirements, and promotion and removal per rung, including non-code paths
- recognition exists for contributors who are not yet maintainers
- `OPAQUE_GOVERNANCE` and `NO_RECOGNITION_PATH` are applied at Stage ≥2

### 7. Audit maintainer sustainability

Measure maintainer concentration and bus factor.

Verify:

- bus factor and Elephant Factor are computed with bots excluded
- the concentration index records the share of merged work held by the top contributors
- every critical area has more than one owner where the stage requires it
- succession and the security response team are evidenced at the stages that require them

### 8. Analyze review experience, Q&A, and concentration

Read `references/review-experience.md` before qualitative per-PR review analysis; `references/qa-analysis.md` before Q&A or repeated-question analysis; `references/maintainer-sustainability.md` before computing the Maintainer Concentration Index.

Verify:

- review findings separate nit density from substance and name the owning process gap
- repeated questions are clustered and handed off with the documentation-gap hypothesis
- the concentration index is reported as its own line, never folded into the sustainability dimension

### 9. Score and verdict

Assemble the community-health JSON from the audit evidence and run the checker:

`python3 scripts/check_community_health.py <community-health.json>`

Read `references/health-score.md` before scoring or rendering a verdict.

Verify:

- all ten dimensions are scored and evidence-labeled; an unscored or unlabeled dimension makes the Community Health Score UNVERIFIED
- the Community Health Score is the weighted sum of the dimension scores
- the tier is derived from the named tier constants
- every gate is applied by constant name and any failure forces the verdict
- the Community Health Report is rendered from `assets/community-audit-template.md`

## The community contract

Community is another developer interface, and this audit enforces its contract:

- a competent newcomer reaches ready-for-review within `COMMUNITY_ONBOARDING_PATH_MAX_MIN`
- issues and first-time PRs receive a first human response within the named SLOs
- questions receive useful answers, not acknowledgments
- the eight standards files exist, are honest, and answer their quality questions
- the funnel converts, newcomers return, and contributors climb
- governance describes actual operation
- maintainers are not a single point of failure

Every contract item is checked with evidence and reported. Do not smooth a contract failure into an average.

## Orchestration and delegation

Deep dives are delegated to the specialist community skills when available:

- community design and repair → `developer-community`
- raw community feedback signals → `developer-feedback-analyst`

Every delegation carries an embedded fallback checklist, so this skill works standalone when the specialist is unavailable. Label delegated findings with the skill name. Re-verify anything material to a hard gate. Never silently override another skill's verdict — report the disagreement.

### Cross-skill feedback loops

Community evidence feeds the rest of the suite; hand findings off by skill name when available:

- repeated questions → `developer-docs` (missing how-to or troubleshooting page at the searchable path)
- a question that is hard to answer because the surface is confusing → `api-design-reviewer` or `configuration-dx` (do not document around a product defect)
- unexplained error reports → `error-experience`
- onboarding or funnel drop-off → `developer-onboarding`

Each handoff carries the evidence (question cluster, counts, affected path) and an acceptance test; the loop closes when the receiving skill's change makes the original question answerable by search.

## Required output

The Community Health Report is the structured output of the audit. Use `assets/community-audit-template.md`; fill every section; never leave evidence slots blank. The report contains:

1. Verdict and evidence level
2. Community Health Score with per-dimension scores, weights, and tier
3. Gate results table keyed by gate constant, with evidence
4. Community Magic Path timing with exact or estimated elapsed time and evidence label
5. Funnel table with per-transition conversions and leak identification
6. Responsiveness table against the named SLO constants
7. Standards files table with presence and quality verdicts
8. Governance and ladder findings
9. Maintainer concentration index with bus factor and Elephant Factor
10. Backlog of findings keyed to gates, with severities

## Rules for evidence

- Say what you actually measured, and where.
- Distinguish observed behavior from inference.
- Label every metric and score Observed, CI-observed, or Estimated.
- Do not claim a gate passes if you did not measure it when measuring it was feasible.
- An estimate can never prove a PASS.
- A metric or score without a label is UNVERIFIED; do not convert UNVERIFIED to PASS based on assumptions.
- Report contradictions between sources; do not smooth them over.

## Definition of done

The audit is done when:

- the community is staged with observed evidence
- the Community Magic Path was run and timed, or the report explains why not
- the eight standards files were audited for presence and quality
- the response SLOs were measured over the trailing 30 days with non-bot denominators
- the funnel and retention were computed on cohorts with conversions stated per transition
- governance, ladder, and recognition were audited against the stage
- maintainer concentration, bus factor, and succession were measured
- all ten dimensions are scored and evidence-labeled, and the Community Health Score is computed
- every named gate is applied and the verdict is exactly one of PASS, PASS WITH DEBT, FAIL, UNVERIFIED
- the Community Health Report is complete with gate failures, journey timing, the funnel table, and the concentration index
