# Metrics, SLIs, SLOs, and Alert Design

Procedure for selecting SLIs, setting SLOs, controlling cardinality, and designing alerts. Read before auditing metrics or SLOs.

## SLI selection

- Select SLIs from user-visible behavior, not internals: availability (successful divided by total), latency (percentiles of serving time), throughput, and error rate.
- Define each SLI over the same measurement window and request scope. A request that is not counted is a gap.
- Start from the four golden signals (latency, traffic, errors, saturation) or the RED trio (rate, errors, duration).
- Record per SLI: the metric, the success definition, the denominator, and the measurement point.

## SLO setting

- Set the target above current observed availability, roughly one nine higher, and never above what the team can measure with confidence. Apply the canonical thresholds in `references/standards.md`.
- Track the error budget for every SLO over its window. A budget with no tracking is a slogan.
- An SLO without a measurement window and a denominator is not an SLO; fix the SLI first.
- For error semantics and Time to Recovery targets, use the `error-experience` skill if available.

## Cardinality control

- Every metric label must be a small enumerated set. Never user IDs, emails, or raw URLs as label values.
- Aggregate high-cardinality dimensions (per-tenant) into histograms or buckets; emit top-N as separate series only.
- Bound the label set at design time. Review dashboards for per-value series (per-user, per-request) that explode cardinality.
- Time-series cardinality beyond the backend's documented limit is a P1 gap.

## Alert design: page vs ticket

- **Page** for: error budget burn rate, availability below target, saturation of a critical resource.
- **Ticket** for: drift, latency trend, capacity growth, non-urgent anomalies.
- Every alert carries: condition, severity, page or ticket, owner, runbook link, and a test procedure.
- Never alert on a metric no one has a runbook for. Never page for noise the on-call cannot act on.
- Test each alert with a fault injection before it matters.

## Verification

- Every SLO has an alert wired to its budget; confirm the firing condition, severity, and owner.
- Confirm label cardinality on three representative dashboards.
- Confirm every alert has a runbook and an owner in the alert configuration.
