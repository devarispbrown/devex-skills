---
name: operational-trust
description: Build consumer trust in operations: status page, incident communication, maintenance windows, SLA and SLO publication, incident history, webhook delivery guarantees, retry behavior, and degraded-state signaling so users can quickly tell whether it is you or them. For product instrumentation use observability-readiness; for announcing changes use change-awareness.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and operational runbooks.
metadata:
  version: "2.9.4"
---

# Operational Trust

## Mission

Users trust an operation they can see. Build the consumer-facing trust surface — status page, incident communication, maintenance windows, SLA and SLO publication, incident history, webhook delivery guarantees, retry behavior, and degraded-state signaling — so that during any failure or maintenance a user can quickly tell whether it is you or them, and what to do next.

Treat the trust surface as a contract. Audit what is published, what is implied, and what is missing, then close the gaps before they are discovered under incident load. A file that exists but is not wired into the live path is a gap, not an asset.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Run `scripts/check_trust_surface.py` against the repository as a first-pass inventory. The script only informs; it never renders a verdict.

For product instrumentation, use the `observability-readiness` skill. For announcing changes, use the `change-awareness` skill. This skill owns the consumer-facing trust surface and does not replace either.

## Trust surface audit

Audit in order. Every step produces entries for the trust report in `assets/trust-audit-template.md`. Label every claim with an evidence type: Observed, CI-observed, or Estimated. An estimate never proves a PASS.

### 1. Inventory the trust surface

Run `scripts/check_trust_surface.py [root]` and record the checklist: status page config, incident templates, SLO/SLA docs, webhook retry logic, degraded-state handling.

For each artifact found, confirm it is the live source of truth. The scanner is heuristic: verify each hit semantically and search for artifacts it cannot name.

### 2. Audit the status page

Read `references/status-page-patterns.md`.

Verify:

- components reflect real, independently failing surfaces
- degraded states use the canonical vocabulary, never euphemisms
- update cadence meets the no-news-is-bad-news rule
- maintenance windows are scheduled, announced in advance, and stated with impact
- the status page is linked from docs, error pages, and SDKs
- incident history is public and machine-readable

### 3. Audit incident communication

Read `references/incident-communication.md`.

Verify:

- templates exist for initial, update, and resolution communications
- the first update lands within the `TTR_TARGET_MIN` window of confirmed impact
- updates follow a stated cadence until resolution; silence is failure
- postmortems are blameless, public, and produce owned action items
- communication reaches users on the channels they already use

### 4. Audit SLA and SLO publication

Read `references/slo-publication.md`.

Verify:

- every published number is measured on the stated window from production telemetry
- SLA (contractual) and SLO (commitment) are never conflated
- no aspirational or unmeasured number is published as fact
- current attainment is shown alongside the target, with carve-outs stated

### 5. Audit webhook delivery guarantees

Read `references/webhook-reliability.md`.

Verify:

- the delivery guarantee is documented in exact terms: at-least-once, at-most-once, ordering
- retry behavior is bounded: max attempts, exponential backoff with jitter, retry-after
- events carry stable IDs and idempotency guidance; consumers can deduplicate
- signatures, timeouts, rate limits, dead-letter behavior, and replay are documented

### 6. Audit degraded-state signaling

Read `references/degraded-states.md`.

Verify:

- degraded behavior is signaled explicitly; a degraded mode that looks like success is a trust defect
- errors distinguish client (4xx) from provider (5xx) with stable codes and correlation IDs
- fallbacks, circuit breakers, and quotas produce documented, readable outcomes
- a user can tell whether it is you or them within one minute of the error

### 7. Assess recovery time

For the three most likely expected errors users hit, confirm each has cause, corrective action, and retry-safety guidance. Time to recovery follows the `TTR_TARGET_MIN` target: 5 minutes from hitting the error to completing the corrective action; >10 minutes is a P2 defect.

### 8. Render the trust report

Fill `assets/trust-audit-template.md`: posture, evidence, checklist, gap analysis with severity, recovery assessment, fix backlog. State the posture explicitly — TRUSTED, PASS WITH DEBT, or BROKEN. Never leave the report as an implied conclusion.

## Status page contract

A status page is the first thing a user checks during an incident. It must be:

- reachable and fast even when the product is down, on separate hosting
- truthful: driven by automated checks, with manual overrides logged
- granular: components that fail independently are listed independently
- honest about degraded states: degraded performance, partial outage, major outage, maintenance
- current: no stale "all systems operational" while an incident is open
- historical: past incidents remain public and inspectable
- linked: docs, dashboards, and error pages point to it

## Incident communication contract

Incident communication must:

- start within the `TTR_TARGET_MIN` window of first confirmed impact
- state what is affected, what users should do, and when the next update arrives
- update on a regular cadence until resolution; silence is a trust failure
- treat the status page as the canonical record and push summaries to user channels
- end with a public postmortem containing timeline, impact, root cause, and owned action items
- be blameless: name systems and fixes, not people

## SLO publication contract

Published reliability numbers must:

- be measured on a stated window from real production telemetry
- distinguish SLA (contractual, with consequences) from SLO (internal commitment)
- show current attainment alongside the target
- state carve-outs and excluded dependencies explicitly
- change only through a defined review process, never through quiet edits

## Webhook delivery contract

Documented webhook behavior must state:

- the delivery guarantee in exact terms: at-least-once, at-most-once, or ordered
- retry policy: maximum attempts, exponential backoff with jitter, retry-after
- event identity: stable event IDs and idempotency guidance for consumers
- authentication and signature verification, with rotation documented
- timeouts, rate limits, and the fate of undeliverable events: dead letter, replay
- a test or probe endpoint consumers can verify against

## Degraded-state contract

Degraded behavior must be signaled explicitly:

- partial results, fallbacks, and stale data are marked, never silent
- API responses use stable error codes and a 4xx/5xx taxonomy so users can tell client error from provider error
- responses carry correlation IDs users can quote to support
- circuit breakers, feature flags, and quotas produce documented, readable outcomes
- a degraded mode that looks identical to a success is a trust defect

## Required output

For every trust surface audit, produce the trust report using `assets/trust-audit-template.md`.

The report must contain:

1. **Posture** — exactly one of TRUSTED / PASS WITH DEBT / BROKEN
2. **Evidence** — repository, environment, checks executed and not executed, evidence labels
3. **Checklist** — per-surface inventory with present/missing and gap classification
4. **Gap analysis** — each gap with severity, user impact, and acceptance test
5. **Recovery assessment** — TTR result for the three most likely expected errors, keyed to `TTR_TARGET_MIN`
6. **Fix backlog** — prioritized items with owners and verification steps

## Definition of done

A trust surface audit is done when:

- every surface is inventoried by the scanner and confirmed against the live path
- every contract item above is verified or recorded as a gap with severity
- every published number is measured, and no unmeasured number is published as fact
- webhook guarantees are documented exactly, with retries bounded and idempotency covered
- degraded states are explicit, and errors let users tell whether it is you or them
- recovery guidance for the most likely expected errors meets `TTR_TARGET_MIN`
- the report is rendered from `assets/trust-audit-template.md` with labeled evidence
- no gap is hidden by a heuristic, an assumption, or a stale file

Hand off internal instrumentation to `observability-readiness` and change announcements to `change-awareness`. This skill gates the consumer-facing trust surface; it does not replace either.
