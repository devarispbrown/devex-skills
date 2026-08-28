# Sandbox Failure Injection

## Purpose

Exercise failure handling inside the sandbox so failures are learned against, and proven against, sandbox-only state. Production never sees a simulated failure.

## Procedure

1. Pick a risky task that produces a failure-relevant event: a webhook, an async job, a provider call, a billing or quota event.
2. Create the sandbox route for the task first. Never inject failure into a path that can reach production.
3. Choose one failure to simulate:
   - provider outage or 5xx from a mock provider
   - failed or delayed webhook delivery to a mock receiver
   - invalid, malformed, or truncated payload
   - expired, revoked, or wrong-scope test key
   - partial batch failure with some items succeeding
4. Execute the task against the sandbox with the failure in place.
5. Record the observable behavior: surfaced error, retry behavior, idempotency, downstream state.
6. Remove the failure, re-run, and verify recovery is complete and state is consistent.
7. Label evidence: **Observed**, **CI-observed**, or **Estimated**. An estimate can never prove failure handling.

## Verification

- the failure was injected in the sandbox, never in a production-touching path
- the product's documented error and recovery behavior matches what was observed
- the sandbox returned to a known state after recovery
- the injected failure left no residue in shared or production resources

## Guardrails

- never throttle, break, or degrade a production service to simulate failure
- never simulate failures with real customer data or real money
- when a product has no sandbox failure path, the finding is a missing sandbox route, not a missing test
- use time travel or event simulation instead of waiting for real schedules when the failure depends on a clock
