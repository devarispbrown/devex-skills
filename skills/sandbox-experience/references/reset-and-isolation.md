# Sandbox Reset and Isolation

## Purpose

Guarantee the sandbox returns to a known state on demand and that experimenters cannot affect one another or production. Reset and isolation are properties of the route, verified by demonstration, never by assumption.

## Reset procedures

1. Define the reset for each route: tear down and recreate, reseed from a fixture, or restore from a snapshot.
2. Reset must restore a known, deterministic state — not merely "empty".
3. Exercise reset at least once during the audit. Record the exact steps and the observed state after reset.
4. Verify the reset is repeatable: reset twice, confirm identical state both times.
5. Reset must be self-service. A route that needs manual approval or a support ticket to restore is not resettable.

## Tenant isolation

- each experimenter (human, agent, CI run) gets a separate tenant, namespace, or environment
- no shared mutable state between tenants
- credentials, test keys, and fixtures are scoped to exactly one tenant
- no tenant's reset can affect another tenant's state

## Cleanup guarantees

- cleanup removes every resource the sandbox created
- cleanup leaves no residue: no records, keys, jobs, or events in shared or production resources
- cleanup never requires manual approval or a support ticket

## Verification checklist

- the reset procedure is documented and demonstrated
- the seeded state is deterministic and inspectable
- isolation between tenants was verified by cross-tenant checks
- cleanup was executed and verified to leave no residue
- evidence is labeled: **Observed**, **CI-observed**, or **Estimated**

An estimate can never prove reset or isolation. A claim without an evidence label is UNVERIFIED.
