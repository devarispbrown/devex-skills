# sample-tool

Tiny fixture repository used to exercise agent-native readiness checks.

## CLI

```text
app run <path> [--json] [--verbose]
```

`--json` emits machine-readable output:

```json
{"status": "ok", "items": 2}
```

Exit codes:

- `0` success
- `2` validation error
- `3` usage error

## Development

Run the test suite with `python3 -m pytest`. See `AGENTS.md` for build and run commands.
