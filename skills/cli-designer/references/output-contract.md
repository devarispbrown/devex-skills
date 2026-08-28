# Output Contract

Procedure for stdout/stderr discipline, exit codes, JSON output, progress, color, and TTY behavior.

## Streams

1. stdout carries data only.
2. stderr carries diagnostics: warnings, progress, logs, errors.
3. In JSON mode, stdout is the JSON payload alone; any other bytes on stdout are a finding.
4. Human text is a rendering of the data, never a second schema.

## Exit codes

1. 0 on success; one distinct nonzero code per failure class; a dedicated code for usage errors.
2. Document exit codes in help and the manual.
3. Exit codes are stable; never reuse a code for a new meaning.
4. Never exit 0 on failure; never exit nonzero on success.

## JSON contract

1. Every data command supports JSON output.
2. Field names, types, nullability, and ordering are stable across releases.
3. Renaming or retyping a field is a breaking change; use release-guardian if available.
4. Errors in JSON mode are structured fields, not prose.
5. Empty results are `[]` or an explicit null field, never an absent key.
6. Timestamps use one format and one timezone, documented.

## Progress and color

1. Color only when stdout is a TTY; never emit raw escape codes into pipes.
2. Progress indicators live on stderr and vanish when stdout is not a TTY.
3. Provide explicit flags to disable color and progress when the default would color or animate.
4. Never gate data on terminal width.

## Pipe safety

1. A command piped to another program emits only complete data: whole lines or whole JSON.
2. Broken pipes exit cleanly without stack traces.
3. Verify with: `cmd --json | jq .`, `cmd 2>/dev/null`, `cmd < /dev/null`.

## TTY detection procedure

1. Call the standard isatty on stdin and stdout; never assume a TTY.
2. Prompt only when stdin is a TTY and no non-interactive flag was given.
3. Formatting keys off stdout's isatty; prompting keys off stdin's isatty.
4. Re-check at use time; never cache one answer for the process lifetime.

## Verify

- redirected stdout contains no color, progress, or diagnostics bytes
- piped JSON parses on every data command
- exit codes match the documented table for success, usage, and each failure class
- broken pipes are clean
