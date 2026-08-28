---
name: compatibility-engineer
description: Maintain and verify the compatibility matrix: runtime versions, databases, platforms, and architectures. Upgrade testing, downgrade behavior, wire compatibility, schema evolution, dependency ranges, and OS/arch matrices. Compatibility claims must carry CI evidence. For versioning recommendations use release-guardian; for actually testing integrations use integration-certifier.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and CI matrix configuration.
metadata:
  version: "2.2.0"
---

# Compatibility Matrix Engineering

## Mission

A compatibility claim is a promise to users. Every version, database, platform, and architecture listed as supported must carry CI or equivalent evidence; claims nobody tested accumulate, rot, and become support obligations the product cannot honor.

Maintain the compatibility matrix as a tested artifact: inventory claims, define the matrix, verify upgrade and downgrade paths, test wire and schema evolution, set dependency ranges, and wire the matrix into CI so evidence regenerates on every relevant change.

Do not publish or preserve a support claim without evidence. Never label a version supported on the basis of "it probably works".

## Claims need evidence

Every matrix claim has exactly one status, decided by evidence, never by intent:

- **EVIDENCED** — a matching CI matrix entry or test evidence marker exists for the exact claimed version or platform.
- **UNTESTED** — the claim carries no evidence; this is the `UNTESTED_SUPPORTED_VERSION` gate failure from `references/standards.md`.
- **MISSING** — evidence was recorded but the marker file or CI match cannot be found; treat as UNTESTED.

Run `scripts/check_compat_matrix.py` against the matrix JSON to produce the claim-vs-evidence table. The script is a first-pass signal, never a substitute for reading the evidence.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read `references/compatibility-matrix.md` when defining matrix dimensions, tier labels, and the matrix JSON schema.

Read `references/upgrade-testing.md` when designing upgrade path tests, data migration checks, and the N-1/N-2 policy.

Read `references/wire-and-schema.md` when verifying wire protocol compatibility, schema evolution, or serialization changes.

Read `references/matrix-ci.md` when wiring matrix cells into CI and budgeting which cells run on every push versus nightly.

Read `references/dependency-ranges.md` when setting dependency version ranges or maintaining minimum supported versions.

## Compatibility engineer workflow

### 1. Inventory compatibility claims

Search the repository for every place a version or platform is claimed: README and docs, package metadata, CI configs, changelogs, support pages, and release notes.

Record each claim as surface plus exact version string plus provenance.

Classify surfaces: runtime, database, platform, architecture, dependency range, wire/schema.

Do not assume docs and metadata agree; surface every contradiction and let the evidence decide.

Verify: every claim is listed, provenance is recorded, and no claim hides in prose that names a version without a matrix row.

### 2. Define the compatibility matrix

Read `references/compatibility-matrix.md`.

Choose the dimensions the product actually runs on; do not pad the matrix with theoretical cells.

Assign every cell exactly one tier: supported, best-effort, or deprecated.

Only supported cells require evidence. Best-effort is explicitly not supported and may break at any time.

Deprecated cells carry an end-of-support date and require no new evidence.

Never claim a cell supported without evidence.

Verify: every inventoried claim maps to a cell, tiers are explicit, and the matrix JSON parses under `scripts/check_compat_matrix.py`.

### 3. Verify upgrade paths

Read `references/upgrade-testing.md`.

Define the upgrade ladder: the current release must upgrade from N-1 and N-2.

Execute upgrades in CI: clean install of the old version, seed representative data, upgrade in place, run migrations.

Run data migration checks after every upgrade: schema drift, backfill completeness, referential integrity, spot queries.

Verify: N-1 and N-2 paths exist, data checks run after each step, and results are recorded as evidence markers.

### 4. Verify downgrade and wire behavior

Define downgrade behavior per release: a tested rollback path, or explicitly documented as unsupported. Never leave it silent.

Verify wire compatibility across versions: requests and responses must round-trip between old and new consumers.

Read `references/wire-and-schema.md`.

Verify: the rollback decision is recorded, and wire tests cover old client against new server and new client against old server.

### 5. Test schema evolution

Read `references/wire-and-schema.md`.

Prefer additive schema changes: new fields, new enum values, expanding contracts.

Test that older readers and writers tolerate the new shape without error.

Test serialization changes round-trip; verify parser strictness and unknown-field tolerance.

Never change a persisted format without an evolution test.

Verify: every persisted format has an evolution test, and breaking changes are routed through versioned contracts.

### 6. Wire matrix CI

Read `references/matrix-ci.md`.

Map every supported cell to a CI job or evidence marker; a supported cell with no job is a gap.

Decide cadence: cheap cells on every push, expensive cells nightly.

Collect evidence: job logs, test result files, and machine-readable matrix reports that `scripts/check_compat_matrix.py` can resolve.

Verify: every supported cell has a job or marker, and CI emits a matrix report on the configured cadence.

## Matrix contract

The matrix is a versioned JSON artifact, not a prose table.

Rules:

- A version may be listed without evidence only in the best-effort or deprecated tiers.
- Evidence is a CI job that exercised the exact version, a test result marker file, or a link to a recorded CI run.
- Evidence must name the exact claimed version; approximate matches do not count.
- Dropping a version is recorded in the deprecated tier, never by silent deletion.
- A tier change is a release event: review it before the tag.

## Upgrade/downgrade contract

- The current release supports upgrading from N-1 and N-2, per the N-1/N-2 policy in `references/upgrade-testing.md`.
- Upgrade tests run against representative data, and migrations are exercised, not skipped.
- Downgrade is tested or explicitly documented as unsupported; silent breakage is a defect.
- Additive wire and schema changes must not break older consumers.
- Breaking wire or schema changes require a versioned contract change and a `release-guardian` review.

## Required output

Produce the compatibility report using `assets/compat-report-template.md`.

The report must contain:

1. **Matrix table** — claim versus evidence per cell: surface, version, tier, evidence, status.
2. **`UNTESTED_SUPPORTED_VERSION` findings** — every supported claim without evidence, named by surface and version, with the fix.
3. **Gap list** — supported cells with no CI job, upgrade paths not tested, schema changes untested, dependency ranges unverified.
4. **Evidence labels** — Observed, CI-observed, or Estimated per row, per `references/standards.md`.

## Definition of done

Compatibility work is done when:

- every compatibility claim is inventoried with provenance
- the matrix JSON parses and every supported claim carries evidence or is reported as `UNTESTED_SUPPORTED_VERSION`
- upgrade paths N-1 and N-2 are tested with data migration checks
- downgrade behavior is tested or explicitly documented
- wire and schema evolution tests cover every persisted format
- every supported cell has a CI job or evidence marker at the configured cadence
- the report is rendered from `assets/compat-report-template.md` with labeled evidence
- no claim was promoted to supported without evidence

Hand off version recommendation to the `release-guardian` skill if available, and integration execution against live systems to the `integration-certifier` skill if available.
