# IDE Experience Audit Report

## Verdict

**IDE gate:** <PASS | PASS WITH DEBT | FAIL | UNVERIFIED>

## Evidence

- Repository/revision: <repo> @ <revision>
- IDE surface inventoried: <VS Code | JetBrains | devcontainer | schemas | task runners | inline docs/navigation>
- Checks executed: <list>
- Checks not executed: <list>
- Evidence labels: <Observed | CI-observed | Estimated> per claim

## Surface inventory

| Surface | Files | Status |
|---|---|---|
| VS Code workspace | .vscode/settings.json, extensions.json, launch.json, tasks.json | <Present \| Missing \| Broken> |
| JetBrains project | .idea/runConfigurations/, codeStyles/, inspectionProfiles/ | |
| Devcontainer | .devcontainer/devcontainer.json | |
| Editorconfig | .editorconfig | |
| LSP servers | <per language> | |
| Debug adapters | <per language> | |
| Schema associations | <config files + schemas> | |
| Inline docs / navigation | <doc comments, symbol navigation> | |

## Findings

| ID | Severity | Location | Finding | Evidence | Recommendation |
|---|---|---|---|---|---|
| <P0–P4> | <file or surface> | | | | |

Cover each surface: VS Code workspace, JetBrains project, LSP/debugging, schema autocomplete, inline docs/navigation, task runners. Never hide a finding because a fix is inconvenient.

## Task runner check

`scripts/check_ide_config.py` results:

| Task | Command | Declared source | Result |
|---|---|---|---|
| <name> | <command> | <Makefile target \| package.json script> | <OK \| STALE> |

List every stale command verbatim. A stale command is fixed or deleted; it is never documented as intentional drift without an explicit acceptance record.

## Feedback budgets

| Budget constant | Measured | Result |
|---|---|---|
| FEEDBACK_FORMATTER_MAX_S (2) | <seconds> | <PASS \| FAIL> |
| FEEDBACK_INCREMENTAL_COMPILE_MAX_S (5) | | |
| FEEDBACK_UNIT_TEST_MAX_S (10) | | |
| FEEDBACK_FOCUSED_INTEGRATION_MAX_S (60) | | |
| FEEDBACK_LOCAL_RELOAD_MAX_S (3) | | |
| Longest forced wait (edit → feedback) | | |

One budget exceeded is P2; two or more is P1. Any forced wait greater than 30 seconds between edit and feedback breaks flow state (P2). Label each measurement Observed, CI-observed, or Estimated.

## Backlog (debt, when PASS WITH DEBT)

| Priority | Finding | Owner type | Acceptance test |
|---|---|---|---|
| <P0–P4> | | | |

## Sign-off

- Verdict: <verdict>
- Tag-blocking items: <list or "none">
