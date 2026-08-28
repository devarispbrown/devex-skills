# Review Experience Analysis

Scope: qualitative per-PR review-experience procedure for the community auditor. This complements the quantitative review dimension (closure ratio and first-review speed, computed by `scripts/check_community_health.py`) and the responsiveness procedure in `responsiveness-monitor.md`; it answers "was the review experience good", not merely "did review happen".

## Procedure

For a sample of recent merged and abandoned PRs from first-time contributors, record per PR:

1. **Response latency** — time from submission to first review, in days.
2. **Review rounds** — number of review iterations before merge or abandonment.
3. **Reviewer consistency** — same reviewer across rounds, or a new person re-litigating earlier feedback.
4. **Unclear requirements** — feedback the contributor could not act on without asking.
5. **Scope creep** — requirements introduced after submission that were not derivable from the original issue.
6. **Nit density** — comments about formatting/style that automation could have caught; count separately from substantive comments.
7. **Blocking vs non-blocking** — whether blocking and suggestion comments are distinguishable.
8. **Explanation quality** — whether reviewers explain why, not just what.
9. **Maintainer disagreement** — contradictory reviewer directions.

## Defect pattern

A PR with many rounds, long open time, high nit density, and late scope creep is a community DX defect even if it eventually merges. Example:

```text
PR #823
7 review rounds
18 days open
42 comments
21 comments were formatting/style feedback that could have been automated
9 requirements were introduced after submission
Contributor never returned
```

Classify: nit density and unclear requirements point at the project (automation gap, issue quality); scope creep points at the issue/PR contract; disagreement points at maintainer process. Report findings with severity per the canonical vocabulary and one named gate or dimension per finding.
