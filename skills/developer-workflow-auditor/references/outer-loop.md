# Outer Loop Audit

## Scope

The outer loop starts at commit and ends at merged, reviewed, previewed work: commit, CI first signal, full CI, PR, preview, review. Measure each segment from action to feedback.

## Segment map and budgets

| Segment | Budget constant | What feedback ends the segment |
|---|---|---|
| CI first signal | FEEDBACK_CI_FIRST_SIGNAL_MAX_MIN | first useful CI result |
| Full CI | FEEDBACK_FULL_CI_MAX_MIN | complete CI result |

PR, preview, and review have no budget constants. Measure and report their latency as flow findings with evidence labels.

## Per-segment measurement

Time from push or commit to the first useful signal, and separately from push to full completion. Record:

- the pipeline trigger (push, PR, manual run)
- queue time versus job time when the pipeline reports it
- the evidence label and the environment

Do not count the first signal as the full result. Do not count a job that reported nothing useful as a signal.

## Common root causes

- queue wait ahead of job time
- missing build or dependency cache
- serial jobs that could run in parallel
- the full suite where focused suites are sufficient
- slow preview deploy or a missing preview link
- review backlog and stale PRs

## Verify

- the first signal is measured, not the full run
- full CI is measured to completion
- both segments carry evidence labels
- queue time is separated from job time when the pipeline reports it
