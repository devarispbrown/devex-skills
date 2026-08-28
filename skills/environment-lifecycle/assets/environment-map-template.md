# Environment Map

## Header

- Repository: <repo> @ <revision>
- Date: <date>
- Author/Owner: <name>
- Evidence labels: Observed / CI-observed / Estimated on every claim

## Stage map

| Stage | Primary job | Deploy automation | Data | Cost owner | URL / entry point |
|---|---|---|---|---|---|
| local | | | | | |
| test | | | | | |
| preview | | | | | |
| staging | | | | | |
| production | | | | | |

## Surface inventory

Rerun `scripts/check_environment_lifecycle.py` against the repository and attach the output:

<inventory output>

## Gaps

| Gap | Severity | Fix | Owner | Evidence |
|---|---|---|---|---|
| | <P0–P4> | | | <Observed\|CI-observed\|Estimated> |

## TTL and cleanup plan

| Environment type | TTL | Enforced by | Cleanup job | Orphan policy |
|---|---|---|---|---|
| preview (per PR/branch) | | | | |
| staging | | | | |
| test (CI) | | | | |

## Cost controls

| Stage | Budget | Alert | Cap | Sleep |
|---|---|---|---|---|
| test | | | | |
| preview | | | | |
| staging | | | | |
| production | | | | |

## Config and secrets

| Stage | Config source | Secret store | Promotion path |
|---|---|---|---|
| local | | none | |
| test | | | |
| preview | | | |
| staging | | | |
| production | | | |

## Seed and clone

| Stage | Seed version | Branch source | Sanitized |
|---|---|---|---|
| test | | n/a | |
| preview | | | |
| staging | | | |

## Definition of done for this map

- every stage is named with one primary job
- TTL and cleanup are defined for every ephemeral environment
- every gap has a severity and an owner
- every claim carries an evidence label: Observed, CI-observed, or Estimated
