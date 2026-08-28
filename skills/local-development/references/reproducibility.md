# Reproducibility

## Clean-machine validation

The gate procedure in `clone-to-productive.md` is the reproducibility check. Run it:

1. on a fresh clone in a separate directory or a clean container
2. from the committed instructions alone, with no shell history and no preinstalled state
3. with the timer running, and record the band against `LOCAL_DEV_MAX_MIN`

Run it again after every change to setup files. A setup that passes once and drifts is still broken.

## CI parity

A clean clone in CI must equal a clean clone on a laptop:

- CI runs the same install-from-lockfile and the same test command as the dev target
- CI builds, and when practical launches, the devcontainer or compose stack to prove it
- CI installs from the same lockfiles; anything CI must not do (interactive prompts, credentials) must also be absent from the documented local path
- a CI-only setup path that developers cannot run locally is a parity defect, not a feature

## "Works on my machine" signals

Detect and eliminate:

- uncommitted env files or config the app silently depends on
- absolute paths (`/Users/<name>/...`) in committed config or docs
- reliance on globally installed tools the setup never installs or pins
- steps only the setup owner can execute (their shell aliases, their database dumps, their credentials)
- cached state that masks real installs — a "works" verdict achieved only on a pre-warmed machine
- timestamps or machine names in generated artifacts that appear in diffs

Each signal is a manual step in disguise and a `NON_REPRODUCIBLE_BUILD` risk.

## Drift checks

Schedule lightweight checks so reproducibility does not rot:

- lockfile vs manifest: install must fail loudly when they disagree
- `.env.example` vs code: a startup check that every variable the code reads is declared in the example
- docs vs commands: extract commands from setup docs and diff them against the Makefile, compose, and scripts
- toolchain pins vs README: the documented runtime matches the pin file
- CI vs local: the CI install command matches the documented local install command

Prefer automated drift checks over review discipline. When a check is impossible, make the manual check a named step in the release or audit gate.
