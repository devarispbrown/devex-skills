# Fuzzing and SAST

SAST and fuzzing are force multipliers, not posture by themselves. Wire them where they pay off, and triage their output like any other finding.

## Where SAST pays off

SAST earns its place on surfaces that hold security-sensitive logic:

- parsers, decoders, and deserializers of untrusted input
- authentication, authorization, and session handling
- command construction, path handling, and file operations
- cryptography, key handling, and validation boundaries
- anything the release process signs or packages

Do not run SAST on generated code, vendored code, or code the project does not ship. Do not let SAST findings that nobody triaged masquerade as coverage.

## Where fuzzing pays off

Fuzz the input boundaries, not the whole program:

1. Identify functions that accept attacker-controlled input: parsers, network handlers, config loaders, format converters.
2. Prefer the ecosystem's native fuzz harness with a seed corpus from real inputs and edge cases.
3. Fuzz in CI on a schedule and on every change to the fuzzed surface, with a fixed time budget per run.
4. Treat a crash or sanitizer finding as P0 until proven unreachable: fuzzing found real bugs, assume this one is real too.

Verify: every fuzz target maps to an input boundary the product actually exposes.

## Wiring them into CI

1. Run SAST on every push and pull request; run fuzzing on schedule and on changes to the fuzzed surface.
2. Make the failure policy match the severity policy: P0/P1 findings block merge, P2/P3 become backlog items with owners.
3. Commit the tool configuration so a fresh clone reproduces the same scans.
4. Keep scan times bounded; a scan nobody waits for is a scan nobody runs.

Verify: a clean clone reproduces every scan locally or in CI with the committed configuration.

## Triage procedure

1. **Verify** the finding reproduces on current main with the committed configuration. A non-reproducible finding is unverified, not fixed.
2. **Classify** the finding: reachable and exploitable, reachable but low impact, or unreachable.
3. **Assign** a severity from the canonical severity vocabulary and an owner.
4. **Fix or accept** with a documented reason and a review date. Accepted findings without a review date are P2.
5. **Record** the evidence label for every claim: Observed, CI-observed, or Estimated.

Never report "scanner clean" as "secure". Scanners find what they are configured to find; the triage trail is the evidence.
