# Performance Gates in CI and Releases

## Purpose

A performance gate turns a budget breach into a release decision. The gate must run in the release path, and its verdict must follow the canonical vocabulary in `references/standards.md`.

## Wiring the gate

- Run `scripts/check_perf_budgets.py` in CI on every relevant change: the budgets file plus the measurements the change produced.
- Store the baseline as a CI artifact or committed file so the check compares like to like.
- Add the performance job to the release pipeline's required checks. A missing job is an unverified gate, not a passed one.

## Budget breach handling

Decide per budget, up front, how a breach behaves:

- **Fail** — a hard breach blocks the release. Use for user-visible surfaces: CLI startup, API p95, cold start.
- **Warn** — a near miss reports a warning and never blocks. Use for tracking metrics that are near their envelope.
- **Debt** — an accepted breach ships only with an owner, a tracked ticket, and a deadline. The gate reports PASS WITH DEBT, never PASS.

Rules:

- Never silently pass a breach.
- Never lower a budget to make a gate green. Changing a budget is a deliberate act with a recorded rationale (see `references/budgets.md`).
- A hard breach in a release pipeline blocks the tag; escalate to the `release-guardian` skill if available to fold it into the release verdict.

## Flake management

- Rerun policy: a failing performance job is rerun once on the same revision before it counts. Two failures are real.
- Quarantine: a benchmark that flakes repeatedly leaves the gate only with a debt ticket and a replacement benchmark, never a silent removal.
- Reduce flakes at the source: more samples, tighter environment pinning, distribution comparison instead of point comparison.
- Treat CI numbers as CI-observed evidence: reproducible locally, decisive.

## Verdicts

- Every gate run returns exactly one verdict: PASS, PASS WITH DEBT, FAIL, or UNVERIFIED, per the vocabulary in `references/standards.md`.
- A score never overrides a breach. An unverified budget cannot prove PASS.
- Record the gate verdict and the measurements that produced it in the performance report before the release decision.

## Verify

- the performance job is a required check in the release pipeline
- breach handling is decided and recorded per budget
- flaky gates carry debt tickets, not silent removals
- the verdict is exactly one of the canonical four, tied to measured values
