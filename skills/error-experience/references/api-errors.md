# API Errors

## Status-code discipline

- Use the correct range: client errors are `4xx`, system errors are `5xx`. A validation failure is never `500`; a healthy server that rejects a request is never `200`.
- Use the precise code within the range: `400` bad request, `401` unauthenticated, `403` forbidden, `404` not found, `409` conflict, `422` unprocessable entity, `429` rate limited, `500` internal, `502`/`503`/`504` dependency failures.
- Never return `200` with an error body. Never return `500` for a problem the caller can fix.
- When a proxy or gateway handles the status, ensure the application-level error body still reaches the caller.
- Retryable statuses are explicit: transient `5xx` and `429` signal "try again"; permanent errors signal "do not".

## Structured error bodies

Every error response carries one consistent schema, shared by all endpoints:

- `code`: the stable machine-readable code.
- `message`: the human explanation (what happened and why).
- `details`: additional structured context where useful.
- `request_id`: the correlation identifier.
- `docs_url`: a link to the error's documentation page.

The body is a single error object or a list of errors, never both, never an ad-hoc shape per endpoint. The schema is versioned and documented; a client can parse any error without endpoint-specific knowledge.

## Machine-readable codes

- Codes are stable strings, documented in the error reference and in the OpenAPI/schema definition.
- Codes never change meaning; messages may change. Never emit two different codes for the same failure class across endpoints.
- Include the code in logs and traces verbatim so support can join the response to the backend event.

## Retryability signals

- Express retry policy in the response, not only in prose: use `Retry-After` on `429` and transient `5xx`.
- Distinguish permanent from transient within the same status when needed, using the code field.
- For idempotent operations, document that retry is safe and how to reuse the request identifier; for non-idempotent operations, say so.
- Clients must be able to decide "retry or not" from the response alone, without reading the docs.

## Field paths

- Validation errors name the exact field using a documented path syntax (dot-path or RFC 6901 JSON Pointer), for example `details.items[2].price`.
- Include the offending value and the constraint: "`price` must be a positive number, got `-5`."
- Never say "invalid request" without saying which field and why.

## Docs links

- `docs_url` resolves to a page describing the error, its causes, and its corrective action.
- Every expected error has a documentation page; every documented error is emitted by the code.
- Link from the docs page back to the code path so engineers can find the emitter.
