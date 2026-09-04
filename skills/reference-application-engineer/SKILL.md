---
name: reference-application-engineer
description: Build production-grade reference applications: minimal, production, multi-tenant, event-driven, high-throughput, serverless, and Kubernetes variants demonstrating auth, config, errors, retries, observability, testing, deployment, shutdown, and security. For the zero-to-value onboarding path use developer-onboarding; for generating starter projects use golden-path-scaffolder.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and build/test tooling.
metadata:
  version: "2.9.4"
---

# Reference Application Engineer

## Mission

A reference application is the strongest example a product can ship: a complete, runnable system that demonstrates production-grade behavior — auth, config, errors, retries, observability, testing, deployment, shutdown, and security — in one tree a developer can read in a sitting and run in minutes.

It is not a demo. A demo shows the happy path; a reference application models production behavior, including failure. Every claim in docs, tutorials, and SDK examples is anchored in these trees, so an example that cannot be traced to a reference application is unverified.

One artifact, three readers: humans learning the product, coding agents using the product, and operations teams modeling deployment. If any of the three cannot run it end-to-end, the reference application is broken.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Design the learning path against the Magic path thresholds and the local development loop against the Local development thresholds in `metrics.md`.

Use the `developer-onboarding` skill for the zero-to-value onboarding path and `golden-path-scaffolder` for generating starter projects. Reference applications are the evidence those skills build on; they are not onboarding content or generated boilerplate.

## Reference application architecture

Build every reference application through the fixed sequence below. Each step has a read, a verify, and a deliverable.

### 1. Select the variant

Read `references/variant-taxonomy.md`.

Map the intended audience and lesson to exactly one variant: minimal, production, multi-tenant, event-driven, high-throughput, serverless, or Kubernetes.

Verify:

- the variant is one of the seven in the variant matrix, chosen for a stated audience and lesson
- the minimal variant is the default for first-value learning; the production variant is the default for customers and operations teams
- a multi-variant suite shares one core and applies overlays; it never forks the core
- the variant's stress point (tenancy, delivery, throughput, platform lifecycle) is stated

### 2. Enumerate the nine mandatory concerns

Read `references/production-readiness-checklist.md`.

Every reference application demonstrates all nine mandatory concerns: auth, config, errors, retries, observability, testing, deployment, shutdown, and security. Variants change how a concern is wired, never whether it exists.

Run `scripts/check_reference_app.py <tree>` as the first-pass coverage signal. The checker confirms evidence of wiring, not quality; semantic review of every concern is still required.

Verify:

- each of the nine concerns maps to at least one file or artifact in the tree
- the checklist entry for each concern records the evidence file and what it demonstrates
- a missing concern is treated as a defect and reported by name, never silently waived

### 3. Wire the cross-cutting concerns

Read `references/cross-cutting-concerns.md`.

Wire auth, config, errors, retries, and observability with the minimal viable patterns from the reference: auth fails closed, config reads the environment with safe defaults, errors carry status and remediation, retries are bounded with backoff, and observability exports logs plus metrics or traces.

Verify:

- secrets are read from the environment at runtime, never hardcoded in the tree
- every config default is safe for a fresh clone; no credential is required to start
- errors expose status, message, and recovery guidance without leaking internals
- retry loops are bounded, logged, and idempotency-safe; there is no unbounded retry
- observability setup exports somewhere observable, not only to a console print

### 4. Design the run path

Design the demo path: from clean clone to verified value in one command sequence, with expected output shown. Budget the learning path against the Magic path thresholds and the local loop against the Local development thresholds in `metrics.md`.

Verify:

- a clean clone reaches running tests and a running app within `LOCAL_DEV_MAX_MIN` using only committed instructions
- the quickstart outcome fits `MAGIC_PATH_MAX_MIN`; commands are copy-pasteable and show expected output
- sample data and credentials are supplied or created by the path, never assumed
- production hardening sits behind first success, not in front of it

### 5. Write tests that match failure modes

Tests prove the reference application behaves as documented, including when things go wrong.

