# Sandbox Quota Simulation

## Purpose

Simulate quota and limit behavior inside the sandbox so throttling, errors, and retries are understood against sandbox-only counters. Production quotas are never consumed or exhausted for learning.

## Procedure

1. Identify quota-consuming tasks: rate-limited endpoints, billable units, storage, seats, jobs, provider calls.
2. Create the sandbox route with test keys and a mock or lowered-quota target.
3. Configure the simulated quota: lowered limits, mock counters, throttled endpoint, short window.
4. Drive the task past the limit and record: status codes, error shape, retry guidance, backoff, idempotency.
5. Verify the product behaves as documented at and beyond the limit.
6. Reset the counters and confirm the sandbox returns to a known state.
7. Label evidence: **Observed**, **CI-observed**, or **Estimated**. An estimate can never prove quota behavior.

## Verification

- the simulation ran against sandbox-only counters and test keys
- behavior at and beyond the limit matches the documented contract
- the reset restored the counters
- no billable unit was consumed and no production quota was touched

## Guardrails

- never exhaust a production quota or rate limit to see what happens
- never use a real card or real spend to observe billing behavior
- when a product lacks a quota-simulation path, the finding is a missing sandbox route for a quota-consuming task
- use time travel when the quota window depends on a clock; do not wait against a production schedule
