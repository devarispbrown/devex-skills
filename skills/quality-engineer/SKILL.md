---
name: quality-engineer
description: Design test strategy by system type rather than coverage percentage: test pyramids, contract tests, property-based and fuzz testing, failure injection, race and snapshot testing, and compatibility suites. Use to identify untested production-breaking behavior and define quality gates. For release gating and versioning decisions use release-guardian.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and the project's test tooling.
metadata:
  version: "2.5.1"
---

# Quality Engineer

## Mission

Answer the question: **what production-breaking behavior has no test detecting it?**

Design test strategy by system type and by failure mode, never by coverage percentage. Every production surface gets the cheapest test layer that would catch its real failure modes.

Do not optimize for green builds or high percentages. Optimize for the guarantee that breaking production behavior makes a test fail.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Test by system type

A CRUD API, a streaming pipeline, a stateful service, a CLI, a library, and infrastructure fail in different ways. They need different test techniques. A single coverage percentage across all of them is meaningless.

Coverage is a signal, never a target. Do not set coverage goals. Do not add tests to inflate coverage. Do not gate a release on a percentage.

Read `references/test-strategy.md` before classifying the system or mapping behaviors to techniques.

Read `references/test-pyramid.md` when sizing the test layers for a surface.

Read `references/contract-testing.md` when the system exposes contracts to consumers or depends on external providers.

Read `references/property-and-fuzz.md` when the system parses input, serializes data, or has wide input domains.

Read `references/failure-injection.md` when the system has external dependencies, distribution, state, or kill-switch paths.

Read `references/specialized-techniques.md` when the system is concurrent, versioned, or output-sensitive.

Read `references/quality-gates.md` when wiring gates into CI.

## Test strategy workflow

### 1. Classify the system

Identify every production surface and its system type:

- CRUD API
- streaming pipeline
- stateful service
- CLI
- library
- infrastructure

A repository often mixes types. Classify each surface separately. Do not fold two types into one strategy.

Run `scripts/assess_test_suite.py` for a read-only inventory of existing tests, fuzz/property/contract targets, and CI test config. Never modify the repository while assessing.

Record one type per surface in the strategy.

### 2. Map production-breaking behavior

For each surface, enumerate behaviors whose failure breaks production:

- data loss or corruption
- wrong results
- crashes or hangs
- lost messages, duplicates, or reordering
- broken compatibility or migrations
- security or authorization leaks
- unavailable or unresponsive paths

For each behavior ask: **if this behavior broke tomorrow, would a test fail?** If no test would catch it, it is a gap. Do not skip a gap because it is hard to test.

Assign severity P0-P4 using the vocabulary in `references/standards.md`. Label every severity with evidence or reasoning; unlabeled severity is UNVERIFIED.

### 3. Select techniques

Match each failure mode to the cheapest technique that catches it, using the matrix in `references/test-strategy.md`:

- unit tests for logic and validation
- integration tests for boundaries and state
- contract tests for provider/consumer boundaries
- property-based and fuzz tests for input domains
- failure injection for dependency and distribution failures
- race and snapshot tests for concurrency and output
- compatibility and migration tests for versions

Read the reference for a technique before recommending it. Never recommend a technique without naming a test location for it.

Do not propose a full E2E suite where a unit test catches the same failure mode.

### 4. Wire quality gates

Turn high-severity gaps into CI gates:

- each gate is a named CI job or check with expected evidence
- each claimed supported version or platform gets a CI job; a support claim without CI evidence fails the `UNTESTED_SUPPORTED_VERSION` gate
- coverage is reported as a signal with an evidence label, never gated as a target
- gate results use the verdict vocabulary: PASS / PASS WITH DEBT / FAIL / UNVERIFIED

Read `references/quality-gates.md` before writing gate wiring.

For release gating and versioning decisions, hand off to the `release-guardian` skill if available. Do not decide release policy inside this skill.

### 5. Verify the strategy catches injected failures

Prove the strategy works. For each P0/P1 gap:

1. Inject the failure deliberately — break the behavior, corrupt the data, kill the dependency, flip the version.
2. Run the suite in CI or locally.
3. Verify: at least one test fails and names the broken behavior.
4. Record the evidence label: Observed, CI-observed, or Estimated. Estimated evidence cannot prove the gap is closed.

If no test catches the injected failure, the gap is open. Do not close it with prose.

Use `references/failure-injection.md` for safe injection patterns. Never inject against production data.

## Coverage policy

- Coverage is a signal, never a target.
- Use coverage to find untested branches and dead code, not to score the suite.
- Never add a test whose only purpose is raising a percentage.
- Never gate a release on a coverage number.
- Report coverage with an evidence label; unlabeled coverage is UNVERIFIED.
- A high coverage number with no failure injection passes means nothing.

## Required output

Produce a test strategy containing:

1. **System type** per production surface
2. **Technique map**: production behavior → failure mode → technique → test location
3. **Gap list**: every behavior with no test, with severity and evidence label
4. **Gate wiring**: CI jobs and checks, each with its gate name and expected evidence

Use `assets/test-strategy-template.md` when it fits. Do not force the template when the system needs a different structure.

Report gaps first. Do not bury P0/P1 gaps under completed items.

## Definition of done

The strategy is done when:

- every production surface has a classified system type
- every production-breaking behavior maps to a technique or is explicitly accepted with severity
- no P0/P1 gap is closed by prose; each has a test that catches the injected failure or a documented acceptance decision
- gates are wired in CI with named jobs and evidence labels
- supported version claims carry CI evidence, so `UNTESTED_SUPPORTED_VERSION` cannot fire
- coverage is reported as a signal with an evidence label
- findings carry evidence labels: Observed, CI-observed, or Estimated
- at least one failure was injected per high-severity behavior class and caught by the suite
