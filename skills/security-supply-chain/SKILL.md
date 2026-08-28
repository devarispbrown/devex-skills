---
name: security-supply-chain
description: Harden the security posture of an open-source project: SECURITY.md, dependency vulnerabilities, secret handling, workflow permissions, branch protection, artifact signing, provenance, SBOMs, dependency pinning, release integrity, CODEOWNERS, SAST, and fuzzing. Distinguish library, runtime, build, release, and repository security. For dependency upgrade hygiene use dependency-health; for permission-model ergonomics use access-and-permissions-dx; for policy-as-code and compliance use policy-experience.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and CI/security tooling.
metadata:
  version: "2.3.0"
---

# Security Supply Chain

## Mission

Security posture is developer experience. A project that leaks secrets, ships unverifiable artifacts, or breaks under a supply-chain incident destroys the trust developers need to adopt and keep it.

Harden the security posture of an open-source project end to end: SECURITY.md and reporting, dependency vulnerabilities, secret handling, workflow permissions, branch protection, artifact signing, provenance, SBOMs, dependency pinning, release integrity, CODEOWNERS, SAST, and fuzzing.

Treat posture as a property of committed configuration, CI, and the release process — never as the output of a single tool run. Do not declare a project secure because one scan came back clean. Never change code, CI, or release configuration during an audit; report and prioritize, then fix in a separate pass.

## Five security surfaces

Security work lands on five distinct surfaces. Audit each separately and never average findings across surfaces:

- **Library security**: the code consumers depend on — its own dependency tree, pinning, and published interface.
- **Runtime security**: the running product — deployment hardening, least privilege, and secrets at runtime.
- **Build security**: the CI pipeline that turns commits into artifacts — actions, permissions, and secrets.
- **Release security**: the artifacts and metadata consumers receive — signing, provenance, SBOMs, checksums, tags.
- **Repository security**: the project's governance surface — SECURITY.md, CODEOWNERS, branch protection, review requirements.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Security posture audit workflow

Run the six steps in order. Every step ends with findings; step 6 turns them into the report.

### 1. Inventory the project

Run `scripts/check_security_posture.py` against the repository root as a first-pass inventory.

Verify:

- SECURITY.md, CODEOWNERS, and `.github/workflows/` presence is recorded, present or absent
- every workflow file is listed with its risky patterns: unpinned `uses:` refs, `pull_request_target` triggers, and `secrets.` references in run blocks
- branch protection is marked as unverifiable from the tree and scheduled for manual verification

The script informs; it never fails a repository and never renders a verdict. When testing the scanner itself, run it against `assets/workflow-risky.example.yml` and confirm it flags the unpinned actions, the `pull_request_target` trigger, and the inline secret.

### 2. Audit repository security

Read `references/repository-security.md` when auditing SECURITY.md, CODEOWNERS, branch protection, workflow permissions, and review requirements.

Verify:

- SECURITY.md satisfies the SECURITY.md contract below, with a real reporting channel
- CODEOWNERS covers every path with a reviewer, including release and CI paths
- branch protection requires reviews, status checks, and signed commits on the default branch
- workflow permissions are least privilege and third-party actions are pinned

Do not report branch protection as present without checking the hosting platform; absence is a finding, unverified is a finding.

### 3. Audit build and CI security

Read `references/build-and-ci-security.md` when hardening GitHub Actions, pinning actions, scoping secrets, protecting PRs from forks, and wiring SAST into CI.

Verify:

- every third-party action is pinned to a full commit SHA, with the version recorded in a comment
- no untrusted input flows into `run:` blocks without escaping or indirection
- secrets are scoped to the job that needs them and mapped through `env:`
- PR-from-fork paths never run untrusted code with base-branch credentials
- SAST runs on every push and pull request and blocks P0/P1 findings

Read `references/fuzzing-and-sast.md` when deciding where SAST and fuzzing pay off, wiring them into CI, and triaging their findings.

### 4. Audit dependency and secret posture

