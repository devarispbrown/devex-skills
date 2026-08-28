# Onboarding and Quickstart Experiments

Patterns for experimenting on quickstart and onboarding flows.

## What to vary

- step count and ordering
- command structure: copy-paste blocks vs. single-line commands
- default language/SDK route
- install method: package manager, binary, container
- authentication flow: key vs. OAuth
- verification step presence and clarity
- error recovery placement

One dimension per experiment.

## What not to vary

- the underlying product contract
- the canonical quickstart route outside the experiment
- documentation the experiment does not instrument
- anything that changes the product's public behavior

## Baseline constraints

The suite magic-path gate is the floor: `MAGIC_PATH_MAX_MIN` = 15. A variant that pushes first value past the gate fails regardless of experiment results. Keep `MAGIC_PATH_MAX_COMMANDS`, `MAGIC_PATH_MAX_CREDENTIALS`, and `MAGIC_PATH_MAX_CONTEXT_SWITCHES` in mind when a treatment adds or removes steps.

## Session design

- same task for all participants
- same start state: no prior product knowledge, same environment class
- same instrumentation on every step
- assignment by flag, never by self-selection

## Metrics

Primary: task completion rate, time to first value.
Secondary: per-step drop-off, error rate, support load, retention.

Definitions in `metric-definitions.md`.

## Execution modes

- **Observed:** a human or agent executes both variants in a clean or representative environment
- **CI-observed:** automation runs the quickstart per variant on every relevant change; undercounts reading/signup time
- **Estimated:** step analysis only; can flag risk, never prove a result

Prefer observed for launch decisions and CI-observed for drift detection.

## Biases to control

- novelty: a new flow always looks better at first; run long enough to saturate
- order: counterbalance when sessions see both variants
- environment: network, cache, and provisioning differences dominate small effects
- selection: participants who opted in differ from the general population

## Decision notes

A quickstart change ships only when completion and time hold on the treatment without raising error rate, drop-off, or support load. Report drop-off per step to find where a treatment loses users, and turn that into the next hypothesis.
