---
name: release-guardian
description: Gate releases through a contract: classify the diff, analyze behavioral compatibility for JSON consumers, enum exhaustiveness, generated SDKs, migrations, and config parsers, recommend a SemVer version, and enforce migration requirements before tagging. For documentation release gating use developer-docs-auditor; for whole-product release readiness use developer-experience-auditor.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with git access and the release pipeline context.
metadata:
  version: "2.9.3"
---

# Release Guardian

## Mission

Releases are contracts. Every release is a compatibility event: version recommendation, migration requirements, and gate verification precede the tag, not follow it.

Gate the release through a contract: classify the diff, analyze behavioral compatibility for the full consumer list, recommend a SemVer version, define migration requirements, and verify the release checklist before the tag is created.

Do not tag first and audit later. The verdict precedes the tag.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read `references/change-classification.md` when classifying changed paths into change classes.

Read `references/compatibility-analysis.md` when walking the consumer list for behavioral compatibility.

Read `references/versioning.md` when recommending a SemVer version.

Read `references/migration-requirements.md` when defining migration requirements for the release.

Read `references/release-gates.md` when verifying the release checklist and applying the gate vocabulary.

## The release contract

Every release passes through a fixed contract, in order:

1. **Diff** — enumerate the changed surface between the base and head revisions.
2. **Classification** — map each changed path to exactly one change class.
3. **Compatibility analysis** — walk the consumer list; behavioral compatibility means documented consumers keep behaving.
4. **Version recommendation** — derive the SemVer bump from the highest-impact class.
5. **Migration requirements** — define what consumers must do before, during, and after upgrade.
6. **Verdict** — apply the release gates and return exactly one verdict.

Do not skip to the version recommendation before the classification and consumer analysis are complete. Never tag a release with an unsatisfied contract item.

## Release guardian workflow

### 1. Classify the change set

Run `scripts/classify_diff.py` with `--base` and `--head` as a first-pass signal when git history is available.

Verify:

- every changed path maps to a change class: breaking, behavioral, deprecated, added, fixed, or internal
- the classification is grounded in the actual diff hunks, not only file paths
- a fix that changes observable behavior is never classified `fixed`
- renames, type changes, removed fields, and changed defaults are caught, not masked by path heuristics

Semantic review of the diff is still required. The script output is heuristic and never a verdict.

### 2. Analyze compatibility

Read `references/compatibility-analysis.md`.

Walk the full consumer list for every classified surface: JSON/response parsers, enum exhaustiveness, generated SDKs, migrations and persisted schemas, config parsers, webhook handlers, dashboards, and shell scripts on CLI output.

Verify:

- behavioral compatibility holds for every documented consumer, stated per consumer and never averaged
- preview/beta consumers relying on documented-but-unstable behavior are accounted for
- every claim carries an evidence label: Observed, CI-observed, or Estimated

Run `scripts/scan_compat_consumers.py` against the tree to surface candidate consumers. Candidates still require semantic confirmation.

### 3. Recommend the version

Read `references/versioning.md`.

Verify:

- the bump is derived from the highest-impact change class, never from diff size or elapsed time
- the recommendation is a concrete target version with rationale tied to the classification
- pre-release and LTS constraints are applied
- a behavioral change that breaks a documented consumer is a MAJOR regardless of how small the code change is

### 4. Define migration requirements

Read `references/migration-requirements.md`.

Verify:

- a migration guide is mandatory for every breaking class entry
- the guide covers what changed, why, and the exact upgrade steps
- a rollback path is defined for operationally risky changes
- deprecations state replacement and timeline

### 5. Verify the release checklist

Read `references/release-gates.md`.

Verify each checklist item and record evidence per item: changelog, compatibility statement, SDK sync, docs sync, quickstart verified, TTR, gate vocabulary application.

Never mark a gate passed without evidence. An estimate cannot prove a PASS.

### 6. Render the verdict

Apply the gate vocabulary exactly as defined in `references/standards.md`. Return exactly one of PASS, PASS WITH DEBT, FAIL, UNVERIFIED.

A score never overrides a gate. Record the verdict in the release report before the tag exists.

## Gate semantics

Gate failures are keyed by gate constant from `references/standards.md`. Hard gates force FAIL regardless of any score:

- `UNDOCUMENTED_BREAKING_API` — a breaking API/CLI/config change ships without changelog entry and migration guidance
- `SDK_API_DRIFT` — a released official SDK is missing operations or contradicts the canonical API
- `STALE_PUBLIC_REFERENCE` — generated reference observably disagrees with current behavior
- `UNTESTED_SUPPORTED_VERSION` — a version/platform is claimed supported without CI or equivalent evidence
- `BROKEN_QUICKSTART` — the canonical quickstart is not reproducible end-to-end
- `BROKEN_CANONICAL_INSTALL` — the canonical install/auth path is broken
- `UNEXPLAINED_ERROR` — a public expected error lacks cause, fix, and retry-safety guidance
- `UNSAFE_EXAMPLES` — security-sensitive examples encourage unsafe credential handling
- `NON_REPRODUCIBLE_BUILD` — a clean checkout cannot reach the productive state using committed instructions

Gate results:

- **PASS:** no P0/P1 gate failures; required hard gates pass.
- **PASS WITH DEBT:** no hard gate failure, but P2/P3 backlog remains.
- **FAIL:** one or more P0/P1 gates fail.
- **UNVERIFIED:** evidence is insufficient to prove critical gates; do not convert this to PASS based on assumptions.

A high numerical score cannot override a hard-gate failure.

## Required output

For every gated release, produce the release verdict report using `assets/release-verdict-template.md`.

The report must contain:

1. **Verdict** — exactly one of PASS / PASS WITH DEBT / FAIL / UNVERIFIED
2. **Evidence** — revisions, environment, checks executed and not executed, with evidence labels
3. **Classification table** — changed path, change class, consumers affected, evidence
4. **Consumer analysis** — per-consumer impact for JSON parsers, enum exhaustiveness, generated SDKs, migrations, config parsers, webhook handlers, dashboards, shell scripts
5. **Version recommendation** — target version, bump rationale, pre-release/LTS notes
6. **Migration requirements** — guide location, content summary, rollback path
7. **Gate results** — per-gate result keyed by gate constant, with evidence

## Definition of done

A release gate is done when:

- every changed path is classified with evidence from the diff
- the consumer list is walked and each documented consumer's behavior is confirmed
- the version recommendation is derived from the highest-impact class
- migration requirements are defined for every breaking or operationally risky change
- every checklist item in `references/release-gates.md` is verified with labeled evidence
- the verdict is exactly one of PASS / PASS WITH DEBT / FAIL / UNVERIFIED
- no gate failure is hidden by a score, a heuristic, or an assumption
- the report is rendered from `assets/release-verdict-template.md` and recorded before the tag

Hand off documentation-release gating to the `developer-docs-auditor` skill if available, and whole-product release readiness to the `developer-experience-auditor` skill if available. Release Guardian gates the product release contract; it does not replace either.
