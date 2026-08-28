# Specialized Techniques

## Race and determinism testing

For concurrent code, stateful services, and shared caches:

1. Run the suite with the language's race detector (Go `-race`, Rust `--cfg`, sanitizers) in CI.
2. Repeat runs to surface nondeterminism: run the same suite N times and fail on flapping results.
3. Inject scheduling perturbations — random sleeps, shuffles, goroutine/thread interleaving — to expose order assumptions.
4. Test the determinism property directly: same inputs, same initial state → same output. Snapshot the result and fail on drift.
5. Never "fix" a race with a sleep; fix the ordering or synchronization.

## Snapshot and golden tests

For CLI output, serialized state, error messages, and UI renderings:

1. Freeze expected output as a committed golden/snapshot artifact.
2. Regenerate the golden deliberately with a reviewed command when output changes intentionally — never by running the suite blindly with auto-accept.
3. Inspect the golden diff in review; the diff is the review.
4. Keep goldens small and human-readable; a golden nobody reads is a wall, not a test.
5. Combine with property tests for the input domain, goldens for the output shape.

## Compatibility and matrix testing

For libraries, SDKs, and anything claiming supported versions:

1. Enumerate every claimed supported version and platform from metadata (package.json engines, python_requires, go.mod, CI manifests).
2. Give each claim a CI matrix job that builds and runs the suite on that version/platform.
3. A claim without CI evidence is an `UNTESTED_SUPPORTED_VERSION` gate risk — remove the claim or add the job. Do not leave both.
4. Test the oldest and newest claimed versions at minimum; add a representative middle version when the matrix is large.

## Migration tests

For schema, state, and data migrations:

1. Test each migration path: old state → apply migration → new state, and rollback where supported.
2. Test migration on a snapshot of realistic production-shaped data, not only empty fixtures.
3. Test upgrades across versions: N-1 data must survive the upgrade to N (see `references/contract-testing.md` for the compatibility side).
4. Migration tests run in CI on every change that touches the migration set.
