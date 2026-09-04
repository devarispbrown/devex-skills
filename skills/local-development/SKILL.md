---
name: local-development
description: Make a fresh repository clone productive in 10 minutes or less: runtime and toolchain setup, dependencies, backing services, environment variables, fixtures, containers, and hot reload. Use to design or repair make dev, devcontainer, and docker compose workflows and replace tribal knowledge with reproducible setup. For designing onboarding journeys use developer-onboarding; to measure an existing setup's timing use developer-experience-auditor.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and build tooling.
metadata:
  version: "2.9.1"
---

# Local Development Setup and Repair

## Mission

A fresh clone reaching a productive state is boring infrastructure. Make it boring: committed automation, one canonical dev command, zero tribal knowledge.

**Reproducibility over tribal knowledge.** Every setup step that lives only in one developer's memory, shell history, or machine is a defect. The standard is a clean checkout that reaches the productive state using only committed instructions and automation, and a setup that fails that standard is a `NON_REPRODUCIBLE_BUILD` gate failure.

**Fix the automation, do not document around it.** When setup is hard to reproduce, repair the automation instead of writing longer READMEs. Documentation records committed automation; it never substitutes for it.

This skill designs and repairs `make dev`, `devcontainer`, and `docker compose` workflows and the environment configuration, backing services, fixtures, and hot reload they rely on.

Read `references/clone-to-productive.md` before measuring or designing the gate procedure.

## Hard gate: productive state on a clean clone

A clean clone must reach the productive state — tests run and the dev loop is exercised — within `LOCAL_DEV_MAX_MIN` using only committed instructions and automation.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

The gate has three parts:

- **Bands.** Interpret elapsed time against the canonical bands defined for `LOCAL_DEV_MAX_MIN` in `references/standards.md`: far under the limit is exceptional, comfortably under is strong, under the limit passes, at or over the limit is P1 FAIL.
- **Gate constant.** A clean checkout that cannot reach the productive state within `LOCAL_DEV_MAX_MIN` using only committed instructions and automation triggers `NON_REPRODUCIBLE_BUILD` (P1). A high-quality README cannot override this gate.
- **Evidence.** Label every measurement **Observed**, **CI-observed**, or **Estimated**. An estimate can never prove a PASS; a metric without an evidence label is UNVERIFIED.

Do not move setup steps into "prerequisites" to game the timer. Do not claim the gate passes without executing it.

## Local-dev workflow

### 1. Inventory the setup

Run `scripts/check_local_dev.py` from the repository root and inspect what it reports:

- dev commands and scripts in `Makefile`, `package.json`, and other task runners
- devcontainer, docker compose, and `.env.example` files
- lockfiles and toolchain pins
- README/contributing setup instructions and CI setup steps

**Find the gaps between what the inventory shows and what a fresh clone actually needs.** Interview the setup owner only to confirm behavior, never to extract steps that should already be committed. Do not accept "everyone knows" or "just run it like I do" as a specification.

### 2. Choose the dev target

**Pick exactly one primary dev target** — `make dev`, a devcontainer, or `docker compose up` — and make it the canonical path. Parallel dev paths are allowed when they serve genuinely different environments, but the chosen one must be the documented default.

Read `references/dev-targets.md` when choosing, repairing, or comparing dev targets.

Decide and record:

- who runs it, and from where
- what it starts, and in what order
- what counts as "up" (healthcheck green, port responding, expected log line)
- what the fallback is when a piece fails

### 3. Eliminate manual steps

**Automate every step a human currently performs by hand**: version selection, install, migration, seed, credential fetch, service start, port forwarding. Manual steps are the source of tribal knowledge.

Verify:

- toolchain install and version pinning are committed
- the number of commands from clone to first successful run stays within `LOCAL_DEV_MAX_COMMANDS`
- no step requires a step owner's memory, a personal shell alias, or a machine-specific path

Read `references/dependencies-toolchain.md` when pinning versions or structuring workspaces.

Do not document a manual step as "expected" when it can be automated.

### 4. Wire services, fixtures, and credentials

**Make backing services, seed data, and test credentials one command away.** Prefer emulators and committed fixtures over shared environments for the default dev loop.

Read `references/services-and-infra.md` when wiring databases, caches, queues, emulators, or fixtures.

Verify:

