# Config and Secrets Promotion

## Config promotion procedure

Config promotes forward, stage by stage, in the same review flow as code:

1. commit config to the repository as code
2. validate on the previous stage: preview validates what staging will use
3. promote to the next stage by diffing against the previous stage's validated config
4. review the diff before production promotion
5. promote to production through the release gate

Rules:

- config is versioned, reviewed, and diffable; no drift by direct edit
- an environment reads config from its stage, never from another stage
- promotion never copies production config backward
- defaults live with the code; stage overrides live in stage files

## Precedence

Explicit precedence per stage, from highest to lowest:

1. stage secret store (values never in files)
2. stage config (committed, environment-specific)
3. shared config (committed)
4. built-in defaults

Document the precedence where config is defined. Undefined precedence is a defect.

## Secrets per stage

- secrets are stored per stage in stage-scoped stores (secret manager, vault, CI environment)
- test and preview use synthetic credentials; they never hold production secrets
- staging holds production-shaped secrets only when required to verify the production path; otherwise synthetic
- production holds the real secrets; nothing else reads that store
- a secret is never promoted downward: preview never reads staging's store, staging never reads production's

## Secret handling rules

- never type, print, or commit secrets; never paste them into files, logs, or chat
- reference secrets by name in config and deploy automation
- rotate on schedule and on any leak suspicion
- mask secrets in logs and CI output
- a leak in one environment is contained to that stage's store

## Promotion check

Before promoting config or secrets to the next stage:

- the diff is reviewed and recorded
- the previous stage validated the config
- secrets are scoped to the target stage, never copied from a higher stage
- rollback is possible: the previous stage's config and secrets are intact
