# Maintenance and the Capability Matrix

Procedural guidance for the capability matrix, generation workflow, versioning, deprecation, and release.

## Capability matrix

The capability matrix is the single source of truth for what each SDK implements.

Columns: one per language. Rows: one per capability. Add rows the product exposes beyond the default list.

Default capability rows: async/concurrent execution, pagination helpers, retry with backoff and jitter, streaming, request IDs and correlation, auth flows (one row each), typed errors with status preservation, retryable classification, telemetry hooks, timeout configuration, proxy and custom HTTP client, idempotency helpers, file upload/download, webhooks and events.

Cell values: `yes` (implemented and tested), `no` (tracked gap with finding ID), `partial` (implemented with documented limits and finding ID).

Never leave a cell blank. A blank cell is an undocumented `no`.

## Generation workflow

- Pin one spec version per generation run; record it in the SDK metadata.
- Re-run generation deterministically; generated files carry a `DO NOT EDIT` header naming the generator and spec version.
- After regeneration, re-run `scripts/check_parity.py` and the full test suite; hand-written layers are reviewed against the diff.

## Versioning vs API version

- The SDK version is independent of the API version; the API version each SDK release targets is recorded in the changelog, package metadata, and matrix.
- Breaking changes follow semantic versioning; a breaking SDK change is a major bump regardless of the API version.
- One spec version per release; never ship a client half-generated from two spec versions.

## Changelog

- Every release gets changelog entries: operations added or removed, behavior changes, dependency bumps, API version targeted.
- Generated changes are summarized at the generator level, not line by line.

## Deprecation

- Deprecation announces the replacement, timeline, and removal version in code attributes and the changelog.
- An operation deprecated in the API is deprecated in the SDK in the same release; silent removal is a P1 defect.
- Deprecated surface keeps working until removal; document the minimum support window.

## Release process

1. Pin the spec version; regenerate if the SDK is generated.
2. Run `scripts/check_parity.py` for every language; zero unexpected misses.
3. Build and test every SDK; run contract tests against the API or a mock.
4. Update the capability matrix; it must match the released code.
5. Write changelog and migration notes; review documentation parity (use `developer-docs-auditor` if available).
6. Tag per semantic versioning, publish packages, and record the API version.
