---
name: developer-onboarding
description: Design zero-to-value onboarding where a brand-new developer reaches verified end-to-end product value in 15 minutes or less: canonical quickstart design, install-mode selection, aggressive step elimination, sandbox credentials, and seeded fixtures. Use for design and architecture of the getting-started path, not its validation. To time or audit an existing path use developer-experience-auditor; for documentation of the path use developer-docs.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and product/design context.
metadata:
  version: "2.7.0"
---

# Developer Onboarding Design

## Mission

Design onboarding systems that take a brand-new developer with zero product knowledge from first contact to independently verified end-to-end product value within `MAGIC_PATH_MAX_MIN`.

This skill owns the **design** of the zero-to-value path: it defines the value outcome, chooses the install mode, eliminates steps, designs auth and configuration, and produces a plan with an owner and an estimate per step.

It does not validate or time an existing path — that is the `developer-docs-auditor` skill's job if available. It does not write the quickstart documentation — that is the `developer-docs` skill's job if available. Deliver a design good enough that both can act on it without redesign.

Design against the timer from the first minute. Every step, command, prompt, and credential in the path is a liability against the budget. The plan is a design with an estimate and an owner, not a wish list.

## Non-negotiable: 15-minute magic path gate

Every external-facing product must have exactly one canonical route by which a brand-new developer reaches and verifies meaningful end-to-end product value within `MAGIC_PATH_MAX_MIN`. Design for the gate; never around it.

**Timer definition.** Start: the developer opens the canonical quickstart. Stop: the developer independently verifies the core product outcome. The timer includes installation, signup/account creation when required, obtaining sandbox credentials, authentication, product-specific configuration, resource creation, execution, waiting, and verification. Recovery from expected errors counts.

Do not move product setup into "prerequisites." Do not hide signup, credentials, or provisioning behind a support contact or an approval step. General machine bootstrap, such as a supported language runtime, may be a platform prerequisite; product CLIs, agents, containers, services, credentials, and configuration belong inside the budget.

**Bands.** ≤5 minutes exceptional; >5 to ≤10 minutes strong; >10 to ≤15 minutes pass; over the limit is a `BROKEN_QUICKSTART` P1 gate failure. No reproducible end-to-end quickstart: `BROKEN_QUICKSTART`. Manual approval/support required with no sandbox route: `BROKEN_QUICKSTART`.

**Evidence labels.** Design estimates are `Estimated` until someone executes the path. Label every timing Observed, CI-observed, or Estimated. An estimate never proves the gate passes; it flags risk. When the path ships, the `developer-docs-auditor` skill if available must time it from a clean environment.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Onboarding design workflow

### 1. Define the value outcome

Choose the smallest end-to-end outcome that still makes the product's core value obvious. Installation, authentication, or a health check is not success.

Specify:

- the benchmark persona: zero product knowledge, no account, no credentials, no sample data
- the start condition: opening the canonical quickstart
- the stop condition: a result the developer can independently verify
- the observable proof: a message sent, a resource created, a request answered, a workflow completed

Never design toward "CLI installed and help prints." Design toward "CLI installed, workflow ran, output verified."

Read `references/magic-path-design.md` when choosing the canonical route and its default choices.

### 2. Choose the install mode

Pick exactly one canonical install path for the primary platform, and make it the only route presented before first success.

Evaluate brew formula, npm package, `go install`, docker image, `npx`, and curl-script against platform coverage, upgrade story, and timer fit. The chosen mode's install, auth, configure, execute, and verify time all sit inside the magic-path timer.

Read `references/install-modes.md` when comparing install modes.

### 3. Eliminate steps

For every step in the path, ask: **why does the developer have to do this step at all?**

Apply the elimination playbook before adding anything: defaults over prompts, `--token` over signup, seeded fixtures over manual resource creation, project templates over scaffold-from-blank, and merging login + create + deploy into one command where the product permits.

Do not accept a step because it is "how the product works today." Surface the product change required to remove it.

Read `references/step-elimination.md` when trimming the step list.

### 4. Design auth and configuration

Make authentication and configuration the shortest segment, not the longest.

