# Runtime Behavior

Design, document, and test runtime defaults. Inherited or copied defaults are defects.

## Retries

- Retry only operations that are safe to retry, unless the API guarantees idempotency.
- Default: 3 attempts total, exponential backoff starting at 500ms, doubling, capped at about 30s, with full jitter (random in `[0, delay)`).
- 429 and 5xx are retryable; other 4xx responses are not, except 408; honor `Retry-After` when present.
- Retryable classification is encoded in the error type — see `references/errors-and-telemetry.md`.
- Never retry a partially sent streaming body unless the protocol supports resume.

## Timeouts

- Separate connect, read, and total timeouts; expose all three.
- Sensible defaults: connect 10s, read 60s, total 2 minutes per request unless the operation is long-lived.
- Streaming operations use read/idle timeouts, not total timeouts.
- Per-call overrides via options; global defaults via client configuration.

## Authentication

- Support every auth flow the API documents: API keys, OAuth2 client credentials, bearer tokens, and refresh flows.
- Credential refresh is automatic and thread-safe; credentials never appear in logs or error messages.
- Per-request auth overrides are allowed; auth state must not leak across tenants or workspaces in one shared client.

## Proxy and HTTP client

- Honor standard proxy environment variables by default; allow explicit proxy configuration and per-request overrides.
- Accept a custom HTTP client or transport per language: Go `*http.Client`, Python `requests.Session` or `httpx.Client`, TypeScript injected `fetch` or dispatcher, Rust `reqwest::Client`.
- TLS verification is never disabled by default.

## Thread and async safety

- Clients are safe to share across goroutines, threads, coroutines, and awaits; document any exception.
- One connection pool per client; constructing a client per request is a P3 performance finding.
- Timeouts, retries, and auth refresh are race-free; concurrency tests are part of the test suite.
