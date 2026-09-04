---
name: sandbox-experience
description: Audit safe experimentation: test keys, fake resources, event simulation, mock webhooks, time travel, failure injection, quota simulation, sample data, and sandbox reset, so every risky learning task has a no-credit-card, no-production-risk sandbox route that passes the sandbox coverage gate. For the clone-to-productive path use local-development; for environment topology use environment-lifecycle; for fixture authoring use test-data-and-fixtures.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and product sandbox context.
metadata:
  version: "2.9.3"
---

# Sandbox Experience Audit

## Mission

Every learning task that is destructive, quota-consuming, or production-touching gets a sandbox route: free (no credit card), isolated from production accounts, resettable, deterministic, and safe by construction. No experimentation runs against production money, production data, or unrecoverable state.

Audit safe experimentation end to end: enumerate the learning tasks, classify their risk, map each risky task to a sandbox route, verify the route's characteristics, exercise failure and quota simulation inside the sandbox, verify reset and isolation, then gate the result through the sandbox coverage checker.

Do not patch a missing sandbox with warnings or manual-approval notes. A risky task without a sandbox route is a gate finding until a real route exists.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read `references/sandbox-characteristics.md` when defining what a valid sandbox route must satisfy.

Read `references/risk-mapping.md` when classifying learning tasks as destructive, quota-consuming, or production-touching.

Read `references/failure-injection.md` when simulating failures in the sandbox.

Read `references/quota-simulation.md` when simulating quota and limit behavior.

Read `references/reset-and-isolation.md` when verifying reset procedures, tenant isolation, and cleanup guarantees.

## Sandbox audit

Run the audit as a fixed sequence. Do not skip classification and jump to coverage counting; a count without a classification is meaningless.

### 1. Enumerate learning tasks

Inventory the documented and requested learning tasks: quickstart steps, tutorial exercises, example workflows, debugging scenarios, and agent tasks. Record each task, the resources it touches, and the account or environment it would run against.

Do not limit the inventory to current docs. Include every task the product invites developers to try.

### 2. Classify risk

Read `references/risk-mapping.md`.

Classify every task as exactly one of:

- **destructive** — deletes, overwrites, resets, or mutates state that is not trivially recoverable
- **quota-consuming** — consumes billable units, rate limits, quotas, or scarce resources
- **production-touching** — reaches a production account, production data, or a live external service
- **safe** — read-only, isolated, free, and recoverable by construction

When in doubt, classify as risky. A task that touches billable or mutable state with an unknown target defaults to production-touching.

### 3. Map risky tasks to sandbox routes

For every destructive, quota-consuming, or production-touching task, define a concrete sandbox route: the sandbox or test environment to use, the test keys or fake resources to create, and the exact command to run.

Build routes from sandbox primitives: test keys, fake resources, sample data, event simulation, mock webhooks, and time travel where scheduled behavior matters.

Map by risk type:

- destructive → resettable, isolated clone or fixture environment with a deterministic seed
- quota-consuming → test keys, mock providers, and simulated quota counters
- production-touching → sandbox tenant with fake resources and mock webhooks

A route that touches a real production account, a real credit card, or real customer data is not a sandbox route; it is the same risk wearing a different name.

### 4. Verify sandbox characteristics

Read `references/sandbox-characteristics.md`.

Verify each route satisfies every characteristic: no credit card, no production account, resettable, deterministic state, safe by construction. Record evidence per characteristic with an evidence label: Observed, CI-observed, or Estimated. An estimate can never prove a characteristic.

### 5. Exercise failure injection

Read `references/failure-injection.md`.

For each risky task, simulate at least one failure inside the sandbox: provider outage, failed webhook delivery, invalid payload, expired or revoked test key. Verify the product fails gracefully and the recovery path works, with the failure contained in the sandbox.

### 6. Exercise quota simulation

Read `references/quota-simulation.md`.

For each quota-consuming task, simulate quota exhaustion inside the sandbox: lowered limits, mock counters, throttled endpoints. Verify the documented throttle, error, and retry behavior. Never simulate against production quotas.

### 7. Verify reset and isolation

Read `references/reset-and-isolation.md`.

Verify the sandbox resets to a known state on demand, that one experimenter's state cannot leak into another's, and that cleanup leaves no residue. Reset the sandbox at least once during the audit and confirm the seeded state returns.

### 8. Run the coverage checker

Build the sandbox manifest from the audit: every risky task with its risk type, sandbox route flag, and characteristics. Run `scripts/check_sandbox_coverage.py` against the manifest.

The checker reports `NO_SANDBOX_FOR_RISKY_PATH` findings for risky tasks without a route and the coverage percentage. When any risky task lacks a route, the checker exits nonzero: the gate has not passed.

Do not adjust the manifest to make the checker pass. Adjust the routes.

### 9. Render the report

Use `assets/sandbox-audit-template.md`. Record the verdict, coverage, per-task route mapping, findings, and evidence before calling the audit complete.

## Sandbox contract

A valid sandbox route satisfies all of the following. A route that fails any one of them is not a sandbox route:

- **No credit card** — requires no payment instrument and no billable resource
- **No production account** — uses a sandbox/test account, tenant, or environment, never a production account
- **Resettable** — returns to a known state on demand
- **Deterministic state** — identical inputs produce identical, inspectable state
- **Safe by construction** — structurally cannot reach production data, production money, or unrecoverable state

Read `references/sandbox-characteristics.md` for the full definitions and verification checklist.

## Manifest contract

The coverage checker reads a single JSON manifest. The manifest:

- has a `name` field identifying the product or workspace
- has a `tasks` array; each task has `id`, `task`, `risky` (boolean), and, when risky, `risk_type` and `sandbox_route` (boolean)
- records the applicable characteristic names on each covered risky task
- is deterministic: the same file always produces the same output

See `assets/sandbox-manifest.clean.json` for a passing manifest and `assets/sandbox-manifest.example.json` for one with uncovered risky tasks.

## Required output

For every sandbox audit, produce the audit report using `assets/sandbox-audit-template.md`.

The report must contain:

1. **Verdict** — PASS, FAIL, or UNVERIFIED
2. **Coverage** — the checker result: risky task count, covered count, coverage percentage, and checker exit status
3. **Task inventory** — every enumerated learning task with its classification and evidence label
4. **Route mapping** — per risky task: risk type, sandbox route, characteristics verified, evidence label
5. **Findings** — every `NO_SANDBOX_FOR_RISKY_PATH` finding, keyed by gate name, with the task and the route required to clear it
6. **Failure and quota simulation** — what was simulated, what was observed, recovery confirmed
7. **Reset and isolation** — reset procedure exercised, isolation confirmed, cleanup verified
8. **Prioritized backlog** — every finding with the change required and its acceptance test

## Definition of done

A sandbox audit is done when:

- every learning task is enumerated and classified with evidence
- every destructive, quota-consuming, or production-touching task has a concrete sandbox route
- every route satisfies the sandbox contract, verified with labeled evidence
- failure injection and quota simulation were exercised inside the sandbox, never against production
- reset and isolation were verified by resetting the sandbox at least once
- the coverage checker exits cleanly with no `NO_SANDBOX_FOR_RISKY_PATH` findings
- no risky task is covered by a warning, a review, or a manual approval instead of a route
- the report is rendered from `assets/sandbox-audit-template.md` with evidence labels on every claim

Hand off the clone-to-productive path to the `local-development` skill, environment topology to the `environment-lifecycle` skill, and fixture authoring to the `test-data-and-fixtures` skill when those concerns dominate the audit.
