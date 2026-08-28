# Good-First-Issue and Opportunity Backlog Audit

## Objective

Newcomer tasks are the fuel of the funnel. Audit whether the project's newcomer-labeled issues are genuinely usable, current, and reviewable, and whether the backlog stays healthy.

## Stale detection

Per `STALE_GOOD_FIRST_ISSUES`: any newcomer-labeled issue open beyond the 90-day staleness horizon without activity is a gate failure, and queued newcomer PRs that sit unreviewed fail the same gate.

Procedure:

1. Enumerate all issues carrying newcomer labels.
2. Compute days since the last non-bot activity for each.
3. Any issue past the horizon without activity → record `STALE_GOOD_FIRST_ISSUES`.
4. Count newcomer PRs queued for review that have received no first human review in the trailing window; the same gate applies.

## Effective newcomer issue counting

An issue is usable, and counts as an effective newcomer issue, only when it has:

- enough context to act without maintainer help
- explicit acceptance criteria or an expected outcome
- pointers to the relevant code or docs
- a label a newcomer can find
- no expired linkage: no closed code paths, no superseded work

Count usable issues per cohort window. Usable divided by open newcomer-labeled issues is the usable ratio; feed it to the contribution-opportunities dimension of the Community Health Score.

## Backlog health

- Newcomer issues that need maintainer help to start are not usable; record them separately.
- More than a cohort of stale newcomer issues signals triage rot; record the count and the trend.
- Issues whose labels have drifted from current project focus are reclassified, never assumed usable.
- A healthy backlog has a steady stream of fresh, scoped, reviewable tasks. Verify the stream over the trailing window, not just today's snapshot.

## Output

Record: open newcomer issues, usable newcomer issues, stale counts, queued unreviewed newcomer PRs, and the stream trend. These feed the gate check, the contribution-opportunities dimension, and the funnel leak analysis.
