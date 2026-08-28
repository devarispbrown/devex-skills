# Performance Budget Definition

## Purpose

Turn "performance matters" into a testable contract: one budget key per surface, with a deliberately chosen number, a unit, an owner, and a recorded rationale.

## Budget keys

Every budget has exactly four required fields, matching the schema of `assets/perf-budgets.example.json`:

- **surface** — the surface the budget governs: cli, api, sdk, build, test, container, serverless, or a project-specific surface
- **metric** — the measured quantity, e.g. `startup_p50_ms` or `p95_latency_ms`
- **budget** — the numeric value
- **unit** — the unit of measurement, matching the measuring tool's output

The (surface, metric) pair is the key. Measurements must use the same key; a mismatched key is unverified, not a pass.

## Per-surface procedure

### CLI: startup time

1. Measure from process start to first usable output on the canonical command, with a cold cache.
2. Budget the median (`startup_p50_ms`); track the p95 separately as a warning metric.
3. Exclude the terminal and shell from the measurement; measure the process.

### API: p95 latency

1. Benchmark the canonical request path end-to-end under a fixed concurrency and payload.
2. Budget the p95 (`p95_latency_ms`); keep the p99 as a warning metric. Do not budget the mean.
3. Record the load profile — concurrency, payload size, data set — in the environment line.

### SDK: overhead

1. Measure import/initialization time over a bare-language baseline with no SDK.
2. Budget the delta, not the total: `init_overhead_ms`.

### Build: time

1. Measure the clean build from checkout and the incremental dev build separately; they are different budgets (`clean_build_seconds`, `incremental_build_seconds`).
2. Run in the same environment class the CI matrix uses. Never compare a warm local cache against a cold CI runner.

### Tests: full suite

1. Measure the full suite from a clean state: checkout, install, run.
2. Budget `full_suite_seconds`. A suite that outlives its budget is a gate finding, not a habit.

### Container: image size

1. Measure the compressed image size as shipped (`image_size_mb`).
2. Budget the shipped size, not the uncompressed working set.

### Serverless: cold start

1. Measure from invocation to first response on a cold instance (`cold_start_ms`).
2. Take a distribution; cold starts are noisy. Budget a high percentile, not the mean.

## Choosing the number

1. Measure the current state first: at least three runs in a pinned environment; use the median as the observed baseline.
2. Set the budget from the baseline with headroom the team can defend — tight enough to catch regressions, loose enough to absorb noise.
3. Record the rationale next to the number: baseline date, environment, headroom, and why this number matters to users.
4. Budgets are project-specific values chosen deliberately. Do not copy another product's budgets; do not accept defaults without measuring.
5. Review budgets on a cadence or when the workload changes. A stale budget is a defect.

## Evidence labels

Every measurement carries an evidence label — Observed, CI-observed, or Estimated — as defined in `references/standards.md`. Never present an estimate as a measurement.

## Verify

- every budget has surface, metric, budget, unit, and a named owner
- the number is derived from a measured baseline with recorded headroom
- the budget key exactly matches the benchmark's output key
- the budget file validates against the example schema
