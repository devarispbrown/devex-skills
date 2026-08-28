# Onboarding plan: <product name>

> **Gate target:** brand-new developer reaches verified end-to-end value within `MAGIC_PATH_MAX_MIN`.
> **Evidence label:** Estimated (design-phase). Re-time with the `developer-docs-auditor` skill if available before shipping.

## 1. Value outcome

- Persona: <zero-knowledge developer with supported OS and runtime only>
- Start: <opening the canonical quickstart>
- Stop: <developer independently verifies the core product outcome>
- Observable proof: <message sent / resource created / request answered / workflow completed>

## 2. Canonical route

- Install mode: <brew formula | npm | go install | docker | npx | curl-script>
- Rationale: <platform coverage, upgrade story, timer fit>
- Default SDK/language: <one, only>
- Alternative routes (post-success links only): <list>

## 3. Step list

| # | Step | Segment | Est. seconds | Commands | Credentials | Context switches | Owner |
|---|---|---|---|---|---|---|---|
| 1 | <step> | <orientation\|install\|account_auth\|configure\|execute\|wait\|verify\|recovery> | <seconds> | <n> | <n> | <n> | <Docs\|Product/DX\|Infrastructure\|External> |
| 2 | <step> | <segment> | <seconds> | <n> | <n> | <n> | <owner> |

## 4. Auth and configuration design

- Sandbox/test route: <test mode, starter token, seeded fixture, ephemeral sandbox>
- Defaults and zero-config decisions: <what is defaulted, what is inferred>
- Credentials the developer must create or find: <list, stay within MAGIC_PATH_MAX_CREDENTIALS>

## 5. Estimated segments vs `MAGIC_PATH_MAX_MIN`

| Segment | Estimated | Guidance | Status |
|---|---|---|---|
| orientation | <seconds> | <=1 min | ok |
| install | <seconds> | <=2 min | ok |
| account_auth | <seconds> | <=3 min | ok |
| configure | <seconds> | <=3 min | ok |
| execute | <seconds> | <=3 min | ok |
| wait | <seconds> | <=3 min | ok |
| verify | <seconds> | <=1 min | ok |
| recovery buffer | <seconds spare> | >=2 min | ok |
| **Total** | **<seconds> (<minutes> min)** | **<= `MAGIC_PATH_MAX_MIN`** | **<PASS (estimated)>** |

Run: `python3 scripts/estimate_magic_path.py assets/<plan>.json`

## 6. Failure recovery

| Symptom | Cause | Fix | Retry safe |
|---|---|---|---|
| <expected failure> | <cause> | <corrective action within TTR_TARGET_MIN> | <yes/no> |

## 7. Production handoff

- One post-success link: <production hardening>
- Next: <how-tos, concepts, reference>

## 8. Open blockers

| Blocker | Owner class | Required change |
|---|---|---|
| <blocker> | <Docs\|Product/DX\|Infrastructure\|External> | <product change required to meet the gate> |

## 9. Eliminations recorded

- Removed steps and why: <step — why the developer did not need it>
- Step-elimination answers per surviving step: <why the developer has to do this step at all>
