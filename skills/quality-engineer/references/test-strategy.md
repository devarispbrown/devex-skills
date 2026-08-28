# Test Strategy by System Type

Procedural guide for classifying production surfaces and matching techniques to failure modes.

## Step 1: Classify each production surface

Identify every surface a user or system interacts with, and label it:

| System type | Typical entry points | Production-breaking failure modes | Techniques that warrant |
|---|---|---|---|
| CRUD API | HTTP/gRPC/GraphQL endpoints | wrong status codes, schema drift, validation holes, authz bypass, pagination/ordering errors, wrong semantics on edge inputs | unit tests on handlers and validators, contract tests, schema tests, property tests on validators, a few E2E happy paths |
| Streaming pipeline | consumer/producer, jobs, topics | message loss, duplicates, reordering, schema evolution break, backpressure stall, partial batch writes | unit tests on transforms, property tests on serialization, integration with a real broker in CI, failure injection (partition, latency, kill), compatibility tests on schemas |
| Stateful service | service entry points, storage | state corruption, race conditions, lost updates, broken migrations, idempotency violations, recovery from crash | unit tests with in-memory state, race/determinism tests, migration tests, snapshot tests of state transitions, failure injection |
| CLI | binary/subcommand entry | wrong exit codes, wrong stdout/stderr, flag parsing errors, partial-failure handling, non-idempotent re-runs, broken help | table-driven unit tests, golden/snapshot tests of output, property tests on argument combos, one E2E smoke per subcommand |
| Library | public/exported API | contract breakage, edge-case crashes, cross-version incompatibility, input-domain errors | unit tests, property-based and fuzz tests on public functions, contract tests, compatibility matrix per supported version, migration tests |
| Infrastructure | terraform/helm/k8s/docker manifests | non-idempotent apply, drift, secret leakage, broken rollback, version incompatibility | plan/apply validation, contract tests for modules, failure injection for rollback, minimal unit tests |

## Step 2: Map behaviors to techniques

For each surface, in order:

1. List the production behaviors the surface performs.
2. For each behavior, list the failure modes that would break production (wrong result, crash, hang, data loss, leak, incompatibility, unavailability).
3. For each failure mode, pick the cheapest technique whose test would fail if that failure occurred.
4. If no technique would fail on that failure mode, it is a gap. Record it with severity.
5. Write the result as a technique map row: behavior → failure mode → technique → test location.

Never reuse one technique for every row. If two failure modes need different techniques, the map shows both.

## Step 3: Check the map against reality

For each technique row, verify the test location exists or is scheduled. A technique with no test location is a gap, not a plan.

Use `scripts/assess_test_suite.py` from the parent skill to inventory what actually exists before writing the map.
