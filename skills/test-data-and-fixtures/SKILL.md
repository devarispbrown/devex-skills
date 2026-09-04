---
name: test-data-and-fixtures
description: Author fixtures, seed data, factories, fake services, mock servers, record-replay cassettes, golden files, synthetic datasets, and sanitization, with a project test-data create pattern. For sandbox route design use sandbox-experience; for per-system-type test strategy use quality-engineer.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and test tooling.
metadata:
  version: "2.7.1"
---

# Test Data and Fixtures

## Mission

Create project test data that is deterministic, realistic where it matters, free of production residue, and regenerable on demand. Test data is committed infrastructure, not an ad hoc side effect: every fixture is authored against truth, checked for hygiene, and owned by the team that maintains it.

Match the fixture to the system's failure modes. Static seeds fit CRUD flows, factories fit variation-heavy logic, fake services fit integration seams, cassettes fit external API consumers, synthetic datasets fit volume and distribution work. Per-system-type test strategy is the `quality-engineer` skill's domain, and sandbox route design belongs to `sandbox-experience`; this skill produces the data those strategies consume.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Fixture authoring

The project test-data create pattern: scope the tree, choose the types, author from truth, keep deterministic, sanitize, verify, and wire regeneration.

### 1. Scope the fixture tree

Choose one canonical test-data location per repository: `testdata/`, `fixtures/`, or `tests/fixtures/`. Put factories and generators beside the fixtures in test support, never in production code.

Rules:

- one location, stable names, one owner
- never ship fixtures in production builds or read them from application runtime paths
- never commit test data the application would treat as real at runtime
- name files by role (`users_seed.csv`, `orders_seed.json`), not by author or date
- a fixture without a documented regeneration path is a liability

### 2. Choose the fixture type by need

| Need | Type |
|---|---|
| fixed, versionable baseline data | static fixture files |
| per-test variation over a shared shape | factories |
| canonical reference rows for local dev and CI | seed data |
| replace a dependency at an integration seam | fake services / mock servers |
| capture and replay external API interactions | record-replay cassettes |
| expected output for formatters, compilers, report generators | golden files |
| volume, distribution, or privacy-free realism | synthetic datasets |
| real behavior with real data removed | sanitized production snapshots |

Read `references/factories-and-seeds.md` when writing factories or seed data. Read `references/mock-servers.md` when deciding between a fake, a mock, or a recorded dependency. Read `references/record-replay.md` when capturing external API interactions. Read `references/golden-files.md` when snapshotting expected output. Read `references/synthetic-datasets.md` when generating data at volume. Read `references/sanitization.md` before any fixture that touches real data.

### 3. Author from truth

Ground every fixture in the real schema, API contract, or spec:

1. Read the schema or contract first; never invent fields, defaults, or enums.
2. Use real shapes with realistic but safe values.
3. Keep each fixture minimal: only the data the test path needs.
4. Reference shared constants from one source; do not duplicate values by hand.
5. Make failure cases explicit fixtures, not mutations of happy-path data.

### 4. Keep fixtures deterministic

- fix every seed, timestamp, and generated identifier
- random variation is explicit and seeded, never implicit
- committed fixtures do not depend on wall clock, hostname, locale, or database ordering
- expected values are asserted against the fixture, not computed from live state
- document the generation command so regeneration reproduces the same bytes

### 5. Sanitize anything that touches real data

Before a fixture can include production-derived data, run the procedure in `references/sanitization.md`: inventory PII and secrets, replace with safe equivalents, preserve distributional realism where the tests need it, verify no original value survives, and record the sanitization in the report. A fixture containing a real email, key, card number, or production marker is a hygiene failure, not a test asset.

### 6. Verify hygiene

Run `scripts/check_fixture_hygiene.py <tree>` before committing and on every relevant change. The checker scans for real-looking email addresses, key-like strings, credit-card patterns, and unsanitized production markers, and exits 1 on any finding. Zero findings is the contract; an exception requires a filed hygiene record, never a silent skip.

### 7. Wire regeneration and ownership

- commit the generator or the regeneration command with the fixtures
- add a smoke test that fails when a fixture drifts from its schema
- record owner and update cadence in the report
- when a golden file changes, review the change; regenerating to silence a review is a defect

## Fixture contract

A fixture is correct when:

- it matches the schema or contract it feeds, including nullability and constraints
- it is deterministic and regenerable from a documented command
- it contains no real emails, keys, secrets, card numbers, or production markers
- its purpose is named and discoverable from the tree
- consumers reference the canonical tree, not copies

## Factory contract

- one factory per domain shape, with a single source of truth for defaults
- defaults are valid, safe, and deterministic; overrides are explicit arguments
- factory-produced values never contain real personal data or secrets
- randomized fields use a seeded RNG with a documented seed
- factories live in test support, never in production code paths

## Mock server contract

Read `references/mock-servers.md`.

A fake service or mock server must:

- mimic documented behavior and error semantics, not incidental implementation
- cover the success path and the failure paths the consumer handles
- hold no real credentials; auth is simulated
- be started and stopped by the test harness, never by external convention
- prefer a fake with real behavior over a mock with canned responses when the seam allows

## Record-replay contract

Read `references/record-replay.md`.

Cassettes must:

- be captured against a sandbox or test environment, never production
- be scrubbed of secrets, tokens, and personal data before commit
- carry the recorded date and provider version so staleness is visible
- be re-recorded deliberately when the contract changes, never silently
- not be used to assert exact bytes unless byte-exactness is the contract

## Golden file contract

Read `references/golden-files.md`.

Golden files must:

- be produced by a committed generator, with the generation command documented
- change only through regeneration, reviewed as a diff
- be updated in the same change as the code that alters the output
- have a stated update policy (auto-bless vs. human-reviewed) per directory
- never be hand-edited to pass; hand-editing a golden file hides drift

## Required output

For every fixture-authoring task, produce:

1. **Fixture tree** — the created or updated files, scoped and named per step 1
2. **Hygiene check** — `scripts/check_fixture_hygiene.py` output with zero findings, or a filed exception
3. **Regeneration path** — the command that reproduces the fixtures, with owner
4. **Sanitization record** — for any real-data source: the source, the transforms applied, and how the original values were verified absent
5. **Report** — `assets/fixture-report-template.md` filled in for large or cross-cutting work

## Definition of done

Fixture authoring is done when:

- every fixture is grounded in schema or contract truth
- the tree is scoped to one canonical location with named roles and an owner
- committed fixtures are deterministic and regenerable from a documented command
- the hygiene checker passes with zero findings
- real-data fixtures carry a sanitization record
- consumers reference the canonical tree; no copies drift
- golden files change only through reviewed regeneration
- cross-skill boundaries are respected: `sandbox-experience` owns sandbox route design, `quality-engineer` owns per-system-type test strategy, and this skill owns the data itself
