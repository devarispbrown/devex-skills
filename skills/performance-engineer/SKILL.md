---
name: performance-engineer
description: Maintain explicit performance budgets for CLIs, APIs, SDKs, builds, tests, and containers: benchmark, compare baselines, profile, identify regressions, bisect, recommend fixes, and update performance tests. Performance regressions become release-gating events. For the local dev loop speed use local-development.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and benchmarking/profiling tooling.
metadata:
  version: "2.9.4"
---

# Performance Engineering: Budgets, Benchmarks, and Gates

## Mission

Performance is an interface. A CLI that stalls at startup, an API whose p95 eats the user's SLA, an SDK that doubles import time, a build that turns a fix into a coffee break — each one loses users the same way a broken command does.

Treat performance as a product surface with explicit, measured contracts:

- every surface has a numeric budget chosen deliberately, not inherited and not vibes
- every budget is checked against real measurements with labeled evidence
- every regression is traced to a cause, fixed against evidence, and re-verified
- performance regressions become release-gating events

Do not tune blind. Never treat a single benchmark run as data. Never let a regression ship silently.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Budgets over vibes

Budgets are the unit of performance work. Without a budget, "this is slow" is an opinion; with one, it is a testable contract.

- Define budgets before benchmarking. The budget file is the contract; the benchmark is the evidence.
- Budget numbers are project-specific values chosen deliberately — measured headroom over an observed baseline, with the rationale recorded. Do not copy another product's numbers.
- Every measurement carries an evidence label as defined in `references/standards.md`. An unlabeled number is not evidence.
- A budget breach is a defect with a severity, not a conversation. A near miss is a warning, not a pass.
- A performance regression is a release-gating event. It cannot ship without an explicit decision.

For the local development loop — clone to productive state, dev server, hot reload — use the `local-development` skill if available.

## Performance engineering workflow

### 1. Define budgets

Read `references/budgets.md` when defining or revising a budget for any surface.

Identify every performance-sensitive surface and give each one a budget key: a surface, a metric, a budget value, and a unit. Cover the surfaces in the budget contract below; add others the project owns.

Verify:

- every budget has exactly one (surface, metric) key and a positive budget value
- the unit is explicit and matches the measuring tool's output
- the number is deliberate: derived from an observed baseline with headroom, and its rationale is recorded
- the owner of each budget is named — a budget without an owner is not enforced
- the budget file matches the schema of `assets/perf-budgets.example.json`

### 2. Benchmark a baseline

Read `references/benchmarking.md` when designing, running, or comparing a benchmark.

Measure before you tune. Build a reproducible benchmark for each budgeted surface and capture the baseline:

- run the benchmark in a pinned environment with warmup and enough samples to see variance
- record environment, revision, and date alongside the numbers
- store baseline measurements where CI and agents can find them, in the shape of `assets/perf-measurements.example.json`

Verify:

- the benchmark exercises the real surface, not a harness approximation
- numbers are medians or distributions, never a single run
- measurements carry evidence labels (Observed or CI-observed, as defined in `references/standards.md`)

Run `scripts/check_perf_budgets.py` against the budget file and the baseline measurements. A baseline that breaches its own budget is a finding, not a new budget.

### 3. Profile

Read `references/profiling.md` when a benchmark points at a slow path.

Profile the measured path, then fix the evidence, not the guess:

- reproduce the slow path under the same conditions the benchmark used
- collect CPU samples or allocations and read the flamegraph top-down: widest frames first, confirmed against code
- never "optimize" a frame that does not appear in the profile
- record the profile artifact with the finding so the fix is auditable

Verify:

- the profile was taken on the measured surface, not on a synthetic micro-benchmark
- the suspected hot path is the widest frame, not merely visible
- the frame's cost is attributable to project code, not to the profiler or the environment

### 4. Identify and bisect regressions

Read `references/regression-bisect.md` when a measurement breaches a budget or drifts from its baseline.

A regression is real only when the measurement says so twice:

- confirm the breach outside CI: same revision, same environment, repeated runs
- bisect to the commit with a performance verdict, not a proximity guess
- attribute the regression only when the change and the mechanism are both identified

