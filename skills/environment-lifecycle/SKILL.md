---
name: environment-lifecycle
description: Design the local-to-test-to-preview-to-staging-to-production path: ephemeral and PR environments, cloning, seed data, config promotion, secrets, cleanup and TTL, cost controls, database branching, and production-like topology. For the single-developer local loop use local-development; for sandbox safety use sandbox-experience.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and CI/deploy configuration.
metadata:
  version: "2.9.2"
---

# Environment Lifecycle

## Mission

Design the environment path from local to production so every stage is self-describing, disposable, promotion-safe, and production-like.

Environments are infrastructure with a contract, not machines that accumulate. Every non-production environment is ephemeral by default: it has a TTL, a cleanup path, and a cost owner at creation. Config and secrets promote through an explicit contract, never by copy-paste. Data outside production is seeded, branched, or sanitized, never raw production data.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Environment topology design

Design the path in order. Do not skip stages; skipping forces production to absorb test weight.

### 1. Map the stages and their responsibilities

Read `references/environment-taxonomy.md`.

Name every stage in the path: local, test, preview, staging, production. Record for each stage its primary job, its deploy automation, its data, and who verifies it. Staging uses production-like topology; it is not production-adjacent optimism.

### 2. Make ephemeral environments the default

Read `references/ephemeral-environments.md`.

Every PR or branch preview is a disposable environment created on demand and destroyed on a schedule. Model creation on the ideal pattern `product env create pr-482 --from=production` even when the tooling is plain scripts: branch from a known snapshot, apply config and seed, report a ready URL, record a TTL.

### 3. Promote config and secrets through a contract

Read `references/config-and-secrets-promotion.md`.

Config promotes forward stage by stage with a review point before production. Secrets are stage-scoped, stored in per-stage stores, and never promoted downward or printed.

### 4. Design seed data and database branching

Read `references/seed-and-clone.md`.

Seed data is deterministic, versioned, and idempotent. Preview environments branch databases from production snapshots; the clone is sanitized before any data crosses the boundary.

### 5. Enforce TTL, cleanup, and cost

Read `references/cleanup-and-cost.md`.

Every ephemeral environment carries a TTL marker at creation. Cleanup automation deletes expired environments and orphans. Cost controls cap what an environment may consume.

### 6. Inventory the current state

Run `scripts/check_environment_lifecycle.py` against the repository. It is inventory only: it lists surfaces and gaps and always exits 0. Treat its output as the baseline, never as the design.

### 7. Render the environment map

Complete `assets/environment-map-template.md`. The map is the contract: what exists, what is missing, and what each stage holds and costs.

## Environment contract

Every environment in the path must be:

- **self-describing**: name, stage, owner, TTL, and creation source are recorded where it is created
- **disposable**: destroying it is safe, scripted, and does not disturb adjacent stages
- **reproducible**: created from committed code and config, never from a hand-built box
- **production-like**: topology and config approach production as the stage nears production
- **observable**: URL, logs, and status are discoverable from the PR or commit

An environment that cannot be destroyed is a server, not an environment.

## Per-stage contract

- **local**: the single-developer loop; fastest feedback, no shared state. Use the `local-development` skill for this stage.
- **test**: automated verification in CI; isolated, fast, disposable, no shared state.
- **preview**: per-PR or per-branch, ephemeral with a TTL, seeded, production-like topology.
- **staging**: promotion gate; production-like data, topology, and config; the last non-production check.
- **production**: stable and gated; cost-controlled; carries no test data.

Nothing tests against production that test, preview, or staging can absorb.

## Ephemeral environment contract

- created on demand, destroyed by schedule or by merge, never left to pile up
- carries a machine-readable TTL marker at creation, not a comment
- extends only with owner approval, for a bounded period
- receives seed data, never raw production data
- reports readiness: URL, status, and creation metadata visible on the PR

## Promotion contract

- code and config promote forward: local → test → preview → staging → production
- promotion is automated, diffed, and reviewed; production promotion requires a gate
- config is committed and versioned; secrets are never typed into files
- secrets live in stage-scoped stores; test and preview use synthetic credentials
- a stage's secrets are never promoted downward or reused by another stage

## Data contract

- seed data is deterministic, versioned, idempotent, and pinned per stage
- preview and staging databases branch from production snapshots
- clones are sanitized before data leaves the boundary; PII is scrubbed
- production data is never copied to a non-production stage un-sanitized
- schema drift is handled by branching from the snapshot, not by guesswork

## Cleanup and cost contract

- every ephemeral environment has a TTL and an enforcement job
- cleanup automation deletes expired environments and orphans on a schedule
- an environment without a cost owner is deleted, not archived
- budgets, alerts, and resource caps are set per stage; preview is the cheapest stage
- cleanup claims carry an evidence label: Observed, CI-observed, or Estimated

## Design checklist

Verify before shipping the environment path:

### Topology

- every stage has one primary job and an owner
- staging mirrors production topology and config
- stage names match the canonical vocabulary

### Ephemeral and PR

- previews are created on demand from a known snapshot
- creation records name, owner, TTL, and source in machine-readable form
- TTL markers are enforced, not advisory
- previews destroy on merge or expiry

### Promotion

- config promotes forward with a diff and a review point
- secrets are stage-scoped and never promoted downward
- test and preview use synthetic credentials

### Data

- seed data is deterministic, versioned, and idempotent
- databases branch from sanitized snapshots
- no raw production data reaches a non-production stage

### Cleanup and cost

- cleanup automation is scheduled and observable
- orphans are deleted on the next run
- budget, alert, and cap are set per stage

### Evidence

- every claim carries an evidence label: Observed, CI-observed, or Estimated

## Required output

For every environment-lifecycle engagement, produce the environment map from `assets/environment-map-template.md`.

The map must contain:

1. **Stage map** — every stage with its primary job, deploy automation, data, and owner
2. **Surface inventory** — the output of `scripts/check_environment_lifecycle.py`
3. **Gap list** — missing surfaces keyed by severity, with the fix and owner
4. **TTL and cleanup plan** — TTL per environment type and the enforcement job
5. **Cost controls** — budget, alert, and cap per stage
6. **Secrets and config** — config source and secret store per stage, promotion path
7. **Evidence labels** — Observed / CI-observed / Estimated on every claim

## Definition of done

An environment path is done when:

- every stage in the path is named and has one primary job
- preview environments are ephemeral, TTL'd, and destroyed by schedule or merge
- cleanup automation exists and is scheduled
- config and secrets promote through the contract, with a production gate
- seed, clone, and sanitization paths exist for every non-production data need
- staging mirrors production topology and config
- the inventory script shows no unexplained gaps in the surfaces
- every claim in the map carries an evidence label
- handoffs are explicit: `local-development` for the single-developer loop, `sandbox-experience` for sandbox safety
