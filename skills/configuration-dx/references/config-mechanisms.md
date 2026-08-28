# Config Mechanisms

A config mechanism is any channel through which a key can reach the running program. The first audit step is enumerating them, because mechanisms that are not on the inventory cannot be audited for duplicates, precedence, or safety.

## Mechanism comparison

| Mechanism | Strengths | Weaknesses |
|---|---|---|
| Environment variables | universal, container/CI native, secrets-friendly | untyped, unstructured, no discovery |
| Flags | per-invocation control, self-documenting via `--help` | per-invocation only, nothing persists |
| YAML | structured, readable, comments | no types without a schema; comments are not validation |
| JSON | ubiquitous, typed, machine-parseable | no comments, single document |
| TOML | typed tables, comments | less universal tooling |
| .env files | convenient local dev | easy to commit, weak escaping, no structure |
| Secret stores | centralized, rotated, audited | external dependency, harder local dev |

## Duplicate-mechanism detection

A duplicate is the same logical key reachable through two or more independent mechanisms (for example, `API_KEY` read from the environment and `api_key` read from YAML, or a `--timeout` flag duplicating a `TIMEOUT` env var).

Procedure:

1. Normalize each key for comparison: lowercase, strip `-`, `_`, and `.`.
2. Group read sites by normalized key and mechanism kind.
3. Any normalized key with two or more mechanism kinds is a duplicate — record every site.
4. Any key appearing in two different config files is a duplicate file source — record both.
5. Confirm each hit semantically; a normalization collision is not a duplicate.

Do not deduplicate silently. The finding is the ambiguity itself: two sources means one of them is dead weight, a precedence trap, or a rotation hazard.

## One-mechanism-per-concern rule

Each config concern resolves through exactly one mechanism. The standard shape:

- **Runtime secrets** — environment or secret store only.
- **Deployment/environment settings** — environment only.
- **Persistent project behavior** — one config file format, loaded by one loader, merged in one documented order.
- **Per-invocation overrides** — flags only, and only for keys that legitimately vary per invocation.

A key that needs per-env and per-file values is one key with defined precedence, not two duplicate keys. When a new mechanism appears for an existing concern, that is a duplicate-mechanism finding until the project's precedence model explicitly adopts it.

Do not add a second mechanism to fix a naming or organization problem. Fix the first mechanism instead.
