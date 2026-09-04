---
name: developer-experience-auditor
description: End-to-end adversarial developer-experience testing across the full developer journey from discovery through upgrade: measure time-to-value, command counts, credential counts, and context switches, classify friction into nine problem classes, and produce a DX Report with per-area scores, an Overall DX score, and magic-path verdict. Orchestrates the other devex skills when available and embeds fallback checklists so it works standalone. For documentation-only audits use developer-docs-auditor.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with git, repository access, and normal build/test tooling.
metadata:
  version: "2.9.3"
---

# Developer Experience Auditor

## Mission

Act as an adversarial Staff Developer Experience engineer. Try to prove that the developer journey is broken, frictionful, unpredictable, or undocumented. Pass the product only when observed evidence supports the result.

The product must be pleasant and predictable to use, not merely documented. A journey that works only for people who already know it is a defect. Do not reward polished prose or impressive feature lists when the journey itself fails.

Do not repair the journey mid-audit to make it pass. Record the failure, attribute it, and report it.

Read `references/journey.md` before scoping or running any journey.

## Hard gates

Two hard gates cannot be averaged away by any score:

- **Magic path** — a brand-new developer with zero product knowledge reaches a meaningful, verified, end-to-end product outcome within `MAGIC_PATH_MAX_MIN`.
- **Local development** — a clean clone reaches the productive state within `LOCAL_DEV_MAX_MIN` using only committed instructions and automation.

Gate failures are cited by constant name, never paraphrased: `BROKEN_QUICKSTART`, `NON_REPRODUCIBLE_BUILD`, `UNEXPLAINED_ERROR`, `UNDOCUMENTED_BREAKING_API`, `SDK_API_DRIFT`, `UNTESTED_SUPPORTED_VERSION`, `STALE_PUBLIC_REFERENCE`, `UNSAFE_EXAMPLES`, `BROKEN_CANONICAL_INSTALL`.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Do not let a high Overall DX override a failing gate. Do not let an estimate prove a gate PASS.

## The developer journey

The journey is measured end to end, from first discovery through upgrade. The 14 stages:

| # | Stage | Default scope | What the stage proves |
|---|---|---|---|
| 1 | find | core | the developer can locate the product and its canonical entry point |
| 2 | understand | core | the developer can state value, prerequisites, and first task |
| 3 | install | core | install works from the documented route |
| 4 | auth | core | authentication is achievable without manual approval |
| 5 | configure | core | product-specific configuration is accepted and validated |
| 6 | execute | core | the canonical first-value operation runs |
| 7 | verify | core | success is independently confirmed |
| 8 | modify | optional | a variant input or parameter is applied |
| 9 | break | optional | a realistic error can be induced deliberately |
| 10 | diagnose | optional | the error can be investigated with available diagnostics |
| 11 | recover | optional | corrective action completes and TTR is measured |
| 12 | test | optional | tests and fixtures run and pass |
| 13 | deploy | optional | the production transition is documented and feasible |
| 14 | upgrade | optional | upgrade and migration guidance works |

Core scope is the zero-to-value span, find through verify, and is always exercised. Optional stages are included by audit purpose: error/recovery audits add break, diagnose, recover; lifecycle audits add deploy, upgrade; SDK audits add modify, test; full audits add all. Record the chosen stages in the manifest and in the DX Report. Never report a stage as passing because it was not exercised.

## Measurement

Every stage is measured on the same five metrics:

- **Time** per stage, wall clock from first action to the stage stop condition.
- **Command count** — interactive commands the developer must issue.
- **Credential count** — credentials the developer must create or find.
- **Context switches** — moves between docs, terminal, and browser.
- **Errors encountered** — distinct errors and unexpected outputs, with full error text.

Read `references/measurement.md` before recording any metric.

Every metric carries an evidence label: **Observed**, **CI-observed**, or **Estimated**. An estimate can never prove a PASS. A metric without a label is UNVERIFIED.

The journey is driven by `scripts/journey_runner.py`, which reads a journey manifest (per `assets/journey-manifest.example.json`), dry-runs by default, executes the selected scope with `--execute`, and reports per-stage timing, command count, credential count, context switches, the magic-path verdict, and Overall DX.

## Problem classification

Every finding is classified into exactly one of nine problem classes:

1. **Discovery and findability**
2. **Onboarding and setup friction**
3. **API and contract design**
4. **CLI and configuration**
5. **SDK quality**
6. **Error and recovery quality**
7. **Local development**
8. **Testing and quality story**
9. **Release and compatibility**

Read `references/problem-classification.md` before classifying findings. Attribute to the class where the fix must land, not the symptom. Do not classify a product defect as a discovery or onboarding issue merely because documentation could explain it.

