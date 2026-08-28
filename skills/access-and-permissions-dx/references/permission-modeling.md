# Permission Modeling Standard

## Objective

Model auth and RBAC so every permission can be named, requested, granted, audited, and revoked independently. A permission model that only admins can read is a defect.

## Source of truth

Enumerate the model from implementation and policy, never from prose:

- authorization checks in code, middleware, and gateway policies
- IAM, role, and scope definitions in config and infrastructure
- tests that assert who can do what
- audit logs of actual denials and grants

When sources disagree, report the contradiction. The machine-readable model is the source the denial text and token previews cite.

## Procedure

1. **Inventory actions.** List every operation that can be denied: endpoints, commands, UI actions, API methods, background jobs.
2. **Name permissions.** Give each guard exactly one name, `resource:action` or the platform's native form. One guard, one name; no synonyms.
3. **Define scopes.** State what each permission covers: resource, workspace, environment, or tenant. A permission without a stated scope is incomplete.
4. **Define roles.** Assign permissions to roles at least-privilege granularity. Name roles for what they do, not who holds them.
5. **Count wildcards.** Enumerate every wildcard and blanket role and how many permissions each grants. Justify each; an unexplained wildcard is a P1 finding per the canonical severity vocabulary.
6. **Verify requestability.** Confirm each permission can be requested in isolation through a self-service route; see `grant-flows.md`.

## Naming rules

- one canonical name per permission, matching the enforcing code
- no separate human and machine names for the same permission
- deny text, request forms, token previews, and audit logs use the same name

## Self-serviceability criteria

A permission is self-service when a denial states it, a request route exists for it, the grant is least-privilege and time-bound, and the grant is auditable. Failing any criterion is a defect, not a documentation gap.
