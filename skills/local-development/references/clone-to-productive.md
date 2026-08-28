# Clone-to-Productive Gate Procedure

## Purpose

Measures the hard gate of the `local-development` skill: a clean clone reaches the productive state within `LOCAL_DEV_MAX_MIN` using only committed instructions and automation. Failure triggers `NON_REPRODUCIBLE_BUILD` (P1).

## Benchmark persona

The developer has:

- a supported operating system
- a terminal and normal network access
- general software-development competence

They have **nothing else**: no repository knowledge, no credentials, no cached dependencies, no preinstalled services beyond declared platform prerequisites, no knowledge of internal conventions, shell aliases, or chat channels.

Do not hide setup in "prerequisites" to game the benchmark.

## Timer definition

**Start:** the developer begins the first documented step after cloning (or opens the setup instructions on a fresh clone).

**Stop:** both conditions hold:

1. the test suite runs and passes (or the documented test command succeeds)
2. the dev loop is exercised: a change to a source file is reflected in the running app, or the documented restart cycle completes and verifies

Installation alone, or a health check alone, is not the productive state. Both conditions must hold.

## Measuring from a clean checkout

1. Clone into a fresh directory outside the working repo, or into a clean container. Do not reuse a populated environment; cached state is not evidence.
2. Follow only the committed instructions. Record every interactive command; count them against `LOCAL_DEV_MAX_COMMANDS`.
3. Start the timer at the first documented step and stop it when both stop conditions hold.
4. Record the breakdown: clone, toolchain, dependencies, services, first success, and recovery. Use the per-segment budget in `references/standards.md` as planning guidance only, never as gate thresholds.
5. Attribute overruns to Setup, Toolchain, Services, Infrastructure, or External dependency. Do not blame the setup for a defect the setup cannot remove.

Never run destructive commands against the working checkout; measure from the copy.

## Band interpretation

- Far under `LOCAL_DEV_MAX_MIN`: exceptional.
- Comfortably under the limit: strong.
- Under the limit but near it: pass.
- At or over the limit: **P1 FAIL** — the `NON_REPRODUCIBLE_BUILD` gate fires.
- No reproducible path at all (no committed automation, a required manual step): **P1 FAIL** for `NON_REPRODUCIBLE_BUILD`, regardless of elapsed time.

Use the exact bands in `references/standards.md`; do not invent intermediate thresholds.

## Evidence labels

- **Observed:** actually executed from a clean checkout and timed.
- **CI-observed:** executed in automation; useful for drift detection but may undercount human reading and typing time.
- **Estimated:** reasoned from steps without execution. An estimate can never prove a PASS.

A metric without an evidence label is UNVERIFIED. Prefer observed evidence periodically and CI-observed evidence on every relevant change.
