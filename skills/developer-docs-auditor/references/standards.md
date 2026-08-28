<!-- GENERATED FILE - do not edit by hand. Source: dx-standards/. Regenerate with: python3 scripts/sync-standards.py -->

# DX Principles

Shared principles for the entire skills suite. Skills apply them; none may contradict them.

## Truth before prose

Source, specs, tests, and observed behavior outrank narrative documentation. Establish truth before writing or judging.

## Time to value is a metric

The getting-started experience has an explicit SLA: `MAGIC_PATH_MAX_MIN` from `metrics.md`. Time to value is measured, not assumed.

## Interfaces are products

APIs, CLIs, SDKs, and config surfaces are products with their own UX. Review them as products, not as technical plumbing.

## One canonical path

There is one canonical onboarding route. Choices come after success. Parallel getting-started routes are a P2 defect.

## Failures are product surface

Error semantics, diagnostics, and troubleshooting are first-class interfaces. An unexplained expected error is a gate failure (`UNEXPLAINED_ERROR`).

## Docs ship with code

Public behavior changes imply documentation impact review in the same change. Docs and code cannot diverge silently.

## Reproducibility over tribal knowledge

Any setup step that only works on one machine or one person's memory is a defect. Committed automation is the standard.

## SDKs are first-class surfaces

Each official language deserves parity and idiomatic UX. A mechanically translated SDK is a product defect.

## Test by system type

Test strategy follows the system's failure modes, not a universal coverage percentage. Coverage is a signal, never a target.

## Releases are contracts

Every release is a compatibility event. Version recommendation, migration requirements, and gate verification precede the tag, not follow it.

## Humans and agents share the corpus

Structure interfaces, docs, and errors so both humans and coding agents can retrieve current authoritative facts and act safely.


# Severity and Verdict Vocabulary

Canonical severity levels and verdict vocabulary for every skill in the suite.

## Severity levels

- **P0 Blocker:** unsafe, impossible, materially incorrect, data/security/production risk.
- **P1 Critical:** blocks first success, breaks a hard gate (magic path, local dev), or incorrectly documents a public contract.
- **P2 Major:** important missing workflow, stale example, API/SDK mismatch, poor error recovery, substantial drift.
- **P3 Minor:** clarity, navigation, terminology, maintainability.
- **P4 Polish:** presentation/style only.

Prioritize defects that prevent developers from succeeding over cosmetic completeness.

## Verdict vocabulary

Every release or audit verdict returns exactly one of:

- **PASS:** no P0/P1 gate failures; required hard gates pass.
- **PASS WITH DEBT:** no hard gate failure, but P2/P3 backlog remains.
- **FAIL:** one or more P0/P1 gates fail.
- **UNVERIFIED:** evidence is insufficient to prove critical gates; do not convert this to PASS based on assumptions.

A high numerical score cannot override a hard-gate failure.

## Report labeling

Every score and timing reported by any skill must carry its evidence label (Observed / CI-observed / Estimated). Unlabeled numbers are UNVERIFIED.

## Evidence hierarchy

Prefer, in order:

1. observed execution against a clean/representative environment
2. implementation/tests/specs
3. generated/current interface output such as `--help`
4. package/release metadata
5. examples
6. prose docs

When sources disagree, report the contradiction.


# DX Metrics and Thresholds

Canonical metrics for the entire skills suite. Skills reference these constants by name; they must never be restated with different values inside a skill's hand-written files.

## Magic path thresholds

- `MAGIC_PATH_MAX_MIN` = 15. Hard gate: a brand-new developer with zero product knowledge reaches a meaningful, verified, end-to-end product outcome in 15 minutes or less.
- Bands: ≤5 min exceptional; >5 to ≤10 min strong; >10 to ≤15 min pass; >15 min P1 FAIL. No reproducible E2E quickstart: P1 FAIL. Manual approval/support required with no sandbox: P1 FAIL.
- The timer includes installation, signup/auth when required, configuration, execution, waiting, and verification. Setup cannot be moved into "prerequisites" to game the metric.
- Targets (P2 when exceeded): `MAGIC_PATH_MAX_COMMANDS` = 8 interactive commands, `MAGIC_PATH_MAX_CREDENTIALS` = 2 credentials the user must create or find, `MAGIC_PATH_MAX_CONTEXT_SWITCHES` = 4 switches between docs, terminal, and browser.
- Per-segment budget (guidance, not gates): orientation ≤1 min, install ≤2, auth ≤3, config ≤3, execute ≤3, verify ≤1, buffer ≥2.

