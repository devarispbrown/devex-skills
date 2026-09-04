---
name: developer-community
description: Design and operate an open-source contribution system: governance models, contributor onboarding, participation loops, recognition programs, community operations, and the discover-to-maintainer funnel with stage-aware gates from Stage 0 founder-led to Stage 4 foundation-scale, grounded in CHAOSS metrics and CNCF governance templates with GitHub as the operating surface. For measuring existing community health use developer-community-auditor; for the single first contribution use contributor-experience.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and community data.
metadata:
  version: "2.7.0"
---

# Developer Community Design and Operations

## Mission

Community is a developer interface. A repository with hostile contribution mechanics, unanswered PRs, opaque governance, or no path to maintainership has poor developer experience no matter how good the code is. Design participation as deliberately as you design an API.

This skill designs and operates the full contribution system: governance models, contributor onboarding, participation loops, recognition programs, community operations, and the discover-to-maintainer funnel with stage-aware gates from Stage 0 founder-led to Stage 4 foundation-scale.

Ground every design in the canonical community vocabulary:

- the 12-step funnel and its owning artifacts
- the response SLOs, cited by constant name: `COMMUNITY_ISSUE_RESPONSE_P50_H`, `COMMUNITY_FIRST_PR_REVIEW_P50_H`, `COMMUNITY_USEFUL_ANSWER_P90_H`
- the community magic path budget, cited as `COMMUNITY_ONBOARDING_PATH_MAX_MIN`
- the stage gates and hard gates by constant name: `NO_CONTRIBUTING_WHILE_WELCOMING`, `NO_CODE_OF_CONDUCT`, `BROKEN_CONTRIBUTION_PATH`, `DEAD_END_COMMUNITY`, `OPAQUE_GOVERNANCE`, `STALE_GOOD_FIRST_ISSUES`, `NO_GOOD_FIRST_ISSUES`, `NO_RECOGNITION_PATH`, `UNRESPONSIVE_ISSUES`, `UNREVIEWED_FIRST_PR`

Never restate numeric thresholds in designs; cite constants by name. Measure against CHAOSS metrics, cited by name: `Time to First Response`, `Change Request Acceptance Ratio`, `New Contributors`, `Contributor Retention`, `Bus Factor`, `Elephant Factor`. Take governance structure from CNCF templates; do not invent governance from scratch.

Do not hand a project a stack of documents. Hand it a designed system: every funnel step has an owner, an artifact, and an acceptance criterion.

For measuring existing community health use the `developer-community-auditor` skill if available. For the single first contribution use the `contributor-experience` skill if available. This skill designs the system; it does not duplicate measurement.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Community is an interface

The contribution funnel is the community's API. Twelve steps, each with one owning artifact. A step with no artifact, no owner, or no acceptance criterion is a defect in the interface.

1. **Discover** — the README is the landing page; it must state what the project is and invite contribution.
2. **Understand** — CONTRIBUTING.md is the manual; it must answer the nine questions: find work, setup, tests, acceptable PR, review process, review time, who can help, decisions, more involvement.
3. **Ask** — SUPPORT.md and chat must route questions before they become issues.
4. **Find** — labels must surface genuinely usable newcomer tasks; stale labels are worse than none.
5. **Setup** — the documented dev environment must work from a clean clone.
6. **First PR** — issue and PR templates must elicit what review needs.
7. **Review** — the review SLA is a contract; `COMMUNITY_FIRST_PR_REVIEW_P50_H` is the floor, never the aspiration.
8. **Accepted** — merge policy must be stated; a PR that never merges is a dead end (`DEAD_END_COMMUNITY`).
9. **Return** — recognition must bring contributors back (`NO_RECOGNITION_PATH`).
10. **Review others** — a documented reviewer path converts contributors into reviewers.
11. **Own area** — the ladder converts reviewers into owners.
12. **Maintainer** — governance converts owners into maintainers with decision authority.

Design the funnel against the community magic path: a competent developer goes from discovering the contribution process to producing a valid contribution ready for maintainer review within `COMMUNITY_ONBOARDING_PATH_MAX_MIN`. Implementation time is excluded; project-imposed friction is not.

## Community design workflow

### 1. Determine the community stage

Read `references/stage-planning.md` when detecting the stage from ratio indicators.

Run `scripts/scan_community_surface.py <repo> --stage <N>` as a first-pass inventory signal. The script is heuristic; verify each finding in the files themselves.

Verify:

- the stage is detected from ratio indicators — bus factor, non-employee contribution share, closure ratio, multiple reviewers and owners, succession — not from ambition
- the stage gates what must be designed, never what the project wishes it were
- evidence is labeled; an unlabeled stage is UNVERIFIED

Do not design a Stage 2 system for a Stage 0 project. Never leave a Stage 2 project without governance and a ladder (`OPAQUE_GOVERNANCE`).

### 2. Design the contribution system

Read `references/contributor-onboarding.md` when designing the eight standards files and newcomer issues.

Design the eight files — LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, SUPPORT.md, GOVERNANCE.md, MAINTAINERS.md, and the contributor ladder — each against its presence and quality questions.

Verify:

- CONTRIBUTING.md answers the nine questions in order and states the canonical test command
- CODE_OF_CONDUCT.md states a report route and an enforcement commitment
- SECURITY.md states a disclosure route; SUPPORT.md routes questions away from the issue tracker
- newcomer issues carry context, outcome, scope, files, acceptance criteria, how to test, difficulty, and a helper name
- the system is walkable from a clean clone using only committed instructions

Do not design a contribution system that only founders can navigate.

### 3. Design governance and the ladder

