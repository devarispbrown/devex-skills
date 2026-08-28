# Security Posture Report

## Scope and evidence

- Repository: <repo> @ <revision>
- Environment: <env>
- Audit date: <date>
- Evidence labels: <Observed | CI-observed | Estimated> per claim; unlabeled findings are UNVERIFIED
- Scanner output: <attach `scripts/check_security_posture.py` output>

## Findings by surface

### Library security

| Finding | Severity | Evidence | Fix |
|---|---|---|---|
| <finding> | <P0–P4> | <evidence label + source> | <fix> |

### Runtime security

| Finding | Severity | Evidence | Fix |
|---|---|---|---|
| <finding> | <P0–P4> | | |

### Build security

| Finding | Severity | Evidence | Fix |
|---|---|---|---|
| <finding> | <P0–P4> | | |

### Release security

| Finding | Severity | Evidence | Fix |
|---|---|---|---|
| <finding> | <P0–P4> | | |

### Repository security

| Finding | Severity | Evidence | Fix |
|---|---|---|---|
| <finding> | <P0–P4> | | |

## Prioritized fix list

| Priority | Finding | Fix | Acceptance test | Owner type |
|---|---|---|---|---|
| <P0–P4> | <finding> | <fix> | <verifiable acceptance test> | <maintainer\|security team\|CI owner> |

## Contract checks

### SECURITY.md contract

| Item | Status |
|---|---|
| Reporting channel (email, form, or private advisory) with what to include | <pass\|fail\|unverified> |
| Response and disclosure timeline stated | |
| Supported versions and security-fix policy stated | |
| Patch release and announcement path stated | |

### Release-integrity contract

| Item | Status |
|---|---|
| Signed artifacts or independently verifiable checksum manifest | <pass\|fail\|unverified> |
| Provenance attestation (how and from what artifacts were built) | |
| SBOM accompanying release artifacts | |
| Release process isolation (protected state, not ad hoc) | |
| Tag protection against force-push and deletion | |

## Posture verdict

**Verdict:** <PASS | PASS WITH DEBT | FAIL | UNVERIFIED>

**Debt or failure list:** <list or "none">

## Sign-off

- Audited surfaces: <library, runtime, build, release, repository>
- Verdict: <verdict>
- Blocking items: <list or "none">
- Unverifiable items recorded: <branch protection, registry settings, ... or "none">
