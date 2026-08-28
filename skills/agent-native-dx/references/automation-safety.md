# Automation Safety

Agents run commands unattended. Every command an agent is expected to run must be safe to run twice and safe to run without a human watching.

## Deterministic scripts

- Fixed execution order; never depend on directory-listing order, sort explicitly.
- No behavior that changes by locale, timezone, or random seed unless the seed is an explicit input.
- No silent network fetches; pin versions and checksums.
- Same input produces the same output for the parts agents compare.

## Idempotency

- Running a command twice converges to the same state; the second run changes nothing or reports "already done".
- Create operations fail cleanly or become no-ops when the resource exists; never double-create.
- Append operations document their duplicate handling.
- Verify: run the command twice against the same state and confirm the second run's result is identical.

## Non-interactive modes

- Every prompt has a flag, env var, or stdin default. An agent that hits a prompt hangs.
- A `--yes`, `--no-input`, or equivalent exists for confirmation prompts.
- The interactive default is never the only path for commands agents are told to run.
- Verify: run the documented command with stdin closed and confirm it completes.

## Destructive-operation guardrails

- Nothing destructive is the default. Deletes, resets, overrides, and data-destroying migrations require explicit opt-in.
- Destructive flags state their exact scope in `--help` and in any confirmation.
- Prefer dry-run defaults: show what would change, then accept an execute flag.
- Never document shell patterns like recursive deletes as the standard approach.
- Verify: the destructive command with no flags performs no destruction.

## Secrets handling

- Secrets are read from env vars or secret stores, never from flags, committed config, or example commands.
- Output and logs never echo secrets; redact before printing.
- Credential files are ignored by version control; sample configs use placeholders.
- Verify: inspect the documented workflow's output for any value that should stay secret.

## Audit checklist

For every script or command in the agent path, confirm: deterministic, idempotent, non-interactive, non-destructive by default, secret-clean. Any violation is a finding with the failing command named.
