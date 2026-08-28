# Contribution Funnel Analytics

## Cohort principle

Measure the funnel on cohorts, not cross-sectional snapshots. A cohort is the set of participants who entered the community in the same trailing window. Report conversion per cohort; never average cohorts together.

## Funnel stages

The eight measured cohort stages map onto the twelve-step contribution journey. Each stage has an owning artifact:

1. **participant** — discovered the project and its contribution route (README).
2. **contributor** — engaged past discovery: read the guide, asked, or found work (CONTRIBUTING, SUPPORT, labels).
3. **first PR** — opened a first pull request (templates).
4. **merged** — first PR merged (merge policy, review SLA).
5. **second contribution** — made a second contribution (recognition).
6. **regular** — contributing at least monthly (reviewer path).
7. **reviewer** — reviewed another contributor's work (ladder).
8. **maintainer** — gained maintainer responsibilities (governance).

## Conversion calculation

For each transition, conversion is: cohort members who reached the later stage divided by cohort members who reached the earlier stage. State the numerator and denominator explicitly. Never report a headline conversion without the per-transition table.

Record the funnel in the fixture-compatible shape: participants, contributors, first_prs, merged, second_contributions, regulars, reviewers, maintainers.

## Leak detection

For every transition, classify the leak:

- **Drop-off** — members who stopped; expected unless unexplained.
- **Bottleneck** — a stage whose conversion is far below its neighbors; inspect the owning artifact before proposing a fix.
- **Dead end** — members who reach a stage and can never progress; this is a gate condition, not a leak.

Flag any transition below the closure-ratio target or below the project's own prior cohorts. A funnel that shows participants but no first PRs points at the newcomer-task backlog; audit it per the opportunity-manager procedure.

## Health indicators

- Activation: participants to first PR.
- Acceptance: first PR to merged, against the closure-ratio target.
- Return: merged to second contribution.
- Participation: regular to reviewer.
- Ladder: reviewer to maintainer.

Report each indicator with its cohort window and evidence label.

## Retention

Retention is the share of the prior window's contributors active in the current window, bots excluded. New-contributor share is new contributors divided by unique contributors in the window. Report both over the trailing 90 days and label the evidence.

## CHAOSS naming

Cite community metrics by their CHAOSS names, never by paraphrase: Time to First Response, Change Request Acceptance Ratio, New Contributors, Contributor Retention, Bus Factor, Elephant Factor. Verify names against chaoss.community while authoring.
