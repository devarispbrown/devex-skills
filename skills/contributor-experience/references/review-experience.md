# Review Experience Audit Procedure

## Documented review expectations

Check CONTRIBUTING.md or a CONTRIBUTING section for stated review expectations. Verify they answer:

- who reviews: maintainer list, rotation, or CODEOWNERS-driven
- how fast: a stated first-response and merge target, or a clear "best effort"
- what a PR must contain before review starts: checks green, DCO signed, template filled
- how disagreements are resolved: maintainer decides, community consensus, or escalation path
- what happens to PRs that stall

Undocumented review expectations are a P2 defect: the contributor cannot tell whether silence means review pending or abandonment.

## Responsiveness measurement

Measure from real PR history, never from maintainer claims. For a sample of recent PRs, including at least the last several first-time-contributor PRs:

1. **First response time** — PR opened to first human comment or status-changing review. Record Observed from the API/timeline.
2. **Time to merge** — PR opened to merged, or to closed without merge.
3. **Stall rate** — fraction of PRs with no activity for the project's own staleness bar.
4. **Reviewer coverage** — whether CODEOWNERS-driven review assignments fire, or PRs wait for a human to notice.

Label every measurement with the sample size and date range. A sample of one PR is not a measurement; state it as anecdotal.

Interpret with the funnel in mind: first-response latency punishes first-time contributors hardest, because they have no history of the project to keep them waiting.

## First-time-contributor friendliness

For each first-time-contributor PR in the sample, verify the review:

- acknowledges the work before correcting it
- explains why, not only what, especially for internal conventions
- suggests, rather than rewrites; a maintainer push over the contributor's branch is a warning sign
- distinguishes blocking requests from optional nits
- lands or shepherds to land, leaving the contributor with a merge credit

Hostile, terse, or context-assuming reviews are a P1 defect: they close the funnel for the specific population it is designed to grow. A welcome bot or first-timer triage path is a strong signal.

## Mentorship paths

Verify there is a documented path past the first PR:

- triage or review-invitation roles for proven contributors
- a mentoring section in CONTRIBUTING or a linked community doc
- maintainer nomination criteria that are stated, not vibes
- events or async programs for first-time contributors where the project participates

A funnel that stops at "merged once" produces no future maintainers: a P2 defect for projects with maintainer scarcity, P1 when no one is left to review.
