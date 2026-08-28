# Observability Readiness Report — <service-name>

- Generated: <date>
- Auditor: <agent or human>
- Scope: <repository root / service paths / environments>
- Evidence labels: <Observed | CI-observed | Estimated>, applied per finding

## Executive summary

<One paragraph: overall readiness, the top gaps, and whether the service passes the 2am test.>

## Surfaces inventory

Per service. Status: COVERED | PARTIAL | GAP.

| Service | Logs | Metrics | Traces | Profiles | Health | Correlation IDs | SLIs/SLOs | Dashboards | Alerts | Privacy/PII | Cardinality | Debug modes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| <service> | <status> | <status> | <status> | <status> | <status> | <status> | <status> | <status> | <status> | <status> | <status> | <status> |

## Per-surface findings

### Logs

<What exists and what is missing: structure, event names, levels, sampling, PII redaction, when events are emitted.>

### Metrics

<Signals emitted, golden signals covered, label cardinality, bucket and aggregation design.>

### Traces

<Span coverage, instrumentation points, sampling policy, error retention, attribute cardinality.>

### Profiles

<Profiling availability for latency and memory investigations, on-demand vs always-on.>

### Health checks

<Liveness/readiness separation, dependency checks with timeouts, degradation reporting.>

### Correlation and request IDs

<Generation boundary, propagation across services and queues, logging placement, trace context.>

### SLIs and SLOs

<SLI definitions with success criteria and denominators, targets, error budgets, budget alerts.>

### Dashboards

<Which incident questions each dashboard answers, pane coverage, runbook links.>

### Alerts

<Page-vs-ticket decisions, condition, severity, owner, runbook, test status per alert.>

### Privacy and PII

<Redaction allowlists, secret exposure, debug-mode gating.>

### Cardinality and sampling

<Label bounds per metric, sampling decisions per surface, retention risk.>

## Gap list

| Gap | Severity | Surface | Evidence | Remediation |
|---|---|---|---|---|
| <gap description> | <P0\|P1\|P2\|P3\|P4> | <surface> | <Observed\|CI-observed\|Estimated> | <fix, owner> |

## 2am test verdict

For each incident question an operator might ask:

- <question> — answered by <surface(s) and how>, or UNANSWERED
- <question> — <answer or UNANSWERED>

**Verdict:** <PASS | PARTIAL | FAIL> — <one-line justification>

## Recommended remediation order

1. <gap> — <why this first>
2. <gap> — <dependency or risk reasoning>

## Definition of done

- [ ] Every surface inventoried per service with grounded findings
- [ ] Correlation IDs verified end to end on three example requests (happy path, error, retry)
- [ ] Logs structured, leveled, sampled, and PII-free
- [ ] Metrics cover user-visible signals with bounded cardinality
- [ ] Traces and profiles cover the request path with error retention
- [ ] Health endpoints separate liveness from readiness and report degradation
- [ ] SLOs exist with alerts wired before budget exhaustion
- [ ] Dashboards and alerts have owners, runbooks, and page-vs-ticket decisions
- [ ] Every gap carries a severity and an evidence label
