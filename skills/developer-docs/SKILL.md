---
name: developer-docs
description: Design, write, restructure, and update world-class documentation for developer-facing and open-source products. Use for READMEs, 15-minute quickstarts, Diátaxis tutorials/how-tos/reference/explanation, API/SDK/CLI/config docs, code comments, examples, integration guides, stakeholder docs, migration docs, and documentation architecture. Establish implementation truth first and flag product/DX design problems instead of documenting around them. For adversarial documentation audits use developer-docs-auditor; for whole-product developer-experience audits use developer-experience-auditor.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and normal build/test tooling.
metadata:
  version: "2.3.0"
---

# Developer Docs Authoring and Architecture

## Mission

Create developer documentation that is technically authoritative, easy to navigate, maintainable with the product, and optimized around real developer outcomes.

Treat documentation as part of product design. If an API, SDK, CLI, configuration model, error model, install flow, or workflow is hard to explain cleanly, identify the underlying developer-experience problem rather than writing around it.

Use Diátaxis as the information-architecture model, not as the complete quality system:

- **Tutorial**: learning through a successful guided experience.
- **How-to**: completing a real task for an already-competent user.
- **Reference**: authoritative description of the system.
- **Explanation**: concepts, architecture, rationale, constraints, and tradeoffs.

Read `references/diataxis.md` when classifying or restructuring content.

## Non-negotiable: 15-minute magic path

Every external developer-facing product must have a canonical Quickstart/Get Started path where a brand-new developer with zero product knowledge can achieve and verify meaningful end-to-end product value in **15 minutes or less**.

Read `references/magic-path.md` before creating or revising onboarding, a README quickstart, installation docs, or the getting-started architecture. Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Design for the timer. Do not hide product-specific setup in prerequisites. Account creation, credentials, product-specific installation/configuration, execution, wait time, and verification count. If production provisioning cannot fit, design a sandbox/test/local path.

Installation, authentication, or a health check alone is not success. The quickstart must demonstrate the product's core value.

## Establish truth before writing

Before editing technical docs:

1. Inspect the repository and identify implementation, tests, public symbols, specs/schemas, CLI definitions, config, examples, SDKs, generated code, release metadata, and existing docs.
2. Identify the authoritative source for each normative claim.
3. Prefer implementation, tests, released interfaces, and machine-readable specifications over prose when they conflict.
4. Never invent endpoints, fields, defaults, flags, limits, status codes, environment variables, versions, behavior, or guarantees.
5. Surface contradictions explicitly.
6. Mark unknowns instead of guessing.

For broad repos, run `scripts/inventory_docs.py` when useful.

## Authoring workflow

### 1. Identify audience, state, and outcome

Determine:

- who the user is
- what they already know
- whether they are learning, working, consulting facts, or building understanding
- environment/runtime constraints
- the exact observable outcome they need

For first-run and external stakeholder docs, assume zero product-specific knowledge.

### 2. Map the developer journey

Cover the connected path:

Discover → Prerequisites → Install → Account/Auth → Configure → First value → Verify → Customize → Debug → Production → Operate → Upgrade → Get help

This list is a docs-scoped subset of the canonical 14-stage developer journey; see `references/standards.md` for the canonical stage definitions. Read `references/docs-architecture.md` for the minimum documentation system.

### 3. Classify with Diátaxis

Give each page or section one primary job. Split mixed pages when modes interfere with one another. Cross-link adjacent modes instead of combining everything into one document.

### 4. Design the magic path first

Before polishing the rest of onboarding:

1. Define the smallest meaningful end-to-end outcome.
2. Define benchmark start and stop conditions.
3. Remove optional branches and choices.
4. Choose a default SDK/language/path when the product supports many.
5. Provide test/sandbox/local resources that eliminate manual provisioning.
6. Make each command complete and copy-pasteable.
7. Show expected output or verification.
8. Budget the path to ≤15 minutes.
9. Put production hardening after first success.
10. Link advanced concepts rather than front-loading them.

If the path cannot credibly meet 15 minutes, report the blocker as Docs, Product/DX, Infrastructure, or External dependency and propose the product change required.

### 5. Review the product surface exposed by docs

When relevant, review:

