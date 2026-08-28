# Reliability Semantics

## Idempotency keys

- Every mutating POST that can be retried accepts an idempotency key.
- The key travels in the `Idempotency-Key` header, is client-generated and opaque, and is reused unchanged on retry.
- The server stores the key with the first response and replays the original response for identical keys. Keys expire after a documented period.
- Do not key idempotency on a body hash; a retry with a slightly different body is a different request, not a replay.
- PUT and DELETE are idempotent by method. PATCH is not; document PATCH retry semantics explicitly.

## Retry semantics

- Retryable errors are documented: 429, 5xx, and network failures. Non-retryable client errors (other 4xx) are not.
- The server provides `Retry-After` on 429 and 503. Never suggest a retry without a number or date.
- The API documents which status codes are retryable and whether the request is idempotent; the client owns its own retry schedule.

## Timeouts

- Document server-side timeouts per operation class: default, long-poll, and streaming.
- A timeout returns a definitive status (504) with a retryable marker. Do not silently drop requests.
- Client-controlled timeouts are allowed only when the API documents the accepted range and the failure response.

## Concurrency

- Optimistic concurrency uses `ETag` on reads and `If-Match` on writes; a mismatch returns 412 Precondition Failed.
- Last-write-wins is documented as such when used. Do not present it as safe concurrency.
- PATCH merges fields independently; document whether concurrent field updates are merged or rejected.
- Conditional writes are supported whenever a client can race another writer on the same resource.

## Rate limits

- Rate limits are documented: window, limit, scope (per key, per IP, per account), and the cost model for expensive calls.
- Responses expose the limit state: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
- 429 includes `Retry-After`; honoring it is the client's job, and the API must not silently forgive clients that ignore it.
- Do not return 400 or 403 for rate limiting. 429 is the only honest code.

## Request and correlation IDs

- Every response carries a request ID in `X-Request-Id`, echoed from the client when provided, generated otherwise.
- Correlation IDs flow unchanged across internal hops so support can trace a request end to end.
- Error responses include the request ID, a timestamp, and the code in stable fields.
- Clients can send their own request ID; the API documents whether it accepts one and under what length constraints.
