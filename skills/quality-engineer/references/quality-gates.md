# Quality Gates in CI

## Gate shape

A gate is a named CI job or check with an explicit expected evidence. Gates are turnstiles, not reports: they pass or fail with the verdict vocabulary PASS / PASS WITH DEBT / FAIL / UNVERIFIED.

## Wiring procedure

1. From the strategy's technique map, list every high-severity technique row that must run in CI.
2. For each row, create a job: framework command, bounded timeout, seeded environment, and a junit/xUnit report so failures are attributable.
3. Give every job a name that states its gate (e.g., "contract-compat", "migration-n1-to-n", "race-detector", "fuzz-5min").
4. Require the job on the merge path for changes that touch its surface. Never let a gate run "informational only" while claiming it protects the release.
5. Report coverage as a signal with an evidence label; never fail the build on a percentage.

## Applying UNTESTED_SUPPORTED_VERSION

The `UNTESTED_SUPPORTED_VERSION` gate fires when a version or platform is claimed supported without CI or equivalent evidence.

1. Extract every support claim: language engines, python_requires, supported runtime matrices, OS support statements, "tested on" claims.
2. For each claim, confirm a CI matrix job exists that builds and tests that exact version/platform.
3. If the job is missing: either add it or remove the claim. Leaving both is a gate failure.
4. Record the evidence level for each claim: Observed, CI-observed, or Estimated.

## Coverage policy in gates

- Coverage numbers are printed next to the job that produced them, labeled with the evidence level.
- Never set a coverage gate or a coverage target in CI config.
- Use coverage output to identify untested branches for the next technique-map pass, not as a merge condition.

## Handoff

For release gating and versioning decisions — what may ship, when, with what version number and migration requirements — hand off to the `release-guardian` skill if available. This skill defines the test gates; release-guardian decides release policy on top of them. Do not invent release policy here.

## Gate hygiene

- A failing gate must be fixable by the change that triggered it; if it is not, the gate is mis-scoped.
- Remove or re-scope gates that never fire; a gate that cannot fail is ceremony.
- Every gate change is itself a reviewed change with its own evidence.
