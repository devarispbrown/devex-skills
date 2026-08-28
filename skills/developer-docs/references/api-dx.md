# API and Developer Experience Review

Documentation is an excellent stress test for API design. If the interface cannot be described predictably, the interface may be the defect.

## Resource model

Check:

- nouns/resources are stable and understandable
- operations use consistent verbs and semantics
- identifiers are opaque unless the format is intentionally public
- parent/child relationships are consistent
- collection and singular resource naming are predictable
- state transitions are explicit

## Requests

For each input document:

- required/optional
- type
- nullable versus omitted
- default
- min/max and other validation
- format and units
- enum values
- whether unknown fields are rejected or ignored
- whether fields are mutable after creation
- conditional requirements

Use examples that demonstrate realistic valid input, not every field at once.

## Responses

Review:

- stable resource shape
- predictable envelopes
- consistent ID names
- timestamps and timezone/format
- nullability
- monetary values and currencies
- units
- URLs and references
- partial/expanded representations
- ordering guarantees
- omitted versus empty values

A developer should not need to reverse-engineer semantics from examples.

## HTTP semantics

Check status codes, method semantics, cacheability where relevant, conditional requests where relevant, and distinction between validation, authorization, conflict, rate limit, and server failures.

Avoid returning a generic success code for semantically different outcomes if clients need to branch reliably.

## Error model

A strong error should provide enough structured information to support both humans and programs.

Prefer fields conceptually equivalent to:

- stable machine-readable code
- human-readable message
- HTTP status
- field/path when validation is localizable
- request/correlation ID
- documentation/help link when useful
- retryable signal or sufficient semantics to derive it
- structured detail for multiple validation failures when appropriate

Review whether error codes are stable enough for programmatic handling.

Document for each major error:

- what it means
- common causes
- corrective action
- whether retry is safe
- whether the same request can be replayed

## Idempotency and retries

For mutating operations, document:

- whether idempotency is supported or automatic
- scope and lifetime of idempotency keys
- duplicate-request behavior
- retry-safe status codes/failures
- server versus client retry responsibility
- backoff and jitter guidance
- side-effect behavior after timeouts

## Pagination

Document:

- cursor/token/page model
- default and maximum page size
- ordering
- stability during concurrent writes
- next/previous link or token
- whether SDKs auto-paginate
- limits on deep traversal

Do not encourage clients to synthesize opaque cursors.

## Rate limits and quotas

Document:

- limit scope where public
- relevant response headers
- 429 behavior
- Retry-After behavior
- burst versus sustained considerations
- per-account/project/resource distinctions
- where limits can be viewed or increased

## Async operations

If work continues after the response, document:

- accepted versus completed semantics
- operation/job resource
- polling or callback/webhook path
- terminal states
- failure states
- cancellation
- retention
- idempotency interaction

## Webhooks/events

Document:

- event catalog and schemas
- delivery guarantees
- ordering guarantees or absence thereof
- duplicate delivery
- retry schedule at a useful level
- signature verification
- clock tolerance if applicable
- endpoint response expectations
- replay/testing tools
- versioning
- event IDs and correlation

## Authentication and authorization

Document:

- credential types
- intended environments
- scopes/roles
- least-privilege guidance
- expiration/rotation
- regional or tenant scope
- testing/sandbox credentials
- where secrets must not be used

Examples must use placeholders or safe test credentials.

## Request IDs and observability

Expose and document request/correlation identifiers when possible. A developer should be able to connect a failed API call to logs, dashboards, or support.

## Versioning

Make clear:

- current stable version
- how a client selects a version
- compatibility policy
- breaking-change cadence
- SDK/API version relationship
- preview/beta semantics
- changelog
- migration path
- sunset policy

## API reference UX

High-quality API reference should make it easy to:

- switch languages/SDKs without losing context
- copy a runnable request
- see request and response together
- distinguish required from optional fields
- inspect nested schemas
- understand errors
- reach conceptual guides and task guides
- use sandbox/test mode
- identify the selected API version
