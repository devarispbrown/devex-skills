# Production Readiness Checklist

The nine mandatory concerns. Every reference application demonstrates all nine, in every variant. The `scripts/check_reference_app.py` checker confirms evidence of wiring; this checklist is the semantic standard each concern must meet.

## The nine mandatory concerns

### 1. Auth

Evidence: an auth module or middleware that gates at least one route or resource.

The concern is met when:

- access is denied by default; no configured credential means no access
- tokens and keys are verified, never merely decoded
- the check is wired to a real code path, not dead code

Missing or bypassable: P1.

### 2. Config

Evidence: settings loaded from the environment with defaults.

The concern is met when:

- every setting reads the environment at startup; none is hardcoded in code
- defaults are safe for a fresh clone; no credential is required to start
- secrets come from the environment or a secret store, never from the tree
- `.env` and equivalent files are gitignored; `.env.example` documents the keys

Missing: P1. Hardcoded secret in the tree: P0.

### 3. Errors

Evidence: a typed error surface with status and message mapping.

The concern is met when:

- errors carry a status and a message a caller can act on
- expected errors are documented with cause, fix, and retry-safety
- internals are not leaked; stack traces stay server-side
- error paths are reachable, not dead code

Missing or unhelpful: P1.

### 4. Retries

Evidence: bounded retry logic with backoff on transient failures.

The concern is met when:

- attempts are bounded; there is no unbounded retry
- backoff grows and is logged, with jitter where appropriate
- retries are idempotency-safe, or the caller is told when they are not
- retry exhaustion surfaces a typed error, not silence

Missing: P1. Unbounded retry: P1.

### 5. Observability

Evidence: logs, metrics, or traces exported to an observable sink.

The concern is met when:

- structured logging is configured at startup, not left to implicit defaults
- at least one metrics or trace export path exists and is called
- correlation identifiers survive the request path where the variant supports them
- observability setup itself cannot crash the app

Missing: P1.

### 6. Tests

Evidence: a runnable test suite in the tree.

The concern is met when:

- tests cover failure paths — auth denial, error mapping, retry exhaustion — not only the happy path
- the suite runs from a clean clone with committed automation
- variant stress points (tenant isolation, delivery, load) have tests

Missing: P1.

### 7. Deployment

Evidence: a deployable artifact definition matching the variant.

The concern is met when:

- the artifact matches the variant's row in the deployment matrix
- health, config delivery, and logs/metrics reachability are defined
- no secrets or machine-specific values are baked in

Missing or mismatched variant: P1.

### 8. Shutdown

Evidence: graceful termination handling for the runtime.

The concern is met when:

- a signal handler stops accepting work, drains in-flight work, closes clients, and exits non-zero on failure
- drain is bounded by a timeout; close is idempotent
- serverless variants document platform-managed termination instead of faking a handler

Missing in a long-running variant: P1. Missing in serverless: P3 — documented platform lifecycle suffices.

### 9. Security

Evidence: secret handling and safe defaults in code and examples.

The concern is met when:

- no secret, personal config, or machine-specific value appears in the tree
- secure defaults are on: auth denied by default, safe headers, no secret logging
- example commands never encourage unsafe credential handling

Hardcoded secret: P0. Insecure example pattern: P1.

## Gate semantics

A checker exit code of 1 on a missing concern is a hard signal: fix the concern and re-run before the tree ships. A missing concern is never waived; the report names it with severity.
