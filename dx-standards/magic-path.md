# 15-Minute Magic Path Standard

## Hard product/documentation objective

A brand-new developer with zero product knowledge must be able to complete the product's canonical end-to-end value path in **15 minutes or less**.

This is not a prose-quality aspiration. It is an acceptance criterion for onboarding and developer experience.

## Benchmark persona

Assume the developer has:

- a supported operating system
- a terminal and browser
- normal network access
- the language runtime/package manager explicitly listed as a platform prerequisite
- general software-development competence

Assume they do **not** have:

- prior product knowledge
- a product account unless one is unavoidable
- product credentials or tokens
- product-specific configuration
- sample data/resources unless the quickstart creates or supplies them
- knowledge of internal terminology

Do not hide product-specific setup in "prerequisites" to game the benchmark.

## Timer definition

**Start:** the developer opens the canonical Quickstart/Get Started path.

**Stop:** the developer has completed the product's core end-to-end workflow and can independently verify a meaningful successful result.

Count wall-clock time for:

- product installation
- signup/account creation when required
- obtaining test/sandbox credentials
- authentication
- product-specific configuration
- creating required product resources
- executing the core workflow
- waiting for synchronous/asynchronous completion
- verifying the output/result

External approval, support intervention, allowlisting, sales contact, manual provisioning, or long-running external dependencies count against the timer unless the product offers a sandbox/test path that removes them.

General machine bootstrap such as installing a supported language runtime may be declared as a platform prerequisite, but product-specific CLIs, agents, plugins, containers, services, credentials, and configuration belong inside the magic-path budget.

## Required characteristics

The canonical magic path must:

1. Have exactly one recommended default route.
2. State prerequisites before step 1.
3. Avoid architecture explanation until after first success unless required to act safely.
4. Use a sandbox, test mode, local mode, or seeded fixture when production setup would exceed the budget.
5. Use copy-pasteable commands and complete examples.
6. Minimize choices and optional branches.
7. Show expected output or a concrete verification step after important transitions.
8. Include the three most likely failure recoveries inline or immediately adjacent.
9. End with a meaningful product outcome, not merely installation or a health check.
10. Point to production hardening and deeper concepts only after the user has succeeded.

## Outcome quality

Installation is not magic-path completion.

Good outcomes demonstrate the product's core value. Examples:

- send and observe a real test message
- ingest data and query/consume it downstream
- deploy an application and make a successful request
- create a workflow and observe successful execution
- call an API and see the resulting resource/state transition
- run an agent/task and inspect the useful output

Choose the smallest end-to-end outcome that still makes the product's value obvious.

## Pass/fail bands

- **≤5 min:** exceptional
- **>5 to ≤10 min:** strong
- **>10 to ≤15 min:** pass
- **>15 min:** fail, P1 onboarding/DX defect
- **No reproducible end-to-end quickstart:** fail, P1
- **Requires manual approval/support with no sandbox path:** fail, P1

A documentation system that fails the magic-path gate cannot be rated world-class regardless of its aggregate documentation score.

## Measurement modes

Always label the evidence:

- **Observed:** actually executed from a clean or representative environment and timed.
- **CI-observed:** executed in automation; useful for drift but may understate human reading/signup time.
- **Estimated:** reasoned from steps without execution. Never present an estimate as proof of passing the gate.

For release gating, prefer observed evidence periodically and CI-observed evidence on every relevant change.

## Diagnostic breakdown

When the path exceeds 15 minutes, attribute time to:

| Segment | Examples |
|---|---|
| Orientation | finding the right quickstart, understanding the outcome |
| Install | package, CLI, agent, container, dependency setup |
| Account/Auth | signup, login, keys, OAuth, permissions |
| Configure | env vars, files, resources, project setup |
| Execute | command/code/workflow execution |
| Wait | provisioning, build, deploy, async processing |
| Verify | confirming the intended outcome |
| Recovery | errors, ambiguous output, backtracking |

Classify the root cause as **Docs**, **Product/DX**, **Infrastructure**, or **External dependency**. Do not blame documentation for product friction that documentation cannot remove.

## Quickstart budget design

A useful planning budget is:

- orientation: ≤1 minute
- install: ≤2 minutes
- account/auth: ≤3 minutes
- minimal config: ≤3 minutes
- execute: ≤3 minutes
- verify: ≤1 minute
- buffer/recovery: ≥2 minutes

This is guidance, not a requirement per segment. The only hard aggregate requirement is ≤15 minutes.
