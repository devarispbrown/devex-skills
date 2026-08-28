# Feedback Analysis Report

## Signal inventory

- Sources: <issue tracker | discussions | chat | docs search | CLI telemetry | API errors | install failures | SDK exceptions | analytics>
- Collection window: <start> — <end>
- Raw signals: <count> | Normalized (deduplicated): <count> | Excluded: <count> (<reason categories>)
- Redaction: <what was redacted; aggregation threshold applied>
- Evidence labels per source: <Observed | CI-observed | Estimated>
- Gaps: <sources or windows that could not be collected>

## Journey clusters (ranked by impact)

| Rank | Cluster | Journey stage | Failure mode | Frequency | Signals | Representative evidence |
|---|---|---|---|---|---|---|
| 1 | <stage + failure mode + cause name> | <install \| auth \| execute \| ...> | <blocked \| unclear \| slow \| ...> | <count + unit> | <n> | <issue links / snippets> |

## Impact ranking

| Rank | Cluster | Reach | Time cost / hit | Recurrence | Total estimated time lost | Evidence label |
|---|---|---|---|---|---|---|
| 1 | | <developers> | <minutes, Estimated> | <times per window> | <hours> | <Observed \| CI-observed \| Estimated> |

## Fix recommendations

| # | Cluster | Root cause | Owner class | Severity | Recommended fix | Acceptance test | Receiving skill |
|---|---|---|---|---|---|---|---|
| 1 | | | <Product \| API \| CLI \| SDK \| Config \| Environment \| Docs \| Infrastructure \| Third-party> | <P0–P4> | | <observable scenario: what a developer does and sees> | <suite skill name, if available> |

## Unmeasured and unowned

| Cluster | Gap | Measurement recommendation | Status |
|---|---|---|---|
| | <reach \| recurrence \| root cause unknown> | <event to emit, funnel to add> | <instrumented \| scheduled \| next window> |

## Sign-off

- Analysis window: <window>
- Clusters reported: <count>
- Findings handed off: <count>
- Unowned / unresolved: <count>
- Next analysis: <date>
