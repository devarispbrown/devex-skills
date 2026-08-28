# Precedence

Precedence answers one question per key: when two sources could both set it, which one wins? If the answer is "whatever loaded last" or "it depends on the machine", the config model is broken.

## Canonical model

**flags > environment > project config > user config > defaults**

Use this model unless the project has an explicit documented alternative. If it does, audit against the documented model — never against a model you invented for the occasion.

Rules:

- Higher-precedence sources may override lower-precedence sources per key; the reverse is never true.
- A key's winner is its value from the highest-precedence source that sets it.
- The model must hold identically in dev, CI, and production.

## Deterministic precedence procedure

1. List every source: flags, environment, each config file, user config, defaults.
2. Order the sources once; write the order down.
3. For each key, identify every source that can set it.
4. Record the winner per key per environment.
5. Prove it: set the same key through two sources and observe the documented winner.

Do not declare precedence from documentation alone. Inspect every read site and every loader's merge order in code, and test at least the keys that matter.

## Precedence matrix artifact

Build a matrix with one row per key and one column per source. Each cell holds the value (or blank) that source contributes, plus the winning source per row. Include the default even when it never wins — defaults are a source.

| Key | Flags | Env | Project config | User config | Default | Winner |
|---|---|---|---|---|---|---|
| `timeout` | `--timeout` | `TIMEOUT` | `timeout:` | — | 30 | Env |

A blank row means the key exists in only one source: note it as fine, not as a gap.

## Conflict resolution

- **Equal precedence, two sources** (two config files, or env in two loaders): unresolved. Pick one file per concern or document a merge order and enforce it in the loader.
- **Overriding the canonical order:** allowed only if the project documents the deviation, and it must be total and consistent — not per-file.
- **Contradictory defaults:** a defect even when precedence is clear, because every default is a promise to someone who sets nothing.
- **Precedence changes:** breaking changes. They change what users observe with the same inputs; they get release treatment, not silent edits.

## Restart requirements

For each key, record whether a change takes effect on restart or on hot-reload.

- A key that is read once at startup requires restart; say so.
- Hot-reload must be explicit and documented — never a side effect of a caching accident.
- Keys that are read at different times (startup vs per-request) get per-read-site entries in the matrix when the winner could differ between sites.

Never let a key be restart-bound in one environment and hot-reloaded in another without saying so.