- resource and method naming
- request/response shape
- HTTP semantics and status codes
- IDs, timestamps, enums, nullability, units, money
- pagination/filtering/sorting
- idempotency/retry behavior
- async operations and webhooks/events
- rate limits and quotas
- errors and remediation
- request/correlation IDs
- auth scopes and environments
- versioning/deprecation
- CLI flags, exit codes, stdout/stderr
- config precedence/defaults/secrets
- SDK ergonomics and language idioms

Read `references/api-dx.md` and `references/sdks.md` as needed.

### 6. Author the correct artifact

Read only the references relevant to the work:

- repository README: `references/readmes.md`
- quickstarts/examples: `references/examples.md` + `references/magic-path.md`
- API/CLI/protocol: `references/api-dx.md`
- SDKs: `references/sdks.md`
- public code docs/comments: `references/code-comments.md`
- stakeholder/internal docs: `references/stakeholder-docs.md`
- migrations/releases/deprecations: `references/lifecycle.md`
- terminology/style/accessibility: `references/style.md`
- coding-agent/LLM usability: `references/llm-ready-docs.md`

Use templates from `assets/` when they fit. Do not force templates when the product needs a better structure.

### 7. Build for maintainability

Prefer:

- generated reference from canonical schemas
- tested example source imported into docs
- shared includes for normative repeated facts
- canonical terminology
- version-aware docs
- changelog and migration links
- machine-readable schemas/examples
- stable headings and anchors

Avoid manually duplicating values that code or schemas can generate.

### 8. Self-check before completion

Verify:

- technical claims are grounded
- the page has one primary Diátaxis purpose
- terminology is consistent
- commands/examples are complete enough to execute
- success is observable
- errors have recovery guidance
- security-sensitive steps use safe credential practices
- version/support scope is clear
- onboarding was designed against the ≤15-minute magic path

When deterministic validation is needed, hand off to or invoke the separate `developer-docs-auditor` skill if available, or `developer-experience-auditor` for product/DX journey measurement.

## README contract

A repository README is a landing page plus a route to first value, not a complete manual.

It should normally contain:

1. project name and one-sentence value proposition
2. who it is for / why it exists
3. maturity/status where important
4. prerequisites
5. canonical quickstart or direct link to it
6. minimal end-to-end example and expected result
7. basic configuration only
8. deeper docs/reference links
9. compatibility/support
10. development/testing
11. contributing/security/community/license

The README onboarding path inherits the ≤15-minute magic-path requirement when it is the canonical getting-started route.

## API and SDK contract

Public API reference should cover, when applicable:

- purpose and operation/signature
- auth/authorization
- inputs, types, constraints, defaults, nullability
- realistic request and response examples
- status/error taxonomy and remediation
- pagination/filtering/sorting
- retries/idempotency
- side effects/state transitions
- async/webhook semantics
- quotas/rate limits
- request/correlation identifiers
- version/deprecation status

Every official SDK is a first-class product surface. Maintain semantic parity with the canonical API while using idiomatic language conventions.

## Code documentation contract

Document public/exported symbols and non-obvious contracts. Prioritize intent, invariants, concurrency, ownership/lifetime, side effects, error semantics, units/formats, performance constraints, security assumptions, compatibility behavior, and rationale.

Do not add comments that merely restate syntax.

## External stakeholder contract

Assume no internal context. Define actors, vocabulary, system boundaries, data flow, responsibilities, dependencies, authentication, failure behavior, operational ownership, security/compliance assumptions, limits, versions, and support/escalation paths as relevant.

## Human and agent usability

Keep canonical technical content available in clean structured text. Use stable descriptive headings, explicit versions, machine-readable schemas, complete examples, and text equivalents for essential diagrams. Consider `llms.txt` or equivalent indexes when useful, but never degrade human usability to optimize for agents.

## Definition of done

Authoring is done when:

- intended users can achieve the intended outcome
- the canonical first-run path is designed to achieve meaningful end-to-end value in ≤15 minutes
- technical claims match authoritative sources
- examples are complete and validation-ready
- terminology is consistent across surfaces
- likely failures have actionable recovery paths
- the Diátaxis purpose is clear
- adjacent docs are connected through useful navigation
- API/SDK/version/lifecycle implications are handled
- repeated normative facts have maintainable sources of truth
- product/DX defects discovered during documentation are surfaced rather than hidden
