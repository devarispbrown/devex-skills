# Fixture Report

## Scope

- Repository/area: <repo or module>
- Task: <what fixture work was done>
- Fixture tree: <canonical location>

## Fixture tree

| File | Role | Notes |
|---|---|---|
| <path> | <seed\|factory\|fake\|cassette\|golden\|synthetic\|sanitized> | <notes> |

## Hygiene check

- Checker: `scripts/check_fixture_hygiene.py <tree>`
- Result: <PASS | findings — list each>
- Exceptions: <filed exceptions or "none">

## Regeneration

- Command: <exact command>
- Owner: <team or individual>
- Cadence: <on change | on release | manual>

## Sanitization record

- Source: <where the data came from>
- Date: <date>
- Transforms: <what was replaced, and with what>
- Verification: <how the originals were proven absent>

## Synthetic data notes

- Generator: <path>
- Seed: <seed>
- Profile: <cardinality/distribution profile stated>

## Open items

| Priority | Item | Owner type | Acceptance test |
|---|---|---|---|
| <P0–P4> | | | |

## Sign-off

- Hygiene result: <PASS / FAIL>
- Report author: <owner>
