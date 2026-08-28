# Benchmark Hygiene

## Purpose

Benchmarks are evidence. Evidence that is warm, noisy, or environment-dependent is not evidence. Follow the rules below so measurements mean the same thing on Monday and in CI.

## Warmup

- Warm the target before sampling: JITs, lazy initialization, caches, and connection pools must reach their steady state.
- Discard the first runs; sample only after the metric stabilizes.
- Measure the steady state unless the budget explicitly targets cold behavior (cold start, cold-cache CLI startup).

## Sample count and variance

- Never decide from one run. Take enough samples to see the distribution.
- Report medians and percentiles, not just means — latency is not normally distributed.
- When two numbers differ by less than the noise band, call them equal. The benchmark must be able to resolve the difference it is asked to prove.

## Environment pinning

- Pin machine type, OS, CPU governor, toolchain, and commit. Record them with every measurement set.
- Run without competing load; check for background jobs before a campaign.
- CI runners are shared and noisy. Treat CI numbers as CI-observed evidence: use them for drift detection, repeat them, and confirm decisive numbers locally.

## Comparing baselines

- Compare like to like: same revision flags, same environment class, same benchmark version.
- Store the baseline alongside the budget file so comparison is automatic.
- A comparison across environments is a warning signal, never a verdict.

## Common traps

- Benchmarking debug builds and calling it product performance.
- Timing the harness: measuring the runner, the JSON parse, or the print, not the surface.
- Including first-run effects in a steady-state budget.
- Averaging multimodal latencies into a meaningless mean.
- Comparing a warm local cache against a cold CI runner.
- Tuning flags until the benchmark passes and shipping without re-measuring the real surface.
- Forgetting the baseline: a benchmark without a stored reference cannot detect a regression.

## Verify

- warmup completed before the first sampled run
- sample size is recorded and variance is visible in the output
- environment line includes machine, OS, toolchain, and revision
- baseline output is stored and dated
- the measured quantity is the budgeted metric, same key and same unit
