# Cross-Cutting Concern Wiring

The five concerns that thread through every code path: auth, config, errors, retries, observability. These are the minimal viable wiring patterns for reference applications. Each pattern is the default; a variant may deepen it, never omit it.

## Auth

- Fail closed: no configured credential means no access.
- Verify, never decode: compare the presented token against the expected value with a constant-time compare; parse claims only when a trusted signature exists.
- Wire the check into the request path so bypassing it requires deleting code, not calling something else.
- Scope to the variant: multi-tenant resolves the tenant from the request before any data access; serverless validates in the handler or platform middleware.

## Config

- One settings object, built at startup from the environment; code reads settings, never `os.environ` directly.
- Every key has a default that is safe for a fresh clone. The fail-closed exception is auth, which must be explicitly set.
- Secrets: environment or secret store at runtime; `.env.example` documents keys with placeholder values; `.env` is gitignored.
- Validation fails fast at startup with the key name, never at first use.

## Errors

- One typed error type carrying status, message, and an optional retryable flag.
- A single mapping from error to wire response; handlers never format responses ad hoc.
- Expected errors are documented with cause, fix, and retry-safety, budgeted against the suite's Time to Recovery target.
- Internals stay server-side: sanitize before sending, log the full error with a correlation id.

## Retries

- Bounded attempts, growing backoff, jitter for concurrent starts, and a log line per attempt.
- Retry only idempotency-safe operations, or document why the operation is safe.
- Exhaustion surfaces a typed error so the caller can distinguish "retried and failed" from "never tried".

## Observability

- Structured logging configured once at startup with a consistent format.
- One metrics or tracing export path, wired and exercised; a counter on a real code path beats an exporter that is never called.
- Correlation identifiers flow through the request path where the variant supports them.
- Observability never crashes the app: exports are best-effort and bounded.
