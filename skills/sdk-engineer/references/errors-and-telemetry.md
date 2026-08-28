# Errors and Telemetry

Procedural guidance for the error model, retryable signals, and observability hooks.

## Typed error hierarchy

- One root error type per SDK carrying: HTTP status code, API error code, message, request ID, and a retryable flag.
- Subtypes for common classes: auth, rate limit, not found, validation, network.
- Per-language shape: Go `error` with `errors.As`, Python exception hierarchy, TypeScript error classes with `code`, Rust `ApiError` enum via `thiserror`.

## Wrapping vs chaining

- Preserve original context: Go `fmt.Errorf` wrapping, Python `raise ... from`, TypeScript cause chains, Rust `#[from]` or `map_err`.
- The HTTP status and request ID survive every wrap; they are never lost in translation layers or retry loops.

## Retryable signals

- The error itself carries retryability (flag, property, or variant) derived from status and API error code.
- Callers choose whether to retry; the SDK never retries behind the caller's back beyond its documented defaults.
- A retryable classification that disagrees with the documented policy is a P1 defect.

## Panic and exception policy

- Expected API errors are values or exceptions — never panics, fatal exits, or unhandled rejections.
- Programmer errors (misuse) may panic or throw per language; document which cases.
- Rust: `Result` for all fallible calls; no `unwrap()` on network paths.

## Telemetry hooks

- Offer hooks or spans for: request start, retry attempt, backoff wait, response, and error.
- Shapes: Go interfaces, Python hooks or OpenTelemetry, TypeScript middleware or events, Rust traits.
- Hooks never change behavior; hook failures are swallowed and logged.
- Default to the ecosystem standard (OpenTelemetry); custom hooks exist alongside.

## Correlation propagation

- Request IDs: the SDK generates one per request when the API does not, sends it, and surfaces it on responses and errors.
- Propagate W3C `traceparent` context on outbound requests when the API supports it.
- Every error and log line carries the request ID.

Verify: a request retried three times keeps one request ID end to end.
