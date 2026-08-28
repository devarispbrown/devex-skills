# Reach Verification

## Definition

Reach is the property that a notice was delivered to, and acknowledged by, the developers it affects. Publishing is not reach. An unreached notice is an uncommunicated change.

## Evidence labels

Every reach claim carries exactly one label, from the suite vocabulary:

- **Observed:** delivered and acknowledged by named members of the affected audience (read receipts, replies, ticket confirmations, survey responses).
- **CI-observed:** delivery confirmed in automation (alert payloads sent, notifications posted, banner shown) without individual acknowledgment.
- **Estimated:** inferred from audience size and channel coverage without delivery confirmation. An estimate never proves reach.

## Methods

| Method | Use for | Evidence it produces |
|---|---|---|
| Announcement channel (blog, mailing list, Slack, Discord) | release notes, advisories | CI-observed post, Observed replies |
| Issue/PR mentions and comments | deprecations, breaking changes | Observed threads, closed loops |
| Dependency-graph alerts (Dependabot and equivalents) | vulnerable or breaking dependency releases | CI-observed delivery, Observed PRs |
| In-product banners and console warnings | deprecation of in-use surfaces | Observed interaction, telemetry |
| Docs and changelog placements | all notices | Estimated unless measured |
| Direct outreach to named integration partners | highest-severity breaks | Observed by definition |

## Measurement rules

1. Count the affected audience first: every segment named in the notice, not just the largest.
2. Report reached versus affected per segment: "12 of 40 affected repos confirmed migration".
3. A notice with no measured acknowledgment is Estimated, even if the channel is public.
4. An unmeasurable audience makes the reach claim UNVERIFIED; convert it to a follow-up (banner, alert, direct outreach) rather than declaring success.
5. Prefer Observed evidence periodically and CI-observed on every relevant change, matching release-gate evidence discipline.

## The record

For each notice, record:

1. notice identifier and surface
2. affected segments and count
3. channels used, with dates
4. reached count and acknowledgments per segment
5. evidence label per claim
6. follow-ups for unreached segments

## Definition of done

Reach for a notice is verified when every affected segment has either Observed or CI-observed acknowledgment, or a documented follow-up with a deadline. "We posted it" is not done.
