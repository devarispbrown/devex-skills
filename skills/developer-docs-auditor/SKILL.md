---
name: developer-docs-auditor
description: Adversarially audit and release-gate developer documentation for correctness, drift, executable examples, API/SDK/CLI/config parity, onboarding friction, terminology, lifecycle coverage, and developer experience. Use for repo/PR/release docs audits, documentation CI, stale-doc detection, 15-minute quickstart validation, SDK parity reviews, and world-class documentation scoring. Prefer observed evidence and fail gates rather than smoothing over product defects. For whole-product developer-experience audits use developer-experience-auditor.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with git, repository access, and normal build/test tooling.
metadata:
  version: "2.8.0"
---

# Developer Docs Auditor

## Mission

Act as an adversarial developer, technical documentation QA engineer, and release gatekeeper.

Do not optimize for being agreeable. Try to prove that the documentation is wrong, stale, incomplete, non-executable, internally contradictory, or hiding developer-experience defects. Pass it only when the evidence supports the result.

Read `references/audit-methodology.md` before broad audits.

## Hard gate: 15-minute magic path

A brand-new developer with zero product knowledge must be able to complete and verify the canonical end-to-end product value path in **15 minutes or less**.

Read `references/magic-path.md` before auditing onboarding. Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

The timer includes product installation, signup/auth when required, product-specific configuration, execution, wait time, and verification. Do not allow teams to game the metric by moving product setup into "prerequisites."

Results:

- ≤5 min: exceptional
- >5 to ≤10 min: strong
- >10 to ≤15 min: pass
- >15 min: **P1, FAIL**
- no reproducible E2E quickstart: **P1, FAIL**
- manual approval/support with no sandbox/test route: **P1, FAIL**

A high documentation score cannot override this gate.

Label timing evidence as **Observed**, **CI-observed**, or **Estimated**. Estimated timing cannot prove a PASS; it can only indicate likely risk or likely feasibility.

If the `developer-experience-auditor` skill is available, defer observed magic-path execution and timing to it and cite its DX Report as the timing evidence; otherwise perform the timing yourself. Documentation-specific gates (finding the path, honest prerequisites, stale instructions) remain this skill's.

## Default operating mode

Audit first. Do not silently rewrite large documentation surfaces before reporting what is broken, because rewriting can destroy evidence of systemic drift.

If the user asks for fixes, prioritize P0/P1 issues, then high-leverage P2s. Preserve separation between documentation defects and underlying Product/DX defects.

## Audit workflow

### 1. Establish authoritative product truth

Inspect:

- implementation and tests
- OpenAPI/AsyncAPI/protobuf/GraphQL schemas
- public/exported symbols
- CLI definitions and actual `--help`
- config schemas/defaults/env vars
- package/runtime/release metadata
- examples/fixtures
- official SDKs/generated clients
- existing docs/changelog/migrations

Use `scripts/inventory_docs.py` for broad inventory when useful.

Never treat prose as authoritative when executable/current sources contradict it.

### 2. Build the documentation impact graph

For a PR/release, identify changed surfaces and likely downstream docs:

Implementation/spec → reference → SDKs → examples → quickstart → README → task/concept docs → changelog/migration

Run `scripts/docs_impact.py` as a first-pass signal when git history is available. Semantic review is still required.

Read `references/drift-detection.md`.

### 3. Find and test the canonical magic path

Identify exactly one recommended getting-started route.

Verify:

- a new user can find it quickly
- prerequisites are honest and explicit
- the outcome is meaningful end-to-end value
- commands/examples are complete
- test/sandbox/local mode avoids provisioning friction
- success can be independently verified
- likely failures have recovery paths
- there are no unnecessary branches before first success

When safe and feasible, actually execute and time it using a clean/representative environment. Use `scripts/magic_path_runner.py` if the project has or can adopt a manifest.

Break elapsed time into orientation, install, account/auth, configure, execute, wait, verify, and recovery. Attribute each blocker to Docs, Product/DX, Infrastructure, or External dependency.

