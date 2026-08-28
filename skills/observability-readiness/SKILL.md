---
name: observability-readiness
description: Make production failures diagnosable: logs, metrics, traces, profiles, request and correlation IDs, health checks, SLIs/SLOs, dashboards, alerts, cardinality, sampling, PII, and debug modes. Bar: developers can answer unexpected questions without adding new instrumentation. For error semantics and Time to Recovery use error-experience.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and runtime/telemetry context.
metadata:
  version: "2.3.0"
---

# Observability Readiness

## Mission

Production failures are inevitable; being unable to diagnose them is not.

Make every service's telemetry surfaces complete enough that a 2am failure can be understood, contained, and explained from existing instrumentation alone. Audit the surfaces, close the gaps, and leave the system diagnosable without a code change.

Instrumentation is product surface. If a failure mode cannot be observed, it will be debugged by guesswork, redeploys, and panic. Treat an unobservable failure mode as a P1 defect, not an operations problem.

Do not audit surfaces you cannot see run. Do not deliver an audit that restates code without checking behavior.

## The 2am test

At 2am, an on-call engineer receives an alert for an unexpected production failure. They have no context, no local reproduction, and no time to add code.

The system passes the 2am test when the engineer can answer questions like:

- Which requests failed, and what were they doing?
- Which tenant, user, region, or deployment is affected?
- Where did the time go, and which hop was responsible?
- Is this an error, a capacity problem, or a dependency problem?
- What changed right before it started?
- Did we page for the right thing?

**Bar:** developers can answer unexpected questions without adding new instrumentation. Any question that requires a code change, a redeploy, or a log pull with no IDs is a gap.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Observability readiness workflow

Run the workflow over each service in scope. Work surface by surface; never summarize a service from a single file.

### 1. Inventory telemetry surfaces

Run `scripts/check_observability.py` against the repository root as a first-pass signal. The script reports which surfaces carry instrumentation (logs, metrics, traces, health, correlation, alerts) and which are missing; `assets/observability-sample/` demonstrates the expected output shape.

Verify:

- every service directory is inventoried, not only the root
- the inventory distinguishes covered, partial, and missing surfaces
- generated, vendored, and test-only files are excluded from coverage claims
- script output is a signal, never a verdict — confirm every hit and every gap in source

### 2. Audit correlation and IDs

Read `references/correlation-ids.md` when checking request and correlation ID design.

Verify:

- every request enters the system with exactly one correlation ID, generated at the first boundary
- the ID propagates across services, queues, retries, and webhooks
- every log line, metric, and span for a request carries the ID
- trace context and correlation ID are both present and consistent

### 3. Audit logs

Read `references/logs.md` when checking logging structure and content.

Verify:

- logs are structured with stable event names and grep-stable messages
- levels are used consistently; errors carry cause, correlation ID, and affected scope
- log volume is sampled where needed; no unbounded per-loop logging
- PII and secrets never reach logs

### 4. Audit metrics

Read `references/metrics-and-slos.md` when checking metrics and SLI/SLO design.

Verify:

- user-visible signals (availability, latency, throughput, errors) are emitted
- metric labels are bounded; cardinality is controlled
- SLIs are defined from user-visible behavior, not internals
- every SLO has an alert that fires before its budget is exhausted

### 5. Audit traces

Read `references/traces-and-profiles.md` when checking traces and profiles.

Verify:

- entry, exit, and dependency calls are spanned with verb-noun names
- spans carry the correlation ID and bounded attributes
- sampling retains error traces; hot paths are rate-limited
- profiles exist or are enabled for latency and memory investigations

### 6. Audit health and SLOs

Read `references/health-and-alerts.md` when checking health endpoints, dashboards, and alert wiring.

Verify:

- liveness and readiness are separate endpoints with correct dependency checks
- graceful degradation is reported, never hidden
- dashboards answer the incident questions, not only present graphs
- every alert has a condition, severity, owner, runbook, and a page-vs-ticket decision

### 7. Audit privacy and cardinality

Re-apply the PII checks from `references/logs.md` and the cardinality checks from `references/metrics-and-slos.md` across every surface.

Verify:

- no PII, tokens, or secrets in logs, traces, metric labels, or profiles
- no unbounded label or attribute values (user IDs, emails, raw URLs)
- debug modes are gated and toggleable without a redeploy
- sampling decisions are explicit and documented per surface

## Correlation contract

Every request that enters the system gets exactly one correlation ID, generated at the first boundary and propagated everywhere the request goes. Every telemetry record produced while serving the request carries the ID. No log line, metric, or span is orphaned.

Do not re-generate an incoming ID. Do not log without the ID. A request whose telemetry cannot be reassembled cannot be diagnosed — that is a P1 gap.

## Health-check contract

Liveness checks the process; readiness checks the ability to serve traffic. They are separate endpoints with separate dependency checks. A service reports its state truthfully, including degraded states, so orchestrators can act and engineers can see the truth.

Never fail readiness on a non-critical dependency. Never report healthy when serving will fail. A health check that lies causes more outages than the one it hides.

## Alerting contract

Every alert is a decision, not a notification. Each alert states the condition, why it matters, the severity, whether it pages or tickets, the owner, and the runbook. Alerts fire on user impact or its leading indicators, never on internal noise. Every SLO has an alert wired to its error budget.

Never page without a runbook. Never alert on something no one is empowered to fix. An untested alert is a gap, not a safeguard.

## Required output

Produce the observability readiness report using `assets/observability-report-template.md`.

The report must contain:

1. **Scope and evidence** — services covered, evidence labels per finding
2. **Surfaces inventory** — per-surface status (covered / partial / gap) per service
3. **Per-surface findings** — what exists, what is missing, and where
4. **Gap list** — every gap with severity (P0–P4), surface, evidence, and remediation
5. **2am test verdict** — the incident questions and how each is answerable today
6. **Remediation order** — recommended fixes in dependency order

Do not emit a score. The report is a gap list and a verdict, not a rating.

## Definition of done

The audit is done when:

- every surface is inventoried per service and findings are grounded in source
- correlation IDs flow from entry to telemetry on every path
- logs are structured, leveled, sampled, and PII-free
- metrics cover user-visible signals with bounded cardinality
- traces and profiles cover the request path with error retention
- health endpoints separate liveness from readiness and report degradation
- SLOs exist with alerts wired before budget exhaustion
- dashboards and alerts have owners, runbooks, and page-vs-ticket decisions
- the report is rendered from `assets/observability-report-template.md`
- every gap carries a severity and an evidence label: Observed, CI-observed, or Estimated

For error semantics, expected-error recovery, and Time to Recovery targets, use the `error-experience` skill if available; the two audits complement each other and do not overlap.
