# Check Parity Procedure

## Definition

Check parity means the contributor's local checks and CI are the same product: the same commands, the same versions, and the same failures. A change that passes locally and fails in CI — or passes CI and fails locally — is a parity defect.

## Procedure

### 1. Identify the canonical local check

Find the repository's canonical local test command:

- Makefile or makefile with a `test:` target — canonical command is `make test`
- otherwise package.json with a `test` script — canonical command is `npm test`
- otherwise the command CONTRIBUTING.md tells contributors to run

If no canonical local check exists, that is a finding by itself: contributors cannot verify their work, a P1 defect.

### 2. Identify what CI runs

List every CI definition: `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/config.yml`, Jenkinsfile, `azure-pipelines.yml`, `.travis.yml`, appveyor.yml.

For each job, record the exact commands that run tests and checks, including setup steps before them.

### 3. Compare commands

Verify:

- the canonical local command, or a command invoking the same check suite, appears in the CI test job
- CI does not run a different test command that local contributors cannot run
- every check CI runs is runnable locally: lint, format, type check, security scans included

Do not accept "CI is green" as evidence the local check is green, and do not accept a green local run as proof CI will pass.

### 4. Compare versions

Verify:

- CI toolchain versions (language runtime, package manager, pinned CI image) match the documented local requirements
- lockfiles are committed where the ecosystem expects them
- a contributor following CONTRIBUTING installs exactly the versions CI uses

A version divergence that produces different results is a P1 parity defect.

### 5. Compare failures

Verify:

- the failure conditions are the same: same checks, same thresholds, same allowed-warning policies
- no check is skipped locally but enforced in CI, or the reverse
- flaky tests are quarantined and visible, not silently retried differently between local and CI

### 6. Detect drift

Drift detection procedure, repeatable at any time:

1. run the canonical local check from a clean clone; record command, versions, result
2. trigger the CI test job on a branch with no changes; record the same fields
3. diff the two results; any difference in command, version, or result is a drift finding with Observed or CI-observed evidence

Re-run the comparison on every audit and after any change to the Makefile, package.json, or CI definitions.

## Severity

- local check exists, CI runs a different check, contributor cannot reproduce CI: P1
- same checks but drifted versions with observable differences: P1
- checks differ in wording only, same suite and versions: P2
- CI enforces a check contributors are never told to run locally: P2
