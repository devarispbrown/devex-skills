# Async Operations and Events

## One pattern, chosen deliberately

- Pick one async pattern per API: 202 plus a job resource with polling, or webhooks, or both with explicit guidance on when each applies.
- 202 Accepted returns a job resource via `Location` header with a `status` field. It never returns a final result body.

## Job resources

- A job resource exposes: `status`, terminal states, progress where meaningful, `created_at` / `started_at` / `finished_at`, and a result or error reference.
- Terminal states are documented and finite: `succeeded`, `failed`, `cancelled`, plus optional partial states.
- Polling is documented: recommended interval, `Retry-After` on 202, and a definitive final state. A job never silently becomes a 404 mid-flight.
- Completion is signaled by a terminal state or an explicit webhook. A disappearing resource is not a signal.

## Cancellation

- Cancellable operations expose a documented cancel endpoint on the job resource.
- Cancelling a finished job is a no-op, not an error.
- Cancellation is recorded in the job's state history with a `cancelled_at` timestamp.

## Webhook delivery guarantees

- Delivery is at-least-once unless documented otherwise. Clients must deduplicate on event ID.
- Every event carries a unique opaque event ID, a timestamp, a type and version, and the affected resource reference.
- Delivery ordering is not guaranteed unless documented. Include `occurred_at` or a sequence number so clients can reorder.
- Event payloads version independently of the API. A breaking payload change is a new event version, never a silent mutation.

## Retry schedules and dead letters

- Failed deliveries retry on a documented exponential schedule with a cap, then land in a dead-letter state or a visible failure record.
- The retry schedule and maximum attempts are documented. Do not retry forever silently.
- Delivery failures are visible to the subscriber through a documented channel: dashboard, email, or a failure endpoint.

## Signatures

- Webhook payloads are signed (HMAC with a shared secret, or equivalent) and clients verify the signature before trusting the payload.
- Document how to obtain, rotate, and revoke secrets. Rotation never invalidates in-flight deliveries without notice.

## Replay and testing

- Replaying a past event reuses the original event ID; receivers deduplicate by event ID and must not double-apply effects.
- Provide a sandbox endpoint, test-mode events, or a replay endpoint for development. Testing against production events is a defect.
- Test payloads are labeled as test events so receivers can distinguish them from production.
