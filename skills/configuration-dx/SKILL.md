---
name: configuration-dx
description: Treat configuration as a public API: ENV, YAML, JSON, TOML, flags, config files, secrets, and defaults. Audit for duplicate mechanisms, contradictory defaults, bad names, boolean explosions, unsafe defaults, secret leakage, unclear precedence, missing validation, and restart requirements; require deterministic precedence. For config documentation use developer-docs; for config compat across releases use release-guardian.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and the config schema/source.
metadata:
  version: "2.9.1"
---

# Configuration DX

## Mission

Configuration is the most neglected developer interface. Code gets review; config rarely does — yet every user of a product reads, sets, or trips over config names, defaults, precedence, and errors.

Audit configuration as a public API: inventory every mechanism, audit names, defaults, precedence, secrets, and validation, and recommend a config model that is deterministic, discoverable, and safe.

Do not patch symptoms. A confusing config surface is a Product/DX defect even when it can be documented accurately.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Config is a public API

Config keys, defaults, precedence, validation, and errors are contracts. Users, scripts, CI, and coding agents depend on them.

- Renaming a key or changing its default is a breaking change.
- Overlapping mechanisms for the same key create ambiguous winners.
- A committed secret default is a leak, not a convenience.
- An error message that hides the key, type, or source is an unexplained expected error.

Never treat config as internal plumbing. Review it with the same rigor as an API.

## Configuration DX workflow

Run `scripts/check_config_surface.py` against the tree early as a first-pass inventory signal. Its findings are heuristics; confirm each semantically before reporting it as a finding.

### 1. Inventory config mechanisms

Read `references/config-mechanisms.md` when inventorying config mechanisms.

Enumerate every mechanism in the tree: environment variable reads, YAML/JSON/TOML/INI config files and their loaders, .env files, flag definitions, and defaults. Record each key, its mechanism, and its location.

Verify:

- every config entry point is found, not just the obvious ones
- each concern resolves through at most one mechanism
- no key is readable through two independent mechanisms without an explicit precedence rule

### 2. Audit names and defaults

Inspect every key name and default value.

Verify:

- names follow one convention and one namespace prefix per product
- names are stable, searchable, and spelled out; no ad hoc abbreviations
- defaults are explicit, safe, and documented; no boolean explosions
- no secret-pattern key (password, token, api key, credential, auth) carries a committed default
- defaults match the environment; dev and prod are never silently mixed

### 3. Audit precedence

Read `references/precedence.md` when auditing precedence.

Determine the precedence model by inspecting every read site and the merge order of every loader. Produce the precedence matrix.

Verify:

- precedence is deterministic: one winner per key, for every key, in every environment
- the model matches the precedence contract below or the project's explicit documented model
- restart requirements are stated per key
- no key falls back through an undocumented chain

### 4. Audit secrets handling

Read `references/secrets-handling.md` when auditing secrets.

Find every value that must not be committed or logged. Verify:

- secrets come from the environment or a secret store, never from committed config
- .env files are gitignored; only a template with placeholders is committed
- logs, errors, and config introspection output redact values
- rotation is possible without editing code or config files

### 5. Audit validation and errors

Read `references/validation-and-errors.md` when auditing validation and errors.

Verify:

- config is validated against a schema at load time; types, ranges, and enums are checked
- missing or invalid keys fail fast with an actionable message naming the key, the expected type, and the source file
- a `config explain`-style capability exists or is recommended
- errors never echo secret values

### 6. Recommend a config architecture

Read `references/config-architecture.md` when designing or recommending a config model.

Deliver a concrete model: mechanism per concern, naming and namespacing, schema versioning, deprecation procedure, and the precedence contract written down.

Never hand back a list of problems without a recommended model.

## Precedence contract

Precedence must be deterministic and documented. The canonical model is:

**flags > environment > project config > user config > defaults**

Or the project's explicit documented model — but one of them, written down, applied everywhere, and testable.

Require:

- exactly one winner per key in every environment
- a precedence matrix artifact recording, per key, which source wins
- precedence changes are breaking changes and get release treatment
- restart requirements are documented per key; hot-reload is explicit, never implicit

Never let a key resolve differently depending on load order or machine.

## Secrets contract

- Secrets never live in committed config files or code defaults.
- Secrets are read from the environment or a secret store at runtime.
- .env files are local and gitignored; committed templates use placeholders only.
- Logs, error messages, and diagnostic output redact secret values.
- Never print, echo, or diff a secret value during the audit.

## Validation contract

- Every config surface validates against a schema before use.
- Validation happens at load time, not on first use of a key.
- Fail fast on missing or invalid keys; be permissive only for explicitly optional keys.
- Error messages name the key, the expected type, and the source file.
- Unknown keys are reported, not silently accepted, unless the model explicitly tolerates them.

## Required output

Produce the config audit using `assets/config-audit-template.md`.

The audit must contain:

1. **Mechanism inventory** — every mechanism and key with locations
2. **Precedence matrix** — per-key winner per source, or the explicit plan to produce one
3. **Findings** — each with a severity from the canonical vocabulary in `references/standards.md`
4. **Recommended config model** — concrete: mechanism per concern, naming, validation, precedence

Label every claim with its evidence label (Observed, CI-observed, or Estimated). Unlabeled numbers are UNVERIFIED.

## Definition of done

A configuration audit is done when:

- every config mechanism is inventoried with locations
- every key has exactly one winner per environment, or an explicit plan to get there
- no secret-pattern key has a committed default
- precedence is deterministic and documented in a matrix
- validation and error behavior are assessed against the validation contract
- restart requirements are stated per key
- findings carry canonical severity labels
- a concrete recommended config model is delivered
- the audit is rendered from `assets/config-audit-template.md`

Hand off config documentation to the `developer-docs` skill if available, and config compatibility across releases to the `release-guardian` skill if available. This skill audits the config surface; it does not replace either.
