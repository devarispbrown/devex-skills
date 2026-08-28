# Environment Taxonomy

## The path

local → test → preview → staging → production

Each stage has exactly one primary job. If a stage's job is unclear, the stage does not exist yet.

## Stage responsibilities

### local

- single-developer loop: edit, run, test, verify
- no shared state; only the developer's own services
- fastest feedback; use the `local-development` skill
- data: seeded fixtures or the developer's own

### test

- automated verification in CI on every push and pull request
- isolated, disposable, parallel-safe
- data: seeded fixtures, never production

### preview

- per-PR or per-branch verification in production-like topology
- ephemeral by default: TTL'd, seeded, observable from the PR
- data: seeded and sanitized branch, never raw production

### staging

- the promotion gate before production
- production-like topology, config, and data shape
- the last place to find production-only problems

### production

- the stable contract with users
- gated, cost-controlled, audited
- data: production; no test data, no demo records

## Topology rules

- staging mirrors production: same services, same scaling knobs, same deploy mechanism, different credentials
- preview mirrors staging minus cost: smallest viable production-like topology
- promotion moves code and config forward; nothing promotes backward
- an environment that diverges from its stage contract is mislabeled and should be recreated
- stage names are fixed vocabulary: local, test, preview, staging, production. Do not invent synonyms.

## Verification per stage

| Stage | Verifies |
|---|---|
| local | the dev loop works |
| test | the change is correct in isolation |
| preview | the change is correct in a production-like topology |
| staging | the change survives the production path |
| production | the change is released |

## Evidence

Claims about what a stage verifies carry an evidence label: Observed, CI-observed, or Estimated.
