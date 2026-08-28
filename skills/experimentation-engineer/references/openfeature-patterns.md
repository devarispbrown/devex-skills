# OpenFeature-Style Flagging Patterns

Reference pattern for flagging DX experiments: provider-agnostic, kill-switchable, exposure-tracked. OpenFeature naming is used; any provider implementing the same contract works.

## Abstraction

The flag layer is a thin provider-agnostic interface:

- application code never imports a vendor SDK directly
- one flag key per experiment
- flag values map to variants: control value, treatment value
- the provider is swappable without touching experiment code

## Flag config

An experiment flag records:

- key: unique, namespaced by product area
- values: one per variant, including the control
- targeting: rule or cohort list
- rollout: starting percentage and ramp plan
- default: the control value

The default is always control. An uninitialized or misconfigured flag resolves to control.

## Targeting

- stable cohorts: the same participant resolves to the same variant for the experiment's lifetime
- even split at launch for equal sample
- no mid-flight retargeting except guardrail trips
- never target by identity attributes that bias the population

## Evaluation

- evaluate per session, once, at the flow start
- record the resolved variant with every result row
- treat evaluation failures as control and log them

## Exposure tracking

- record an exposure event on every flag evaluation
- exposure count is the denominator for completion and error metrics
- report exposure per variant with the results

## Kill switch

- every experiment flag has a kill switch that reverts all variants to control immediately
- the kill switch is independent of targeting and rollout config
- guardrail trip and kill-switch state are recorded in the report

## Rollout

- start at the minimum sample that can decide
- ramp up only while guardrails hold
- full rollout is a product change, not an experiment; it gets its own release decision and changelog entry

## CLI and agent surfaces

For CLI output and agent-facing variants, evaluation happens at process start or command invocation. Same rules: stable cohort, exposure event, kill switch, default control.

## Manifest mapping

Record the flag contract in the experiment manifest `flag` object: key, provider, values per variant, targeting, rollout. The checker requires the key and the variant-to-flag mapping to be present.
