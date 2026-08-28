# Webhook Delivery Reliability

Webhook delivery guarantees, retries, and idempotency. Read this when auditing or documenting webhook behavior.

## State the guarantee exactly

Choose a guarantee and document it in exact terms:

- **at-least-once**: every event delivered at least once; consumers must deduplicate
- **at-most-once**: best effort; events may be lost, and the docs must say so
- **ordered**: per-source ordering is preserved, with the limits of that guarantee stated
- exactly-once does not exist across a network; document the closest real guarantee

Verify:

- the documented guarantee matches implementation
- "at-least-once" implies idempotency guidance, which exists and is linked

## Retry behavior

Document and verify:

- maximum attempts, bounded, never infinite
- exponential backoff with jitter
- retry-after semantics when the consumer is rate-limited
- backpressure: what happens when a consumer is slow (queue, drop with notification)
- the dead-letter path for undeliverable events
- a replay mechanism consumers can invoke

Verify:

- retries never replay side effects on the consumer without idempotency protection
- retry limits are tuned so a dead consumer cannot multiply load indefinitely

## Event identity and idempotency

Verify:

- every event carries a stable, unique event ID
- consumers can deduplicate on event ID or an idempotency key
- retries of the same event reuse the same ID; a new event never reuses an ID
- the payload includes event type, version, timestamp, and resource ID

## Security

Verify:

- signatures or an authenticated header verify origin, with rotation documented
- consumers are told how to verify and how to handle verification failure
- webhook URLs are secret and scoped to the integration

## Testing and observability

Verify:

- a test or probe endpoint lets consumers validate their integration
- delivery attempts, failures, and dead letters are measurable and visible to operators
- delivery metrics appear in postmortems when webhooks were affected
