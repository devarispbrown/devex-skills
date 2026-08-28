# Funnel Fixes

Apply fixes in the order given in the workflow: parity first, then guidance, then discoverability, then review. Each fix lands with an acceptance test: re-run the affected journey stage and observe the improvement.

## Setup scripts

Problem: build or test fails on a clean clone. Fix: committed automation.

- add a canonical setup target (`make setup`) that installs pinned toolchain versions and dependencies, and a `make test` that runs the exact suite CI runs
- commit lockfiles; pin the CI image to the same versions the setup script installs
- add a devcontainer or equivalent where environment setup is otherwise manual

Acceptance test: a clean clone reaches green tests with two commands, and the local check output matches CI.

## Fixture seeds

Problem: tests or examples need services or data the contributor cannot produce. Fix: make fixtures first-class.

- commit fixture generators or seed scripts that produce test data deterministically
- make services optional: in-memory or containerized defaults over externally provisioned ones
- document where fixtures live and how to reset them

Acceptance test: a fresh contributor can run the affected test with the fixture command from CONTRIBUTING, no internal knowledge required.

## Small first issues

Problem: labeled issues are not first-timer-sized. Fix: an issue-shaping discipline.

- size every good-first-issue: bounded change, one file set, no architectural prerequisite
- write each with a clear acceptance criterion and a pointer to the relevant fixture or test
- sweep stale or claimed labels; re-verify the list on a schedule
- add an auto-labeler to the triage workflow where issue volume justifies it

Acceptance test: a sampled good-first-issue can be completed by a contributor who has only read CONTRIBUTING.

## Bots that run checks on PRs

Problem: contributors cannot tell what their PR must pass. Fix: make checks run and visible on PRs.

- run the full check suite on every pull request, not just pushes to main
- require status checks in branch protection and list them in CONTRIBUTING
- enable the DCO or CLA bot so agreement compliance is automatic and explained
- add a welcome bot or first-timer triage comment where review capacity is scarce

Acceptance test: an opened PR immediately shows the status checks CONTRIBUTING promises, and any agreement block explains the fix.

## Contribution telemetry

Problem: funnel problems are invisible until a contributor gives up. Fix: measure the funnel.

- track stage conversion from commit sources: issue-to-PR link rate, PR-to-merge rate, first-time-contributor share of merged PRs
- track review latency per queue: first response, time to merge
- expose a dashboard or periodic report; keep the numbers in a file the team reads, not a private dashboard

Acceptance test: the funnel numbers exist with evidence labels, and the team can name the current widest stage. Never state telemetry numbers without their evidence labels; unlabeled numbers are UNVERIFIED.
