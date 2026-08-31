---
name: web-console-dx
description: Remove dashboard and portal friction: resource CRUD, API key management, logs, metrics, webhooks, events, usage, errors, and permissions UI where every operation answers what happened, what API call it made, can it be automated, and can the CLI be copied. For the command-line surface use cli-designer.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and the console codebase or docs.
metadata:
  version: "2.3.2"
---

# Web Console DX

## Mission

The web console is a product surface, not plumbing. Every button, toggle, empty state, and permission screen either removes developer friction or generates a support ticket. Design and audit dashboards and portals so that every operation answers four questions:

1. **What happened?** The UI states the result, the failure, and the next step.
2. **What API call did it make?** The operation maps to a real, named API endpoint.
3. **Can it be automated?** An API or CLI equivalent exists for every UI operation.
4. **Can the CLI be copied?** The equivalent command is one click or keystroke away.

Never design a console operation the product cannot express in its API. Never ship a button with no automation equivalent: someone will script it in CI, and a console-only path forces them through the browser.

Ground every claim in the codebase and the docs. Never invent endpoints, fields, defaults, status codes, or behavior; mark unknowns instead of guessing.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read `references/console-audit-method.md` before auditing a console. Read `references/automation-parity.md` before evaluating operation-to-command mapping.

## Console friction audit

Audit as an adversarial developer: first as a user who must complete real work in the browser, then as an operator who must script the same work in CI. Complete the eight steps in order and record findings per operation.

### 1. Enumerate the operation surface

List every operation the console exposes. Cover at minimum:

- resource CRUD — create, read, update, delete, list — per resource type
- API key management — create, rotate, revoke, scope, expiry
- logs, metrics, webhooks, and events views
- usage, billing, and error browsing
- permissions and member management

Write the inventory as a JSON manifest with fields `name`, `has_api_equivalent`, `has_cli_equivalent`, and `docs_link`; see `assets/console-ops.example.json` for the shape. Follow `references/resource-crud.md` for CRUD and bulk-operation UX patterns.

Verify:

- every navigation item maps to one or more inventory entries
- the inventory names the page and the operation, not the page alone
- shared operations (invite, switch environment) appear once per surface they touch

### 2. Walk the console or its docs

Walk the console surface end to end using the live UI when available, otherwise the console docs. Follow `references/console-audit-method.md` for the walkthrough procedure and recording format.

Record per operation:

- where it lives and how many clicks it takes
- what inputs it demands and which are pre-filled
- what it shows on success and on failure
- whether the result names the underlying API call
- whether a CLI command is visible and copyable

### 3. Trace the API call behind every operation

For each operation, identify the exact API call that implements it: endpoint, method, parameters, and response shape. Use the codebase, API docs, and network inspection as evidence.

Verify:

- the traced call is grounded in code or docs, never guessed
- the traced parameters match the UI inputs
- async operations trace to a request and a status/result poll or webhook
- an operation with no traceable API call is recorded as a product defect or docs gap, not papered over

### 4. Check automation parity

Run `scripts/check_console_ops.py` against the manifest. The report is advisory and never a verdict, but use it to find every gap.

Verify:

- no operation is missing both an API and a CLI equivalent; provide the automation surface or remove the UI operation
- every operation with one surface only is recorded as a partial gap with a fix
- the parity claim for each operation carries an evidence label

### 5. Check copy-command affordances

For every operation with a CLI equivalent, verify the console offers a copyable command per `references/automation-parity.md`.

Verify:

- the affordance is visible on the operation view, not hidden in a menu
- the copied command is complete: auth context, required flags, and the current page's entity
- the copied command works from a fresh terminal without editing

### 6. Audit observability views

Check logs, metrics, webhooks, and events views against `references/observability-views.md`.

Verify:

- filters match API capabilities, not a fixed subset
- timestamps, fields, and aggregation definitions are documented
- views link to the API calls that produced the data
- each view answers all four questions

### 7. Audit keys and permissions

Check API key management against `references/api-key-management.md`.

Verify:

- keys can be created, scoped, rotated, and revoked without contacting support
- the secret is shown once and rotation policy is stated
- permission grants map to documented API permissions and are revocable
- every grant or revocation is traceable to an API call

### 8. Rank findings and render the report

Classify each finding by surface and severity using the canonical vocabulary from `references/standards.md`. Prioritize by developer impact: operations that block automation, destroy data without recovery, leak permissions, or hide errors outrank cosmetic issues.

Verify:

- severity labels match the canonical vocabulary exactly
- every finding carries an evidence label: Observed, CI-observed, or Estimated
- the report is rendered from `assets/console-audit-template.md`

## Operation contract

Every console operation must satisfy:

- the UI states what happened, with error details and the next step
- the operation names the API call it made, with parameters
- an API or CLI equivalent exists
- the CLI equivalent is copyable in one action
- destructive operations require confirmation and state their irreversibility
- async operations show progress and a completion signal

## Automation parity contract

Follow `references/automation-parity.md`:

- no console operation exists without an API or CLI equivalent
- the equivalent command is complete, including auth context and required flags
- copy-command affordances appear on every operation view
- the copied command works from a fresh terminal
- scripted equivalents are versioned and documented

## Observability contract

Follow `references/observability-views.md`:

- logs are searchable, filterable, and paginated with documented fields
- metrics views state their definition, aggregation, and time range
- events and webhooks views show payloads, delivery status, and retries
- every view links to the API call that produced the data

## Keys and permissions contract

Follow `references/api-key-management.md`:

- keys can be created, scoped, rotated, and revoked without contacting support
- key creation surfaces the secret once and states rotation policy
- permission grants map to documented API permissions and are revocable
- key and permission operations are automatable

## Required output

Produce the console audit report from `assets/console-audit-template.md`. The report must contain:

1. **Scope** — console surfaces audited, environment, evidence labels
2. **Operation inventory** — the full manifest with parity status per operation
3. **Friction findings** — per-operation findings with severity, surface, and evidence
4. **Automation parity** — gaps and partial gaps, each with a required fix
5. **Observability findings** — logs, metrics, webhooks, and events issues
6. **Keys and permissions findings** — key lifecycle and permission issues
7. **Prioritized backlog** — ranked changes with acceptance tests

## Definition of done

Console work is done when:

- every operation answers all four questions: what happened, what API call, can it be automated, can the CLI be copied
- no operation lacks an API or CLI equivalent unless intentionally removed
- copy-command affordances are present and executable
- logs, metrics, webhooks, and events views meet the observability contract
- API keys and permissions are fully manageable and automatable
- findings are ranked with the canonical severity vocabulary
- the report is rendered from `assets/console-audit-template.md`

For the command-line surface, use the `cli-designer` skill. For error text and recovery, use `error-experience`. For config model design, use `configuration-dx`. For whole-product developer-experience measurement, use `developer-experience-auditor`. For release compatibility of console-facing API and CLI output, use `release-guardian`.
