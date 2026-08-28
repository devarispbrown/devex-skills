# Factories and Seed Data

Factory patterns and seed data design for the `test-data-and-fixtures` skill.

## When to use factories

Use factories when tests vary one or a few fields over a shared shape and the shape is stable. Use plain fixture files when the data is fixed and tests assert against the file as-is. Use seed data when many flows share the same baseline rows and the database is the unit under test.

## Factory design

1. One factory per domain shape (User, Order, Invoice), sharing one defaults module.
2. Defaults are valid, safe, and deterministic. Every factory call without overrides returns a usable object.
3. Overrides are explicit arguments, never hidden global state.
4. Sequences (`user-1@example.com`, `order-1`) increment deterministically per run.
5. Random fields use a seeded RNG; the seed is recorded so a failure reproduces.
6. Traits compose: `with_plan("pro")`, `as_inactive()`, `with_credit_card()` — each trait changes only the documented fields.
7. Factories build in-memory objects by default; database persistence is an explicit step so unit tests never touch the DB unless they must.

## Seed data design

- Seeds are the canonical baseline rows for local dev and CI: a small, curated set, not a dump.
- Seeding is idempotent: rerunning produces the same state (upsert by natural key).
- Seeds carry a schema version or checksum so stale seeds fail loudly instead of silently.
- Environment-specific rows (dev vs CI vs e2e) live in separate files that share a base, never duplicated.
- Seed values obey the same hygiene rules as any fixture: placeholder domains, no real secrets, no production markers.

## Anti-patterns

- a factory whose default output is invalid or unsafe
- factories reaching into production config or env at import time
- seed files that hand-edit generated output
- copying the fixture tree per test file; reference the canonical location
