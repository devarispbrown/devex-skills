# README Review and Authoring Guide

A README has three jobs:

1. Explain the project quickly.
2. Help the right user reach first success.
3. Route the user to deeper documentation and contribution paths.

## Recommended sequence

1. Project name and one-line value proposition
2. Short "why" or problem statement
3. Status/maturity warning if needed
4. Quickstart
5. Minimal example with expected result
6. Core concepts only if required for first success
7. Basic configuration
8. Documentation links
9. Compatibility/support
10. Local development and tests
11. Contributing
12. Security reporting
13. Community/support
14. License

## Quickstart test

A strong quickstart answers:

- What do I need installed?
- What command installs this?
- What is the smallest working configuration?
- What do I run?
- What should I see?
- What do I do next?

The canonical Quickstart must target and be designed for the hard **≤15-minute end-to-end magic path** defined in `magic-path.md`. Prefer ≤10 minutes when feasible. Installation alone does not count as success.

## Avoid

- leading with company history
- badges before explaining the product
- installation that silently assumes unrevealed tooling
- configuration keys not explained anywhere
- examples that omit imports/setup needed to run
- stale screenshots of rapidly changing interfaces
- dumping full API reference into the README
- multiple conflicting install paths without a recommended default
- using "simple" or "obvious" for steps that may fail

## Open-source additions

Check:

- CONTRIBUTING.md
- CODE_OF_CONDUCT.md when appropriate
- SECURITY.md
- issue/PR templates if the project accepts community contributions
- support expectations
- release/versioning policy
- governance/maintainer expectations when material
