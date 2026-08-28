# DX Experiment Design

Canonical rules for designing developer-experience experiments. Read before framing any experiment.

## Hypothesis

A hypothesis is one falsifiable claim:

- surface changed
- change under test
- primary metric
- expected direction and minimum meaningful effect

Write it as: "Changing X on surface Y moves metric Z by at least D in direction S."

Signs of a bad hypothesis:

- no direction or effect size stated
- multiple metrics claimed as primary
- multiple surfaces changed at once
- no possible outcome can fail it

## Variant design

- exactly one control: the current shipped behavior
- treatments differ from control in exactly one dimension
- one flag key per experiment; flag values map to variants
- stable variant ids that never change mid-experiment
- exclude noise sources: version skew, cache state, environment class

Compound changes confound. Split them.

## Metrics

Pick one primary metric; secondary metrics explain why.

Define metrics before launch. Post-hoc metrics cannot prove a hypothesis.

Definitions live in `metric-definitions.md`. Suite constants in `dx-standards/metrics.md` are referenced by name and never restated with different values.

## Guardrails

Guardrails are thresholds that stop the experiment before it harms developers:

- error rate ceiling
- drop-off ceiling per step
- support-load ceiling (tickets or escalations per 100 sessions)
- completion floor for the control variant

Trip action: stop exposure, revert to control, page the owner. A trip is a P1 finding; continue only after root cause is understood and the plan is amended.

## Sample and exposure

- smallest valid sample the expected effect allows
- even split at launch; stable cohort targeting
- record exposure on every flag evaluation
- kill switch reverts all variants to control
- no mid-flight retargeting except guardrail trips

## Ethics of user experiments

Experiments run on real developers are user research, not free changes:

- Do not deceive participants about observable behavior changes.
- Limit exposure to the smallest sample that can decide.
- Provide an opt-out that restores the control experience.
- Never route developers to broken variants beyond what the sample requires.
- Never capture credentials, tokens, or secrets in instrumentation.
- Guardrail every experiment that touches first-run or production paths.
- Report findings with evidence labels; never hide harm in anonymous aggregates.

A sandboxed, resettable, safe-by-construction path is required when the task is destructive, quota-consuming, or production-touching (suite `NO_SANDBOX_FOR_RISKY_PATH`).

## Decision rules

- **ship:** primary metric moves as hypothesized, guardrails hold, no P1 finding
- **iterate:** signal exists but is insufficient, or secondary metrics raise a new question
- **kill:** primary metric does not move, or a guardrail tripped

Record the decision with the flag state. An experiment without a recorded decision is unfinished work.
