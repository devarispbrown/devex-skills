# CLI Review: <CLI-NAME>

- Reviewed: <YYYY-MM-DD>
- Scope: <version | commit | tree path>
- Evidence: <Observed | CI-observed | Estimated>

## Verdict

<placeholder: PASS | PASS WITH DEBT | FAIL | UNVERIFIED>

## Findings

| ID | Severity | Command / area | Finding | Evidence | Proposed change |
|---|---|---|---|---|---|
| F1 | <P0-P4> | <command> | <what is wrong> | <Observed / CI-observed / Estimated> | <concrete change> |
| F2 | <P0-P4> | <command> | <what is wrong> | <Observed / CI-observed / Estimated> | <concrete change> |

## Per-command audit table

| Command | Help complete | JSON output | Exit codes documented | Automation safe | Destructive protected |
|---|---|---|---|---|---|
| <command> | <yes / no> | <yes / no / na> | <yes / no> | <yes / no> | <yes / no / na> |
| <command> | <yes / no> | <yes / no / na> | <yes / no> | <yes / no> | <yes / no / na> |

## Automation test matrix

| Command | Scripted invocation | Expected exit code | stdout expectation | stderr expectation | Result |
|---|---|---|---|---|---|
| <command> | <cmd --flags> | <code> | <parseable JSON / clean text / empty> | <diagnostics only> | <pass / fail> |
| <command> | <cmd --flags> | <code> | <parseable JSON / clean text / empty> | <diagnostics only> | <pass / fail> |

## Destructive operations

| Command | Interactive confirmation | Automation bypass flag | Dry run | Reversibility stated |
|---|---|---|---|---|
| <command> | <prompt / name-typing / none> | <flag name / none> | <yes / no> | <what is lost, what survives> |
| <command> | <prompt / name-typing / none> | <flag name / none> | <yes / no> | <what is lost, what survives> |

## Recommended changes

<placeholder: prioritized list of changes, each with severity and target release>

## Evidence notes

<placeholder: what was executed, what was inspected, what remains unverified>
