# CLI Errors

## Exit codes

- Exit `0` only on success. Any failure exits non-zero. Never exit `0` with an error on stderr.
- Use a documented, per-surface exit-code table: a distinct code for usage/argument errors, a distinct code for runtime failures, and one for operational/config errors.
- Exit codes are stable across releases and documented in `--help` and the man page. Scripts depend on them; do not change a code's meaning.
- When the process is killed by a signal, report the signal-derived code (`128 + signal`) and state it in the error text.
- Distinguish "the command did not run" from "the command ran and failed". Callers need both.

## stderr and stdout discipline

- Data the user asked for goes to stdout. Errors, warnings, and progress go to stderr. Never mix them in one stream.
- When stdout is consumed by another program, error diagnostics on stderr must not break the data stream.
- One payload, one stream: never write the same result to both.
- Progress indicators, spinners, and log lines never reach stdout, even in `--verbose`.

## --verbose and --json

- Default output is concise: the result, or the error and its fix.
- `--verbose` adds detail (context, underlying cause, timing) to stderr, never to the data stream.
- `--json` emits a stable, documented schema: on success the result object; on failure an error object with `code`, `message`, and `request_id` if one exists.
- `--json` error objects follow the same field names across commands so parsers need one schema.
- The human-readable text and the JSON payload never contradict each other.

## Non-TTY behavior

- Never require interaction. When stdin is not a TTY, do not prompt: fail with an actionable message or read from the provided input.
- Disable color and progress when stdout or stderr is not a TTY, or when `NO_COLOR` is set.
- When not a TTY, print full error text rather than a one-line teaser; there is no human to page.
- Interactively, keep the error on one or two lines with the fix; in non-interactive mode, allow multi-line detail.

## Pipes

- Respect broken pipes: when the downstream consumer closes early, exit cleanly instead of crashing.
- Never buffer indefinitely waiting for a pipe consumer.
- Progress and status lines never travel through the pipe; only data does.

## Actionable text

Every error message states: what failed, why, and the exact next action. Use the **"Run: cmd"** pattern:

```
Error: no config file found at /etc/tool/config.toml.
Run: tool init --config /etc/tool/config.toml
```

- Write the fix as a complete, copy-pasteable command, not as prose instructions.
- Never say "an error occurred". State the failure.
- Include the relevant path, value, or identifier in the message so the user does not search for it.