Prefer sandbox-first credentials: a test mode, a starter token, a seeded fixture, or an ephemeral sandbox account over production signup. Prefer zero configuration: sane defaults, a single generated config file, or configuration inferred from the auth step.

Never require a credit card, an approval, or production data access before first success. Label every credential the developer must create or find; stay within `MAGIC_PATH_MAX_CREDENTIALS`.

### 5. Script first success

Make every command complete and copy-pasteable. No ellipses, no "you should already have", no prose in the middle of a block.

Define the expected observable output after each transition: version after install, token cached after auth, resource id or URL after execute, verified value at the end. If a command can fail on a common machine, put the recovery inline before the next step.

Keep the number of interactive commands within `MAGIC_PATH_MAX_COMMANDS` and context switches within `MAGIC_PATH_MAX_CONTEXT_SWITCHES`.

### 6. Design recovery

Design the three most likely failures and their corrective actions before writing the happy path.

For each expected failure, define what happened, why, where it occurred, how to fix it, and whether retrying is safe. Target recovery inside `TTR_TARGET_MIN`. "Contact support" is not a recovery path.

Failures you cannot design around become blockers attributed to Docs, Product/DX, Infrastructure, or External dependency — record them, do not hide them.

### 7. Production handoff

Put production hardening, advanced configuration, and concepts after first success, as one link, not a wall.

Design the post-success surfaces: how the developer moves to production credentials, real resources, scale, and operations. If a containerized development environment is under consideration, it is an accelerator, never a requirement of the magic path.

Read `references/onboarding-architecture.md` when designing the onboarding system end to end — samples, templates, support, and telemetry.

Read `references/devcontainers.md` when a devcontainer for the path is under consideration.

### 8. Estimate and hand off

Turn the plan into JSON and run `scripts/estimate_magic_path.py` against it. The estimator sums per-segment seconds, compares the total with `MAGIC_PATH_MAX_MIN`, and flags command, credential, and context-switch counts over their targets.

If the estimate exceeds the budget, cut steps or propose product changes — do not relabel the estimate as a pass.

Hand off the plan with a named owner per step and the evidence label `Estimated` attached to every timing. Note which steps require the auditor to verify by execution.

## Onboarding plan contract

The onboarding plan is the deliverable artifact. It must specify:

1. the value outcome with benchmark persona, start, stop, and observable proof
2. exactly one canonical route; all alternatives are post-success links
3. the step list: step, segment, estimated seconds, commands, credentials, context switches, and owner
4. the install mode and the rationale for choosing it
5. the auth and configuration design: sandbox-first credentials, defaults, seeded fixtures
6. estimated per-segment totals vs `MAGIC_PATH_MAX_MIN`, labeled `Estimated`
7. the failure recovery table: symptom, cause, fix, retry safety
8. the production handoff: one post-success link and the next steps
9. open blockers attributed to Docs, Product/DX, Infrastructure, or External dependency

Use `assets/onboarding-plan-template.md` as the starting structure, and keep the JSON step plan in sync with it. Use `assets/magic-path-plan.example.json` as the schema reference.

## Required output

The onboarding plan, covering at minimum:

- the value outcome and its verification
- the canonical route, with exactly one install mode
- the step list with an owner per step
- estimated segments vs `MAGIC_PATH_MAX_MIN`, labeled `Estimated`
- recovery table and production handoff

When the plan changes, re-run `scripts/estimate_magic_path.py` and report the new totals.

## Definition of done

The onboarding plan is done when:

- a brand-new developer can reach verified end-to-end value within `MAGIC_PATH_MAX_MIN` by the estimate, and the estimate is labeled and queued for real timing
- the value outcome is meaningful, not installation or a health check
- exactly one canonical route exists; no parallel getting-started routes
- every step has an owner, a segment, and an estimate
- install mode, auth, and configuration are designed, not assumed
- step elimination was applied and the elimination rationale is recorded
- expected failures have inline recovery within `TTR_TARGET_MIN`
- command, credential, and context-switch counts meet their targets
- the estimator passes and the JSON plan matches the written plan
- production hardening is a post-success handoff, not a prerequisite
- product changes required to meet the gate are surfaced, not documented around