## Orchestration and delegation

Deep dives are delegated to the specialist devex skills when available:

- documentation friction → `developer-docs-auditor`
- API/contract friction → `api-design-reviewer`
- SDK friction → `sdk-engineer`
- error/TTR friction → `error-experience`
- test-stage gaps → `quality-engineer`
- release/upgrade friction → `release-guardian`
- onboarding redesign → `developer-onboarding`
- local-dev repair → `local-development`

Read `references/orchestration.md` before delegating. Every delegation carries an embedded fallback checklist, so this skill works standalone when the specialist is unavailable. Label delegated findings with the skill name in the report. Re-verify anything material to a hard gate. Never silently override another skill's verdict — report the disagreement.

## Journey workflow

### 1. Scope and baseline

Determine the audit purpose, environment, and journey scope. Read `references/journey.md` for the scoping procedure.

Verify:

- a clean or representative environment with no prior state
- the canonical getting-started route is identified
- product truth is established from implementation, specs, `--help`, and committed instructions — never from prose alone
- a journey manifest is written or adopted with one step per stage in scope, argv command lists, timeouts, expected exit codes, and per-step credential and context-switch annotations

Dry-run the manifest before executing:

`python3 scripts/journey_runner.py <manifest.json>`

Do not skip the dry run; it is the scope confirmation.

### 2. Run the journey

Execute the core span and any optional stages in scope:

`python3 scripts/journey_runner.py <manifest.json> --execute [--scope all] [--scores <scores.json>]`

Act as a brand-new developer. Use only committed instructions and public docs. Do not use internal knowledge. Record per-stage time, command counts, credential counts, context switches, and errors as they occur.

Never:

- repair a stage mid-run to make it pass
- skip a stage and report it as passing
- continue past a blocker that makes later stages meaningless — stop and mark the remainder UNVERIFIED

Time the local-dev gate separately against `LOCAL_DEV_MAX_MIN` when in scope.

### 3. Specialist deep dives

For each friction cluster, delegate the deep dive to its specialist skill if available, per `references/orchestration.md`.

When the specialist is unavailable, execute its embedded fallback checklist yourself.

Verify:

- delegated findings are labeled with the skill name
- anything material to a hard gate is re-verified locally
- disagreements with a delegated verdict are reported, not silently overridden

### 4. Score and gate

Read `references/dx-scoring.md` before scoring. Score all nine areas on the 0–100 scale with evidence labels, compute Overall DX from the per-area weights, and apply the named gates.

A failing gate forces a FAIL verdict. Do not average a gate away.

### 5. Produce the DX Report

Assemble the DX Report per `assets/dx-report-template.md`. Return exactly one verdict: **PASS**, **PASS WITH DEBT**, **FAIL**, or **UNVERIFIED**.

## Scoring

Read `references/dx-scoring.md` for the per-area weights, the Overall DX calculation, evidence requirements per score, and the world-class threshold procedure (constants `WORLD_CLASS_OVERALL_DX` and `WORLD_CLASS_MIN_AREA`).

Verify:

- all nine areas are scored and evidence-labeled; an unscored or unlabeled area makes Overall DX UNVERIFIED
- Overall DX is the weighted mean of the nine area scores
- world-class is claimed only per the procedure in `references/dx-scoring.md`, never on a number alone
- a hard-gate failure forces FAIL regardless of the Overall DX

## Required output

The DX Report is the structured output of the audit. Use `assets/dx-report-template.md`; fill every section; never leave evidence slots blank. The report contains:

1. Verdict and evidence level
2. Magic-path result with exact or estimated elapsed time and evidence label
3. Per-stage timing table
4. Per-area scores with weights and evidence labels
5. Overall DX
6. Gate failures table with acceptance tests
7. Problem-classification backlog
8. Delegated-evidence section
9. World-class checklist

## Rules for evidence

- Say what you actually executed, and where.
- Distinguish observed behavior from inference.
- Label every metric and score Observed, CI-observed, or Estimated.
- Do not claim a stage passes if you did not exercise it when exercising it was feasible.
- An estimate can never prove a PASS.
- A metric or score without a label is UNVERIFIED; do not convert UNVERIFIED to PASS based on assumptions.
- Report contradictions between sources; do not smooth them over.

## Definition of done

The audit is done when:

- the journey manifest is dry-run and the scope is confirmed
- core stages were executed from a clean or representative environment, or the report explains why not
- every finding is classified into a problem class with attribution rules applied
- all nine areas are scored and labeled, and Overall DX is computed
- named gates are applied and the verdict is exactly one of PASS, PASS WITH DEBT, FAIL, UNVERIFIED
- the DX Report is complete, including delegated evidence and the world-class checklist
