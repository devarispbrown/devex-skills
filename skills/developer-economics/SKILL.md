---
name: developer-economics
description: Treat pricing, limits, and quotas as API behavior: rate limits, usage meters, billing events, overages, free tier, spend caps, and cost estimation before deploy, with usage, quota, and estimate commands that make cost predictable. For production usage observability use observability-readiness.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and billing/usage data.
metadata:
  version: "2.5.1"
---

# Developer Economics

## Mission

Pricing, limits, and quotas are API behavior, not back-office configuration. Every metered surface — rate limit, usage meter, billing event, overage, free tier, spend cap — is a product surface that developers must be able to see, predict, and act on.

Cost must be predictable before deploy. A developer should never discover the bill after the fact.

Design, implement, and audit the economic surface: rate limits with standard headers, quotas with used/limit/reset/estimated_cost visibility, estimate commands that price a workload before it runs, spend caps that stop the bleed, and a free tier with a clean upgrade path.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read `references/rate-limit-design.md` when designing, implementing, or reviewing rate limit behavior.

Read `references/quota-and-metering.md` when designing quota and usage visibility.

Read `references/cost-estimation.md` when designing cost estimation before deploy.

Read `references/spend-controls.md` when designing spend caps, alerts, and overage behavior.

Read `references/free-tier-design.md` when designing, changing, or reviewing a free tier.

## Pricing as API behavior

Treat every pricing, limit, and quota decision as a public interface decision with the same rigor as a response shape. The economic surface ships with the code, is documented, observable, and testable, and never surprises developers with an invoice.

### 1. Inventory the metered surface

Enumerate every surface that consumes or constrains usage:

- endpoints and commands with rate limits, quotas, or usage meters
- token, compute, request, storage, and seat meters with their pricing units
- billing events emitted on usage, upgrade, downgrade, and overage
- free tier limits and the upgrade path
- spend caps, alerts, and enforcement behavior

For each surface record: name, kind (endpoint, command, meter, billing event), quota visibility, and cost estimation status.

Build a surface manifest from implementation, OpenAPI, `--help` output, and billing/usage data, then run `scripts/check_quota_surface.py` against it to flag surfaces missing quota visibility or cost estimation. Use the manifest shape in `assets/quota-example.clean.json`. The script output is heuristic; semantic review of every flagged surface is still required.

### 2. Design rate limits as API behavior

Read `references/rate-limit-design.md`.

Verify:

- limits are returned in standard headers and documented
- Retry-After is present on every 429 response
- burst vs sustained limits are distinguished and both are visible
- clients can compute remaining budget from the response, not from prose
- limit changes are versioned or announced like any behavior change

### 3. Make quotas and usage visible

Read `references/quota-and-metering.md`.

Verify:

- responses expose used, limit, and reset for every metered resource
- estimated cost is exposed where per-use pricing applies
- a usage/quota command exists for every metered surface
- meter semantics (unit, window, reset, counting rules) are documented
- quota exhaustion has a documented, actionable error

### 4. Estimate cost before deploy

Read `references/cost-estimation.md`.

Verify:

- an estimate command prices a workload before it runs
- per-unit prices are explicit and machine-readable where possible
- the estimate covers the full run, not the first call
- confidence/error bounds are stated where material
- surprise-invoice risk is assessed per surface

### 5. Design spend controls

Read `references/spend-controls.md`.

Verify:

- spend caps exist for metered surfaces that can run unbounded
- alerts fire before the cap, not after
- hard limits are enforced server-side, never client-side only
- overage behavior is defined, documented, and billed predictably
- cap changes are communicated as behavior changes

### 6. Design the free tier

Read `references/free-tier-design.md`.

Verify:

- the free tier's what, limits, and upgrade path are explicit
- free limits are visible in the same surfaces as paid limits
- upgrade is a documented self-serve path, not a sales funnel
- abuse protection exists without degrading the legitimate experience
- downgrade behavior is defined

### 7. Audit the economic surface

Run `scripts/check_quota_surface.py` on the manifest and review every flag with evidence. For each surface record the finding, severity, and required change. Produce the report from `assets/economics-audit-template.md`.

Label all evidence as Observed, CI-observed, or Estimated. An estimate never proves a PASS.

## Rate limit contract

Every rate-limited surface must:

1. return limit, remaining, and reset in standard headers
2. return Retry-After with a concrete value on every 429
3. document burst vs sustained limits when both apply
4. document the limit per (key, window) with units and counting rules
5. treat a limit change as a behavior change: versioned or announced

## Quota and meter contract

Every metered resource must expose used, limit, reset, and estimated cost where per-use pricing applies, via response fields or a usage command. Meter semantics must be documented: unit, window, reset time, and counting rules. Exhaustion must produce a documented, actionable error, never a silent degradation.

## Cost estimation contract

Before any deploy that consumes metered resources, an estimate must exist that prices the full run with explicit per-unit prices and stated bounds. A deploy without an estimate is a risk change, not a routine change.

## Spend control contract

Metered surfaces that can run unbounded must have a spend cap, an alert before the cap, and server-side enforcement. Overage behavior must be defined and billed predictably. Client-side checks are supplementary, never the enforcement.

## Free tier contract

The free tier must state what is free, the exact limits, and the upgrade path, with limits visible in the same surfaces as paid limits. Free tier changes are behavior changes.

## Required output

For every economics design or audit task, produce the economics report using `assets/economics-audit-template.md`.

The report must contain:

1. **Surface inventory** — every metered surface with kind, quota visibility, and cost estimation status
2. **Checker results** — `scripts/check_quota_surface.py` output and exit code, or why it was not run
3. **Findings** — per-surface gaps keyed by name, with severity and evidence label
4. **Design review** — rate limit, quota, cost estimation, spend control, and free tier verdicts
5. **Estimated deploy cost** — the pre-deploy estimate with per-unit prices and bounds
6. **Gate results** — per-surface PASS / FAIL / UNVERIFIED, never score-averaged

## Definition of done

Developer economics work is done when:

- every metered surface is inventoried and categorized
- quota visibility and cost estimation are present on every metered surface
- rate limits follow the header and Retry-After contract
- an estimate exists before any metered deploy
- spend caps and alerts are server-side enforced where surfaces can run unbounded
- the free tier states what, limits, and upgrade path
- `scripts/check_quota_surface.py` exits 0 on the manifest, or every remaining flag has a severity and an owner
- the report is rendered from `assets/economics-audit-template.md` with labeled evidence
- no finding is hidden by a score, a heuristic, or an assumption

Hand off production usage observability to the `observability-readiness` skill by name. Developer Economics makes cost predictable; it does not replace runtime observability.
