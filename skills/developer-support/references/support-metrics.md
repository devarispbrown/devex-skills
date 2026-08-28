# Support Routing Metrics

## Metrics

- **Routing efficiency** — the share of requests resolved without a human: self-served over total. Measures how well self-service channels work.
- **Escalation rate** — the share of requests that reach engineering: engineering tickets over total. A rising rate with flat volume signals a routing or product defect, not more support.
- **First-ack time** — receipt to acknowledgment. Stated per channel with a commitment.
- **Time to recovery** — from hitting the failure to completing the corrective action, measured against `TTR_TARGET_MIN` (canonical definition in dx-standards/metrics.md; cited by name only).
- **Promotion bounce rate** — requests returned for missing diagnostics. A high bounce rate means the collection design asks for what it could supply.

## Measurement points

- self-served resolution: counted where the resolution happens (error, troubleshooting, search, community)
- escalation: counted at each ladder promotion, keyed by rung
- diagnostics: counted at the ticket gate and at every promotion
- time to recovery: measured per request class for the three most likely failures

## Evidence labels

Every number is labeled:

- **Observed:** a human or agent actually executed the path.
- **CI-observed:** automation executed the path; may undercount human reading time.
- **Estimated:** analyzed but not executed.

An estimate can never prove a target is met. A metric without a label is UNVERIFIED.

## Targets

| Metric | Direction | Note |
|---|---|---|
| Routing efficiency | high | baseline per product; re-measure after each ladder change |
| Escalation rate | low and stable | spikes trigger a routing review |
| First-ack time | within commitment | per channel, per class |
| Time to recovery | ≤ `TTR_TARGET_MIN` | measured per class, labeled |

## Verification

Confirm each metric is computable from the design's entry points before the design ships. A metric that cannot be measured is not a metric; it is an aspiration.
