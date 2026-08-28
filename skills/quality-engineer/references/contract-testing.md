# Contract Testing

## What contracts protect

A contract is any machine-readable agreement across a boundary: API schemas, message schemas, queue topics, published events, generated clients. Contract tests pin the boundary so providers and consumers can evolve independently.

## Provider tests

1. Identify every published contract: OpenAPI/AsyncAPI specs, protobuf/JSON schemas, event schemas.
2. Test that the provider's real behavior matches the published spec: response shape, status codes, validation errors, pagination fields, schema validity.
3. Validate the spec file itself (it is code, not prose): lint it, and fail CI when a published spec changes without a compatibility check.

## Consumer tests

1. For each consumer, capture what it actually requires: field presence, types, enums, status codes, retry semantics.
2. Write consumer-driven contract tests using consumer expectations as the source of truth (pact-style) when consumers are external or many.
3. Run consumer tests against the provider's latest contract in CI so drift surfaces at the boundary, not in production.

## Schema and compatibility suites

1. Maintain schemas as versioned, backward-compatible artifacts. Never hand-edit generated schema exports.
2. Run a compatibility suite for schema evolution: adding optional fields is safe, removing or narrowing fields is breaking.
3. For events and messages, test that a new producer version can be consumed by the oldest supported consumer version.
4. A compatibility suite failing is a release-blocking finding; it means a claimed supported version breaks.

## Wiring

- Contract tests run in CI on both sides of every boundary.
- Test fixtures and sample payloads are part of the suite; never mock the contract itself in the provider's own contract test.
- Report contract drift with evidence and severity using the parent skill's vocabulary. Do not smooth over a boundary break because "the consumer can adapt."