Do not attribute by commit proximity alone. Never blame the environment before the bisect finishes.

### 5. Fix and verify

Fix against profile evidence, then prove it with the benchmark:

- make the smallest change that addresses the profiled frame
- re-run the same benchmark in the same environment; the measured gain must show up in the same metric
- keep the before/after profiles as evidence of the mechanism
- update performance tests when the fix changes the expected envelope, and record the new baseline

Verify:

- the fix improves the budgeted metric, not a different one
- the gain is larger than the noise band the benchmark can resolve
- no adjacent budget regressed as a side effect

### 6. Wire performance gates

Read `references/performance-gates.md` when wiring performance checks into CI or release gates.

Make the budget check part of the release path, not a report that is read after the tag:

- run `scripts/check_perf_budgets.py` in CI on every relevant change, with the stored baseline as reference
- decide breach handling up front per budget: fail the release, warn, or accept as tracked debt
- a hard breach blocks the release; accepted debt must carry an owner and a deadline
- never disable a flaky gate silently — quarantine it with a debt ticket

Hand off release verdicting to the `release-guardian` skill if available, and test strategy to the `quality-engineer` skill if available. Performance gates feed the release contract; they do not replace it.

## Budget contract

Every performance-sensitive surface carries a budget key with a deliberately chosen number. Budgets are project-specific values chosen by measurement, not by inheritance; the values live in the project's budget file, never in this skill.

| Surface | Budget dimension | Budget metric | Unit |
|---|---|---|---|
| CLI | time to first usable command output | startup_p50_ms | ms |
| API | end-to-end latency on the canonical request | p95_latency_ms | ms |
| SDK | import/initialization overhead over a bare baseline | init_overhead_ms | ms |
| Build | clean build from checkout; incremental dev build | clean_build_seconds | s |
| Tests | full suite from a clean state | full_suite_seconds | s |
| Container | compressed image size | image_size_mb | MB |
| Serverless | cold start to first response | cold_start_ms | ms |

The measured value for a key must be produced by a benchmark that covers that surface. A budget with no measurement is unverified and cannot prove PASS.

## Regression-gate contract

A performance regression is a release-gating event:

- a measurement that breaches its budget fails the performance gate
- a near miss warns the gate; it does not fail it
- an accepted breach is debt: it requires an owner, a tracked ticket, and a deadline, and the gate reports PASS WITH DEBT, never PASS
- a budget with no valid measurement is UNVERIFIED; do not convert it to PASS on assumptions

Verdicts and severities follow the canonical vocabulary in `references/standards.md` — apply exactly one verdict, and never let a score or sentiment override a hard breach.

## Required output

For every performance investigation, produce the performance report using `assets/performance-report-template.md`.

The report must contain:

1. **Budgets** — every budgeted surface and metric with its budget value, unit, and owner
2. **Measured vs budget** — per-budget measured values, status (PASS / NEAR MISS / BREACH / UNVERIFIED), and evidence labels
3. **Findings** — each finding with severity (P0–P4 vocabulary from `references/standards.md`), the profiled evidence, and a fix recommendation
4. **Gate recommendation** — exactly one of PASS / PASS WITH DEBT / FAIL / UNVERIFIED, with reasoning tied to the measured values

## Definition of done

Performance work is done when:

- every surface in the budget contract has a budget with a named owner and a recorded rationale
- a reproducible benchmark exists for every budgeted surface and a baseline is recorded with environment and evidence label
- every budget is checked against measurements; statuses are PASS, NEAR MISS, BREACH, or UNVERIFIED, never assumed
- regressions are confirmed twice, bisected to a commit, and attributed to a mechanism
- fixes are verified against the same benchmark in the same environment, with before/after evidence
- performance gates run in CI and breach handling is decided per budget: fail, warn, or tracked debt
- the performance report is rendered from the template with budgets, measured vs budget, findings with severity, and a gate recommendation
- no regression, near miss, or unverified budget shipped in a release without an explicit decision

Cross-skill handoffs are explicit: the `local-development` skill owns dev-loop bootstrap speed if available, and `release-guardian` owns the release verdict if available.
