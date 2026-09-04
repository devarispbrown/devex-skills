---
name: integration-certifier
description: Verify that claimed integrations actually work: which versions, under what configurations, when last tested. Build certification matrices with real test evidence per version/configuration pair. Eliminates 'technically supported'. For maintaining version ranges across releases use compatibility-engineer.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and test/CI infrastructure.
metadata:
  version: "2.9.0"
---

# Integration Certifier

## Mission

Integration claims without evidence are the product's most common lie. Every "supports X", "works with Y", or "compatible with Z" is a promise a user will act on. Make each promise a verified fact with a date on it.

Certify through a contract: inventory every claim, define the certification matrix, design real integration tests, run and record evidence, publish the matrix, and recertify on schedule. A claim becomes a certified cell only when it carries a version, a configuration, test evidence, and a last-tested date.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read `references/claim-inventory.md` when collecting integration claims from docs, marketing, README, and packaging metadata.

Read `references/certification-matrix.md` when designing the matrix and its evidence requirements.

Read `references/integration-tests.md` when designing tests that exercise the real service.

Read `references/recertification.md` when planning recertification cadence and drift response.

Read `references/certification-publishing.md` when publishing the matrix and deprecating uncertified claims.

## No technically supported

"Technically supported" means nobody ever verified it. It is the standard phrase for an unverified claim, and it is banned from docs, README, marketing copy, support matrices, and release notes.

A claim is either certified — a version, a configuration, test evidence, and a last-tested date — or it is uncertified. There is no third state.

Do not soften the truth. Never write "should work with", "generally compatible", or "tested in most environments". Never keep an uncertified claim in user-facing text while matrix work is pending. Uncertified claims are removed or explicitly labeled, not deferred.

## Integration certifier workflow

### 1. Inventory integration claims

Sweep the product surfaces for every integration claim: docs, README, marketing, packaging metadata, adapter code, and support artifacts.

Read `references/claim-inventory.md` when collecting claims.

Verify:

- every claim names the integration target and an explicit version
- every claim states the configuration it covers
- every claim has a source: file, URL, or commit
- claims that fail the testability test are dropped or returned to the owner

Never carry a versionless claim into the matrix.

### 2. Define the certification matrix

Turn the claims list into the matrix: integrations × versions × configurations, one cell per claim. Start from `assets/cert-matrix.example.json` when shaping a new matrix.

Read `references/certification-matrix.md` when designing the matrix.

Verify:

- each cell names the integration, version, configuration, evidence link, and last-tested date
- cell tiers are assigned: certified, certified with caveats, stale, uncertified
- the matrix is machine-readable JSON so the checker can audit it

Do not merge configurations that exercise different code paths into one cell.

### 3. Design real integration tests

Design a test per cell that exercises the real service end to end — not a mock.

Read `references/integration-tests.md` when designing tests.

Verify:

- the test runs against the real service: container, sandbox, or official test environment
- it performs real operations with test credentials and asserts on real responses
- it has explicit timeouts and flake control
- it is committed to the repo and reproducible

Never certify a cell from a mock, a health check, or a connection probe.

### 4. Run and record evidence

Run the tests and record the evidence in each cell.

Run `scripts/check_certifications.py` against the matrix JSON. It flags cells with missing evidence and cells whose last-tested date is older than the staleness threshold (default 90 days, override with `--stale-after-days`), prints the table, and exits 1 when any uncertified or stale cell exists.

Verify:

- every evidence link resolves and points to a real test run
- every last-tested date is the date the evidence was produced
- evidence labels are recorded: Observed, CI-observed, or Estimated
- an estimate never certifies a cell

### 5. Publish the matrix

Publish the matrix where users can find it, honestly labeled.

Read `references/certification-publishing.md` when publishing the matrix.

Verify:

- the published page shows tier, last-tested date, evidence link, and evidence label per cell
- stale and uncertified cells are visible, never hidden
- uncertified claims are removed from marketing and README text or rewritten as time-boxed evaluation
- the report is rendered from `assets/certification-report-template.md`

### 6. Recertify on schedule

Certification expires. Recertify on the cadence and on drift.

Read `references/recertification.md` when planning recertification.

Verify:

- recertification is scheduled, not incidental
- dependency bumps, service changes, config changes, evidence link failures, and user reports trigger immediate recertification
- stale cells are downgraded to uncertified until retested
- each recertification produces a report

## Certification contract

A certification is a promise with four parts:

1. **Integration** — the exact target product or service.
2. **Version** — the target versions actually tested; never a range without per-version evidence.
3. **Configuration** — auth, protocol, runtime, SDK, and deployment details exercised.
4. **Evidence** — a link to a real test run plus the date it passed (last-tested).

Every cell in the matrix is governed by this contract. A cell is certified only when all four parts are present and the last-tested date is within the staleness threshold.

Do not certify from code review, from another product's documentation, from a mock, or from an estimate. Do not keep a certified cell whose evidence link has rotted.

## Recertification contract

Certification is a timestamp, not a property:

- every cell expires; expiry follows the staleness threshold and the recertification cadence
- stale is not "pending" — a stale cell is uncertified until retested
- drift triggers immediate recertification: dependency bumps, service changes, config changes, evidence link failures, user-reported breakage
- no last-tested date is extended without a real test run

## Required output

For every certification effort, produce the certification report using `assets/certification-report-template.md`.

The report must contain:

1. **Summary** — counts of certified, stale, and uncertified cells
2. **Matrix table** — integration, version, configuration, last-tested date, evidence link, and status per cell
3. **Uncertified claims** — each flagged with the reason and the source that claimed it
4. **Stale claims** — each with its last-tested date and the required action
5. **Actions** — what must change before the next recertification

Uncertified claims are flagged in the report and in the published matrix. Never ship a report that hides a stale or uncertified cell.

## Definition of done

Certification is done when:

- every integration claim in scope is inventoried with a source
- every claim is either a certified cell or explicitly dropped or uncertified
- every certified cell carries version, configuration, evidence link, and last-tested date
- evidence links resolve and evidence labels are recorded
- `scripts/check_certifications.py` exits 0 against the current matrix
- the matrix is published with stale and uncertified cells visible
- uncertified claims are removed from user-facing text
- recertification is scheduled and owned
- the report is rendered from `assets/certification-report-template.md`

Hand off documentation work around the published matrix to the `developer-docs` skill if available, and version-range maintenance across releases to the `compatibility-engineer` skill if available. The certifier verifies what is claimed; it does not invent claims or extend support ranges.
