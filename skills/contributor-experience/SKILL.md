---
name: contributor-experience
description: Make first meaningful open-source contribution take under 30 minutes: fork, clone, build, test, find issue, change, checks, PR, review, merge. Audit CONTRIBUTING, CODEOWNERS, issue/PR templates, good-first-issue, dev environment, fixtures, DCO/CLA, review expectations, and whether make test matches CI. For the local setup itself use local-development.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with git and repository access.
metadata:
  version: "2.9.1"
---

# Contributor Experience Audit and Repair

## Mission

The first meaningful contribution is the product's open-source funnel. Every future contributor, reviewer, and maintainer enters through it; a blocked funnel caps the community at the size of the founding team.

Treat the fork-to-merge path as a product with its own SLA. Measure it, find the friction, and repair the repository so a brand-new contributor with no project-specific knowledge goes from fork to a PR-ready change quickly and to a merged change predictably.

Fix the repository, do not document around it. When setup, checks, or guidance make contribution hard, repair the automation and the files instead of adding longer READMEs.

The local setup itself — toolchain, dependencies, services, fixtures, hot reload — belongs to the `local-development` skill if available. This skill audits the funnel around that setup; it does not duplicate it. For whole-product journey measurement use `developer-experience-auditor` if available, and for designing onboarding journeys use `developer-onboarding` if available.

Read `references/contributor-journey.md` when walking the fork-to-merge path step by step.

Read `references/guidance-files.md` when auditing CONTRIBUTING, CODEOWNERS, issue/PR templates, good-first-issue labeling, or DCO/CLA.

Read `references/check-parity.md` when verifying that local checks match CI.

Read `references/review-experience.md` when measuring review responsiveness and first-time-contributor friendliness.

Read `references/funnel-fixes.md` when repairing funnel defects found by the audit.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Hard target: first contribution within FIRST_CONTRIBUTION_TARGET_MIN

A brand-new contributor with no prior project knowledge must go from fork to a first PR-ready change within `FIRST_CONTRIBUTION_TARGET_MIN`, using only committed instructions and automation.

This is a target, not a hard gate: landing inside the target is the goal, exceeding it is a PASS WITH DEBT signal, and exceeding it substantially is a P2 defect per `references/standards.md`.

The timer starts at the fork and stops when the change is PR-ready: the change is made, local checks pass, and CI runs the same checks. The contributor journey after PR-ready — review and merge — is measured separately and reported per stage.

Do not move repository friction into "contributor prerequisites". A requirement the repo cannot verify is a defect, not a prerequisite.

The repo's contribution guidance must make the journey walkable from a clean clone using only committed instructions. Any step that lives only in a maintainer's memory is a `NON_REPRODUCIBLE_BUILD` gate failure.

## Contributor experience workflow

### 1. Audit the contributor journey

Read `references/contributor-journey.md`.

Walk each stage of the journey — fork, clone, build, test, find issue, change, checks, PR, review, merge — against the target repository exactly as a first-time contributor would.

Verify:

- build and test succeed from a clean clone using only committed instructions
- each stage's friction is recorded with per-stage timing and an evidence label
- the contributor can verify a change locally with the same checks CI runs
- fixtures or seed data exist where the tests or examples need them

Do not average stages. Report per stage; the bottleneck is the longest stage, not the mean. If the local setup fails a clean-clone check, hand the setup repair to the `local-development` skill if available before continuing.

### 2. Audit repo guidance files

Read `references/guidance-files.md`.

Run `scripts/check_contributor_funnel.py <repo>` as a first-pass inventory signal. The script is heuristic; verify each finding in the files themselves.

Verify:

- CONTRIBUTING.md exists and answers how to run tests, how to make a change, and what review expects
- CODEOWNERS covers the change paths and is current
- issue and PR templates exist, are current, and match the repo's actual workflow
- DCO/CLA is stated, enforceable, and its bot check is enabled
- the good-first-issue labeling procedure is documented

Never accept a CONTRIBUTING.md that points at tribal knowledge or an unreachable setup.

### 3. Audit issue discoverability

Read `references/guidance-files.md` for the labeling procedure.

Verify:

- good-first-issue issues are small, self-contained, and free of internal jargon
- each labeled issue has a clear acceptance criterion
- labeled issues are fresh, not stale triage backlog
- the label is discoverable from the README or CONTRIBUTING

