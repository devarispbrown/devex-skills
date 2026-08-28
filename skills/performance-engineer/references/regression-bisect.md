# Regression Detection and Bisection

## Purpose

A regression is a budget breach that is real twice: reproduced outside CI, then attributed to a specific change. Detection and bisection are separate jobs; do not skip the first to get to the second.

## Detection in CI

- Run the budget check on every relevant change against the stored baseline.
- Watch distributions, not just point values: a stable median with a fatter p95 is still a regression signal.
- CI noise is expected; a single red CI run is a signal to reproduce, not a verdict.
- Never "fix" CI by lowering the budget or disabling the gate before reproduction (see `references/performance-gates.md`).

## Reproduce outside CI

1. Pin the revision and environment; re-run the benchmark locally or on a dedicated runner.
2. Repeat until the breach repeats: one occurrence can be a flake, two agreeing occurrences are a regression.
3. Record environment, revision, and the repeated numbers as CI-observed or Observed evidence, per the labels in `references/standards.md`.

## Bisect procedure

1. Find the first known-good and first known-bad revisions.
2. Drive `git bisect` with a verdict script that runs the benchmark for the budgeted metric and returns 0 (good) or 1 (bad) — the same check the CI runs.
3. Alternate runs to cancel noise: when a midpoint is borderline, repeat it and use the majority verdict.
4. Land on the smallest change that flips the verdict.

## Performance-change attribution

- A regression is attributed only when both hold: the bisect lands on a specific change, and the mechanism is confirmed (profile diff or measured allocation change).
- Do not attribute by commit proximity, message subject, or blame.
- When the bisect lands on a commit that cannot plausibly matter, suspect the environment and re-check: runner changes, dependency resolution, cache misses.
- After the fix, verify the budgeted metric returns inside its budget with before/after evidence.

## Verify

- breach reproduced on a pinned revision outside CI
- bisect driven by a performance verdict, not by inspection
- attribution includes both the change and the mechanism
- fix verified against the same benchmark and recorded
