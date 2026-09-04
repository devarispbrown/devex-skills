---
name: sdk-engineer
description: Design, implement, and maintain idiomatic SDKs for Go, Python, TypeScript, and Rust with semantic parity: retries, timeouts, pagination helpers, streaming, authentication, typed errors, telemetry hooks, versioning, and capability matrices. Use to prevent mechanically translated SDKs and verify parity across languages. For the underlying API surface use api-design-reviewer; for SDK documentation parity use developer-docs-auditor.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and SDK build/test tooling.
metadata:
  version: "2.7.0"
---

# SDK Engineering

## Mission

Design, implement, and maintain SDKs for Go, Python, TypeScript, and Rust that are idiomatic in each language and semantically equivalent to the canonical API.

Idiomatic over literal. A mechanically translated client is a product defect, not a shortcut. Parity is about behavior: operations, authentication, retries, pagination, streaming, and errors must behave the same across languages even when their shape differs.

SDK bugs are product bugs. A retry policy that treats 429 as non-retryable, a pagination loop that drops pages, a typed error that discards the HTTP status — each is a product defect at the same severity as a server-side bug.

Read `references/sdk-design-principles.md` when defining parity for a new SDK or deciding whether a deviation from the API surface is justified.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## SDK-as-product principles

- **Semantic parity first**: every operation in the API is reachable from every SDK with equivalent behavior and defaults.
- **Idiomatic surface per language**: the API defines what exists; the language defines how it is presented.
- **Explicit runtime behavior**: retries, timeouts, auth, and streaming have designed, documented, and tested defaults — never inherited accidents.
- **No silent gaps**: an unimplemented operation is a tracked entry in the capability matrix, never an unlisted absence.
- **Ship docs and tests with surface changes**: a public surface change requires tests, documentation parity review, and a changelog entry in the same change.
- **Errors are surface**: typed errors, retryability, and remediation guidance are part of the product.

## SDK engineering workflow

### 1. Fix the API contract first

The SDK cannot be better than the contract it wraps.

Verify:
- the OpenAPI/AsyncAPI spec is authoritative and current
- operations, status codes, error bodies, pagination, and auth flows are defined
- ambiguous or underspecified behavior is resolved before client code is written
- the spec itself is reviewed (use `api-design-reviewer` if available)

Do not compensate for a bad contract with clever client code. Report the contract defect as a finding; never patch it silently inside the SDK.

### 2. Choose generation vs hand-written

Decide per language, not once for the suite.

Generate when the surface is large and mechanical; hand-write when language ergonomics matter more than coverage speed. Both can coexist: generated transport, hand-written surface. Pin one spec version per generation run.

Read `references/surface-design.md` when choosing the generation strategy or designing the method surface.

### 3. Design the language surface

Design names, types, and shapes the way each language expects.

- method names follow language conventions (see the table below)
- options and builders replace long positional argument lists
- pagination and streaming are first-class helpers, not URL assembly
- resource objects are typed and validated, never raw maps of JSON

Read `references/language-idioms.md` when naming or typing anything public.

Read `references/surface-design.md` when designing surfaces, options, pagination helpers, or streaming.

### 4. Runtime behavior

Runtime behavior is designed, documented, and tested — never inherited from a copied example.

Define per language:
- retry defaults, backoff schedule, jitter, and max attempts
- connect, read, and total timeouts
- supported auth flows and credential refresh
- proxy and custom HTTP client support
- thread-safety and async-safety guarantees

Read `references/runtime-behavior.md` when defining runtime defaults.

### 5. Errors and telemetry

Errors and telemetry are product surface.

- typed error hierarchy with the HTTP status preserved end to end
- retryable classification carried on the error, not recomputed by callers
- no panics or fatal exits for expected API errors
- telemetry hooks and spans with request ID propagation

Read `references/errors-and-telemetry.md` when designing the error model or telemetry hooks.

### 6. Verify parity

Parity is verified, not assumed.

- run `scripts/check_parity.py` against the OpenAPI JSON spec and each SDK tree, once per language
- every reported missing or uncertain operation is a candidate for review
- build, run, and test each SDK; do not rely on reading alone
- test retry, timeout, pagination, streaming, and error paths against the API or a contract test server

Use the fixture clients in `assets/sdk-example/` to exercise the checker.

Read `references/sdk-design-principles.md` when judging whether a finding is a parity defect or an intentional deviation.

### 7. Versioning and the capability matrix

The SDK has its own version; the API version it targets is recorded, not implied.

Maintain the capability matrix: one row per capability, one column per language, no blank cells.

Read `references/maintenance-matrix.md` when versioning, deprecating, or maintaining the matrix.

### 8. Release and maintenance

Releases are compatibility events.

Verify:
- changelog entries and migration notes exist
- deprecations name the replacement and the timeline
- generated clients are regenerated from the pinned spec version
- the capability matrix matches the released code
- documentation parity is reviewed (use `developer-docs-auditor` if available)

Read `references/maintenance-matrix.md` for the full release checklist.

## Language conventions

| Aspect | Go | Python | TypeScript | Rust |
|---|---|---|---|---|
| Method naming | `ListWidgets` | `list_widgets` | `listWidgets` | `list_widgets` |
| Error handling | `error` + `errors.Is/As` | typed exception hierarchy | error classes with `code` | `Result<T, ApiError>` + `thiserror` |
| Concurrency | safe for concurrent use | sync + async, thread-safe | `async`/`await` + `AbortSignal` | `Send + Sync`, feature-flagged async |
| Packaging | one `go.mod` module | PyPI package with type hints | npm package with `.d.ts`, ESM+CJS | crates.io crate with feature flags |
| Doc conventions | `go doc` on exports | docstrings, sphinx/mkdocs | TSDoc `@param`/`@returns` | `///` rustdoc with doc tests |

Read `references/language-idioms.md` for the full per-language conventions.

## Required output

Deliver an SDK review or design document containing:

1. per-language surface: methods, types, options, and naming decisions
2. parity findings: operations missing, uncertain, or deviating per language, severity-tagged P0-P4 per `references/standards.md`
3. capability matrix: implemented capabilities per language, no blank cells
4. runtime behavior summary: retries, timeouts, auth, streaming, safety
5. error and telemetry model summary
6. versioning, deprecation, and release notes
7. verdict: PASS / PASS WITH DEBT / FAIL / UNVERIFIED

Use `assets/sdk-review-template.md` when producing a review; use `assets/capability-matrix-template.md` when building the matrix.

## Definition of done

Work is done when:

- every API operation is reachable in every SDK, or the gap is tracked in the capability matrix with a severity-tagged finding
- each language surface follows the conventions in `references/language-idioms.md`
- retries, timeouts, auth, pagination, streaming, and errors behave equivalently across languages
- `scripts/check_parity.py` reports no unexpected misses for any language
- SDKs build, tests pass, and documented examples are valid
- versioning, deprecations, changelog, and the capability matrix are current
- findings are severity-tagged with the vocabulary in `references/standards.md`
