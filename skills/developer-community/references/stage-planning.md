# Stage Planning Procedure

## Detect the stage

Stages gate requirements, not scores. Detect the stage from ratio indicators measured over a trailing 90-day window, counting unique human authors with bots excluded:

- Stage 0 **Founder-led** — bus factor below 2.
- Stage 1 **Early community** — bus factor at least 2, non-employee contribution share growing.
- Stage 2 **Growing** — closure ratio at least 0.7, multiple reviewers.
- Stage 3 **Scale** — multiple owners per critical area.
- Stage 4 **Foundation** — succession defined.

Procedure:

1. Compute each indicator with an evidence label from repository data.
2. Take the highest stage whose indicators all hold.
3. Treat missing data as UNVERIFIED, never as a pass.
4. Recheck on a cadence; the stage is a moving target.

Measure the indicators with CHAOSS definitions by name: `Bus Factor`, `Change Request Acceptance Ratio`, `New Contributors`, `Contributor Retention`, `Elephant Factor`.

## What to build at each stage

- Stage 0: CONTRIBUTING.md, CODE_OF_CONDUCT.md, issue/PR templates, documented dev environment. One owner; founder decisions; overhead near zero.
- Stage 1: response SLO monitoring, good-first-issue labels with a labeling procedure, triage process. Response SLOs are monitored by constant name.
- Stage 2: GOVERNANCE.md describing actual operation, a maintainer ladder with promotion and removal, a recognition program.
- Stage 3: contributor analytics, delegation, moderation, CoC enforcement. Multiple owners per critical area.
- Stage 4: foundation governance, security response team, succession defined.

Do not add Stage 3 machinery to a Stage 0 project. Do not defer Stage 2 essentials — governance, ladder, recognition — because they are the difference between a community and a following.

## Promotion criteria

Design promotion into the ladder before Stage 2:

- promotion criteria per rung are objective, written, and observable
- the removal process exists and is fair
- non-code paths reach the same rungs as code paths
- every critical area has a successor before Stage 4 is claimed

Never promote by tenure alone. Never remove without a recorded process.

## Cross-check

Map every design decision to the stage requirement that justifies it. The gates `OPAQUE_GOVERNANCE`, `NO_GOOD_FIRST_ISSUES`, `NO_RECOGNITION_PATH`, and `STALE_GOOD_FIRST_ISSUES` are keyed by constant name; cite them when a design decision touches their territory.
