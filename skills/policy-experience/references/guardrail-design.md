# Guardrail Design

A guardrail is the enforcement point of a rule: a deterministic check at a fixed checkpoint that blocks, warns, or advises, and records its result.

## Placement

Attach each rule to the earliest checkpoint where the violation is actionable (see the wiring-point table in `policy-as-code.md`). Placement rules:

- prefer pre-deploy checkpoints over post-deploy discovery
- a rule discovered at release time is a rule wired too late
- runtime guardrails are for safety-critical rules and rate-of-change alarms, not for relocating CI

## Blocking semantics

- P0/P1 rules block: no PASS WITH DEBT for them without an approved exception
- P2 rules warn with a deadline and escalate when it passes
- P3/P4 rules advise and feed the backlog
- pre-deploy guardrails default to blocking; runtime guardrails default to log-and-alert

A guardrail's verdict uses the suite vocabulary: PASS / PASS WITH DEBT / FAIL / UNVERIFIED, defined in `references/standards.md`.

## Guardrail anatomy

Each guardrail records:

- `guardrail_id` and the `policy_id` it enforces
- `checkpoint` — where it runs
- `blocking` — true/false and the severity basis
- `message_builder` — produces the violation message (see `violation-actionability.md`)
- `evidence` — what was checked, against what input, with what result

## Failure clarity

The guardrail message is the developer's only context at failure time. Use the violation message standard; never emit "policy check failed". If the failure cannot be explained, the guardrail is a bug: severity P1, fix the message builder before the check.

## No silent failures

Every run records a result and evidence:

- **PASS** — check ran and passed
- **FAIL** — check ran and a violation was produced
- **UNVERIFIED** — the guardrail could not run; never report PASS on a skipped check

A guardrail that cannot run in a clean checkout contributes to `NON_REPRODUCIBLE_BUILD`. An expected failure without cause, fix, and retry guidance triggers `UNEXPLAINED_ERROR`.

## Bypass resistance

- guardrail configuration changes go through the same PR flow as code
- disabling a guardrail is a policy change: reviewed, recorded, and reversible
- ad-hoc bypass (skip flags, disable switches) is a P1 finding