Read `references/dependencies-and-secrets.md` when triaging dependency vulnerabilities, reviewing lockfile and pinning policy, detecting secrets, and remediating historical exposure.

Verify:

- lockfiles are committed and dependency versions are pinned per the policy in the reference
- every known vulnerability has a triage entry: affected, exploitable, patched, or accepted, with severity
- secret detection runs on the diff in CI, not only on the tree
- exposed historical secrets are revoked, rotated, purged, and consumers updated

Never treat a scrubbed secret as fixed. Fixed means revoked, rotated, purged, and consumers updated.

### 5. Audit release integrity

Read `references/release-integrity.md` when auditing artifact signing, provenance and SLSA, SBOMs, checksums, release process isolation, and tag protection.

Verify:

- released artifacts are signed and checksums are published
- a provenance attestation describes how and from what the artifacts were built
- an SBOM accompanies the release artifacts and matches what shipped
- the release process runs from protected state, never ad hoc from a developer machine
- tags are protected against force-push and deletion

Do not ship a release without the integrity material consumers would need to verify it.

### 6. Prioritize fixes

Map every finding to a severity using the canonical severity vocabulary in `references/standards.md`.

Verify:

- P0 findings (exploitable unpatched dependencies, exposed live secrets, unsigned release artifacts, unprotected tag or registry writes) are scheduled immediately
- P1 findings block release; P2/P3 enter a tracked backlog; P4 is deferred
- every finding carries an evidence label: Observed, CI-observed, or Estimated
- the prioritized fix list states the fix, the acceptance test, and the owner type for each item

Hand off dependency upgrade hygiene to the `dependency-health` skill if available, release contract verification to `release-guardian` if available, and deep code-level review to `security-review` if available. This skill owns the posture audit; it does not replace those.

## SECURITY.md contract

A repository that accepts public contributions must ship a SECURITY.md at the repository root. It must state:

1. where to report a vulnerability (email, form, or private advisory) and what to include
2. the expected response and disclosure timeline
3. supported versions and which receive security fixes
4. how patches are released and announced

Do not ship a placeholder SECURITY.md with no reporting channel. Never ask reporters to file public issues for vulnerabilities.

## Release-integrity contract

A release is not complete until it ships the integrity material its artifacts require:

1. signed artifacts, or an independently verifiable checksum manifest
2. a provenance attestation describing how and from what the artifacts were built
3. an SBOM listing the dependency inventory of the artifact
4. release process isolation: release builds run from protected state, not ad hoc
5. tag protection against force-push and deletion

Never sign artifacts from an unverified build. A release missing any item above fails the release-integrity contract.

## Required output

Produce the security posture report using `assets/security-posture-template.md`.

The report must contain:

1. **Scope and evidence** — repository, revision, environment, and an evidence label (Observed / CI-observed / Estimated) for every claim
2. **Findings by surface** — one table per surface (library, runtime, build, release, repository): finding, severity, evidence, fix
3. **Prioritized fix list** — every finding ordered by severity, with fix, acceptance test, and owner type
4. **Contract checks** — SECURITY.md contract and release-integrity contract, item by item, pass/fail/unverified
5. **Posture verdict** — exactly one of PASS / PASS WITH DEBT / FAIL / UNVERIFIED, with the debt or failure list

Every finding carries its evidence label. Unlabeled findings are UNVERIFIED.

## Definition of done

The audit is done when:

- the step 1 inventory is complete and the scanner output is attached
- every surface was audited and every finding is recorded with severity and evidence label
- the SECURITY.md and release-integrity contracts are checked item by item
- the prioritized fix list schedules P0 work immediately and ties P1 work to the release
- the report is rendered from `assets/security-posture-template.md`
- no finding is hidden behind a score, a single tool run, or an assumption
- unverifiable claims (branch protection, registry settings) are marked UNVERIFIED, never assumed
- cross-skill handoffs (dependency upgrade hygiene, release gating, code-level review) are named where they apply
