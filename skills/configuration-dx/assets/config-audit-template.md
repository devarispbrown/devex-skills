# Config Audit

## Scope

- Repository/revision: `<repo> @ <ref>`
- Config surface audited: `<directories, entry points, and config files>`
- Evidence labels: `<Observed | CI-observed | Estimated>` per claim; unlabeled claims are UNVERIFIED

## Mechanism inventory

| Key | Mechanism | Location | Default | Notes |
|---|---|---|---|---|
| `<key>` | `<env\|yaml\|json\|toml\|flags\|dotenv>` | `<path:line>` | `<default or none>` | `<restart \| hot-reload, dupes>` |

## Precedence matrix

| Key | Flags | Environment | Project config | User config | Default | Winner |
|---|---|---|---|---|---|---|
| `<key>` | `<source or blank>` | `<source or blank>` | `<source or blank>` | `<source or blank>` | `<default>` | `<winning source>` |

## Findings

| Severity | Finding | Location | Recommendation |
|---|---|---|---|
| `<P0–P4>` | `<duplicate mechanism \| unsafe default \| contradictory defaults \| unclear precedence \| bad name \| boolean explosion \| missing validation \| missing restart statement \| secret leak \| undocumented key>` | `<path:line>` | `<concrete fix>` |

## Restart requirements

- `<key>: <restart required | hot-reload>` — `<evidence>`

## Recommended config model

- Mechanism per concern: `<one mechanism per concern, plus override tiers>`
- Naming: `<namespace prefix, case convention, canonical term per concept>`
- Schema and validation: `<schema location, fail-fast policy, unknown-key policy>`
- Precedence contract: `<flags > environment > project config > user config > defaults, or the explicit model>`
- Deprecation procedure: `<deprecate → warn → remove timeline, alias policy>`
- Config introspection: `<config explain or equivalent, redaction policy>`

## Sign-off

- Open blockers: `<P0: N, P1: N, P2: N, P3: N>`
- Config verdict: `<PASS | PASS WITH DEBT | FAIL | UNVERIFIED>`
