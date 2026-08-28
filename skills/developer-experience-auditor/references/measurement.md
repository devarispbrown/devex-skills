# Journey Measurement

Measure the journey as a developer would experience it. Define each metric before recording; unlabeled numbers are UNVERIFIED.

## Time

- Wall-clock time per stage, from the first action intended to reach the stage objective to the stage stop condition.
- Run stages one at a time; do not overlap or parallelize during measurement.
- Wait time counts inside the stage where it occurs: install waits, build waits, provisioning waits.
- Round to the nearest second per stage; report totals in minutes and seconds.

## Command count

- Count every interactive command the developer must issue to reach the stage objective, including retries and corrections.
- A failed attempt counts as a command.
- One command that invokes a committed script counts as one command; the script's internal subcommands do not.
- Tab completion and shell-history reuse count as the command they produce.

## Credential count

- Count every credential the developer must create or find: API keys, tokens, passwords, account signups, secret environment variables.
- A credential reused across stages counts once.
- Credentials provisioned automatically by sandbox or test automation count only when the developer must find or copy them.
- Record where each credential came from.

## Context switches

- Count each move between contexts: docs, terminal, and browser.
- Moving within one context (a second doc tab, a second terminal pane) is not a switch.
- A copy-paste of a value between contexts is one switch.

## Errors encountered

- Record every distinct error or unexpected output per stage, with full error text and the stage where it appeared.
- Errors induced deliberately in the break stage are recorded separately from journey errors.
- Note whether each error explains what happened, why, and how to fix it, and whether it carries a support-correlation identifier.

## Rounding

- Times to the nearest second; counts as integers.
- Do not round away a failure, and do not round a near-miss into a pass.

## Evidence labels

- **Observed**: executed from a clean or representative environment by a human or agent.
- **CI-observed**: automation executed the steps; may undercount reading and signup time.
- **Estimated**: analyzed but not executed.
- An estimate can never prove a PASS. A metric without a label is UNVERIFIED.

## Recording

- Encode the journey as a manifest consumed by `scripts/journey_runner.py` (see `assets/journey-manifest.example.json`), with per-step `credentials` and `context_switches` annotations.
- The runner reports per-stage timing, command count, credential count, and context switches; the auditor adds error text and evidence labels in the DX Report.