Read `references/governance-models.md` when choosing the governance model and designing the ladder.

Choose a stage-appropriate model — benevolent dictator, maintainer council, or foundation — and design the ladder with responsibilities, privileges, requirements, and promotion and removal process per rung, including non-code paths.

Verify:

- governance describes actual operation and decision authority, never an aspirational structure
- outsiders have a documented path to responsibility
- decisions are recorded in decision records, not maintainer memory
- the ladder has promotion criteria and a removal process, not just titles
- foundation governance and succession are designed before Stage 4 is claimed

### 4. Design participation loops

Read `references/participation-loops.md` when designing loops beyond code.

Design loops for triage, support, docs, testing, design, and events — each with an owner, a channel, and a cadence.

Verify:

- every loop has a named owner and a failure signal
- non-code contribution paths feed the ladder, not a dead end
- no loop depends on one person; each has a rotation or a deputy

Do not design loops that go silent when the founder is busy.

### 5. Design recognition

Read `references/recognition-programs.md` when designing recognition.

Design recognition for code and non-code labor: first-PR recognition, reviewer promotion, and release acknowledgements.

Verify:

- non-code labor is credited on the same footing as code
- recognition is immediate enough to affect retention
- logistics are automated; appreciation is human

Never automate the appreciation itself. A bot-generated thank-you is noise that devalues real recognition.

### 6. Plan community operations

Read `references/community-operations.md` when planning triage, moderation, meetings, telemetry, and maintainer sustainability. Read `references/community-tooling.md` when choosing the tooling stack (GitHub, CHAOSS, GrimoireLab, Bitergia, Common Room). Read `references/community-automation.md` when designing automation.

Design the operations plan: triage procedures, moderation policy, meeting cadence, community telemetry, and maintainer sustainability practices. Select the tooling stack per the matrix; automation serves named gates and SLO constants.

Verify:

- triage has a response path against `COMMUNITY_ISSUE_RESPONSE_P50_H`
- moderation exists before it is needed, at Stage 1 or earlier
- telemetry covers the CHAOSS metrics the stage requires
- delegation and concentration reduction are concrete, not intentions
- every automation maps to a named gate or SLO constant, has a kill switch, and never substitutes for human appreciation

## Community automation

Automate logistics, never appreciation. The playbook (welcome, routing, repro detection, unanswered-question digests, stale-PR nudges, SLO-breach prompts, milestone recognition, reviewer-eligibility nomination) lives in `references/community-automation.md`. A bot may report "Tests failing: integration/postgres"; a maintainer says "Thanks for working through this."

## Community feedback loops

Community signals feed the rest of the suite. Repeated questions indicate a documentation gap (`developer-docs`); questions that are hard to answer because the surface is confusing indicate a product defect (`api-design-reviewer`, `configuration-dx`); unexplained error reports feed `error-experience`. Hand off with the evidence cluster and an acceptance test.

## Governance contract

- governance documentation describes how the project actually operates: who decides what, and how outsiders gain responsibility
- the model is stage-appropriate — founder-led, council, or foundation — chosen per `references/governance-models.md`
- the ladder defines responsibilities, privileges, requirements, and promotion and removal process per rung, including non-code paths
- decisions are recorded in decision records, not in maintainer memory
- `OPAQUE_GOVERNANCE` is a P1 failure: Stage 2 or higher requires GOVERNANCE.md and a maintainer ladder describing actual operation

## Recognition contract

- every contribution path has a recognition path; `NO_RECOGNITION_PATH` is a P2 failure at Stage 2 or higher
- first-PR contributors are recognized at first merge
- reviewers are promoted along a documented path
- non-code labor — triage, docs, testing, design, events — is credited like code
- release acknowledgements credit all contributors, not just committers
- logistics — tokens, labels, lists — are automated; appreciation is written by a person

## Contribution-system contract

- the eight standards files exist with their quality signals, staged by community stage
- CONTRIBUTING.md answers the nine questions and states the canonical test command
- CODE_OF_CONDUCT.md has a report route and an enforcement commitment
- SECURITY.md has a disclosure route; SUPPORT.md routes questions away from issues
- GOVERNANCE.md describes actual operation and advancement; MAINTAINERS.md names maintainers with areas
- the ladder covers responsibilities, privileges, requirements, promotion, and removal, including non-code paths
- newcomer issues are genuinely usable: context, outcome, scope, files, acceptance, how to test, difficulty, helper
- the community magic path is designed against `COMMUNITY_ONBOARDING_PATH_MAX_MIN`
- response SLOs are set by constant name and monitored at the stage that requires them

## Required output

For every community design, produce the community design plan using `assets/community-plan-template.md`.

The plan must contain:

1. **Stage** — detected stage with labeled evidence
2. **Funnel design** — the 12 steps, each with its owning artifact and acceptance criterion
3. **Governance model** — model, decision authority, decision records, outsider advancement
4. **Ladder** — rungs with responsibilities, privileges, requirements, promotion and removal
5. **Recognition program** — first-PR, reviewer, release acknowledgements, non-code credit
6. **Operations plan** — triage, moderation, meetings, telemetry, sustainability practices

## Definition of done

A community design is done when:

- the stage is determined from ratio indicators with labeled evidence
- every funnel step has an owning artifact and an acceptance criterion
- the eight standards files are designed against their quality questions
- the governance model is stage-appropriate and the ladder includes promotion and removal
- recognition covers code and non-code contributions
- the operations plan names owners and failure signals for every loop
- no numeric threshold is restated; canonical constants are cited by name
- the plan is rendered from `assets/community-plan-template.md` with all six sections
