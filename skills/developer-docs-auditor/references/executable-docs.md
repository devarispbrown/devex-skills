# Executable Documentation Testing

Prefer proof over visual review.

## Priority

1. execute the exact checked-in example in integration/CI
2. import documentation snippets from tested example source
3. compile/type-check extracted snippets
4. validate request/response examples against schemas
5. snapshot stable expected output

## What to test

- installation commands
- quickstart commands
- authentication against test/sandbox mode where safe
- API examples
- SDK examples in Tier 1 languages
- CLI commands and exit codes
- config examples
- migration steps where test fixtures exist

## Safety

Do not run destructive production commands merely to validate docs. Prefer local, ephemeral, sandbox, fixture, or mock environments. Identify tests that need human-controlled credentials or infrastructure.

## Evidence labeling

Report each check as PASS, FAIL, SKIPPED, or UNVERIFIED and state the command/evidence used. Never infer execution success from syntactically plausible snippets.
