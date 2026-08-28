# SDK Documentation and Parity Guide

## SDK inventory

For each official SDK record:

- language
- package/repository
- supported runtime versions
- latest supported major version
- API version mapping
- generation source if generated
- release cadence
- support tier

## Parity audit

Compare the canonical API/protocol surface with each SDK:

- resources/endpoints
- methods/operations
- request fields
- response fields/types
- errors
- pagination
- streaming
- webhooks/event helpers
- retries/timeouts
- idempotency options
- authentication methods

Flag gaps as generated-client lag, intentionally unsupported behavior, or undocumented divergence.

## Idiomatic API

Do not require every language to look syntactically identical. Review whether the SDK feels native:

- naming conventions
- option/config builders
- context/cancellation idioms
- async/await or futures
- iterators/generators
- typed errors
- nullable/optional types
- resource cleanup

## Documentation baseline

Every SDK should include:

- install
- initialization/authentication
- first request
- error handling
- pagination
- retries/timeouts
- major workflows
- debugging
- version compatibility
- migration notes for breaking releases

## Example parity

For major workflows, semantic behavior should be consistent across languages even when syntax differs.

Use a small canonical example matrix to prevent one language from becoming first-class while others silently rot.