### 4. Test docs as code

Prefer deterministic validation:

- execute examples
- compile/type-check snippets
- validate schemas/examples
- compare CLI docs with actual help output
- compare config docs with schemas/source
- check links/anchors
- check generated reference for drift
- check version/package claims
- inspect deprecated/removed symbols still referenced

Read `references/executable-docs.md`.

Use `scripts/check_markdown_links.py` and `scripts/check_terminology.py` where appropriate.

### 5. Audit public contracts

For APIs, CLIs, configs, events, and SDKs, compare documentation to current product behavior.

Inspect:

- names and resource model
- inputs/types/defaults/nullability
- responses/status codes
- errors/remediation/retryability
- pagination/filtering/sorting
- idempotency/retries
- async state and webhooks/events
- rate limits/quotas
- auth/scopes
- request/correlation IDs
- versions/deprecations
- SDK semantic parity and language idioms

Read `references/api-dx.md` and `references/sdks.md`.

A confusing contract is a Product/DX defect even if it can be documented accurately.

### 6. Audit information architecture and user coverage

Check that the system supports distinct needs:

- tutorial/learning
- how-to/task completion
- reference/facts
- explanation/understanding
- troubleshooting/recovery
- production/operations
- migration/lifecycle

Do not demand every page contain every mode. Look for gaps and bad mixing.

### 7. Audit lifecycle and release impact

For changed public behavior, verify:

- reference updated/generated
- SDKs updated or divergence intentional
- examples still valid
- quickstart still works
- changelog entry exists when useful
- breaking changes have migration guidance
- deprecations identify replacement and timeline
- preview/stable/support/version scope is explicit

Read `references/lifecycle.md` and `references/release-gating.md`.

### 8. Audit terminology and retrieval quality

Look for concept drift across API, CLI, SDK, UI, errors, and docs. Prefer one canonical term per concept.

Check that humans and coding agents can retrieve authoritative current facts without reconstructing them from screenshots, marketing pages, or contradictory duplicates.

Read `references/terminology.md` and `references/llm-ready-docs.md`.

### 9. Score independently

When evidence is sufficient, report both:

- **Documentation Quality Score /100**
- **Underlying Developer Experience Score /100**

Read `references/scoring.md`.

Never allow aggregate scoring to hide a hard-gate failure.

### 10. Produce a release verdict

Return:

- **PASS**
- **PASS WITH DEBT**
- **FAIL**
- **UNVERIFIED**

Use the exact rules in `references/release-gating.md`.

## Required comprehensive audit output

For a broad repo/product audit, report:

1. Executive verdict
2. Evidence level and environments tested
3. Magic-path result, exact/estimated elapsed time, and segment breakdown
4. Documentation Quality Score
5. Developer Experience Score
6. P0/P1 gate failures
7. Developer journey failure points
8. Correctness/drift findings
9. API/CLI/config design defects
10. SDK parity findings
11. Executable example/test findings
12. Errors/troubleshooting findings
13. Diátaxis/information-architecture gaps
14. Security/production/lifecycle findings
15. Terminology/navigation/agent-readiness findings
16. Prioritized backlog with severity, defect class, owner type, and acceptance test
17. Release verdict

Use `assets/audit-report-template.md` when useful.

## PR review output

For a PR, keep the report focused:

- changed public behavior
- docs surfaces affected
- stale/missing changes
- executable checks performed
- magic-path impact if onboarding changed
- required release/migration/changelog updates
- P0-P4 findings
- PASS / PASS WITH DEBT / FAIL / UNVERIFIED

## Rules for evidence

- Say what you actually executed.
- Distinguish observed behavior from inference.
- Do not claim a link, command, example, SDK, or quickstart passes if you did not verify it when verification was feasible.
- Do not call documentation world-class when the magic path is unverified or >15 minutes.
- Do not downgrade a product/DX defect to a documentation wording issue merely because docs can explain it.
