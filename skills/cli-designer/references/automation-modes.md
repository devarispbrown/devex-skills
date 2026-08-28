# Automation Modes

Procedure for non-interactive mode, CI-safe behavior, scripted usage tests, and idempotency.

## Non-interactive mode

1. Every prompt has a scripted path: `--yes`, `--no-input`, or a documented flag that supplies the answer.
2. When stdin is closed or not a TTY, never hang; fail fast or act on the documented default.
3. `--no-input` fails when a decision is required; it never guesses.
4. Interactive conveniences (editor, pager, picker) never launch when stdin is not a TTY.

## CI-safe behavior

1. The tool works with no terminal, no color, no width, and no human.
2. Secrets are never echoed; tokens come from env, config, or stdin, and never leak into logs.
3. Output is bounded; no infinite progress streams or unbounded logs.
4. Exit codes are reliable enough for CI assertions.

## Scripted usage tests

Exercise every automation path and record each row in the review's automation test matrix:

1. `cmd --json | jq .` — machine path runs and parses.
2. `cmd 2>/dev/null` — stdout stays clean and parseable.
3. `cmd < /dev/null` — no hang, no prompt loop.
4. `cmd --no-input` — fails fast when a decision is needed.
5. `cmd --yes` — the destructive automation path completes without prompts.

## Idempotency

1. Re-running a command reaches the same end state; re-runs are safe.
2. When idempotency is impossible, the tool reports what changed and what did not.
3. Create/update commands report "already exists" or "no changes" instead of erroring.

## Verify

- every prompt maps to a flag
- no hang under closed stdin
- every matrix row passes with a documented expected exit code
- running the command twice leaves identical state
