# Validation and Errors

Config errors are developer interface. A config failure that names the key, the expected type, and the source file is a fixable moment; a failure that says only "invalid configuration" is an unexplained expected error.

## Schema validation

- Define the config surface as a schema: per-key type, allowed range, allowed enum values, required/optional, default.
- Validate against the schema at load time, before the program depends on the values.
- Validate everything up front, not key by key on first use — first-use validation produces failures that depend on code path.
- Validate each mechanism's parsed result; validation of the file format (valid YAML/JSON/TOML) is necessary but not sufficient.

A missing schema is a finding even when the program happens to work, because it means every behavior is implicit.

## Fail-fast vs permissive

- **Fail-fast** is the default for required keys and invalid values: refuse to start, print one actionable error.
- **Permissive** applies only to explicitly optional keys with defined defaults.
- Never silently ignore an unknown key: warn or fail. Silent acceptance makes typos invisible.
- Dev and production may differ in strictness (dev warns, prod fails) — but the difference must be documented and deliberate.

Do not trade an early hard failure for a late confusing one. Fail at the boundary, with the message below.

## Config error messages

Every config error message names three things:

1. **The key** — exact name, as the user would set it (`TIMEOUT`, `db.password`, `--timeout`).
2. **The expected type or constraint** — `expected integer between 1 and 300`.
3. **The source file** — where the invalid value was read (`config.yaml:3`, `.env`, `environment variable TIMEOUT`).

Message shape to verify against:

```
Invalid value for TIMEOUT (config.yaml:3): expected integer between 1 and 300, got "thirty".
```

Also include: what was accepted as a default or fallback, and how to fix it. Never include the raw secret value in a validation error.

## `config explain` capability

A `config explain`-style command resolves a key to its effective value and its provenance:

- the winner and its value (redacted for secret-pattern keys)
- every source that was consulted, in precedence order, with the file/line or env var
- the declared default, and whether it was used
- whether the change requires restart or hot-reload

This capability makes precedence observable instead of trustable. If it does not exist, recommend it as part of the config architecture; it is the `--help` of config.
