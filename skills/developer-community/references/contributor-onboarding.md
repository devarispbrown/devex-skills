# Contribution System Design Procedure

## The eight standards files

Each file has presence AND quality requirements. Design them in this order:

1. **CONTRIBUTING.md** — the contribution manual. Must answer, in order: how to find work, how to set up, how to run tests, what an acceptable PR is, how review works, how long review takes, who can help, how decisions are made, how to become more involved. State the canonical test command. A CONTRIBUTING.md that cannot be executed from a clean clone is a P1 defect.
2. **CODE_OF_CONDUCT.md** — a report route and an enforcement commitment. A CoC without a report route or without enforcement consequences fails its quality question.
3. **SECURITY.md** — a disclosure route. State the private channel and what happens after a report.
4. **SUPPORT.md** — routes questions away from the issue tracker. Name the community channels; say explicitly that support questions do not belong in issues.
5. **GOVERNANCE.md** — actual operation, decision authority, how outsiders gain responsibility. Design per `references/governance-models.md`.
6. **MAINTAINERS.md** — named maintainers with areas. Handles and areas, current, not a historical roster.
7. **Contributor ladder** — responsibilities, privileges, requirements, promotion and removal process per rung, including non-code paths.

## Newcomer issue quality

An issue is usable by a newcomer only when it states all of:

- **context** — why the problem matters, with links
- **outcome** — what "done" looks like
- **scope** — what is in and out of bounds
- **files** — where the change lives
- **acceptance** — the observable acceptance criterion
- **how to test** — the exact command to verify
- **difficulty** — an honest difficulty label
- **helper** — a named person to ask

An issue missing acceptance criteria or how-to-test is not first-timer-sized, however small the code change. Labeling it `good first issue` anyway is a `NO_GOOD_FIRST_ISSUES` defect.

## Staged setup guidance

- Stage 0: ship the minimum four — CONTRIBUTING.md, CODE_OF_CONDUCT.md, issue/PR templates, documented dev environment. Do not gold-plate.
- Stage 1: add the labeling procedure and triage. Keep labeled issues fresh; a stale labeled issue is `STALE_GOOD_FIRST_ISSUES`.
- Stage 2: add GOVERNANCE.md, the ladder, and recognition.
- Stage 3 and up: add analytics, delegation, and moderation.

Never add Stage 3 machinery to a Stage 0 project. The stage gates what must exist, and also what may be deferred.

## Community magic path

Design the path from discover to ready-for-review against `COMMUNITY_ONBOARDING_PATH_MAX_MIN`. Implementation time is excluded; every project-imposed step — signing up, configuring, waiting, asking — counts.

Walk the path from a clean clone with only committed instructions. When the path exceeds the budget, fix the repository; never move friction into "prerequisites".
