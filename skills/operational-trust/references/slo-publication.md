# SLO and SLA Publication

How to publish reliability numbers honestly: SLA versus SLO, measurement windows, attainment, and carve-outs. Read this before publishing or auditing any reliability commitment.

## SLA versus SLO

- **SLA**: contractual. Has consequences (credits, refunds), review, and legal sign-off. Publish only what legal has approved.
- **SLO**: internal commitment to users. Publish as an operating statement with current attainment.

Verify:

- the two are never conflated on the same page
- an SLA is never invented in docs or on a status page
- an SLO is published with its measurement window and aggregation

## Only publish what is measured

Verify:

- every published percentage or target is measured from production telemetry on the stated window
- unmeasured or aspirational numbers are marked as targets, never as facts
- a number that stops being measured is withdrawn or marked stale, never silently kept
- attainment is computed from real traffic, not curated samples

## What to publish

For each reliability commitment, publish:

- the promise: availability or latency target over the window
- the window and aggregation (for example 99.9% over the trailing 30 days)
- current attainment versus target, updated on a defined schedule
- carve-outs: excluded dependencies, maintenance windows, force majeure
- where to view incident history and error budget status

## Changing a commitment

Verify:

- changes go through a defined review process with rationale, never quiet edits
- a downgrade is announced with the reasoning and the new measurement
- an upgrade is not published until it is actually being met

## Error budgets

Verify:

- the error budget is stated or linked wherever the SLO is published
- users can tell how much room remains
- exhausting the budget triggers the documented process (freeze, review), and that process is public
