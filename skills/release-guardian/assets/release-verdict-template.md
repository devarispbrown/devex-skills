# Release Verdict Report

## Verdict

**Release gate:** <PASS | PASS WITH DEBT | FAIL | UNVERIFIED>

**Recommended version:** <current-version> → <target-version> (<MAJOR | MINOR | PATCH>)

## Evidence

- Repository/revision: <repo> @ <base>...<head>
- Environment: <env>
- Checks executed: <list>
- Checks not executed: <list>
- Evidence labels: <Observed | CI-observed | Estimated> per claim

## Classification table

| Changed path | Change class | Consumers affected | Evidence |
|---|---|---|---|
| <path> | <breaking\|behavioral\|deprecated\|added\|fixed\|internal> | <consumer list> | <evidence> |

## Consumer analysis

| Consumer | Impact | Per-consumer result | Evidence |
|---|---|---|---|
| JSON/response parsers | | <compatible\|breaking\|unverified> | |
| Enum exhaustiveness | | | |
| Generated SDKs | | | |
| Migrations / DB schemas | | | |
| Config parsers | | | |
| Webhook handlers | | | |
| Dashboards / metrics | | | |
| Shell scripts on CLI output | | | |

## Version recommendation

- Target version: <version>
- Bump rationale: <classification-derived rationale>
- Pre-release / LTS notes: <notes or "none">

## Migration requirements

- Migration guide: <required | not required> — <location>
- What changed / why / steps: <summary>
- Rollback path: <steps or "none required">

## Gate results

| Gate constant | Result | Evidence |
|---|---|---|
| UNDOCUMENTED_BREAKING_API | <PASS\|FAIL\|UNVERIFIED> | |
| SDK_API_DRIFT | | |
| STALE_PUBLIC_REFERENCE | | |
| UNTESTED_SUPPORTED_VERSION | | |
| BROKEN_QUICKSTART | | |
| BROKEN_CANONICAL_INSTALL | | |
| UNEXPLAINED_ERROR | | |
| UNSAFE_EXAMPLES | | |
| NON_REPRODUCIBLE_BUILD | | |

## Backlog (debt, when PASS WITH DEBT)

| Priority | Finding | Owner type | Acceptance test |
|---|---|---|---|
| <P0–P4> | | | |

## Sign-off

- Recommended version: <version>
- Gate verdict: <verdict>
- Tag-blocking items: <list or "none">
