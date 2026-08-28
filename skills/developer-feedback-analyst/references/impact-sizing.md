# Impact Sizing

## Impact model

Impact = reach x time cost per hit x recurrence.

- reach — how many developers hit the cluster
- time cost per hit — minutes lost per occurrence, including recovery
- recurrence — how often each affected developer hits it

Total estimated developer time lost per window = reach x cost x recurrence.

## Sizing procedure

1. Reach: prefer telemetry counts and issue participants. When only issues exist, count distinct reporters and state the undercount.
2. Time cost per hit: use measured recovery time when available; otherwise estimate the span from first friction to resolved state and label it Estimated. Reference the canonical time-to-recovery target when setting the benchmark for what recovery should cost.
3. Recurrence: telemetry can show repeated attempts per developer; otherwise assume one and say so.
4. Multiply, then rank clusters descending by total estimated time lost.
5. Apply the canonical severity vocabulary: clusters that block first success are P1 regardless of the time math.
6. Tie-break by journey position: earlier stages cost the most because they stop developers before value.

## When to instrument instead of guess

Do not rank clusters on invented numbers. When a cluster's reach or recurrence is unknown:

- mark the cluster unmeasured in the report
- write a measurement recommendation: which event to emit, where, and what funnel it feeds
- instrument it and re-run the analysis next window

Never present an estimate as measured impact. Never rank an unmeasured cluster above a measured one on assumption.

## Evidence labels

Every number carries its label: Observed (measured), CI-observed (telemetry), Estimated (reasoned). Unlabeled numbers are UNVERIFIED and do not appear in the ranking.
