# Maintainer Sustainability Analysis

Scope: audit procedure for maintainer workload concentration — a better bus factor. Complements the sustainability dimension (bus factor, maintainer count, ownership coverage) computed by `check_community_health.py` and the operations guidance in the `developer-community` skill's `community-operations.md`; this file covers the concentration measurement and its interpretation.

## Maintainer Concentration Index

For each active maintainer, collect shares per axis over the trailing 90 days:

- `review_share` — fraction of all reviews.
- `merge_share` — fraction of all merges.
- `response_share` — fraction of all first human responses.

Concentration = the maximum single-maintainer share across the three axes. The checker reports it as its own line: `Maintainer Concentration Index: <max share> (max single-maintainer share across review/merge/response)`.

Risk bands (report with the index):

| Concentration | Risk | Action |
|---|---|---|
| <0.4 | low | none |
| 0.4–0.6 | medium | delegate one axis to a second maintainer |
| >0.6 | high | succession plan; require two reviewers per area |

## Supporting signals

- Backlog trend: open issues/PRs growing while response times rise.
- Review throughput trend: reviews per week declining.
- Inactivity: maintainers with no activity for 90 days on their owned areas.
- Single-owner areas: critical areas with exactly one owner (already scored; list them here for action).

## Rule

Concentration is a reported line, never folded into the sustainability score. Two projects with identical sustainability scores can differ sharply in risk; the index is what maintainers act on.