## Local development thresholds

- `LOCAL_DEV_MAX_MIN` = 10. Hard gate: a clean clone reaches the productive state — tests run, the dev loop is exercised — using only committed instructions and automation.
- Bands: ≤3 min exceptional; >3 to ≤6 strong; >6 to ≤10 pass; >10 min P1 FAIL.
- Targets (P2 when exceeded): `LOCAL_DEV_MAX_COMMANDS` = 4 commands from clone to first successful run.
- Budget (guidance): clone ≤1 min, toolchain ≤2, dependencies ≤2, services ≤2, first success ≤2, buffer ≥1.

## Contribution thresholds

- `FIRST_CONTRIBUTION_TARGET_MIN` = 30. Target, not a hard gate: fork to first PR-ready change. 30–60 min = PASS WITH DEBT signal; >60 min = P2.

## Recovery thresholds

- `TTR_TARGET_MIN` = 5. Time to Recovery target for expected errors: from hitting the error to completing the corrective action. >10 min = P2.

## Evidence labels

- **Observed**: a human or agent actually executed the path from a clean or representative environment.
- **CI-observed**: automation executed the product steps; may undercount human reading/signup time.
- **Estimated**: steps analyzed but not executed.
- An estimate can never prove a PASS. A metric without an evidence label is UNVERIFIED.


# Release Gates

Canonical named gates for the suite. Each gate names a release-blocking condition; a skill finding references the gate constant, not a paraphrase. Gates supersede and extend the prose gate list in `skills/developer-docs-auditor/references/release-gating.md`, which points here.

## Gate identifiers

| Gate constant | Severity | Fails when |
|---|---|---|
| `BROKEN_QUICKSTART` | P1 | magic path exceeds `MAGIC_PATH_MAX_MIN`, no reproducible end-to-end quickstart exists, or manual approval/support is required with no sandbox route |
| `NON_REPRODUCIBLE_BUILD` | P1 | a clean checkout cannot reach the productive state within `LOCAL_DEV_MAX_MIN` using only committed instructions/automation |
| `UNEXPLAINED_ERROR` | P1 | a public, expected error lacks what happened / why / where / how to fix / retry-safety, or a support-correlation identifier |
| `UNDOCUMENTED_BREAKING_API` | P0 | a breaking API/CLI/config change ships without changelog entry and migration guidance |
| `SDK_API_DRIFT` | P1 | a released official SDK is missing operations or contradicts the canonical API |
| `UNTESTED_SUPPORTED_VERSION` | P1 | a version/platform is claimed supported without CI or equivalent evidence |
| `STALE_PUBLIC_REFERENCE` | P1 | generated reference observably disagrees with current behavior |
| `UNSAFE_EXAMPLES` | P1 | security-sensitive examples encourage unsafe credential handling |
| `BROKEN_CANONICAL_INSTALL` | P1 | canonical install/auth path is broken |

## Gate semantics

- Hard gates cannot be averaged away by any score. A failing gate forces FAIL regardless of the Overall DX number.
- Conditional gates (missing SDK update/parity, undocumented new errors/events/config, missing changelog entry, missing production guidance for preview-to-stable promotion, missing rollback/migration path) become blockers when material to the changed surface.
- Gate result: PASS / PASS WITH DEBT / FAIL / UNVERIFIED, per the verdict vocabulary in `severity.md`.


## Canonical terms

- **magic path**: the canonical getting-started route delivering verified end-to-end value.
- **quickstart**: the artifact documenting the magic path.
- **zero-to-value**: the find→verify span of the journey.
- **Time to Recovery (TTR)**: time from hitting an expected error to completing its corrective action.
- **DX Report**: the structured output of a developer-experience audit (per-area scores, Overall DX, gates).
- **capability matrix**: per-SDK/language table of implemented capabilities.
- **drift**: divergence between documentation/generated artifacts and current behavior.
- **parity**: semantic equivalence of SDKs (or docs) with the canonical API.