- services start with the dev target, or with one documented command
- the database arrives with a schema and seeded data
- credentials are generated locally, never shared or committed
- no developer needs access to a shared staging or production environment to run the app

### 5. Configure hot reload

**Make the dev loop restart-free where the stack supports it**: file watchers, auto-reload, live-reload, or container volume mounts. The dev loop is one of the two stop conditions of the hard gate; if editing a file does not show up in the running app within a reasonable cycle, the loop is not exercised.

Read `references/dev-targets.md` for hot-reload wiring per target.

Verify: change a file, observe the reload, confirm the change is live. If hot reload is not possible, document the exact restart cycle and count it in the timer.

### 6. Automate and document setup

**Commit the automation, then document what remains.** Setup instructions in the README must match committed automation exactly; every command must be copy-pasteable and every requirement stated up front.

Read `references/environment-config.md` when designing `.env.example` and environment handling.
Read `references/reproducibility.md` when designing clean-machine validation.

Verify:

- a fresh clone plus the documented commands reproduces the environment
- `.env.example` is the contract and matches what the code reads
- docs cover the three most likely failures and their recovery

Use the `developer-docs` skill if available when authoring setup documentation.

### 7. Validate from a clean machine

**Execute the gate procedure end to end on a clean checkout**, record the elapsed time, label the evidence, interpret the band, and return the verdict.

Read `references/clone-to-productive.md` before measuring.

Never convert UNVERIFIED to PASS based on assumptions. Never report a band you did not measure.

Hand off to the `developer-experience-auditor` skill if available for an independent audit, and to `developer-onboarding` if available when the goal is the full onboarding journey rather than the dev environment.

## Dev-target contract

The primary dev target must expose a predictable contract.

- **`make dev`**: a `Makefile` with standard phony targets — `install`, `services`, `migrate`, `seed`, `dev`, `test`, `lint`, `clean` — where `dev` is a dependency chain that ends with a running, health-checked dev process and a documented stop target.
- **devcontainer**: a `devcontainer.json` with a pinned image, declared features, a `postCreateCommand` that completes the setup, and forwarded ports matching the app's default ports. It must work from the default config with no manual edits. See `assets/devcontainer.example.json` for the shape.
- **`docker compose up`**: a compose file whose services declare healthchecks, whose app service mounts source for hot reload, and whose "up" result is verifiable (port responds, healthcheck green).

**Graceful degradation**: when a required piece is unavailable (port taken, image missing, feature unsupported), fail with a clear message naming the cause and the recovery — never a silent partial start.

## Environment configuration contract

**`.env.example` is the contract.** It lists every variable the code reads, with safe development defaults and a comment for each non-obvious value.

- Discover variables from code, CI, and config files — never from memory.
- Keep secrets out of the repo: real values live in gitignored local files or a local secret store; dev defaults must be safe to commit.
- Use the framework's canonical precedence order and document it. Do not invent a load order that contradicts the framework.
- On a missing or invalid variable, fail with the variable name and its role, or use an explicitly safe default — never a silent wrong value.

Read `references/environment-config.md` for the full procedure.

## Required output

Produce a **local-dev assessment** containing:

1. **Verdict**: PASS / PASS WITH DEBT / FAIL / UNVERIFIED, using the vocabulary in `references/standards.md`.
2. **Evidence label** for every measurement: Observed, CI-observed, or Estimated.
3. **Gate result**: elapsed time against `LOCAL_DEV_MAX_MIN`, the band, and — when it fails — the `NON_REPRODUCIBLE_BUILD` trigger.
4. **Dev-target contract status**: which contract elements hold and which are missing.
5. **Environment contract status**: `.env.example` completeness and precedence behavior.
6. **Findings** with severity (P0–P4) and the specific repair for each.

## Definition of done

The work is done when:

- a clean clone reaches the productive state within `LOCAL_DEV_MAX_MIN` using only committed instructions and automation, verified from a clean checkout
- one canonical dev target is documented and works
- every manual setup step found during inventory is automated or explicitly justified
- services, fixtures, and credentials come up with the dev target or one documented command
- hot reload works, or the restart cycle is documented and counted in the timer
- `.env.example` matches the code and holds no real secrets
- the local-dev assessment reports a verdict, an evidence label, and severities
- tribal-knowledge steps that could not be automated are listed explicitly as debt, never silently
