# The Developer Journey

The journey is the connected path a developer follows from first discovery through upgrade. Audit it as one experience; do not judge isolated stages.

## Stage definitions

For each stage: objective (what must be true), measurement points (what is recorded), stop condition (when the stage ends), and scope (core is always exercised; optional is included by audit purpose).

### find

Objective: locate the product and its canonical entry point. Measure: time from intent to the quickstart or entry page; whether search and navigation surface it. Stop: the canonical entry point is found, or one search attempt block ends. Scope: core.

### understand

Objective: state the value proposition, prerequisites, and first task. Measure: reading time; number of prerequisite conditions; contradictions between pages. Stop: a first actionable step is identified. Scope: core.

### install

Objective: install the product and its dependencies from the documented route. Measure: install time; command count; environment assumptions. Stop: the binary or package is present and invocable. Scope: core.

### auth

Objective: reach an authenticated state without manual approval. Measure: auth time; credential count; whether a sandbox or test route exists. Stop: an authenticated session or test token is usable. Scope: core.

### configure

Objective: product-specific configuration is accepted and validated. Measure: config time; context switches; whether defaults work. Stop: the configuration is accepted by the product. Scope: core.

### execute

Objective: the canonical first-value operation runs. Measure: execution and wait time; command count. Stop: the operation returns. Scope: core.

### verify

Objective: success is confirmed independently. Measure: verification time; whether a verification step exists at all. Stop: success is confirmed or a contradiction is found. Scope: core.

### modify

Objective: a variant input or parameter is applied. Measure: time; whether the documented path generalizes beyond the single example. Stop: the variant is applied. Scope: optional.

### break

Objective: induce a realistic error deliberately. Measure: how the product presents the error. Stop: the error is induced. Scope: optional.

### diagnose

Objective: investigate the induced error with available diagnostics. Measure: diagnostic support; log and correlation identifiers. Stop: a root-cause hypothesis is formed. Scope: optional.

### recover

Objective: complete the corrective action. Measure: TTR against `TTR_TARGET_MIN`; retry safety. Stop: the product is usable again. Scope: optional.

### test

Objective: run the project's tests and fixtures. Measure: test run time; coverage of the journey's own steps. Stop: the test-suite outcome is known. Scope: optional.

### deploy

Objective: the production transition is documented and feasible. Measure: deploy-path friction; production-only steps. Stop: deploy steps are executed or blocked. Scope: optional.

### upgrade

Objective: upgrade and migration guidance works. Measure: upgrade time; migration correctness; breaking-change handling. Stop: the upgraded version is verified. Scope: optional.

## Scoping procedure

1. State the audit purpose: time-to-value, error/recovery, lifecycle, SDK, or full journey.
2. Core scope is always find through verify. Include the optional stages the purpose requires: error/recovery audits add break, diagnose, recover; lifecycle audits add deploy, upgrade; SDK audits add modify, test; full audits add all.
3. Record the chosen stages in the journey manifest with `scope: "core"` or `scope: "optional"`, and in the DX Report.
4. A stage not in scope is reported as "not in scope" — never as passing.
5. When a blocker makes the remaining stages meaningless, stop the run, record the blocker, and mark the remainder UNVERIFIED.
