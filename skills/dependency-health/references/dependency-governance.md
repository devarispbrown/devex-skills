# Dependency Governance

## Purpose

Define how dependencies enter, are owned, and leave the graph. Governance makes the health report executable; without it, findings decay into a backlog nobody owns.

## Approval process for new dependencies

A new direct dependency requires approval before it enters a manifest:

1. **Reason:** the capability is not provided by the standard library, the platform, or an existing dependency.
2. **Evidence:** a use site exists; the author can name the importing code.
3. **Alternatives:** duplicates and in-house options were compared; the winner is named.
4. **Maintenance check:** the dependency passes the maintenance-risk assessment, or its deficits are accepted with an owner.
5. **Policy entry:** the dependency gets a policy entry stating why it exists, its class, and its owner.

Never add a dependency without a policy entry. Do not let a bot or a codegen tool add dependencies that skip this process.

## Ownership

- Every direct dependency has exactly one owner: a person or team accountable for maintenance assessment and upgrade decisions.
- Owners are recorded in the report and named in the backlog.
- An unowned dependency is a finding; assign an owner or schedule removal.

## Sunsetting

When a dependency is classified for removal or replacement:

1. State the removal target and the survivor.
2. Write the migration: use sites, behavior changes, verification steps.
3. Land the migration, then remove the dependency and its unused transitive subtree.
4. Update the policy entry to resolved with the removal date.

Do not leave a removed dependency's reason entry as "was here". Record the resolution.

## Monorepo dependency centralization

In monorepos and multi-package repos:

- Centralize shared dependency versions at the workspace root (workspace dependencies, a root manifest, a shared constraints file) instead of repeating per-package pins that drift.
- A dependency declared in more than one manifest is a finding until centralized or justified per package.
- Per-package overrides must be justified in the report; silent divergence between packages is a defect.

## Verify

- every new dependency passed approval and has a policy entry
- every direct dependency has a named owner
- sunsetted dependencies have a completed migration record
- monorepo shared dependencies are centralized or justified
