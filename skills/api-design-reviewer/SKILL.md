---
name: api-design-reviewer
description: Review an API as a product beyond OpenAPI syntax: resource modeling, naming, pagination, filtering, idempotency, concurrency, async operations, webhooks, error model, rate limits, request IDs, timeouts, retries, versioning, and authentication. Use to probe guessability and internal consistency and to report an API DX score separate from OpenAPI correctness. For API documentation parity use developer-docs-auditor; for SDK ergonomics use sdk-engineer.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and the API contract (OpenAPI/Proto).
metadata:
  version: "2.9.1"
---

# API Design Reviewer

## Mission

Review an API as a product, not as a schema. The contract is an interface; developers are its users, and their success is the outcome that matters. OpenAPI syntax is only one surface of the product.

Guessability is the test. **Can a developer with the product's domain vocabulary predict the endpoint, the path parameters, the response shape, the error, and the enum values without reading the docs?** An API that needs documentation for every call has a design defect, not a documentation gap.

Do not repair a confusing API by documenting it. Flag the underlying API defect and attribute it to the surface that owns the fix.

For a surface exposed to agents as tool definitions or an MCP server, hand the tool-surface
review to `agent-integration-dx` if available. This skill owns the HTTP contract beneath it.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Two scores, always

Report two independent scores whenever the evidence exists:

- **API DX Score /100** — the API as a product: resource modeling, naming, consistency, guessability, reliability semantics, errors, auth, and versioning.
- **OpenAPI Correctness Score /100** — the contract as a document: structure, refs, response coverage, and examples.

Neither score averages away the other. A perfectly valid OpenAPI file can earn a low API DX score, and a guessable API can ship with a broken spec. Report both; never merge them into one number.

Findings use the canonical P0–P4 severity vocabulary. Every finding carries an owner: **API** (contract design), **Product** (scope and decisions), or **Docs** (documentation and guidance).

## API design review workflow

### 1. Inventory the surface

Collect the contract and the evidence to review it against:

- the API contract: OpenAPI/Proto/AsyncAPI/GraphQL schema or the authoritative definition
- server implementation and tests, when the repository is available
- generated clients, official SDKs, and example code
- existing docs, changelogs, and migration notes

Do not review the contract in isolation when the repository is available. Verify behavior against implementation and tests; never treat the schema as truth when code contradicts it.

Record what was reviewed and what was not. Label findings and scores with evidence: **Observed**, **CI-observed**, or **Estimated**.

### 2. Resource model and naming

Read `references/resource-modeling.md` when evaluating resource boundaries and naming.

Check:

- resources are nouns, collections are plural, actions live in HTTP methods
- identifiers are opaque and consistent across resources
- parent/child relationships use one canonical path form
- state transitions are explicit and documented
- resource boundaries follow the decision tree in the reference

**Do not** accept "documented" as a fix for a confusing model. **Never** approve a path that mixes naming conventions within one API.

### 3. Requests and responses

Read `references/requests-responses.md` when reviewing request and response shapes.

Check:

- required vs optional fields, null vs omitted, defaults, and units
- one canonical timestamp and ID convention across the API
- one envelope and one pagination vocabulary
- filtering, sorting, and field selection are named after the fields they operate on

**Verify:** the same concept (IDs, timestamps, pagination fields, error fields) has one name and one shape everywhere.

### 4. Reliability semantics

Read `references/reliability.md` when evaluating idempotency, retries, timeouts, concurrency, and rate limits.

Check:

- mutating POSTs accept an idempotency key; PUT/DELETE are idempotent by method
- retryable errors are explicit, with `Retry-After` where relevant
- timeouts are documented and end in a definitive status
- concurrency control (ETag/If-Match) exists where writes can race
- rate limits and request/correlation IDs are part of the contract

**Do not** let "the client handles it" cover for an API that never defines retry, timeout, or limit semantics.

### 5. Async operations and events

Read `references/async-and-events.md` when reviewing async operations, webhooks, and event delivery.

Check:

- async operations use 202 plus a job resource, with documented terminal states
- cancellation is explicit and recorded
- webhooks define delivery guarantees, retry schedules, signatures, and event IDs

**Never** approve a webhook with no documented delivery guarantee or signature scheme.

### 6. Errors

Review the error model as a product surface:

- error responses have one stable shape: code, message, details, request ID
- status codes are honest: 4xx for client mistakes, 5xx for server faults, 429 for rate limits, 409 for conflicts
- error codes are unique, documented, and actionable; the message tells the developer what to change
- validation errors identify the failing field and the constraint

**Do not** use 400 for everything. **Never** emit an error body that lacks the request ID a developer needs to report the problem.

### 7. Authentication, authorization, and versioning

Check:

- one primary auth scheme, with scopes and permissions named consistently
- the token lifecycle: issue, refresh, revoke — is explicit
- the versioning strategy is explicit: URL, header, or media type, with documented deprecation and removal policy
- breaking changes are versioned; never mutate an existing contract silently

**Verify:** a developer can predict which credentials and which version they need to make the first successful call.

### 8. Guessability probes

Read `references/guessability.md` before running guessability probes.

Probe the contract with the question bank: can a developer predict the endpoint, the path parameters, the pagination shape, the error codes, and the enum values without reading the docs?

Run `scripts/guessability_check.py` on the OpenAPI JSON and treat its output as candidates, not verdicts. Verify each candidate against the question bank before reporting it.

**Do not** score guessability from the documentation. Cover the docs; guess from the domain.

### 9. OpenAPI correctness separately

Run `scripts/check_openapi_shape.py` on the OpenAPI JSON; it prints findings and exits 1 when any exist. Convert YAML to JSON with your own tooling first; the scripts accept JSON input only.

Check the structural pass independently of the product review: refs resolve, operationIds are unique, examples decode, and operations declare 4xx/5xx responses.

Correctness findings are contract defects. They lower the OpenAPI Correctness Score; they do not by themselves lower the API DX Score.

### 10. Score and report

Read `references/scoring.md` before assigning scores.

Compute the API DX Score across the weighted dimensions and the OpenAPI Correctness Score from the structural pass. Label both with evidence.

**Never** let a high correctness score hide a low DX score, or vice versa. A score without evidence is UNVERIFIED; do not convert estimates into verdicts.

Hand off documentation parity to the `developer-docs-auditor` skill and SDK ergonomics to the `sdk-engineer` skill if available.

## Required output

An API review report that includes:

1. API DX Score /100 and OpenAPI Correctness Score /100, each with an evidence label
2. findings with severity and owner — API, Product, or Docs
3. a per-finding recommendation and acceptance test
4. a prioritized backlog ordered by severity, not by effort
5. a verdict when one applies: PASS, PASS WITH DEBT, FAIL, or UNVERIFIED

Use `assets/api-review-report-template.md` when useful.

## Definition of done

The review is done when:

- the full surface was inventoried, or the missing evidence is recorded
- both scores are reported and never merged
- guessability probes were run against the contract, not the docs
- every finding has a severity, an owner, and an acceptance test
- reliability, async, error, auth, and versioning semantics were reviewed, not skipped
- the OpenAPI structural pass ran and its findings appear in the report
- script candidates were verified against the question bank before being reported as findings
- no defect was downgraded to a documentation issue merely because docs can explain it
- every score is labeled Observed, CI-observed, or Estimated
