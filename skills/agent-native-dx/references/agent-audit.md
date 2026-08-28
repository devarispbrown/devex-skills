# Agent-Native Audit Procedure

The audit answers one question: can a coding agent that has only this repository and product context build, run, verify, extend, and debug it?

## 1. Define simulated agent tasks

Pick the tasks agents will actually be asked to do:

- build the project from a clean checkout
- run the test suite and a single test
- run the product locally with defaults
- verify a change worked
- make a small documented extension
- diagnose a seeded failure

Tasks must be representative, not exhaustive. A repo that passes the six above passes most of the work.

## 2. Trace the tool-use path

For each task, record the exact commands an agent would run, in order, drawing only from what the repo itself provides: the entry file, README, `--help` output, and conventional structure. The trace is the audit evidence.

## 3. Execute as an agent would

Run each task following the trace, with these constraints:

- use only commands the repo documents or conventional structure implies
- read the entry file first, not the git history and not the author's memory
- never skip a verification step the trace lacks
- when a command fails, recover from what the repo offers: error messages, exit codes, `--help`, docs

## 4. Record tool-use traces

For each step record: command, expected result, actual result, and where the agent had to guess. The guessing points are the findings.

## 5. Classify failure modes

Agents hit failure modes humans do not:

- **Stale entry files** — documented commands no longer work; the agent trusts the file.
- **Interactive prompts** — a command hangs waiting for input an agent cannot give.
- **Missing verification steps** — no documented way to confirm success, so the agent assumes.
- **Unstructured output** — output the agent must scrape instead of parse.
- **Undocumented exit codes** — failure indistinguishable from success, or one failure from another.
- **Schema drift** — the machine surface disagrees with implementation; the agent trusts the machine.
- **Secrets in output** — the agent echoes them into traces and logs.
- **Non-idempotent commands** — rerunning corrupts state; the agent retries on failure.

Map each finding to the surface that causes it: entry file, schema, CLI, error model, script, tests, structure.

## 6. Label evidence

Label every finding's evidence: Observed (executed), CI-observed (executed in automation), or Estimated (reasoned from the trace without execution). Never present an estimate as proof a step works.

## 7. Render findings

Report per-surface findings with severity from the canonical vocabulary, the agent failure each causes, and the product change that removes it. Then hand the report to the audit owner for prioritization.
