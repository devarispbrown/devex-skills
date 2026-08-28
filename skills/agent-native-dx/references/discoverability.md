# Discoverability

An agent that cannot find the build, the tests, or the commands cannot work in the repository. Discovery is structure, not prose.

## Repository structure clarity

- Conventional top-level layout: source, tests, docs, packaging, and tooling in predictable places.
- No mystery directories; every top-level entry has an obvious job or a one-line README.
- Naming is consistent across the tree: same concept, same name.
- The README or entry file maps the tree in a few lines.

## Test discoverability

- Tests live in a conventional location: a `tests/` directory or `test_`/`_test`-named files adjacent to code.
- One documented command runs the full suite; one documented pattern runs a single test.
- Test names describe behavior, not implementation.
- CI runs the same command the docs name; an agent that follows docs reproduces CI.
- Verify: an agent given only the repo can find and run the suite without asking.

## Command discovery

- `--help` output is complete: every subcommand and flag documented, with defaults and units.
- A top-level help or `list` command enumerates subcommands.
- `--version` exists and matches the release metadata.
- Flags use stable, conventional names; aliases are documented, not assumed.

## State inspectability

- A `status`, `describe`, `show`, or equivalent command reads current state without mutating it.
- State commands emit machine-readable output in addition to human text.
- `--dry-run` and `--what-if` variants exist for operations with effects, showing the change without applying it.
- Logs are agent-readable too: stable format, timestamps, correlation ids, no secrets.

## Verify with a simulated agent

An agent is lost at every point where it must guess:

- guess the build command → naming it in the entry file closes the guess
- guess how to run one test → the single-test pattern closes it
- guess a flag name → `--help` closes it
- guess the current state → a status command closes it

Audit the repository for each guessing point and close the ones the agent path crosses.
