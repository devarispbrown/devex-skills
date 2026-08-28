# Language Idioms

Per-language conventions for SDK surfaces. The API defines what exists; the language defines how it is presented.

## Go

| Aspect | Convention |
|---|---|
| Naming | exported CamelCase (`ListWidgets`, `GetWidget`); packages lowercase, one module per SDK |
| Error handling | `error` values; sentinel and typed errors via `errors.Is`/`errors.As`; never panic for expected API errors |
| Concurrency | clients safe for concurrent use; document goroutine safety; no channels on the public SDK surface |
| Packaging | one `go.mod` module; `Client` in the root or `client` package; options as `type Option func(*config)` |
| Docs | `go doc` comments on every exported symbol; document zero values, nil handling, and concurrency guarantees |

## Python

| Aspect | Convention |
|---|---|
| Naming | snake_case methods (`list_widgets`); CamelCase classes; lowercase modules |
| Error handling | exception hierarchy rooted in `ApiError`; never return error tuples; `raise ... from` to preserve context |
| Concurrency | sync by default; optional async variant with identical semantics; clients thread-safe |
| Packaging | PyPI package with explicit `__init__.py` exports; type hints on the public API |
| Docs | docstrings on every public symbol; sphinx/mkdocs-ready; doctest-valid examples |

## TypeScript

| Aspect | Convention |
|---|---|
| Naming | lowerCamelCase methods (`listWidgets`); interface `Widget`, never `IWidget` |
| Error handling | typed error classes carrying `code`; `instanceof`-testable; never throw strings |
| Concurrency | `async`/`await`; `AbortSignal` for cancellation; one shared client instance |
| Packaging | npm package with `.d.ts`; ESM and CJS compatibility; `strict` mode |
| Docs | TSDoc with `@param`/`@returns`; no `any` leaks on the public surface |

## Rust

| Aspect | Convention |
|---|---|
| Naming | snake_case functions, CamelCase types (`list_widgets`, `WidgetsClient`); `new()` constructors |
| Error handling | `Result<T, ApiError>`; `thiserror` for the SDK error enum; no panics for expected API errors |
| Concurrency | explicit `Send + Sync` on the client; document blocking vs async feature flags |
| Packaging | crates.io crate; feature flags for the async runtime; no unstable APIs |
| Docs | `///` rustdoc on public items; doc tests that compile and run |

## Cross-language invariants

- Convert operation IDs per language: `listWidgets` → `ListWidgets` (Go) / `list_widgets` (Python, Rust) / `listWidgets` (TypeScript). `scripts/check_parity.py` encodes these conversions.
- Do not rename resources across languages; only method presentation changes.
- Doc style follows the language; factual content is shared across languages.
- Never copy error handling or concurrency patterns between languages; apply the table above.
