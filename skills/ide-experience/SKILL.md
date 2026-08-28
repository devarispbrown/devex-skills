---
name: ide-experience
description: Make IDEs and editors excellent: VS Code and JetBrains configuration, LSP servers, debug adapters, schema autocompletion, inline documentation, navigation, and task runners, producing .vscode, devcontainer, launch.json, and tasks.json assets. For the command-line clone experience use local-development.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and IDE configuration.
metadata:
  version: "2.2.0"
---

# IDE Experience

## Mission

Make the IDE an asset, not a tribal-knowledge tax. Every developer opens the repository and gets working configuration, language intelligence, debugging, autocompletion, and one-command tasks — committed, reproducible, and discoverable.

The IDE surface is product surface. Configuration that lives only in one developer's machine is a defect. When IDE setup is hard, repair the committed configuration; do not write longer READMEs around it.

This skill audits and builds the GUI IDE experience: VS Code and JetBrains configuration, LSP servers, debug adapters, schema autocompletion, inline documentation and navigation, and task runners. For the command-line clone experience use the `local-development` skill.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## IDE experience audit

### 1. Inventory the IDE surface

Enumerate what exists and what is missing:

- .vscode/: settings.json, extensions.json, launch.json, tasks.json
- .idea/: run configurations, code style, inspection profiles
- .devcontainer/ and devcontainer.json
- .editorconfig
- LSP servers and debug adapters declared or installed
- schema associations for configuration files
- task definitions across tasks.json, Makefile, and package.json

A missing surface is a finding, not a preference. Record each surface as Present, Missing, or Broken.

### 2. Audit VS Code workspace configuration

Read `references/vs-code-setup.md`.

Verify:

- settings.json holds only intentional project-level settings; machine-specific settings stay in user settings
- extensions.json lists only needed extensions, with version pins where reproducibility matters
- every launch.json configuration has a name, a type, and a working request flow
- no secrets, tokens, or machine-specific paths are committed
- the workspace opens with no red squiggles on a clean checkout

### 3. Audit JetBrains project configuration

Read `references/jetbrains-setup.md`.

Verify:

- run configurations are committed under .idea/runConfigurations/
- workspace.xml and other personal state are not committed
- SDK selection and run configuration defaults match the canonical commands
- before-launch build steps are declared, not implied

### 4. Audit LSP and debug adapter wiring

Read `references/lsp-and-debug-adapters.md`.

Verify:

- every language in the repository has a working language server
- diagnostics appear on save
- hover, go-to-definition, find-references, and rename work for representative symbols
- every launch.json type maps to an installed debug adapter
- breakpoints hit, variables inspect, and stack traces walk
- launch and attach flows are both verified when the project supports both

### 5. Audit schema autocompletion

Read `references/schema-autocomplete.md`.

Verify:

- configuration files carry schema associations via settings.json `json.schemas` or a `$schema` key
- $schema URLs resolve
- autocompletion surfaces descriptions, enums, defaults, and examples
- invalid values and unknown keys are flagged before runtime
- custom config formats have a schema, not a wiki page

### 6. Audit task runners and one-command tasks

Read `references/task-runners.md`.

Run `scripts/check_ide_config.py` when .vscode/launch.json, .vscode/tasks.json, Makefile, or package.json exist. Treat its findings as evidence, not as the whole audit.

Verify:

- tasks.json and run configurations reference commands declared in Makefile or package.json
- no stale or duplicated command strings remain
- exactly one canonical dev-loop task exists and is the default build task
- the canonical task reproduces the `make dev` / `npm run dev` from the README
- devcontainer post-create and JetBrains run configs point at the same canonical commands

### 7. Audit inline documentation and navigation

Verify:

- public symbols have doc comments describing intent, not restated syntax
- hover shows behavior, parameters, defaults, and error semantics
- go-to-definition, find-references, and rename work across the workspace
- reference is available in-editor; users are not forced to leave the IDE
- generated config documentation does not drift from schemas

### 8. Apply the Workflow feedback budgets

