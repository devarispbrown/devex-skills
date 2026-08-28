# Ephemeral and PR Environments

## Defaults

- every PR or branch preview is ephemeral
- ephemeral means: created on demand, destroyed on a schedule, safe to delete at any moment
- a preview alive past its TTL is an orphan, not an environment

## Creation

Model every creation path on the ideal CLI pattern:

`product env create pr-482 --from=production`

The pattern implies:

- `pr-482` — the environment is named for its source; the name is the address
- `--from=production` — the environment is branched from a known snapshot, never assembled by hand
- creation is one command; everything needed (config, secrets, seed, URL) is derived, never asked for

When the tooling is plain scripts, implement the same contract: a single create script that takes the source ref and stage and records name, owner, TTL, and creation time in machine-readable form.

## TTL

- every environment carries a TTL marker at creation: machine-readable, e.g. `ttl: 24h`, `TTL=24h`, or an `expires_at` field
- default TTL: 24 hours for preview, 7 days for staging, unless the product says otherwise
- extensions are explicit, owner-approved, and bounded; an environment cannot extend itself
- the TTL marker is the enforcement input; nothing deletes an environment without one

## Lifecycle hooks

Model environment lifecycles with hooks where the platform supports them:

- **on-create**: branch snapshot, apply config and secrets, run seed, report URL
- **on-ready**: health check passes; status and URL visible on the PR
- **on-destroy**: run teardown, release resources, record why it ended

Hooks keep lifecycle code attached to the environment instead of scattered across ad-hoc scripts.

## Naming and URLs

- name = source + stage: `pr-482`, `feature-login-preview`, `main-staging`
- URL is stable for the environment's life and dies with it
- the PR or commit links to the environment's URL and status

## Destruction rules

- destroyed on merge of its PR, on TTL expiry, or by explicit delete
- destruction is scripted, safe, and leaves no stage behind
- recreate is cheaper than repair: when a preview drifts, destroy and recreate

## Orphans

- an orphan is any ephemeral environment past its TTL, or unowned
- orphan detection is part of cleanup automation; see `cleanup-and-cost.md`
- unowned environments are deleted on the next cleanup run

## Sandbox safety

For sandbox safety — learning, experiments, destructive paths — use the `sandbox-experience` skill. Preview environments are not sandboxes.
