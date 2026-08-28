# Testing Harness

## Purpose

Give extension authors a fast, faithful way to prove their extension works against the declared contract, without running the real host. The harness is part of the extension API; a surface without a harness is an incomplete surface.

## Mock core

Every extension API ships a mock core that:

- records every call an extension makes, with arguments, so tests can assert interaction
- injects fixture events and payloads in the documented shapes
- simulates failures: refused, timed out, limited, crashed — matching the isolation reference's failure taxonomy
- enforces the same sandbox as production; the harness and production boundaries are identical

## Contract tests

Contract tests assert both directions of the contract:

- the extension satisfies the declared interface: hook signatures, interface shapes, config schema
- the host behavior the extension relies on exists: call semantics, error shapes, capability set

Run them against the mock core in CI on every change, and against every core version in the extension's declared range.

## Fixtures

- One representative fixture set per hook and interface, in the manifest's own payload shapes.
- Include edge shapes: empty, maximal, malformed, unknown fields.
- Fixtures are versioned with the contract they exemplify.

## Required scenarios

- happy path: the extension does its job
- error path: every documented failure mode is exercised
- timeout and limit: the extension's behavior under budget pressure
- permission denial: the extension handles refused access
- version mismatch: loading outside the declared range refuses cleanly
- missing capability: negotiation without the capability does not misbehave

## Tooling contract

- The scaffolded project ships tests that pass before the author writes code.
- `test` is fast: contract tests run in seconds, local, without network or host.
- CI runs the full matrix; results are the evidence for the declared version range.
- Coverage targets are defined per surface kind, not globally: hooks and interfaces require contract coverage; helpers do not.

## Determinism

- Use injected clocks, tokens, and ids; never wall-clock or global state in assertions.
- Failures are asserted by type, not by message text.
- A flaky harness is a harness defect, not a test-writing problem.
