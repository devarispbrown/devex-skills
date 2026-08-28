# Migration Requirements

Migration requirements define what consumers must do before, during, and after upgrade. They are part of the release contract, not an afterthought.

## When a migration guide is mandatory

- any breaking class entry
- any change to persisted schemas or data formats
- any change to authentication, credentials, or configuration precedence
- any operational or rollout behavior change (retries, quotas, webhook delivery)
- promotion of preview surface to stable

A breaking change without a migration guide is `UNDOCUMENTED_BREAKING_API`.

## Content contract

A migration guide must cover:

1. **What changed** — the surface, before and after, with examples.
2. **Why it changed** — the motivation and the intended behavior.
3. **Upgrade steps** — ordered, complete, copy-pasteable where applicable.
4. **Compatibility window** — how far back supported versions go and what that means for the upgrade path.
5. **Deprecations** — replacement and timeline for every deprecated surface touched.
6. **Verification** — how the consumer confirms the migration succeeded.
7. **Rollback path** — how to undo the upgrade and what is lost.

## Rollback path

Define the rollback path for any operationally risky change: schema changes, webhook payload changes, auth changes, background data transforms.

Verify:

- the rollback restores the prior behavior without data loss, or the data loss is stated
- rollback steps are ordered and tested where feasible
- irreversible changes are flagged before the release, not in an incident

## Procedure

1. Identify every class entry that triggers a mandatory guide.
2. Draft the guide against the content contract.
3. Verify the rollback path with the owning team.
4. Record the guide location and rollback path in the verdict report.

Never release a breaking change with the migration guide pending.
