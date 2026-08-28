# Contributor Journey Walkthrough

## How to measure

Walk the journey as a first-time contributor would: create a fresh fork, work from the fork, and follow only committed instructions. Do not use internal knowledge.

Time each stage with a stopwatch-equivalent. Label every number Observed (executed and timed), CI-observed (executed in automation), or Estimated (reasoned, not executed). A number without a label is UNVERIFIED and cannot support a finding.

The fork-to-PR-ready total is budgeted against `FIRST_CONTRIBUTION_TARGET_MIN`. Treat the post-PR stages — review and merge — as a separate measured span.

Never report an average across stages. Report each stage's time; the funnel is as slow as its slowest stage.

## Stages and friction patterns

### Fork

Fork the repository, add the upstream remote, and set up the local clone.

Friction patterns: the repo is missing, renamed, or archived; no fork button (not public); clone over a throttled network; no `upstream` guidance in CONTRIBUTING.

### Clone

Clone from the fork to a fresh checkout.

Friction patterns: submodules or LFS blobs not documented; large history and no shallow-clone guidance; branch-protection or push rules not explained.

### Build

Reach a state where the project compiles or loads.

Friction patterns: undocumented toolchain version; a build that only works on a maintainer's machine; a pinned version that is no longer downloadable; steps that assume a preconfigured environment. A build that fails on a clean clone is a `NON_REPRODUCIBLE_BUILD` failure.

### Test

Run the test suite to green.

Friction patterns: tests need services or fixtures that are not seeded; test command differs from what CI runs; tests are flaky on a fresh checkout; a test run takes so long the contributor gives up mid-way.

### Find issue

Identify an issue the contributor can own.

Friction patterns: no good-first-issue label; labeled issues are stale or claimed by others; issues lack acceptance criteria; internal jargon blocks comprehension; the issue tracker is so noisy the labeled issues are invisible.

### Change

Make the change and add or adjust tests.

Friction patterns: no guidance on branching conventions; no fixture or sample to extend; the change surface is undocumented; a "small" issue that turns out to require the whole architecture.

### Checks

Run the local checks the PR will face: tests, lint, formatting, type checks.

Friction patterns: the local checks are undocumented; CI runs checks that the contributor cannot run locally; the checks differ between local and CI; a green local run fails in CI.

### PR

Open the pull request.

Friction patterns: no PR template or a template that demands internal context; DCO/CLA not explained and the bot blocks with an unexplained error; branch protection rejects the PR with no guidance; required checks unknown in advance.

### Review

Get the PR reviewed.

Friction patterns: first response takes days or never comes; reviewers rewrite instead of suggesting; feedback references internal context; no process stated for disagreements; the contributor cannot tell whether the PR is alive.

### Merge

See the change land.

Friction patterns: merge lag after approval; auto-merge disabled with no guidance; the contributor is not credited in release notes; no acknowledgment makes the first contribution feel terminal rather than the start of a relationship.

## Measurement procedure

1. Fork and clone from scratch; record fork and clone times.
2. Follow CONTRIBUTING.md literally. The moment a step is not executable, stop the walk and record the stage as blocked with the blocking file and line.
3. When a stage is blocked, estimate the remaining journey from analogous projects and mark every subsequent stage Estimated. Do not keep walking from tribal knowledge.
4. For each stage, record time, evidence label, and the friction patterns hit.
5. Sum the fork-to-PR-ready stages and compare the total to `FIRST_CONTRIBUTION_TARGET_MIN` by name; never restate its value.
6. Report per-stage rows and the total; attribute each finding's root cause to Documentation, Product, Environment, Infrastructure, or Third-party.
