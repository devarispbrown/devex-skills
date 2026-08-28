# Config Architecture

The recommendation step converts findings into a config model. A config model is the answer to: what are the keys, where do they live, who wins, and how does the surface evolve.

## Naming conventions

- One namespace prefix per product (`MYAPP_TIMEOUT`, `MYAPP_*` env; `myapp.timeout` in files) so keys are groupable and collisions are visible.
- One convention across mechanisms: env vars uppercase with underscores, file keys in the same case family; document the mapping once.
- Spell names out; no ad hoc abbreviations (`max_conns` vs `max_connections`).
- One canonical name per concept. Two keys for the same concept (with synonyms, case variants, or typos tolerated in code) is a finding.
- Names describe the observable behavior, not the implementation detail.

## Boolean explosions

A boolean explosion is a set of `enable_x` / `use_y` flags that encode a concept that has more than two states, or grow combinatorially.

Detect:

- paired booleans where only some combinations are valid
- boolean flags whose false state silently selects a hidden default behavior
- feature-ish booleans better expressed as an enum or a single mode key

Fix by replacing the boolean cluster with one enum key with named values, validated against the schema. When a boolean is genuinely binary, keep it — but document what each state changes.

## Deprecation procedure

Deprecating a config key is a public contract change:

1. **Deprecate:** keep the key working, emit a warning naming the replacement, set a removal version.
2. **Warn:** the warning must be visible in logs and docs, keyed to the deprecation.
3. **Remove:** delete in the announced version, as a breaking change with release treatment.

Rules:

- Never remove a key without a named replacement and a timeline.
- Support the old name as an alias with a warning only when an automated migration is infeasible; aliases are debt, not a strategy.
- Map legacy values to new semantics during the alias window; do not let two spellings silently mean different things.

## Versioned config schemas

When config files or defaults evolve, version them:

- Carry a schema version in the config file itself (top-level `version` or `schema_version` key).
- The loader validates the version before parsing; unknown versions fail fast with an actionable message.
- Defaults change with the schema version; a default change is a behavioral change and gets release treatment.
- Migration: the loader may translate an older schema version to the current one, deterministically, and warn. Silent translation of one version is acceptable; open-ended compatibility is debt.

Version the schema when it changes, not when someone notices breakage. An unversioned config file that used to parse and now does not is a release bug, not a user error.
