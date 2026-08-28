# Internal and External Stakeholder Technical Documentation

Diataxis still applies, but stakeholder docs often emphasize explanation and reference over executable integration steps.

## External stakeholder baseline

Do not assume internal vocabulary or architecture knowledge.

Include, when relevant:

- purpose and intended outcome
- audience
- glossary/acronyms
- system context
- actors and responsibilities
- trust boundaries
- architecture and data flow
- integration points
- prerequisites and dependencies
- authentication/authorization
- data ownership and retention
- failure behavior
- operational responsibilities
- security/compliance assumptions
- limits and non-goals
- version/support expectations
- escalation/support path

## Diagrams

A diagram should answer a specific question. Label boundaries, data direction, protocols, ownership, sync/async behavior, and trust zones when material.

Never use a diagram as a substitute for normative text if implementation correctness depends on the detail.

## Decision and architecture docs

For ADRs/design docs explain:

- context/problem
- constraints
- options considered
- decision
- rationale
- consequences/tradeoffs
- migration/rollout
- open questions
- observability and rollback

## Internal runbooks

Runbooks are how-to documentation. They must be operationally executable and include prerequisites, safety checks, verification, rollback, escalation, and failure branches.
