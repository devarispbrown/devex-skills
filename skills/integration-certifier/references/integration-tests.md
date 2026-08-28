# Real Integration Tests

## Purpose

Design tests that prove the integration against the real service, so the evidence cell in the matrix means something.

## The mock trap

A unit test with a mocked service proves the mock, not the integration. Mocks are allowed to keep other suites fast; they never certify a matrix cell.

## What a real integration test needs

1. **The real service** — a container, a test or sandbox instance, or the service's official test environment. Prefer service containers (Docker Compose or testcontainers-style) pinned to the exact version under test.
2. **Real credentials** — test or sandbox keys obtained through the service's normal auth path, never production credentials.
3. **Real operations** — create, read, update, delete (or the service's equivalent verbs) exercised end to end. A health check or connection probe alone is not an integration test.
4. **Assertions on service behavior** — responses are parsed and validated against the documented contract, including error paths.

## Fixtures

- Seed minimal deterministic data for every test; start the service container fresh per run where cheap.
- Keep fixtures inside the repo so the run is reproducible.
- Do not depend on shared long-lived external instances that others can mutate.

## Timeouts

- Give every external interaction an explicit timeout, shorter than the CI job's overall timeout.
- Treat the first hang of an external call as a test failure, not as a reason to retry forever.

## Flake control

- Tag and quarantine flaky tests instead of deleting them or retrying indefinitely.
- Allow a small bounded retry only for genuinely transient failures such as connection resets, and record the retry in the evidence.
- A test that flakes more than roughly 1 in 10 runs is a defect: fix it or quarantine it.

## CI placement

- Run integration tests in a dedicated CI job, never inside the unit-test job.
- Use the CI matrix to cover version × configuration cells; each cell's evidence is the job run URL.
- Run the full matrix on a schedule and on changes to the integration layer; see `references/recertification.md` for the schedule.
- Record the job URL in the cell at publish time.

## Evidence capture

For every run that will certify a cell, record:

- job or run URL, or the recorded command
- commit or product version under test
- service version and configuration exercised
- date and evidence label: Observed, CI-observed, or Estimated
