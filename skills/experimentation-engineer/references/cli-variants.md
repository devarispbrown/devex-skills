# CLI Output and Error Formatting Experiments

Patterns for experimenting on CLI output variants, error formatting, and feedback surfaces.

## What to vary

- output layout and verbosity: compact vs. detailed
- progress and spinner behavior
- error message structure: cause, fix, retry-safety
- error remediation placement: inline vs. linked
- `--help` ordering and examples
- color and formatting where parsers are not affected

One dimension per experiment.

## What not to vary

- exit codes and stdout/stderr contracts
- machine-readable output parsed by scripts
- flag names, defaults, and config precedence
- any surface a documented consumer parses

Public CLI behavior is a compatibility contract. An experiment that changes it is a release decision, not a UI tweak. Gate it with `release-guardian`.

## Metric mapping

- time to successful command completion
- error rate: sessions that hit an error and recover
- recovery time: from error to corrective action; suite `TTR_TARGET_MIN` = 5 is the target
- drop-off: sessions abandoned after an error or long output
- support load: tickets or escalations per 100 sessions
- retention: repeat use over the window

Definitions in `metric-definitions.md`.

## Error formatting experiments

Test error variants on:

- error title and cause statement
- actionable next step and its placement
- retry-safety guidance and idempotency note
- expected output for the corrected run

Measure recovery time and drop-off. The variant that gets developers to the fix fastest wins, subject to guardrails.

## Execution modes

- **Observed:** run both variants in a representative terminal
- **CI-observed:** scripted runs diffing stdout/stderr per variant on every change
- **Estimated:** reasoned from output without execution; risk-only

## Notes

A prettier error that parses worse for scripts is a regression, not a win. Check machine-readable output parity across variants before launch.
