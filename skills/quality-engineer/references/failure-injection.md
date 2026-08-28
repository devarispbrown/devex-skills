# Failure Injection

## What failure injection proves

Tests that assume dependencies always succeed cannot predict production. Failure injection proves the system degrades safely: retries, timeouts, circuit breakers, dead-lettering, and kill-switch behavior.

## Injection patterns

- **Latency**: add delay to a dependency call; verify timeout handling and that the request still completes or fails cleanly.
- **Timeouts**: make a dependency hang; verify the caller's deadline enforcement and error path.
- **Partitions**: block traffic to one replica, one broker node, or one dependency; verify failover, reconnection, and no silent data loss.
- **Kill**: terminate a process mid-transaction; verify recovery, idempotent re-processing, and startup consistency.
- **Crash of a dependency**: restart the database/broker/cache mid-request; verify backoff, retry with jitter, and eventual consistency.
- **Poison inputs**: send malformed messages or bad records; verify they are rejected or dead-lettered, never silently dropped with data loss.

## In-CI injection

1. Choose injection points from the failure modes mapped for the system (see `references/test-strategy.md`).
2. Add at least one injection test per high-severity dependency path.
3. Run injection in CI with real containers/test doubles — never mock the dependency's failure modes entirely, or the test proves nothing.
4. Record results as CI-observed evidence.

## Kill switches

1. Identify every kill switch, feature flag, and circuit breaker in the system.
2. Test that flipping the switch actually changes behavior in both directions.
3. Test that the switch is reachable during an incident: documented path, no auth bottleneck, idempotent toggling.
4. A kill switch that has never been tested is a liability, not a feature.

## Rules

- Never inject failures against production data or real user traffic.
- Prefer staging and CI environments; if a game day runs against production-like infrastructure, use isolated tenants and a documented rollback.
- Label injection results with evidence and environment. An injection test that did not actually fail anything proves nothing — verify the system reacted, then recovered.
