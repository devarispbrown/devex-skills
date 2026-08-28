# Documentation Drift Detection

Documentation drift occurs when product truth changes but one or more developer-facing surfaces do not.

## Drift graph

Think in dependencies:

Implementation/spec → generated reference → SDKs → examples → quickstarts → README → how-to/explanation → changelog/migration

A change near the left side can invalidate multiple downstream surfaces.

## Inspect changed files for impact

Public changes commonly imply documentation work when they touch:

- route/handler/schema/proto definitions
- exported/public types or methods
- CLI commands/flags/defaults
- config structs/schema/env vars
- authentication/authorization
- error codes/messages/types
- events/webhooks
- package/runtime support
- deployment/install scripts
- generated SDK inputs

Use `scripts/docs_impact.py` to produce an initial candidate impact report from git changes, then verify semantically.

## Deterministic checks

Use repository-native tooling first. Add recurring checks for:

- broken local links/anchors
- snippets that no longer compile/run
- examples that fail integration tests
- documented commands/flags that differ from `--help`
- documented env/config keys that no longer exist
- response examples that fail schema validation
- generated reference with uncommitted drift
- unsupported package/runtime versions in docs
- removed symbols still referenced
- stale SDK operation coverage
- contradictory duplicated terminology

Automation finds candidates; semantic review decides whether the behavior is correct.
