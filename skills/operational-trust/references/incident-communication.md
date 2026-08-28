# Incident Communication

Procedure for communicating incidents to users: first update, cadence, channels, and postmortems. Read this when auditing incident communication or writing during an incident.

## First update

The first update defines the incident for the user. It must appear within the `TTR_TARGET_MIN` window of first confirmed impact (target 5 minutes; >10 minutes is a P2 defect).

Include:

- what is affected: component, user segment, region
- what users should do: nothing, retry, avoid a feature
- when the next update arrives
- an incident number or correlation ID users can quote

Do not include:

- speculation about root cause
- internal jargon, team names, or blame
- empty reassurances

## Update cadence

- Follow-ups every 30 minutes, or at each meaningful change, whichever is sooner.
- Every update repeats the incident number and current status.
- No-news-is-bad-news: a missed update is a trust failure even when the fix is on track.
- The status page is the canonical record; summaries go to the channels users already use (email, Slack, in-app, social).

## Templates

Every incident must run from templates, never drafted from scratch. Verify templates exist for:

- initial incident report
- status update
- resolution notice
- maintenance announcement

## Postmortems

After resolution, publish a postmortem within 5 business days containing:

- timeline: detection, updates, resolution
- impact: user-facing, measured in numbers where possible
- root cause: one paragraph, in systems language
- corrective actions: each with an owner, a due date, and an acceptance test

Verify:

- postmortems are blameless: fix systems, not people
- every corrective action has an owner and a verification step
- incident history links to the postmortem

## Evidence

Label every claim with an evidence type: Observed, CI-observed, or Estimated. Never present a guess as fact in a user-facing update.
