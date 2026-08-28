# Documentation Architecture

Use Diátaxis to separate user intent, then design navigation around developer journeys.

## Minimum external documentation system

For most developer-facing products, provide:

- Get Started / Quickstart: canonical ≤15-minute magic path
- Tutorials: guided learning experiences beyond first success
- How-to: task-oriented recipes for working users
- Reference: API, SDK, CLI, config, events, errors, limits, schemas
- Explanation: concepts, architecture, mental models, tradeoffs
- Troubleshooting: symptom → diagnosis → remediation
- Operations / production: security, reliability, observability, scaling
- Lifecycle: versions, changelog, migrations, deprecations
- Support / contribution: where to ask questions, report bugs, contribute

Do not force the repository README to become the documentation site. The README should explain the project, get the right developer to first success, and route them onward.

## Canonical sources

Prefer one source of truth for normative facts:

- OpenAPI/AsyncAPI/protobuf/GraphQL schema for protocol shape
- CLI command definitions for flags/defaults
- typed config schema for configuration
- implementation/tests for behavior
- package metadata for supported runtimes/versioning

Generate reference from canonical sources where practical. Hand-written docs should add examples, task context, explanation, and recovery guidance rather than duplicate schema facts.

## Developer journey map

Connect documents so users can move through:

Discover → Quickstart → Learn → Build → Debug → Production → Upgrade

This is a docs-scoped subset of the canonical 14-stage developer journey; see `references/standards.md` for the canonical stage definitions.

Every major page should have an obvious next action or adjacent reference without turning navigation into an exhaustive link dump.
