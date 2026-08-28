# Graceful Shutdown and Security Defaults

## Graceful shutdown

Termination is part of the contract. A long-running reference application must handle SIGTERM (and SIGINT in local development):

1. Stop accepting new work — close listeners, unsubscribe, stop intake.
2. Drain in-flight work — finish current requests and events, bounded by a timeout.
3. Close clients — close connections, commit or roll back, idempotently; closing twice is safe.
4. Exit — non-zero when drain failed or work was lost.

Verification: send SIGTERM mid-request and confirm the request completes and the exit code is 0; repeat with the drain timeout exhausted and confirm a non-zero exit.

Serverless variants do not implement signal handlers; the platform manages termination. The README states the platform contract — grace period, forced stop — and the app keeps handlers stateless so termination is safe at any point.

Kubernetes variants verify against the platform: readiness probes gate traffic, terminationGracePeriod bounds the drain, and SIGTERM is delivered to the container.

## Security defaults in examples

Reference applications model secure behavior; insecure examples teach insecure products.

- No secrets in the tree: no real tokens, keys, or passwords in code, docs, fixtures, or commits. Placeholder values only, sourced from the environment.
- Secrets flow through config only: `.env` is gitignored, `.env.example` documents the keys, and examples read from environment variables.
- Auth is on by default: deny when unconfigured. Examples never show "disable auth for simplicity" as the first step.
- Never log secrets: redact tokens, keys, and headers in log statements.
- Error output is sanitized: status, message, and remediation reach the caller; internals stay server-side.
- Safe response defaults: security headers (X-Content-Type-Options, X-Frame-Options), no-store on sensitive responses, TLS in deployment artifacts.
- Least privilege in deployment: minimal IAM and RBAC, scoped credentials, non-root container users where the platform allows.
- Unsafe examples are a defect: any sample that hardcodes credentials or disables a security control without a documented, deliberate reason is a P1.