Verify:

- unit tests cover auth denial, error mapping, and bounded retries, not only the happy path
- integration tests exercise the run path for the variant: HTTP request, event delivery, tenant isolation
- the suite runs from a clean clone with committed automation
- test strategy follows the variant's failure modes per the suite standards

### 6. Add deployment and operations artifacts

Read `references/deployment-matrix.md`.

Every variant ships a deployable artifact definition matching the variant, plus a health check and a config delivery path.

Verify:

- the deployment artifact matches the variant's row in the deployment matrix
- health, config, and logs/metrics are reachable after deploy per the matrix
- the artifact contains no secrets and no machine-specific values

### 7. Implement shutdown and security defaults

Read `references/shutdown-and-security.md`.

Production variants handle termination: a signal handler that stops accepting work, drains in-flight work, closes clients with bounded timeouts, and exits non-zero on failure. Examples ship security defaults: auth on by default, secrets via config only, no secret logging, sanitized error output.

Verify:

- termination is graceful: drain before exit, bounded timeouts, idempotent close
- serverless variants rely on the platform lifecycle and state that in the README; they do not fake a signal handler
- examples never hardcode secrets or encourage unsafe credential handling
- secure defaults are on unless a documented, deliberate override exists

### 8. Verify the tree

Run the full verification loop before shipping.

Verify:

- `scripts/check_reference_app.py <tree>` exits 0 with all nine concerns evidenced
- tests pass from a clean clone
- the app runs and the documented outcome is produced
- every command in the README is executed, not estimated
- the coverage report from `assets/reference-app-checklist.md` is filled in

## Reference application contract

- A reference application is complete, runnable, and honest: it demonstrates all nine mandatory concerns from `references/production-readiness-checklist.md` and admits what it stubs.
- It has one canonical run path; the README reproduces it from a clean clone.
- It is product-generic where possible; product-specific steps are isolated, documented, and justified.
- Secrets never appear in the tree; gitignored env files carry placeholder values in examples only.
- The tree is small enough to read in one sitting; depth is earned, not accumulated.
- A claim in docs or tutorials that cannot be traced to the reference application is unverified.

## Example code contract

- Every example in docs, tutorials, and SDKs is traceable to a reference application; no invented endpoints, fields, status codes, or behavior.
- Example code is complete and copy-pasteable, with expected output shown.
- Comments state contracts, invariants, and error semantics; they never restate syntax.
- When docs and the reference application disagree, that is a P1 defect; report it, do not hide it.

## Variant contract

- One variant per lesson; a suite of variants shares a core and adds overlays.
- Every variant carries all nine mandatory concerns; the variant's stress point (tenancy, delivery, throughput, platform lifecycle) determines how they are wired.
- Read `references/variant-taxonomy.md` before selecting or adding a variant.

## Required output

For every reference application, produce the coverage report using `assets/reference-app-checklist.md`.

The report must contain:

1. **Variant** — the selected variant and its audience/lesson rationale.
2. **Concern evidence** — all nine mandatory concerns with the evidence file and what each demonstrates; the checker output is attached.
3. **Run path** — the exact commands from clean clone to verified outcome, with expected output.
4. **Verification** — test results, checker exit code, and whether the run was observed or estimated.
5. **Known gaps** — anything stubbed or deferred, with severity.

## Definition of done

A reference application is done when:

- the checker exits 0 and all nine mandatory concerns carry evidence
- a clean clone reaches running tests and a running app within `LOCAL_DEV_MAX_MIN` from the Local development thresholds
- the quickstart fits `MAGIC_PATH_MAX_MIN` from the Magic path thresholds
- tests cover failure modes, not only the happy path
- the deployment artifact matches the variant's row in the deployment matrix
- graceful termination is wired and verified for production variants; serverless variants state platform-managed lifecycle
- no secret, personal config, or machine-specific value appears in the tree
- every doc and tutorial example is traceable to the tree; nothing is invented
- the coverage report is rendered from `assets/reference-app-checklist.md` with evidence labels