Measure the canonical edit-to-feedback loop against the Workflow feedback budgets: formatter/linter ≤ `FEEDBACK_FORMATTER_MAX_S`, incremental compile ≤ `FEEDBACK_INCREMENTAL_COMPILE_MAX_S`, unit test ≤ `FEEDBACK_UNIT_TEST_MAX_S`, focused integration ≤ `FEEDBACK_FOCUSED_INTEGRATION_MAX_S`, local reload ≤ `FEEDBACK_LOCAL_RELOAD_MAX_S`.

Any forced wait greater than 30 seconds between edit and feedback breaks flow state (P2). One budget exceeded is P2; two or more is P1.

Time the loop in the canonical environment. Label evidence Observed, CI-observed, or Estimated. An estimate cannot prove a PASS.

## Contracts

### VS Code workspace contract

The committed .vscode directory is the project's IDE truth:

1. settings.json declares project-wide defaults only; secrets and machine paths never appear
2. extensions.json declares recommended and unwanted extensions
3. launch.json configurations are named, typed, and runnable
4. tasks.json tasks reference commands declared in Makefile or package.json
5. formatter and linter configuration is shared via .editorconfig and committed config files
6. a clean checkout opens with no red squiggles

Read `references/vs-code-setup.md` when writing or repairing these files.

### JetBrains project contract

1. run configurations are committed under .idea/runConfigurations/
2. personal state (workspace.xml, local history, cache indexes) is excluded from the repository
3. SDK and run configuration defaults match the canonical commands
4. before-launch build steps are declared
5. keymaps, themes, and UI preferences stay out of the repository

Read `references/jetbrains-setup.md` when writing or repairing these files.

### LSP and debugging contract

1. every language in the repository has a language server wired to the IDE
2. diagnostics, hover, go-to-definition, find-references, and rename work for representative symbols
3. every launch.json type maps to an installed debug adapter
4. breakpoints, variables, and stack traces work end to end
5. debugging setup is committed, documented, and reproducible

Read `references/lsp-and-debug-adapters.md` when wiring servers and adapters.

### Schema autocomplete contract

1. every configuration file with a fixed format has a schema association
2. autocompletion provides descriptions, enums, defaults, and examples
3. invalid values are flagged before runtime
4. schema sources are pinned and resolvable, never ephemeral

Read `references/schema-autocomplete.md` when associating or authoring schemas.

### Task runner contract

1. Makefile or package.json is the single source of truth for commands
2. tasks.json and run configurations reference, never duplicate, those commands
3. exactly one canonical one-command task starts the dev loop
4. task names mirror script names: dev, build, test, lint, format
5. stale task commands are removed, not documented

Read `references/task-runners.md` when designing or repairing tasks.

## Required output

Produce the audit report using `assets/ide-audit-template.md`.

The report must contain:

1. **Verdict** — exactly one of PASS / PASS WITH DEBT / FAIL / UNVERIFIED
2. **Evidence** — repository revision, IDE surface inventoried, checks executed and not executed, with evidence labels
3. **Inventory** — per-surface status: Present, Missing, or Broken
4. **Findings** — per-surface findings with severity, location, evidence, and recommendation
5. **Feedback budgets** — measured edit-to-feedback times against the Workflow feedback budgets
6. **Task runner results** — `scripts/check_ide_config.py` findings, including stale commands
7. **Backlog** — prioritized P0-P4 items with owner type and acceptance test

For the command-line clone experience, hand off to the `local-development` skill. For onboarding journey measurement, use the `developer-experience-auditor` skill if available. For documentation audits, use the `developer-docs-auditor` skill if available.

## Definition of done

An IDE experience is done when:

- every surface in the inventory is Present, and Broken surfaces are fixed or explicitly accepted
- the repository opens with working language intelligence for every language used
- debugging works end to end for the canonical run flows
- configuration files autocomplete and validate against pinned schemas
- exactly one canonical task starts the dev loop and matches the README
- no stale task command remains
- the edit-to-feedback loop fits the Workflow feedback budgets
- no secrets or machine-specific state are committed
- the report is rendered from `assets/ide-audit-template.md` with the verdict recorded
