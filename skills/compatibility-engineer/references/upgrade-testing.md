# Upgrade Path Testing

## Purpose

Prove that users on previous releases reach the current release without data loss or behavior change. Upgrade testing is the evidence behind every "upgrade supported" claim.

## N-1/N-2 policy

- The current release must be upgrade-tested from N-1 (previous release) and N-2 (two releases back).
- The policy applies per supported platform: a platform without N-1/N-2 coverage is not supported.
- If N-2 coverage is unaffordable, withdraw the N-2 support claim in the matrix and changelog; never leave it silently unverified.

## Procedure per upgrade path

1. Provision a clean install of the old version on the target platform.
2. Seed representative data: a fixture covering the data shapes the migrations touch.
3. Upgrade in place using the documented upgrade procedure; a fresh reinstall is not an upgrade test.
4. Run migrations; record warnings and failures.
5. Verify behavior: smoke test the main flows against the migrated data.
6. Save the run as an evidence marker (log, JUnit XML, or JSON) and reference it from the matrix.

## Data migration checks

- Schema drift: the migrated schema matches a fresh-install schema of the new version.
- Backfills: every backfill ran and row counts match expectations.
- Referential integrity: no orphaned rows after migration.
- Spot queries: representative reads return correct migrated values.

## Downgrade behavior

- Decide per release: downgrade is tested (rollback path) or explicitly unsupported. Never leave it silent; users will downgrade anyway.
- When supported, test: install the old version over new data and verify the documented rollback path.
- When unsupported, state it in the release notes and the matrix.

## Evidence markers

- Name markers after the path, for example `test-results/upgrade-n1-python311.md`.
- A failed or stale marker is missing evidence, not evidence; the matrix checker reports it.
