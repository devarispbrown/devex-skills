# Loop Measurement

## Segment definition

A loop segment is one action-to-feedback pair. Start: the developer's action completes or initiates the stage. Stop: the feedback the developer needs arrives. Everything between is measured wall-clock time.

## Method

For each segment:

1. Pick the representative command or watch.
2. Time from action completion to feedback arrival.
3. Run at least once clean and once warm when both states are realistic.
4. Record measured_seconds and the environment with the measurement.
5. Label the evidence.

Do not measure only the happy path. Do not time a different command than the one the developer runs. Do not report the fastest sample as the truth.

## Sampling

Measure the developer's default path. Prefer three samples and report the median or the default-path sample; never cherry-pick.

## Manifest schema

The checker reads a JSON manifest with a steps list. Each step has:

- `name` — stage name
- `command` — the command or watch that produces feedback; informational, never executed
- `budget_seconds` — the budget for this stage, expressed in seconds
- `measured_seconds` — wall-clock measurement
- `evidence` — exactly one evidence label

## Evidence labels

- **Observed** — a human or agent actually executed the step and timed it from a clean or representative environment.
- **CI-observed** — automation executed the step; useful for drift, may undercount human reading or setup time.
- **Estimated** — reasoned from steps without execution.

An estimate can never prove a PASS. A metric without an evidence label is UNVERIFIED.
