# Seed Data and Database Branching

## Seed data

Seed data is what non-production stages run against. It must be:

- **deterministic**: same version produces the same data, every time
- **versioned**: seed version is pinned per stage; code and seed version travel together
- **idempotent**: applying twice is safe and yields one copy
- **small**: enough to exercise the flows, not a copy of production
- **realistic**: shape and cardinality resemble production where it matters

Seed runs as part of environment creation (see `ephemeral-environments.md`) and in CI before tests.

## Database branching

Preview and staging databases branch from a known snapshot, not from scratch:

- branch from the production snapshot at a recorded point
- the branch inherits schema and data shape at the snapshot
- migrations apply on the branch; schema drift is caught in preview, not production
- a branch is destroyed with its environment; nobody fixes a drifted branch

The `product env create pr-482 --from=production` pattern is database branching plus environment creation in one operation.

## Sanitized clones

Any copy of production data leaving the production boundary is sanitized first:

- PII is scrubbed: names, emails, phones, addresses, and identifiers are randomized or replaced
- payment and credential material is stripped or replaced with test fixtures
- content is checked for secrets before the clone is shared
- sanitization is scripted and part of the clone path, never manual

A clone without a sanitization step is a leak, not a fixture.

## Freshness

- snapshots refresh on a schedule; stale snapshots are deleted
- seed version mismatches are surfaced in the inventory and fixed at creation time
- staging data is refreshed from production-like sources, never from a developer's laptop

## Evidence

Seed and clone claims carry an evidence label: Observed, CI-observed, or Estimated.
