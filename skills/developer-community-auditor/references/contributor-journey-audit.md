# Community Magic Path Audit

## Objective

The Community Magic Path is the contribution analogue of the product magic path: a competent developer goes from discovering the contribution process to producing a valid contribution ready for maintainer review within `COMMUNITY_ONBOARDING_PATH_MAX_MIN`.

Implementation time is excluded. The metric measures project-imposed contribution friction, not the difficulty of the task.

## Benchmark persona

The newcomer has a supported OS, a terminal, normal tooling, and general development competence. They do not have prior project knowledge, internal access, a project account, or project-specific configuration. Assume they do not have the product credentials, sample data, or internal terminology that the project has not provided.

## The six measured stages

Run each stage in order and stop the timer only at ready-for-review:

1. **discover** — open the repo landing page and find the canonical contribution route (README to CONTRIBUTING). Stop when the route is identified.
2. **understand** — read CONTRIBUTING.md and be able to state how to find work, set up, test, and open a PR. Stop when the contributor can state the process.
3. **ask** — locate the support route (SUPPORT.md, chat, or discussions) and confirm where questions are answered. Stop when the ask route is identified.
4. **find** — locate a newcomer-usable task via labels or the newcomer path. Stop when a task with context and acceptance criteria is chosen.
5. **setup** — follow the committed dev-environment instructions to a clean, working tree with runnable tests. Stop when the test command passes.
6. **first PR** — implement a small real change, run the required checks, and open a PR using the template. Stop at ready for maintainer review.

If any stage cannot be completed, stop the timer and record the blocker with its stage.

## What to actually attempt

- Clone and create a branch using only committed instructions.
- Make a trivial but real contribution: a docs fix, a test, or a small bug fix; prefer a real newcomer-labeled issue when one exists.
- Open the PR with the project's template and link the issue.
- Do not use internal knowledge, maintainer assistance, or project chat. The README and committed files are the only allowed sources.

## Timer rules

- **Start:** the newcomer opens the contribution route.
- **Stop:** the PR is ready for maintainer review.
- **Count:** orientation, reading, environment setup, dependency install, test runs, and PR creation.
- **Exclude:** implementation of the change itself. If a task consumes more than the implementation allowance, switch to a smaller task and note the switch.
- Bots, templates, and automation that gate the newcomer count as project friction. Do not exclude them from the timer.

## Friction attribution

Attribute every delay to exactly one owner:

- **Docs** — missing, wrong, or contradictory instructions.
- **Labels** — no newcomer path or no usable newcomer tasks.
- **Setup** — the dev environment does not reproduce from committed instructions.
- **Review** — no reviewer available; first human review is slow.
- **Governance** — process, permissions, or ownership is opaque.

Never attribute friction to the newcomer. A path that works only for people who already know it is a defect.

## Bands and verdict

Compare the measured time to `COMMUNITY_ONBOARDING_PATH_MAX_MIN`. Time at or under the constant passes; time over it fails with `BROKEN_CONTRIBUTION_PATH`. A path with no newcomer-usable issue is a P2 finding per the community standards. A path that cannot be completed at all is a P1 failure. Record the evidence label: Observed, CI-observed, or Estimated. An estimate can never prove a PASS.
