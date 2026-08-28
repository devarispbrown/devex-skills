# Scaffolding CLI

## Purpose

Design `create`, `test`, and `publish` commands that carry an author from an empty directory to a shipped extension without host internals knowledge. The CLI is the author's first impression of the extension API; it must succeed on the first run.

## Command contract

Each command:

- has exactly one default route and minimal interactive choices; prompts are avoided where a safe default exists
- validates inputs before mutating anything
- writes machine-readable results to stdout (JSON when requested) and diagnostics to stderr
- is idempotent and safe to re-run
- exits nonzero only on genuine failure, with an actionable message naming the fix

## create

From an empty directory to a runnable extension skeleton:

- generates the manifest with a version contract, hooks, interfaces, config, and isolation permission set
- ships tests that pass immediately, and a mock-core harness wired to `test`
- labels every exported surface with a stability tier so the surface inventory is clean
- validates the extension id: namespaced, unique, matching the registry naming rules
- refuses to overwrite an existing project

The skeleton must pass `scripts/check_extension_surface.py` with no gaps.

## test

- Runs contract tests against the mock core in the production sandbox.
- Fast local feedback loop: seconds, no network, no host installation.
- Reports per-test results and a machine-readable summary for CI.
- CI mode runs the version matrix declared in the version contract.

## publish

- Validates: manifest completeness, surface checklist, version contract, tests green, package contents.
- Refuses to publish with any checklist gap, a missing version contract, or an unsigned artifact when signatures are required.
- Packages deterministically, computes integrity metadata, signs, and registers the version.
- Publishing the same version twice is refused; version bumps follow the SemVer contract.
- Reversible where the registry supports it: unpublish is a takedown, not a delete.

## Scaffold updates

- An `update` or migration path regenerates template parts without clobbering author code.
- Template drift is detected and reported, never silently overwritten.
- Updating the skeleton never breaks the author's existing tests silently; migrations are documented per the breaking-change policy.
