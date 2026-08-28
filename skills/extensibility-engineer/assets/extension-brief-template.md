# Extension Author Experience Brief

## Scope

- Host/product: <name>
- Extension API: <name and revision>
- Author persona: <who builds extensions and their prior knowledge>
- Repository/revision: <repo> @ <revision>
- Evidence labels: <Observed | CI-observed | Estimated> per claim

## 1. Surface inventory

| Surface | Kind (hook/interface/config/provider) | File | Stability tier | Evidence |
|---|---|---|---|---|
| <name> | | | | |

Source: `scripts/check_extension_surface.py <tree>` output, reconciled semantically.

## 2. Stability map

| Surface | Tier | Change policy | Deprecation window | Promotion path |
|---|---|---|---|---|
| | <internal\|experimental\|stable\|deprecated> | | | |

## 3. Isolation boundaries

- Read: <paths, env, host state>
- Write: <paths, caches>
- Execute: <commands, runtimes>
- Network: <endpoints>
- Secrets: <explicit credential API — yes/no>
- Failure containment: <timeouts, limits, quarantine, disable>
- Production sandbox == test sandbox: <yes/no>

## 4. Version contract

- Supported core range: <min_core_version ... max_core_version>
- api_version: <version>
- Enforcement point: <load-time refuse | degraded mode, documented>
- Negotiation rules: <capabilities queried, no silent fallback>
- CI matrix: <core versions run in CI>

## 5. Discovery metadata

- Manifest schema: <fields and where defined>
- Registry identity: <namespacing, canonical id>
- Integrity model: <checksums, signatures, provenance>
- Lifecycle: <install/update/remove idempotent and versioned>

## 6. Testing plan

- Mock core: <location, recorded calls, failure simulation>
- Contract tests: <what is asserted in each direction>
- Fixtures: <list, including edge shapes>
- Scenarios: <happy, error, timeout, permission denied, version mismatch, missing capability>
- CI: <matrix and gate>

## 7. Scaffolding workflow

| Command | Behavior | Flags | Exit codes |
|---|---|---|---|
| create | | | |
| test | | | |
| publish | | | |

`publish` refusal conditions: <checklist gaps, missing version contract, unsigned artifact>

## 8. Gap list

| # | Gap | Severity | Owner | Acceptance test |
|---|---|---|---|---|
| | | <P0–P4> | | |

## Verdict

- Author experience: <pass | pass with debt | fail | unverified>
- Blocking items: <list or "none">