Do not count a label as a signal when the underlying issues are not first-timer-sized.

### 4. Audit check parity (local make test vs CI)

Read `references/check-parity.md`.

Verify:

- the canonical local check command exists (Makefile `test` target or package.json `test` script) and runs green from a clean clone
- CI runs the same command, the same versions, and the same failure conditions
- no check passes locally and fails in CI, or vice versa

Do not accept "CI is green" as evidence that the contributor's local check is green. Drift between the two is a parity defect, not an environment quirk.

### 5. Audit review responsiveness

Read `references/review-experience.md`.

Verify:

- review expectations are documented: who reviews, how fast, what happens on disagreement
- first-response time and time-to-merge are measured on real PRs with evidence labels
- first-time contributors get a constructive, welcoming review
- there is a path from first contribution to reviewer or maintainer

Do not label a repo "responsive" from maintainer claims. Sample actual PR history.

### 6. Fix the funnel

Read `references/funnel-fixes.md`.

Prioritize by severity vocabulary from `references/standards.md`. Fix in this order:

1. check parity — a contributor who cannot verify their change locally is blocked at the widest point
2. guidance and templates — a missing or wrong CONTRIBUTING costs every contributor
3. discoverability — small first issues unblock the first contribution specifically
4. review responsiveness — merge latency caps the funnel's throughput

Implement each fix with an acceptance test: the repair is done when a fresh walk of the stage passes. Never claim a fix without re-running the affected journey step.

## CONTRIBUTING contract

CONTRIBUTING.md is the canonical contribution guide. It must answer, in order:

1. how to set up the environment and run the checks
2. how to find an issue to work on, including the good-first-issue procedure
3. how to make and verify a change
4. what CI will run and what the PR must contain
5. review expectations: who reviews, how long, what the process is
6. DCO/CLA requirements and how to satisfy them

A missing CONTRIBUTING.md is a P1 defect. A CONTRIBUTING.md that is stale, contradicts the repo, or cannot be executed is a P1 defect. A CONTRIBUTING.md that omits the DCO/CLA requirement is a P2 defect.

## Issue and template contract

The issue surface is the contributor's first product interaction:

- bug and feature templates exist, are current, and collect the information reviewers need
- a bug template must elicit reproduction steps and environment
- a PR template must elicit the change summary, test evidence, and checklist
- good-first-issue issues are first-timer-sized: small scope, clear acceptance criterion, no blockers
- the DCO/CLA requirement is enforced by automation, not by memory

A missing PR template is a P2 defect. A bug template without reproduction steps is a P2 defect. Labeled issues that are not first-timer-sized are a P2 defect.

## Check-parity contract

The contributor's local checks and CI must be the same product:

- same commands: the canonical local test command is what CI runs
- same versions: the CI toolchain versions match the documented local ones
- same failures: a green local run predicts a green CI run
- any divergence between local and CI results is a parity defect: P1 when it blocks the contributor, P2 when it only causes re-runs
- when the documented local check command does not appear in CI configuration at all, a green local run predicts nothing and the release fails `UNVERIFIABLE_CI_PARITY`

Never treat a passing CI as a substitute for a passing local check.

## Required output

For every audit, produce the contributor experience report using `assets/contributor-report-template.md`.

The report must contain:

1. **Journey timing** — per-stage times for the fork-to-merge journey, each with an evidence label
2. **Funnel findings** — each finding with severity, evidence, and affected stage
3. **Fix list** — prioritized fixes, each with an acceptance test and owner type

## Definition of done

A contributor experience audit is done when:

- the journey is walked end to end and every stage carries a labeled measurement
- every funnel finding carries a severity and an evidence label
- check parity is verified against actual local and CI commands
- review responsiveness is measured on real PR history, not claims
- the report is rendered from `assets/contributor-report-template.md` with journey timing, findings, and a fix list
- no numeric threshold is restated in the report; the canonical constants are cited by name
- fixes are implemented with acceptance tests that re-run the affected stage

Hand off the local setup repair to `local-development` if available, onboarding design to `developer-onboarding` if available, and whole-product journey measurement to `developer-experience-auditor` if available. This skill owns the contributor funnel; it does not replace any of them.
