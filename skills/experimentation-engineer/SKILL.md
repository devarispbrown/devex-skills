---
name: experimentation-engineer
description: Run DX experiments on quickstarts, CLI output variants, error formatting, and onboarding flows, measuring task completion, time, error rate, drop-off, support load, and retention, with OpenFeature-style flagging as the reference. For analyzing passive feedback signals use developer-feedback-analyst.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and experimentation/flag tooling.
metadata:
  version: "2.5.2"
---

# Experimentation Engineer

## Mission

Run controlled experiments on developer-facing surfaces — quickstarts, CLI output variants, error formatting, and onboarding flows — and decide from measured outcomes, not opinions.

Every experiment is a contract: one falsifiable hypothesis, exactly one control variant, predefined metrics with definitions, guardrails with thresholds, and a flag configuration. Run it, label the evidence, and ship, iterate, or kill based on the result.

Never experiment on developers without guardrails. Never report an experiment that cannot decide anything.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## DX experiment design

Design every experiment in this order. Do not implement before the plan is complete.

### 1. Frame the hypothesis

State exactly one falsifiable claim:

- the surface changed: quickstart step count, CLI output layout, error message text, onboarding flow
- the change under test
- the primary metric it moves
- the expected direction and the minimum meaningful effect

A hypothesis that cannot fail cannot decide. If the expected effect size is not stated, estimate it before proceeding.

### 2. Define the variants

Define exactly one control and one or more treatments. The control is the current shipped behavior and is never an afterthought.

- every variant has a stable id, a flag key, and a value
- exactly one variant is marked `control`
- treatments differ from the control in exactly one dimension
- record what the experiment does not cover and why

Changing more than one dimension confounds the result. Split compound changes into separate experiments.

### 3. Define the metrics

Pick one primary metric and a small set of secondary metrics. Definitions live in `references/metric-definitions.md`; record a name, direction, and definition for every metric.

Define metrics before launch. A metric added after results arrive is post-hoc and cannot prove the hypothesis.

For onboarding work the suite magic-path gate remains the floor: a variant that pushes first value past `MAGIC_PATH_MAX_MIN` fails regardless of experiment results.

### 4. Set guardrails

Define the thresholds that stop the experiment early:

- a ceiling for error rate, drop-off, or support load
- a floor for the control's completion rate
- the comparison direction for every threshold
- the trip action: stop exposure, revert to control, page the owner

A guardrail trip is a P1 finding. Continue the experiment only after the root cause is understood and the plan is amended.

### 5. Configure the flag

Implement the experiment with provider-agnostic flagging per `references/openfeature-patterns.md`.

- one flag key, one control value, one treatment value
- targeting by stable cohort with an even split at launch
- exposure tracking on every evaluation
- a kill switch that reverts every variant to control
- no flag reuse across unrelated experiments

### 6. Validate the manifest

Record the plan as an experiment manifest JSON and run `scripts/check_experiment_metrics.py` on it.

The checker exits 0 only when name, hypothesis, variants with exactly one control, metric definitions, guardrail thresholds, and flag config are all present.

A manifest that fails the checker is a sketch, not an experiment. Fix it before launch.

### 7. Run the experiment

Run with the smallest sample that the expected effect and guardrails allow:

- sessions are homogeneous: same task, same environment class, same instrumentation
- assignment comes from the flag, never from self-selection
- label every result Observed, CI-observed, or Estimated
- collect completion, time, error, drop-off, support, and retention data per variant
- watch guardrails continuously, not after the run

Observed beats CI-observed beats Estimated. An estimate never proves a result.

### 8. Analyze and decide

Compare every treatment to control on the primary metric, then on secondary metrics and guardrails:

- report statistical and practical significance
- state per-variant evidence; never average across variants
- report the effect on task completion, time, error rate, drop-off, support load, and retention
- decide exactly one of: ship the treatment, iterate on a follow-up hypothesis, or kill it and keep control
- record the decision, the evidence, and the flag state in the experiment report

A result that does not move the primary metric within the expected effect is a kill or an iterate, not a ship.

## Experiment contract

An experiment is launchable only when its manifest records:

1. `name` — a unique identifier for the experiment
2. `hypothesis` — the falsifiable claim with direction and expected effect
3. `variants` — exactly one control and at least one treatment
4. `metrics` — primary and secondary, each with a definition
5. `guardrails` — thresholds, comparison direction, and trip action
6. `flag` — key, values, targeting, rollout, kill switch

## Evidence contract

Every number in the report carries one of the suite evidence labels:

- **Observed:** executed from a clean or representative environment
- **CI-observed:** executed in automation; may understate human time
- **Estimated:** reasoned without execution; can never prove a result

Unlabeled numbers are UNVERIFIED and cannot drive a ship decision.

## References

- `references/experiment-design.md` — hypothesis, variants, guardrails, ethics of user experiments
- `references/onboarding-experiments.md` — quickstart and onboarding A/B patterns
- `references/cli-variants.md` — CLI output and error formatting experiments
- `references/metric-definitions.md` — task completion, time, error rate, drop-off, support load, retention
- `references/openfeature-patterns.md` — OpenFeature-style flagging patterns

## Required output

Produce the experiment report from `assets/experiment-plan-template.md` containing:

1. Experiment identity, hypothesis, and variant table
2. Metrics with definitions and evidence labels
3. Guardrails and trip status
4. Results per variant: task completion, time, error rate, drop-off, support load, retention
5. Decision — ship, iterate, or kill — with rationale
6. Flag state and rollout plan for the shipped variant

## Definition of done

An experiment is done when:

- the hypothesis is falsifiable and states direction and expected effect
- exactly one control variant exists and treatments differ in one dimension
- every metric has a definition recorded before launch
- guardrails carry thresholds, comparison direction, and a trip action
- the manifest passes `scripts/check_experiment_metrics.py` with exit 0
- the run is complete and every result carries an evidence label
- the report compares every treatment to control, never averaging variants
- the decision is exactly one of ship, iterate, or kill, recorded with the flag state
- guardrail trips are reported as P1 findings, never hidden in averages

For passive feedback signals — surveys, sentiment, support tickets — use the `developer-feedback-analyst` skill if available. Experimentation Engineer measures; it does not replace passive-signal analysis.
