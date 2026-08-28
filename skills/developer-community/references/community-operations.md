# Community Operations Planning

## Triage procedures

- Every new issue receives a first human response within the issue-response SLO; design against `COMMUNITY_ISSUE_RESPONSE_P50_H` as the floor and plan for the P90 as well.
- Labels are a small fixed set — bug, enhancement, good-first-issue, needs-triage — with a documented labeling procedure.
- Stale labeled issues are removed; `STALE_GOOD_FIRST_ISSUES` fails when newcomer issues sit untouched.
- First-time PRs receive a first review within `COMMUNITY_FIRST_PR_REVIEW_P50_H`.
- Bots may triage; bots never count toward responsiveness.

## Moderation

- Write the moderation policy before it is needed, at Stage 1 or earlier.
- Enforce the CoC with a stated escalation path; the enforcement commitment is part of the CoC's quality requirements.
- One person is not a moderation policy. Record the escalation chain so enforcement survives rotation.

## Meetings

- A regular maintainer meeting with a published agenda and recorded notes. Decisions made in meetings enter the decision records.
- No meeting without a purpose. Cancel rather than hold an empty meeting.
- Rotate meeting times to share the time-zone burden.

## Telemetry

- Measure the CHAOSS metrics the stage requires, cited by name.
- Track response times by constant name and watch the trend, not single points.
- Every score carries an evidence label; unlabeled data is UNVERIFIED.

## Maintainer sustainability

- **Concentration reduction** — identify areas with a single owner using `Bus Factor` and `Elephant Factor` by name, and grow deputies before the owner burns out.
- **Delegation** — every critical area has an owner and a successor; decisions are pushed to area owners at Stage 3.
- **Maintainer onboarding** — ladder promotion, not founder invitation. New maintainers get documented duties and a review period.
- **Succession** — defined for every critical role before Stage 4 is claimed.

Verify each practice is a named process with an owner, not an intention.
